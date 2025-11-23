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
    fitness_level = Column(String, nullable=True)  # beginner, intermediate, advanced
    fitness_goals = Column(JSON, nullable=True)  # ["muscle_gain", "weight_loss", "endurance"]

    # Relationships
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    workout_logs = relationship("WorkoutLog", back_populates="user")


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
