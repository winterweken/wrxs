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
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goals: Optional[List[str]] = None
    weight_unit: Optional[str] = None
    distance_unit: Optional[str] = None
    measurement_unit: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    location: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goals: Optional[List[str]] = None
    weight_unit: Optional[str] = None
    distance_unit: Optional[str] = None
    measurement_unit: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    location: Optional[str] = None

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


# Personal Trainer Schemas
class TrainerProgramRequest(BaseModel):
    program_type: str  # "daily" or "multi_week"
    duration_weeks: Optional[int] = None
    days_per_week: int = 3
    fitness_level: Optional[str] = None
    fitness_goals: Optional[List[str]] = None
    available_equipment: Optional[List[str]] = None
    time_per_session_minutes: int = 60
    preferences: Optional[dict] = None


class DailyWorkoutExerciseResponse(BaseModel):
    id: int
    exercise: Exercise
    order: int
    sets: int
    reps: List  # Can be List[int] or List[str] for ranges like "10-12"
    rest_seconds: int
    intensity_level: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class DailyWorkoutResponse(BaseModel):
    id: int
    workout_name: str
    focus_areas: List[str]
    estimated_duration_minutes: int
    notes: Optional[str] = None
    day_number: int
    exercises: List[DailyWorkoutExerciseResponse] = []

    class Config:
        from_attributes = True


class WeeklyPlanResponse(BaseModel):
    id: int
    week_number: int
    theme: Optional[str] = None
    notes: Optional[str] = None
    daily_workouts: List[DailyWorkoutResponse] = []

    class Config:
        from_attributes = True


class AITrainingProgramResponse(BaseModel):
    id: int
    program_type: str
    name: str
    description: Optional[str] = None
    ai_rationale: str
    fitness_level: str
    fitness_goals: List[str]
    available_equipment: Optional[List[str]] = None
    duration_weeks: Optional[int] = None
    days_per_week: int
    difficulty: str
    status: str
    created_at: datetime
    weekly_plans: List[WeeklyPlanResponse] = []

    class Config:
        from_attributes = True


class AdaptationInsight(BaseModel):
    id: int
    insight_type: str
    insight_text: str
    data_basis: dict
    recommendation: Optional[str] = None
    applied_to_program: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Gym Profile Schemas
class GymProfileBase(BaseModel):
    name: str
    gym_chain: Optional[str] = None
    equipment: List[str]


class GymProfileCreate(GymProfileBase):
    pass


class GymProfileUpdate(BaseModel):
    name: Optional[str] = None
    gym_chain: Optional[str] = None
    equipment: Optional[List[str]] = None


class GymProfile(GymProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
