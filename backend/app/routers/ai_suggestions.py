from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db
from app.config import settings
import json

router = APIRouter(prefix="/api/ai", tags=["ai-suggestions"])


def generate_workout_suggestion_with_openai(
    user: models.User,
    request: schemas.WorkoutSuggestionRequest,
    db: Session
) -> dict:
    """Generate workout suggestion using OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Get user's recent workout history
        recent_logs = db.query(models.WorkoutLog).filter(
            models.WorkoutLog.user_id == user.id
        ).order_by(models.WorkoutLog.date.desc()).limit(10).all()

        # Build context
        context = f"""User Profile:
- Fitness Level: {request.current_fitness_level or user.fitness_level or 'Not specified'}
- Available Equipment: {', '.join(request.available_equipment or [])}
- Time Available: {request.time_available_minutes or 60} minutes
- Target Muscle Groups: {', '.join(request.target_muscle_groups or [])}
- User Goals: {', '.join(user.fitness_goals or [])}

Recent Workout History:
{len(recent_logs)} workouts logged recently
"""

        # Get available exercises
        query = db.query(models.Exercise)
        if request.available_equipment:
            for equipment in request.available_equipment:
                query = query.filter(models.Exercise.equipment.contains([equipment]))

        if request.target_muscle_groups:
            for muscle in request.target_muscle_groups:
                query = query.filter(models.Exercise.muscle_groups.contains([muscle]))

        available_exercises = query.all()

        exercises_info = "\n".join([
            f"- {ex.name} ({ex.category}, {ex.difficulty}): {', '.join(ex.muscle_groups)}"
            for ex in available_exercises[:20]
        ])

        prompt = f"""{context}

Available Exercises:
{exercises_info}

Based on this information, suggest 4-6 exercises for today's workout. Consider:
1. User's fitness level and goals
2. Available equipment
3. Target muscle groups
4. Time constraints
5. Balanced muscle group targeting

Respond with a JSON object containing:
- "exercises": list of exercise names from the available exercises
- "rationale": explanation of why these exercises were selected (2-3 sentences)
"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional fitness trainer providing workout recommendations."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating AI suggestion: {str(e)}"
        )


def generate_workout_suggestion_rule_based(
    user: models.User,
    request: schemas.WorkoutSuggestionRequest,
    db: Session
) -> dict:
    """Generate workout suggestion using rule-based system (fallback)"""

    # Determine fitness level
    fitness_level = request.current_fitness_level or user.fitness_level or "beginner"

    # Get recent workout logs to avoid same muscle groups
    from datetime import datetime, timedelta
    recent_date = datetime.utcnow() - timedelta(days=2)
    recent_logs = db.query(models.WorkoutLog).filter(
        models.WorkoutLog.user_id == user.id,
        models.WorkoutLog.date >= recent_date
    ).all()

    recent_exercise_ids = [log.exercise_id for log in recent_logs]

    # Query exercises
    query = db.query(models.Exercise).filter(
        models.Exercise.difficulty == fitness_level,
        ~models.Exercise.id.in_(recent_exercise_ids)
    )

    # Filter by equipment if specified
    if request.available_equipment:
        exercises_by_equipment = []
        for equipment in request.available_equipment:
            exs = query.filter(models.Exercise.equipment.contains([equipment])).all()
            exercises_by_equipment.extend(exs)

        # Also include bodyweight exercises
        bodyweight = query.filter(models.Exercise.equipment == None).all()
        exercises_by_equipment.extend(bodyweight)

        available_exercises = exercises_by_equipment
    else:
        available_exercises = query.all()

    # Filter by target muscle groups if specified
    if request.target_muscle_groups:
        filtered = []
        for ex in available_exercises:
            if any(muscle in ex.muscle_groups for muscle in request.target_muscle_groups):
                filtered.append(ex)
        available_exercises = filtered

    # Select diverse exercises (max 6)
    selected_exercises = []
    covered_muscle_groups = set()

    for exercise in available_exercises:
        if len(selected_exercises) >= 6:
            break

        # Try to get diverse muscle groups
        exercise_muscles = set(exercise.muscle_groups)
        if not exercise_muscles.intersection(covered_muscle_groups) or len(selected_exercises) < 3:
            selected_exercises.append(exercise.name)
            covered_muscle_groups.update(exercise_muscles)

    # Generate rationale
    rationale = f"Selected {len(selected_exercises)} exercises suitable for {fitness_level} level"
    if request.target_muscle_groups:
        rationale += f", targeting {', '.join(request.target_muscle_groups)}"
    rationale += ". This workout provides balanced muscle engagement and avoids recent exercises."

    return {
        "exercises": selected_exercises,
        "rationale": rationale
    }


@router.post("/suggest-workout", response_model=schemas.WorkoutSuggestion)
def suggest_workout(
    request: schemas.WorkoutSuggestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Generate AI-powered workout suggestions based on user profile and preferences"""

    # Try OpenAI if API key is available
    if settings.OPENAI_API_KEY:
        try:
            result = generate_workout_suggestion_with_openai(current_user, request, db)
        except Exception as e:
            # Fall back to rule-based
            print(f"OpenAI API failed, falling back to rule-based: {e}")
            result = generate_workout_suggestion_rule_based(current_user, request, db)
    else:
        # Use rule-based system
        result = generate_workout_suggestion_rule_based(current_user, request, db)

    # Get exercise objects
    suggested_exercise_names = result.get("exercises", [])
    exercises = db.query(models.Exercise).filter(
        models.Exercise.name.in_(suggested_exercise_names)
    ).all()

    return schemas.WorkoutSuggestion(
        recommended_workout_plan_id=None,
        suggested_exercises=exercises,
        rationale=result.get("rationale", "")
    )
