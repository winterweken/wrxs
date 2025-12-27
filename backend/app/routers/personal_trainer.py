from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app import models, schemas, auth
from app.database import get_db
from app.services.ai_trainer import AITrainerService

router = APIRouter(prefix="/api/trainer", tags=["personal-trainer"])


@router.post("/generate-program", response_model=schemas.AITrainingProgramResponse)
def generate_training_program(
    request: schemas.TrainerProgramRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Generate a new AI training program (multi-week or daily)"""

    # Validate request
    if request.program_type not in ["daily", "multi_week"]:
        raise HTTPException(status_code=400, detail="program_type must be 'daily' or 'multi_week'")

    if request.program_type == "multi_week" and not request.duration_weeks:
        raise HTTPException(status_code=400, detail="duration_weeks required for multi_week programs")

    if request.program_type == "multi_week" and (request.duration_weeks < 1 or request.duration_weeks > 16):
        raise HTTPException(status_code=400, detail="duration_weeks must be between 1 and 16")

    # Generate program using AI trainer service
    try:
        trainer = AITrainerService(db, current_user)
        program = trainer.generate_program(request)

        # Reload with relationships
        program = db.query(models.AITrainingProgram).options(
            joinedload(models.AITrainingProgram.weekly_plans).joinedload(models.AIWeeklyPlan.daily_workouts).joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
        ).filter(models.AITrainingProgram.id == program.id).first()

        return program

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating program: {str(e)}")


@router.get("/active-program", response_model=Optional[schemas.AITrainingProgramResponse])
def get_active_program(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user's currently active training program"""

    program = db.query(models.AITrainingProgram).options(
        joinedload(models.AITrainingProgram.weekly_plans).joinedload(models.AIWeeklyPlan.daily_workouts).joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
    ).filter(
        models.AITrainingProgram.user_id == current_user.id,
        models.AITrainingProgram.status == "active"
    ).first()

    return program


@router.get("/programs", response_model=List[schemas.AITrainingProgramResponse])
def get_all_programs(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all training programs for the user"""

    query = db.query(models.AITrainingProgram).options(
        joinedload(models.AITrainingProgram.weekly_plans).joinedload(models.AIWeeklyPlan.daily_workouts).joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
    ).filter(
        models.AITrainingProgram.user_id == current_user.id
    )

    if status:
        query = query.filter(models.AITrainingProgram.status == status)

    programs = query.order_by(models.AITrainingProgram.created_at.desc()).all()

    return programs


@router.get("/program/{program_id}", response_model=schemas.AITrainingProgramResponse)
def get_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get a specific training program"""

    program = db.query(models.AITrainingProgram).options(
        joinedload(models.AITrainingProgram.weekly_plans).joinedload(models.AIWeeklyPlan.daily_workouts).joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
    ).filter(
        models.AITrainingProgram.id == program_id,
        models.AITrainingProgram.user_id == current_user.id
    ).first()

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    return program


@router.post("/accept-program/{program_id}")
def accept_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Accept and activate a training program"""

    # Get the program
    program = db.query(models.AITrainingProgram).filter(
        models.AITrainingProgram.id == program_id,
        models.AITrainingProgram.user_id == current_user.id
    ).first()

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    # Deactivate any other active programs
    db.query(models.AITrainingProgram).filter(
        models.AITrainingProgram.user_id == current_user.id,
        models.AITrainingProgram.status == "active"
    ).update({"status": "archived"})

    # Activate this program
    program.status = "active"
    program.accepted_at = datetime.utcnow()
    program.started_at = datetime.utcnow()

    db.commit()

    return {"message": "Program accepted and activated", "program_id": program_id}


@router.post("/archive-program/{program_id}")
def archive_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Archive a training program"""

    program = db.query(models.AITrainingProgram).filter(
        models.AITrainingProgram.id == program_id,
        models.AITrainingProgram.user_id == current_user.id
    ).first()

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    program.status = "archived"
    db.commit()

    return {"message": "Program archived", "program_id": program_id}


@router.get("/daily-workout", response_model=Optional[schemas.DailyWorkoutResponse])
def get_todays_workout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get today's workout from active program"""

    # Get active program
    program = db.query(models.AITrainingProgram).filter(
        models.AITrainingProgram.user_id == current_user.id,
        models.AITrainingProgram.status == "active"
    ).first()

    if not program:
        return None

    # For daily programs, get the most recent workout
    if program.program_type == "daily":
        workout = db.query(models.AIDailyWorkout).options(
            joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
        ).filter(
            models.AIDailyWorkout.training_program_id == program.id
        ).order_by(models.AIDailyWorkout.created_at.desc()).first()

        return workout

    # For multi-week programs, calculate which day we're on
    # This is a simple implementation - could be made more sophisticated
    if program.started_at:
        days_since_start = (datetime.utcnow() - program.started_at).days
        week_number = (days_since_start // 7) + 1
        day_in_week = (days_since_start % 7) + 1

        # Get the workout for this week and day
        weekly_plan = db.query(models.AIWeeklyPlan).filter(
            models.AIWeeklyPlan.training_program_id == program.id,
            models.AIWeeklyPlan.week_number == week_number
        ).first()

        if weekly_plan:
            workout = db.query(models.AIDailyWorkout).options(
                joinedload(models.AIDailyWorkout.exercises).joinedload(models.AIDailyWorkoutExercise.exercise)
            ).filter(
                models.AIDailyWorkout.weekly_plan_id == weekly_plan.id,
                models.AIDailyWorkout.day_number == min(day_in_week, program.days_per_week)
            ).first()

            return workout

    return None


@router.get("/insights", response_model=List[schemas.AdaptationInsight])
def get_adaptation_insights(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get adaptation insights for the user"""

    insights = db.query(models.AIAdaptationInsight).filter(
        models.AIAdaptationInsight.user_id == current_user.id
    ).order_by(models.AIAdaptationInsight.created_at.desc()).limit(limit).all()

    return insights


@router.post("/generate-insights", response_model=List[schemas.AdaptationInsight])
def generate_new_insights(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Generate new adaptation insights based on workout history"""

    try:
        trainer = AITrainerService(db, current_user)
        insights = trainer.generate_adaptation_insights()

        return insights

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.delete("/program/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Delete a training program"""

    program = db.query(models.AITrainingProgram).filter(
        models.AITrainingProgram.id == program_id,
        models.AITrainingProgram.user_id == current_user.id
    ).first()

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    db.delete(program)
    db.commit()

    return {"message": "Program deleted", "program_id": program_id}
