from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.get("/", response_model=List[schemas.Exercise])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    muscle_group: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    query = db.query(models.Exercise)

    # Filter by category
    if category:
        query = query.filter(models.Exercise.category == category)

    # Filter by difficulty
    if difficulty:
        query = query.filter(models.Exercise.difficulty == difficulty)

    # Filter by muscle group
    if muscle_group:
        query = query.filter(models.Exercise.muscle_groups.contains([muscle_group]))

    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/{exercise_id}", response_model=schemas.Exercise)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.post("/", response_model=schemas.Exercise)
def create_exercise(
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_exercise = models.Exercise(
        **exercise.model_dump(),
        is_template=False,
        created_by_id=current_user.id
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Only allow deletion of user-created exercises
    if exercise.is_template or exercise.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete this exercise")

    db.delete(exercise)
    db.commit()
    return {"message": "Exercise deleted successfully"}
