from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey,
    Boolean, Text, Table, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# Association table for workout plans and exercises
workout_exercise_association = Table(
    'workout_exercise_association',
    Base.metadata,
    Column('workout_plan_id', Integer, ForeignKey('workout_plans.id')),
    Column('exercise_id', Integer, ForeignKey('exercises.id')),
    Column('sets', Integer, default=3),
    Column('reps', Integer, default=10),
    Column('rest_seconds', Integer, default=60),
    Column('order', Integer, default=0),
    Column('notes', Text, nullable=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # User fitness profile
    weight_kg = Column(Float, nullable=True)
    height_cm = Column(Float, nullable=True)
    fitness_level = Column(String, nullable=True)  # complete_beginner, beginner, novice, intermediate, advanced, expert
    fitness_goals = Column(JSON, nullable=True)  # ["muscle_gain", "weight_loss", "endurance"]

    # User preferences
    weight_unit = Column(String, default='kg')  # kg or lbs
    distance_unit = Column(String, default='km')  # km or miles
    measurement_unit = Column(String, default='cm')  # cm or in
    age = Column(Integer, nullable=True)
    sex = Column(String, nullable=True)  # male or female
    location = Column(String, nullable=True)  # city, country

    # Relationships
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    workout_logs = relationship("WorkoutLog", back_populates="user")
    ai_training_programs = relationship("AITrainingProgram", back_populates="user")
    gym_profiles = relationship("GymProfile", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # strength, cardio, flexibility, sports
    muscle_groups = Column(JSON, nullable=False)  # ["chest", "triceps"]
    equipment = Column(JSON, nullable=True)  # ["barbell", "bench"]
    difficulty = Column(String, nullable=False)  # beginner, intermediate, advanced
    instructions = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_template = Column(Boolean, default=True)  # True for system exercises
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workout_plans = relationship("WorkoutPlan", secondary=workout_exercise_association, back_populates="exercises")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_template = Column(Boolean, default=False)  # True for shared templates
    difficulty = Column(String, nullable=False)  # beginner, intermediate, advanced
    duration_weeks = Column(Integer, nullable=True)
    days_per_week = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="workout_plans")
    exercises = relationship("Exercise", secondary=workout_exercise_association, back_populates="workout_plans")
    workout_logs = relationship("WorkoutLog", back_populates="workout_plan")


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    # Performance metrics
    sets_completed = Column(Integer, nullable=False)
    reps = Column(JSON, nullable=False)  # [12, 10, 8] - reps per set
    weight_kg = Column(JSON, nullable=True)  # [50, 50, 52.5] - weight per set
    duration_seconds = Column(Integer, nullable=True)  # for cardio
    distance_km = Column(Float, nullable=True)  # for cardio

    notes = Column(Text, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)  # 1-10

    # Relationships
    user = relationship("User", back_populates="workout_logs")
    workout_plan = relationship("WorkoutPlan", back_populates="workout_logs")
    exercise = relationship("Exercise")


class AITrainingProgram(Base):
    __tablename__ = "ai_training_programs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Program metadata
    program_type = Column(String, nullable=False)  # "daily" or "multi_week"
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Training parameters (stored as snapshot)
    fitness_level = Column(String, nullable=False)
    fitness_goals = Column(JSON, nullable=False)
    available_equipment = Column(JSON, nullable=True)
    training_preferences = Column(JSON, nullable=True)  # e.g., {"focus": "strength", "time_per_session": 60}

    # Program structure
    duration_weeks = Column(Integer, nullable=True)  # NULL for daily programs
    days_per_week = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)

    # AI metadata
    ai_rationale = Column(Text, nullable=False)  # Why this program was designed
    generation_model = Column(String, default="gpt-4-turbo-preview")

    # Status tracking
    status = Column(String, default="active")  # "active", "completed", "archived"
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="ai_training_programs")
    weekly_plans = relationship("AIWeeklyPlan", back_populates="training_program", cascade="all, delete-orphan")
    daily_workouts = relationship("AIDailyWorkout", back_populates="training_program")
    adaptation_insights = relationship("AIAdaptationInsight", back_populates="training_program")


class AIWeeklyPlan(Base):
    __tablename__ = "ai_weekly_plans"

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey("ai_training_programs.id"), nullable=False)
    week_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.

    theme = Column(String, nullable=True)  # e.g., "Strength Foundation", "Progressive Overload"
    notes = Column(Text, nullable=True)  # AI guidance for this week

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    training_program = relationship("AITrainingProgram", back_populates="weekly_plans")
    daily_workouts = relationship("AIDailyWorkout", back_populates="weekly_plan", cascade="all, delete-orphan")


class AIDailyWorkout(Base):
    __tablename__ = "ai_daily_workouts"

    id = Column(Integer, primary_key=True, index=True)
    training_program_id = Column(Integer, ForeignKey("ai_training_programs.id"), nullable=False)
    weekly_plan_id = Column(Integer, ForeignKey("ai_weekly_plans.id"), nullable=True)  # NULL for standalone daily workouts

    day_number = Column(Integer, nullable=False)  # For multi-week: day within week; For daily: sequential number
    workout_name = Column(String, nullable=False)  # e.g., "Upper Body Strength", "Leg Day"
    focus_areas = Column(JSON, nullable=False)  # ["chest", "triceps", "shoulders"]
    estimated_duration_minutes = Column(Integer, default=60)

    notes = Column(Text, nullable=True)  # AI coaching notes for this session

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    training_program = relationship("AITrainingProgram", back_populates="daily_workouts")
    weekly_plan = relationship("AIWeeklyPlan", back_populates="daily_workouts")
    exercises = relationship("AIDailyWorkoutExercise", back_populates="daily_workout", cascade="all, delete-orphan")


class AIDailyWorkoutExercise(Base):
    __tablename__ = "ai_daily_workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    daily_workout_id = Column(Integer, ForeignKey("ai_daily_workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    order = Column(Integer, default=0)
    sets = Column(Integer, nullable=False)
    reps = Column(JSON, nullable=False)  # [12, 10, 8] or ["10-12", "8-10", "6-8"]
    rest_seconds = Column(Integer, default=60)

    # Progressive overload tracking
    intensity_level = Column(String, nullable=True)  # "warm_up", "working", "heavy", "deload"
    notes = Column(Text, nullable=True)  # AI tips for this specific exercise

    # Relationships
    daily_workout = relationship("AIDailyWorkout", back_populates="exercises")
    exercise = relationship("Exercise")


class AIAdaptationInsight(Base):
    __tablename__ = "ai_adaptation_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    training_program_id = Column(Integer, ForeignKey("ai_training_programs.id"), nullable=True)

    insight_type = Column(String, nullable=False)  # "strength_plateau", "volume_increase", "recovery_needed", etc.
    insight_text = Column(Text, nullable=False)  # Human-readable insight
    data_basis = Column(JSON, nullable=False)  # {"analyzed_logs": 15, "time_range_days": 30, "key_metrics": {...}}

    recommendation = Column(Text, nullable=True)  # What the AI suggests
    applied_to_program = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    training_program = relationship("AITrainingProgram", back_populates="adaptation_insights")


class GymProfile(Base):
    __tablename__ = "gym_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)  # Custom name or gym chain name
    gym_chain = Column(String, nullable=True)  # e.g., "Goodlife Fitness", "Hone Fitness", etc.
    equipment = Column(JSON, nullable=False)  # ["barbell", "dumbbells", "cable machine", ...]

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="gym_profiles")
