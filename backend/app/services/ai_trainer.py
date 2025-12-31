from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models, schemas
from app.config import settings
import json


class AITrainerService:
    """Service for AI-powered personal training program generation"""

    def __init__(self, db: Session, user: models.User):
        self.db = db
        self.user = user

    def generate_program(self, request: schemas.TrainerProgramRequest) -> models.AITrainingProgram:
        """Generate a training program (multi-week or daily)"""

        # Use user's profile if not provided in request
        fitness_level = request.fitness_level or self.user.fitness_level or "beginner"
        fitness_goals = request.fitness_goals or self.user.fitness_goals or ["general_fitness"]

        # Try OpenAI first, fall back to rule-based
        if settings.OPENAI_API_KEY:
            try:
                if request.program_type == "multi_week":
                    return self._generate_multi_week_with_openai(request, fitness_level, fitness_goals)
                else:
                    return self._generate_daily_with_openai(request, fitness_level, fitness_goals)
            except Exception as e:
                print(f"OpenAI generation failed, using rule-based: {e}")
                return self._generate_program_rule_based(request, fitness_level, fitness_goals)
        else:
            return self._generate_program_rule_based(request, fitness_level, fitness_goals)

    def _generate_multi_week_with_openai(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Generate multi-week program using OpenAI"""
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Analyze workout history
        workout_history = self._analyze_workout_history(days=30)

        # Get available exercises
        exercises = self._get_available_exercises(
            equipment=request.available_equipment,
            fitness_level=fitness_level
        )

        # Build comprehensive prompt
        prompt = self._build_multi_week_prompt(
            request, fitness_level, fitness_goals, workout_history, exercises
        )

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an elite personal trainer with expertise in exercise science, periodization, and progressive overload principles."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=3000
        )

        result = json.loads(response.choices[0].message.content)

        # Create database models from AI response
        return self._create_program_from_ai_response(result, request, fitness_level, fitness_goals)

    def _generate_daily_with_openai(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Generate single daily workout using OpenAI"""
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Get recent workouts to avoid overtraining
        recent_workouts = self._get_recent_workouts(days=3)

        # Get available exercises
        exercises = self._get_available_exercises(
            equipment=request.available_equipment,
            fitness_level=fitness_level
        )

        prompt = self._build_daily_workout_prompt(
            request, fitness_level, fitness_goals, recent_workouts, exercises
        )

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a personal trainer creating today's workout session."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500
        )

        result = json.loads(response.choices[0].message.content)

        # Create daily workout program
        return self._create_daily_program_from_ai_response(result, request, fitness_level, fitness_goals)

    def _generate_program_rule_based(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Generate program using rule-based templates (fallback)"""

        if request.program_type == "multi_week":
            return self._generate_multi_week_template(request, fitness_level, fitness_goals)
        else:
            return self._generate_daily_template(request, fitness_level, fitness_goals)

    def _analyze_workout_history(self, days: int = 30) -> Dict:
        """Analyze user's recent workout logs"""
        start_date = datetime.utcnow() - timedelta(days=days)

        logs = self.db.query(models.WorkoutLog).join(
            models.Exercise
        ).filter(
            models.WorkoutLog.user_id == self.user.id,
            models.WorkoutLog.date >= start_date
        ).all()

        if not logs:
            return {
                "total_workouts": 0,
                "summary": "No recent workout history"
            }

        total_workouts = len(logs)
        avg_difficulty = sum(log.difficulty_rating or 5 for log in logs) / len(logs)

        # Track muscle group frequency
        muscle_frequency = {}
        for log in logs:
            if log.exercise and log.exercise.muscle_groups:
                for muscle in log.exercise.muscle_groups:
                    muscle_frequency[muscle] = muscle_frequency.get(muscle, 0) + 1

        return {
            "total_workouts": total_workouts,
            "avg_difficulty_rating": round(avg_difficulty, 1),
            "muscle_group_frequency": muscle_frequency,
            "summary": f"{total_workouts} workouts in last {days} days, avg difficulty: {avg_difficulty:.1f}/10"
        }

    def _get_recent_workouts(self, days: int = 3) -> List[str]:
        """Get recent workouts to avoid muscle fatigue"""
        start_date = datetime.utcnow() - timedelta(days=days)

        logs = self.db.query(models.WorkoutLog).join(
            models.Exercise
        ).filter(
            models.WorkoutLog.user_id == self.user.id,
            models.WorkoutLog.date >= start_date
        ).all()

        recent_exercises = []
        for log in logs:
            if log.exercise:
                recent_exercises.append(f"{log.exercise.name} ({', '.join(log.exercise.muscle_groups)})")

        return recent_exercises

    def _get_available_exercises(
        self,
        equipment: Optional[List[str]] = None,
        fitness_level: str = "beginner"
    ) -> List[models.Exercise]:
        """Get exercises matching criteria"""
        query = self.db.query(models.Exercise).filter(
            models.Exercise.difficulty == fitness_level
        )

        if equipment:
            # Get exercises matching equipment
            exercises = []
            for equip in equipment:
                exs = query.filter(models.Exercise.equipment.contains([equip])).all()
                exercises.extend(exs)

            # Add bodyweight exercises
            bodyweight = query.filter(models.Exercise.equipment == None).all()
            exercises.extend(bodyweight)

            # Remove duplicates
            seen = set()
            unique_exercises = []
            for ex in exercises:
                if ex.id not in seen:
                    seen.add(ex.id)
                    unique_exercises.append(ex)

            return unique_exercises
        else:
            return query.all()

    def _build_multi_week_prompt(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str],
        workout_history: Dict,
        exercises: List[models.Exercise]
    ) -> str:
        """Build comprehensive prompt for multi-week program"""

        exercises_info = "\n".join([
            f"- {ex.name} ({ex.category}, {', '.join(ex.muscle_groups)})"
            for ex in exercises[:50]
        ])

        prompt = f"""You are an elite personal trainer designing a {request.duration_weeks}-week training program.

USER PROFILE:
- Fitness Level: {fitness_level}
- Goals: {', '.join(fitness_goals)}
- Available Equipment: {', '.join(request.available_equipment or ['bodyweight'])}
- Time per Session: {request.time_per_session_minutes} minutes
- Training Frequency: {request.days_per_week} days/week

WORKOUT HISTORY:
{workout_history['summary']}

TRAINING PRINCIPLES TO APPLY:
1. Progressive Overload: Gradually increase volume, intensity, or frequency
2. Periodization: Structure with phases (foundation → strength → hypertrophy)
3. Recovery: Include deload weeks (every 4th week at 60-70% intensity)
4. Specificity: Align exercises with stated goals
5. Variation: Change exercises/rep ranges across weeks
6. Balance: Avoid muscle imbalances

AVAILABLE EXERCISES:
{exercises_info}

PROGRAM REQUIREMENTS:
- Duration: {request.duration_weeks} weeks
- Weekly Structure: {request.days_per_week} training days
- Session Length: ~{request.time_per_session_minutes} minutes

OUTPUT JSON FORMAT:
{{
  "program_name": "descriptive name",
  "program_description": "2-3 sentence overview",
  "program_rationale": "explain strategy and why it fits user's goals",
  "weeks": [
    {{
      "week_number": 1,
      "theme": "Foundation Week",
      "notes": "Focus on form and establishing baseline",
      "workouts": [
        {{
          "day_number": 1,
          "workout_name": "Upper Body Strength",
          "focus_areas": ["chest", "triceps", "shoulders"],
          "estimated_duration_minutes": {request.time_per_session_minutes},
          "notes": "Establish baseline with moderate weights",
          "exercises": [
            {{
              "exercise_name": "Barbell Bench Press",
              "sets": 3,
              "reps": "10-12",
              "rest_seconds": 90,
              "intensity_level": "working",
              "notes": "Focus on controlled eccentric"
            }}
          ]
        }}
      ]
    }}
  ]
}}

Design an effective, balanced program."""

        return prompt

    def _build_daily_workout_prompt(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str],
        recent_workouts: List[str],
        exercises: List[models.Exercise]
    ) -> str:
        """Build prompt for daily workout"""

        exercises_info = "\n".join([
            f"- {ex.name} ({ex.category}, {', '.join(ex.muscle_groups)})"
            for ex in exercises[:30]
        ])

        recent_info = "\n".join(recent_workouts) if recent_workouts else "No recent workouts"

        prompt = f"""Create today's workout session.

USER CONTEXT:
- Fitness Level: {fitness_level}
- Goals: {', '.join(fitness_goals)}
- Equipment: {', '.join(request.available_equipment or ['bodyweight'])}
- Time: {request.time_per_session_minutes} minutes

RECENT WORKOUTS (avoid overtraining):
{recent_info}

AVAILABLE EXERCISES:
{exercises_info}

PRINCIPLES:
1. Choose 5-7 exercises for time and fitness level
2. Compound movements first, isolation later
3. Balance muscle groups
4. Avoid recently trained muscles

OUTPUT JSON:
{{
  "workout_name": "descriptive name",
  "focus_areas": ["muscle groups"],
  "estimated_duration_minutes": {request.time_per_session_minutes},
  "rationale": "why these exercises today",
  "notes": "coaching tips",
  "exercises": [
    {{
      "exercise_name": "exact name from available exercises",
      "sets": 3,
      "reps": "8-10",
      "rest_seconds": 60,
      "notes": "coaching cue"
    }}
  ]
}}"""

        return prompt

    def _create_program_from_ai_response(
        self,
        ai_response: Dict,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Create database models from AI-generated multi-week program"""

        # Create main program
        program = models.AITrainingProgram(
            user_id=self.user.id,
            program_type="multi_week",
            name=ai_response.get("program_name", "AI Training Program"),
            description=ai_response.get("program_description"),
            fitness_level=fitness_level,
            fitness_goals=fitness_goals,
            available_equipment=request.available_equipment,
            training_preferences=request.preferences,
            duration_weeks=request.duration_weeks,
            days_per_week=request.days_per_week,
            difficulty=fitness_level,
            ai_rationale=ai_response.get("program_rationale", ""),
            status="draft"
        )

        self.db.add(program)
        self.db.flush()  # Get program.id

        # Create weekly plans
        for week_data in ai_response.get("weeks", []):
            weekly_plan = models.AIWeeklyPlan(
                training_program_id=program.id,
                week_number=week_data["week_number"],
                theme=week_data.get("theme"),
                notes=week_data.get("notes")
            )
            self.db.add(weekly_plan)
            self.db.flush()

            # Create daily workouts
            for workout_data in week_data.get("workouts", []):
                daily_workout = models.AIDailyWorkout(
                    training_program_id=program.id,
                    weekly_plan_id=weekly_plan.id,
                    day_number=workout_data["day_number"],
                    workout_name=workout_data["workout_name"],
                    focus_areas=workout_data["focus_areas"],
                    estimated_duration_minutes=workout_data.get("estimated_duration_minutes", 60),
                    notes=workout_data.get("notes")
                )
                self.db.add(daily_workout)
                self.db.flush()

                # Add exercises
                for idx, ex_data in enumerate(workout_data.get("exercises", [])):
                    exercise = self.db.query(models.Exercise).filter(
                        models.Exercise.name == ex_data["exercise_name"]
                    ).first()

                    if exercise:
                        workout_exercise = models.AIDailyWorkoutExercise(
                            daily_workout_id=daily_workout.id,
                            exercise_id=exercise.id,
                            order=idx,
                            sets=ex_data["sets"],
                            reps=ex_data["reps"] if isinstance(ex_data["reps"], list) else [ex_data["reps"]],
                            rest_seconds=ex_data.get("rest_seconds", 60),
                            intensity_level=ex_data.get("intensity_level"),
                            notes=ex_data.get("notes")
                        )
                        self.db.add(workout_exercise)

        self.db.commit()
        self.db.refresh(program)
        return program

    def _create_daily_program_from_ai_response(
        self,
        ai_response: Dict,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Create database models from AI-generated daily workout"""

        # Create program
        program = models.AITrainingProgram(
            user_id=self.user.id,
            program_type="daily",
            name=ai_response.get("workout_name", "Daily Workout"),
            description="AI-generated daily workout",
            fitness_level=fitness_level,
            fitness_goals=fitness_goals,
            available_equipment=request.available_equipment,
            training_preferences=request.preferences,
            duration_weeks=None,
            days_per_week=request.days_per_week,
            difficulty=fitness_level,
            ai_rationale=ai_response.get("rationale", ""),
            status="draft"
        )

        self.db.add(program)
        self.db.flush()

        # Create single daily workout
        daily_workout = models.AIDailyWorkout(
            training_program_id=program.id,
            weekly_plan_id=None,
            day_number=1,
            workout_name=ai_response.get("workout_name", "Today's Workout"),
            focus_areas=ai_response.get("focus_areas", []),
            estimated_duration_minutes=ai_response.get("estimated_duration_minutes", 60),
            notes=ai_response.get("notes")
        )
        self.db.add(daily_workout)
        self.db.flush()

        # Add exercises
        for idx, ex_data in enumerate(ai_response.get("exercises", [])):
            exercise = self.db.query(models.Exercise).filter(
                models.Exercise.name == ex_data["exercise_name"]
            ).first()

            if exercise:
                workout_exercise = models.AIDailyWorkoutExercise(
                    daily_workout_id=daily_workout.id,
                    exercise_id=exercise.id,
                    order=idx,
                    sets=ex_data["sets"],
                    reps=ex_data["reps"] if isinstance(ex_data["reps"], list) else [ex_data["reps"]],
                    rest_seconds=ex_data.get("rest_seconds", 60),
                    intensity_level=ex_data.get("intensity_level"),
                    notes=ex_data.get("notes")
                )
                self.db.add(workout_exercise)

        self.db.commit()
        self.db.refresh(program)
        return program

    def _generate_multi_week_template(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Generate template-based multi-week program (rule-based fallback)"""

        # Create basic program
        program = models.AITrainingProgram(
            user_id=self.user.id,
            program_type="multi_week",
            name=f"{request.duration_weeks}-Week {fitness_level.title()} Program",
            description=f"Template-based training program for {', '.join(fitness_goals)}",
            fitness_level=fitness_level,
            fitness_goals=fitness_goals,
            available_equipment=request.available_equipment,
            duration_weeks=request.duration_weeks,
            days_per_week=request.days_per_week,
            difficulty=fitness_level,
            ai_rationale="Rule-based program using progressive overload principles",
            status="draft"
        )

        self.db.add(program)
        self.db.flush()

        # Get exercises
        exercises = self._get_available_exercises(request.available_equipment, fitness_level)

        # Create simple program structure
        for week in range(1, request.duration_weeks + 1):
            weekly_plan = models.AIWeeklyPlan(
                training_program_id=program.id,
                week_number=week,
                theme=f"Week {week}",
                notes=f"Progressive training week {week}"
            )
            self.db.add(weekly_plan)
            self.db.flush()

            # Create workouts for this week
            for day in range(1, request.days_per_week + 1):
                daily_workout = models.AIDailyWorkout(
                    training_program_id=program.id,
                    weekly_plan_id=weekly_plan.id,
                    day_number=day,
                    workout_name=f"Workout {day}",
                    focus_areas=["full_body"],
                    estimated_duration_minutes=request.time_per_session_minutes
                )
                self.db.add(daily_workout)
                self.db.flush()

                # Add some exercises
                for idx, exercise in enumerate(exercises[:6]):
                    workout_exercise = models.AIDailyWorkoutExercise(
                        daily_workout_id=daily_workout.id,
                        exercise_id=exercise.id,
                        order=idx,
                        sets=3,
                        reps=["10-12"],
                        rest_seconds=60
                    )
                    self.db.add(workout_exercise)

        self.db.commit()
        self.db.refresh(program)
        return program

    def _generate_daily_template(
        self,
        request: schemas.TrainerProgramRequest,
        fitness_level: str,
        fitness_goals: List[str]
    ) -> models.AITrainingProgram:
        """Generate template-based daily workout (rule-based fallback)"""

        program = models.AITrainingProgram(
            user_id=self.user.id,
            program_type="daily",
            name="Daily Workout",
            description="Template-based daily workout",
            fitness_level=fitness_level,
            fitness_goals=fitness_goals,
            available_equipment=request.available_equipment,
            days_per_week=request.days_per_week,
            difficulty=fitness_level,
            ai_rationale="Rule-based workout selection",
            status="draft"
        )

        self.db.add(program)
        self.db.flush()

        # Get exercises
        exercises = self._get_available_exercises(request.available_equipment, fitness_level)

        daily_workout = models.AIDailyWorkout(
            training_program_id=program.id,
            day_number=1,
            workout_name="Today's Workout",
            focus_areas=["full_body"],
            estimated_duration_minutes=request.time_per_session_minutes
        )
        self.db.add(daily_workout)
        self.db.flush()

        # Add exercises
        for idx, exercise in enumerate(exercises[:6]):
            workout_exercise = models.AIDailyWorkoutExercise(
                daily_workout_id=daily_workout.id,
                exercise_id=exercise.id,
                order=idx,
                sets=3,
                reps=["10-12"],
                rest_seconds=60
            )
            self.db.add(workout_exercise)

        self.db.commit()
        self.db.refresh(program)
        return program

    def generate_adaptation_insights(self) -> List[models.AIAdaptationInsight]:
        """Analyze workout logs and generate adaptation insights"""

        workout_history = self._analyze_workout_history(days=30)

        if workout_history["total_workouts"] < 5:
            return []  # Not enough data

        insights = []

        # Check for high difficulty ratings (overtraining indicator)
        if workout_history.get("avg_difficulty_rating", 5) > 7.5:
            insight = models.AIAdaptationInsight(
                user_id=self.user.id,
                insight_type="recovery_needed",
                insight_text="Your recent workouts show consistently high difficulty ratings, which may indicate you need more recovery time.",
                data_basis={
                    "avg_difficulty_rating": workout_history["avg_difficulty_rating"],
                    "analyzed_logs": workout_history["total_workouts"]
                },
                recommendation="Consider adding a deload week with reduced volume and intensity."
            )
            insights.append(insight)
            self.db.add(insight)

        # Check for consistent training (positive)
        if workout_history["total_workouts"] >= 12:  # 3+ workouts/week
            insight = models.AIAdaptationInsight(
                user_id=self.user.id,
                insight_type="progression_detected",
                insight_text="Excellent consistency! You've maintained regular training frequency.",
                data_basis={
                    "total_workouts": workout_history["total_workouts"],
                    "time_range_days": 30
                },
                recommendation="Consider progressive overload - gradually increase weight or reps."
            )
            insights.append(insight)
            self.db.add(insight)

        self.db.commit()
        return insights
