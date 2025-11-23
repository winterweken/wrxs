"""
Seed database with sample exercises
Run with: python -m app.seed_data
"""
from app.database import SessionLocal, engine
from app.models import Base, Exercise

# Sample exercises database
SAMPLE_EXERCISES = [
    # Chest exercises
    {
        "name": "Bench Press",
        "description": "Classic chest exercise using a barbell on a bench",
        "category": "strength",
        "muscle_groups": ["chest", "triceps", "shoulders"],
        "equipment": ["barbell", "bench"],
        "difficulty": "intermediate",
        "instructions": "Lie on bench, lower bar to chest, press up explosively"
    },
    {
        "name": "Push-ups",
        "description": "Bodyweight chest exercise",
        "category": "strength",
        "muscle_groups": ["chest", "triceps", "core"],
        "equipment": [],
        "difficulty": "beginner",
        "instructions": "Start in plank, lower body to ground, push back up"
    },
    {
        "name": "Dumbbell Flyes",
        "description": "Isolation exercise for chest",
        "category": "strength",
        "muscle_groups": ["chest"],
        "equipment": ["dumbbells", "bench"],
        "difficulty": "intermediate",
        "instructions": "Lie on bench, arc dumbbells out and down, squeeze chest to bring back up"
    },
    # Back exercises
    {
        "name": "Pull-ups",
        "description": "Bodyweight back exercise",
        "category": "strength",
        "muscle_groups": ["back", "biceps"],
        "equipment": ["pull-up bar"],
        "difficulty": "intermediate",
        "instructions": "Hang from bar, pull body up until chin over bar"
    },
    {
        "name": "Barbell Rows",
        "description": "Compound back exercise",
        "category": "strength",
        "muscle_groups": ["back", "biceps"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "instructions": "Bend at hips, pull bar to lower chest, squeeze shoulder blades"
    },
    {
        "name": "Lat Pulldown",
        "description": "Machine exercise for back width",
        "category": "strength",
        "muscle_groups": ["back", "biceps"],
        "equipment": ["cable machine"],
        "difficulty": "beginner",
        "instructions": "Pull bar down to upper chest, control the ascent"
    },
    # Leg exercises
    {
        "name": "Squats",
        "description": "King of leg exercises",
        "category": "strength",
        "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "instructions": "Bar on upper back, descend until thighs parallel, drive up through heels"
    },
    {
        "name": "Lunges",
        "description": "Unilateral leg exercise",
        "category": "strength",
        "muscle_groups": ["quadriceps", "glutes"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "instructions": "Step forward, lower back knee, push back to starting position"
    },
    {
        "name": "Romanian Deadlift",
        "description": "Hamstring and glute focused",
        "category": "strength",
        "muscle_groups": ["hamstrings", "glutes", "lower back"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "instructions": "Keep back straight, hinge at hips, lower bar along legs"
    },
    {
        "name": "Leg Press",
        "description": "Machine-based quad exercise",
        "category": "strength",
        "muscle_groups": ["quadriceps", "glutes"],
        "equipment": ["leg press machine"],
        "difficulty": "beginner",
        "instructions": "Push platform away with feet, control the descent"
    },
    # Shoulder exercises
    {
        "name": "Overhead Press",
        "description": "Compound shoulder exercise",
        "category": "strength",
        "muscle_groups": ["shoulders", "triceps"],
        "equipment": ["barbell"],
        "difficulty": "intermediate",
        "instructions": "Press bar from shoulders to overhead, keep core tight"
    },
    {
        "name": "Lateral Raises",
        "description": "Isolation for side delts",
        "category": "strength",
        "muscle_groups": ["shoulders"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "instructions": "Raise arms to sides until parallel with ground"
    },
    # Arm exercises
    {
        "name": "Bicep Curls",
        "description": "Classic bicep exercise",
        "category": "strength",
        "muscle_groups": ["biceps"],
        "equipment": ["dumbbells"],
        "difficulty": "beginner",
        "instructions": "Curl weights up, keep elbows stationary"
    },
    {
        "name": "Tricep Dips",
        "description": "Bodyweight tricep exercise",
        "category": "strength",
        "muscle_groups": ["triceps", "chest"],
        "equipment": ["dip bars"],
        "difficulty": "intermediate",
        "instructions": "Lower body by bending elbows, push back up"
    },
    # Core exercises
    {
        "name": "Plank",
        "description": "Isometric core exercise",
        "category": "strength",
        "muscle_groups": ["core", "abs"],
        "equipment": [],
        "difficulty": "beginner",
        "instructions": "Hold push-up position, keep body straight"
    },
    {
        "name": "Hanging Leg Raises",
        "description": "Advanced ab exercise",
        "category": "strength",
        "muscle_groups": ["abs", "core"],
        "equipment": ["pull-up bar"],
        "difficulty": "advanced",
        "instructions": "Hang from bar, raise legs to 90 degrees"
    },
    # Cardio exercises
    {
        "name": "Running",
        "description": "Cardiovascular exercise",
        "category": "cardio",
        "muscle_groups": ["legs", "cardiovascular"],
        "equipment": [],
        "difficulty": "beginner",
        "instructions": "Run at steady pace for desired duration"
    },
    {
        "name": "Burpees",
        "description": "Full body cardio exercise",
        "category": "cardio",
        "muscle_groups": ["full body", "cardiovascular"],
        "equipment": [],
        "difficulty": "intermediate",
        "instructions": "Drop to push-up, kick feet back, push up, jump"
    },
    {
        "name": "Jump Rope",
        "description": "Cardio and coordination",
        "category": "cardio",
        "muscle_groups": ["calves", "cardiovascular"],
        "equipment": ["jump rope"],
        "difficulty": "beginner",
        "instructions": "Jump over rope with each rotation"
    },
]


def seed_exercises():
    db = SessionLocal()
    try:
        # Check if exercises already exist
        existing_count = db.query(Exercise).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} exercises. Skipping seed.")
            return

        # Add exercises
        for exercise_data in SAMPLE_EXERCISES:
            exercise = Exercise(
                **exercise_data,
                is_template=True,
                created_by_id=None
            )
            db.add(exercise)

        db.commit()
        print(f"Successfully seeded {len(SAMPLE_EXERCISES)} exercises")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding database with sample exercises...")
    Base.metadata.create_all(bind=engine)
    seed_exercises()
