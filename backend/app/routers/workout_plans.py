from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, auth
from app.database import get_db
from app.models import workout_exercise_association

router = APIRouter(prefix="/api/workout-plans", tags=["workout-plans"])


@router.get("/", response_model=List[schemas.WorkoutPlan])
def get_workout_plans(
    skip: int = 0,
    limit: int = 100,
    templates_only: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if templates_only:
        plans = db.query(models.WorkoutPlan).filter(
            models.WorkoutPlan.is_template == True
        ).offset(skip).limit(limit).all()
    else:
        plans = db.query(models.WorkoutPlan).filter(
            models.WorkoutPlan.user_id == current_user.id
        ).offset(skip).limit(limit).all()

    return plans


@router.get("/{plan_id}", response_model=schemas.WorkoutPlan)
def get_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    plan = db.query(models.WorkoutPlan).filter(models.WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    # Check if user owns the plan or it's a template
    if plan.user_id != current_user.id and not plan.is_template:
        raise HTTPException(status_code=403, detail="Not authorized to access this plan")

    return plan


@router.post("/", response_model=schemas.WorkoutPlan)
def create_workout_plan(
    plan_data: schemas.WorkoutPlanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Create workout plan
    db_plan = models.WorkoutPlan(
        name=plan_data.name,
        description=plan_data.description,
        difficulty=plan_data.difficulty,
        duration_weeks=plan_data.duration_weeks,
        days_per_week=plan_data.days_per_week,
        user_id=current_user.id,
        is_template=False
    )
    db.add(db_plan)
    db.flush()

    # Add exercises to plan
    for exercise_detail in plan_data.exercise_details:
        exercise = db.query(models.Exercise).filter(
            models.Exercise.id == exercise_detail.exercise_id
        ).first()
        if not exercise:
            raise HTTPException(
                status_code=404,
                detail=f"Exercise {exercise_detail.exercise_id} not found"
            )

        # Add to association table with details
        stmt = workout_exercise_association.insert().values(
            workout_plan_id=db_plan.id,
            exercise_id=exercise_detail.exercise_id,
            sets=exercise_detail.sets,
            reps=exercise_detail.reps,
            rest_seconds=exercise_detail.rest_seconds,
            order=exercise_detail.order,
            notes=exercise_detail.notes
        )
        db.execute(stmt)

    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.put("/{plan_id}", response_model=schemas.WorkoutPlan)
def update_workout_plan(
    plan_id: int,
    plan_update: schemas.WorkoutPlanUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    plan = db.query(models.WorkoutPlan).filter(models.WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    if plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this plan")

    # Update basic fields
    if plan_update.name is not None:
        plan.name = plan_update.name
    if plan_update.description is not None:
        plan.description = plan_update.description
    if plan_update.difficulty is not None:
        plan.difficulty = plan_update.difficulty
    if plan_update.duration_weeks is not None:
        plan.duration_weeks = plan_update.duration_weeks
    if plan_update.days_per_week is not None:
        plan.days_per_week = plan_update.days_per_week

    # Update exercises if provided
    if plan_update.exercise_details is not None:
        # Clear existing exercises
        db.execute(
            workout_exercise_association.delete().where(
                workout_exercise_association.c.workout_plan_id == plan_id
            )
        )

        # Add updated exercises
        for exercise_detail in plan_update.exercise_details:
            stmt = workout_exercise_association.insert().values(
                workout_plan_id=plan_id,
                exercise_id=exercise_detail.exercise_id,
                sets=exercise_detail.sets,
                reps=exercise_detail.reps,
                rest_seconds=exercise_detail.rest_seconds,
                order=exercise_detail.order,
                notes=exercise_detail.notes
            )
            db.execute(stmt)

    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/{plan_id}")
def delete_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    plan = db.query(models.WorkoutPlan).filter(models.WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    if plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this plan")

    db.delete(plan)
    db.commit()
    return {"message": "Workout plan deleted successfully"}
