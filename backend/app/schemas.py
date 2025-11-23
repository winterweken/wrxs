from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goals: Optional[List[str]] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goals: Optional[List[str]] = None

    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    muscle_groups: List[str]
    equipment: Optional[List[str]] = None
    difficulty: str
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int
    is_template: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Workout Plan Schemas
class WorkoutExerciseDetail(BaseModel):
    exercise_id: int
    sets: int = 3
    reps: int = 10
    rest_seconds: int = 60
    order: int = 0
    notes: Optional[str] = None


class WorkoutPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty: str
    duration_weeks: Optional[int] = None
    days_per_week: Optional[int] = None


class WorkoutPlanCreate(WorkoutPlanBase):
    exercise_details: List[WorkoutExerciseDetail] = []


class WorkoutPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    duration_weeks: Optional[int] = None
    days_per_week: Optional[int] = None
    exercise_details: Optional[List[WorkoutExerciseDetail]] = None


class WorkoutPlan(WorkoutPlanBase):
    id: int
    user_id: int
    is_template: bool
    created_at: datetime
    exercises: List[Exercise] = []

    class Config:
        from_attributes = True


# Workout Log Schemas
class WorkoutLogBase(BaseModel):
    exercise_id: int
    workout_plan_id: Optional[int] = None
    sets_completed: int
    reps: List[int]
    weight_kg: Optional[List[float]] = None
    duration_seconds: Optional[int] = None
    distance_km: Optional[float] = None
    notes: Optional[str] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)


class WorkoutLogCreate(WorkoutLogBase):
    pass


class WorkoutLog(WorkoutLogBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True


# AI Suggestion Schemas
class WorkoutSuggestionRequest(BaseModel):
    current_fitness_level: Optional[str] = None
    available_equipment: Optional[List[str]] = None
    time_available_minutes: Optional[int] = None
    target_muscle_groups: Optional[List[str]] = None


class WorkoutSuggestion(BaseModel):
    recommended_workout_plan_id: Optional[int] = None
    suggested_exercises: List[Exercise]
    rationale: str
