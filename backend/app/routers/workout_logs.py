from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/workout-logs", tags=["workout-logs"])


@router.get("/", response_model=List[schemas.WorkoutLog])
def get_workout_logs(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    exercise_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    query = db.query(models.WorkoutLog).filter(
        models.WorkoutLog.user_id == current_user.id
    )

    if start_date:
        query = query.filter(models.WorkoutLog.date >= start_date)
    if end_date:
        query = query.filter(models.WorkoutLog.date <= end_date)
    if exercise_id:
        query = query.filter(models.WorkoutLog.exercise_id == exercise_id)

    logs = query.order_by(models.WorkoutLog.date.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/stats")
def get_workout_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    start_date = datetime.utcnow() - timedelta(days=days)

    # Total workouts
    total_workouts = db.query(func.count(models.WorkoutLog.id)).filter(
        and_(
            models.WorkoutLog.user_id == current_user.id,
            models.WorkoutLog.date >= start_date
        )
    ).scalar()

    # Total sets
    total_sets = db.query(func.sum(models.WorkoutLog.sets_completed)).filter(
        and_(
            models.WorkoutLog.user_id == current_user.id,
            models.WorkoutLog.date >= start_date
        )
    ).scalar() or 0

    # Most performed exercises
    most_performed = db.query(
        models.Exercise.name,
        func.count(models.WorkoutLog.id).label('count')
    ).join(
        models.WorkoutLog,
        models.Exercise.id == models.WorkoutLog.exercise_id
    ).filter(
        and_(
            models.WorkoutLog.user_id == current_user.id,
            models.WorkoutLog.date >= start_date
        )
    ).group_by(models.Exercise.name).order_by(func.count(models.WorkoutLog.id).desc()).limit(5).all()

    return {
        "period_days": days,
        "total_workouts": total_workouts,
        "total_sets": total_sets,
        "most_performed_exercises": [{"name": name, "count": count} for name, count in most_performed]
    }


@router.get("/{log_id}", response_model=schemas.WorkoutLog)
def get_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    log = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")

    return log


@router.post("/", response_model=schemas.WorkoutLog)
def create_workout_log(
    log_data: schemas.WorkoutLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify exercise exists
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == log_data.exercise_id
    ).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Verify workout plan exists if provided
    if log_data.workout_plan_id:
        plan = db.query(models.WorkoutPlan).filter(
            models.WorkoutPlan.id == log_data.workout_plan_id
        ).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Workout plan not found")

    db_log = models.WorkoutLog(
        **log_data.model_dump(),
        user_id=current_user.id
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.delete("/{log_id}")
def delete_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    log = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this log")

    db.delete(log)
    db.commit()
    return {"message": "Workout log deleted successfully"}
