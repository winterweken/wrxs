"""
Import exercises from wger.de API into WRXS database
Run with: python -m app.import_wger_exercises
"""
import requests
import time
from app.database import SessionLocal, engine
from app.models import Base, Exercise


# wger API configuration
WGER_API_BASE = "https://wger.de/api/v2"
WGER_EXERCISE_INFO = f"{WGER_API_BASE}/exerciseinfo/"

# Mapping wger categories to WRXS categories
CATEGORY_MAPPING = {
    "Arms": "strength",
    "Legs": "strength",
    "Abs": "strength",
    "Chest": "strength",
    "Back": "strength",
    "Shoulders": "strength",
    "Calves": "strength",
    "Cardio": "cardio",
}

# Muscle group name mapping (wger uses different names)
MUSCLE_MAPPING = {
    "Biceps brachii": "biceps",
    "Anterior deltoid": "shoulders",
    "Serratus anterior": "chest",
    "Pectoralis major": "chest",
    "Triceps brachii": "triceps",
    "Latissimus dorsi": "back",
    "Brachialis": "biceps",
    "Obliquus externus abdominis": "abs",
    "Trapezius": "back",
    "Gluteus maximus": "glutes",
    "Quadriceps femoris": "quadriceps",
    "Biceps femoris": "hamstrings",
    "Gastrocnemius": "calves",
    "Soleus": "calves",
    "Rectus abdominis": "abs",
    "Deltoid": "shoulders",
    "Erector spinae": "lower back",
}

# Equipment name mapping
EQUIPMENT_MAPPING = {
    "Barbell": "barbell",
    "Dumbbell": "dumbbells",
    "Gym mat": "mat",
    "Swiss Ball": "swiss ball",
    "Pull-up bar": "pull-up bar",
    "none (bodyweight exercise)": None,
    "Bench": "bench",
    "Incline bench": "bench",
    "Kettlebell": "kettlebell",
    "EZ Bar": "ez bar",
    "Cable": "cable machine",
    "Cables": "cable machine",
}


def fetch_wger_exercises(limit=None):
    """
    Fetch exercises from wger API

    Args:
        limit: Maximum number of exercises to fetch (None for all)
    """
    exercises = []
    url = WGER_EXERCISE_INFO
    page = 1

    print(f"Fetching exercises from {WGER_API_BASE}...")

    while url:
        try:
            response = requests.get(url, params={"language": 2})  # 2 = English
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            exercises.extend(results)

            print(f"Fetched page {page}: {len(results)} exercises (Total: {len(exercises)})")

            # Check if we've reached the limit
            if limit and len(exercises) >= limit:
                exercises = exercises[:limit]
                break

            # Get next page
            url = data.get("next")
            page += 1

            # Rate limiting - be nice to the API
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"Error fetching exercises: {e}")
            break

    return exercises


def transform_wger_exercise(wger_exercise):
    """
    Transform wger exercise data to WRXS format

    Args:
        wger_exercise: Exercise data from wger API

    Returns:
        dict: Exercise data in WRXS format, or None if invalid
    """
    # Get category name
    category_data = wger_exercise.get("category", {})
    category_name = category_data.get("name", "")
    wrxs_category = CATEGORY_MAPPING.get(category_name, "strength")

    # Get primary muscles
    muscles = []
    for muscle in wger_exercise.get("muscles", []):
        # Try name_en first (cleaner), fallback to name
        muscle_name_en = muscle.get("name_en", "").strip()
        muscle_name = muscle.get("name", "").strip()

        # Use name_en if available and not empty
        if muscle_name_en:
            mapped_muscle = muscle_name_en.lower()
        else:
            mapped_muscle = MUSCLE_MAPPING.get(muscle_name, muscle_name.lower())

        if mapped_muscle and mapped_muscle not in muscles:
            muscles.append(mapped_muscle)

    # Get secondary muscles
    for muscle in wger_exercise.get("muscles_secondary", []):
        # Try name_en first (cleaner), fallback to name
        muscle_name_en = muscle.get("name_en", "").strip()
        muscle_name = muscle.get("name", "").strip()

        # Use name_en if available and not empty
        if muscle_name_en:
            mapped_muscle = muscle_name_en.lower()
        else:
            mapped_muscle = MUSCLE_MAPPING.get(muscle_name, muscle_name.lower())

        if mapped_muscle and mapped_muscle not in muscles:
            muscles.append(mapped_muscle)

    # Get equipment
    equipment_list = []
    for equip in wger_exercise.get("equipment", []):
        equip_name = equip.get("name", "")
        mapped_equip = EQUIPMENT_MAPPING.get(equip_name, equip_name.lower())
        if mapped_equip and mapped_equip not in equipment_list:
            equipment_list.append(mapped_equip)

    # Get exercise name and description from translations
    translations = wger_exercise.get("translations", [])
    if not translations:
        return None  # Skip if no translation available

    # Find English translation (language = 2)
    english_translation = None
    for trans in translations:
        if trans.get("language") == 2:
            english_translation = trans
            break

    # If no English translation, use first available
    if not english_translation:
        english_translation = translations[0]

    name = english_translation.get("name", "").strip()
    description = english_translation.get("description", "").strip()

    # Clean HTML from description if present
    if description:
        # Simple HTML tag removal (for basic cases)
        import re
        description = re.sub('<[^<]+?>', '', description)
        description = description.replace('&nbsp;', ' ').strip()

    # Get first image URL if available
    images = wger_exercise.get("images", [])
    image_url = images[0].get("image") if images else None

    # Get first video URL if available
    videos = wger_exercise.get("videos", [])
    video_url = None
    if videos:
        # Videos can have different sources, prefer YouTube
        for video in videos:
            if video.get("url"):
                video_url = video.get("url")
                break

    # Determine difficulty based on equipment and muscles
    # This is a simple heuristic since wger doesn't provide difficulty
    difficulty = "beginner"
    if len(muscles) > 3 or any(eq in ["barbell", "cable machine"] for eq in equipment_list):
        difficulty = "intermediate"
    if not equipment_list:  # Bodyweight exercises
        if len(muscles) <= 2:
            difficulty = "beginner"
        else:
            difficulty = "intermediate"

    return {
        "name": name,
        "description": description[:500] if description else None,  # Limit description length
        "category": wrxs_category,
        "muscle_groups": muscles,
        "equipment": equipment_list,
        "difficulty": difficulty,
        "instructions": description,
        "video_url": video_url,
        "image_url": image_url,
        "is_template": True,
        "created_by_id": None
    }


def import_exercises(limit=None, skip_existing=True, force=False):
    """
    Import exercises from wger into WRXS database

    Args:
        limit: Maximum number of exercises to import (None for all)
        skip_existing: If True, skip import if exercises already exist
        force: If True, skip confirmation prompt
    """
    db = SessionLocal()

    try:
        # Check if exercises already exist
        if skip_existing and not force:
            existing_count = db.query(Exercise).filter(Exercise.is_template == True).count()
            if existing_count > 0:
                print(f"Database already contains {existing_count} template exercises.")
                response = input("Do you want to continue importing? (yes/no): ")
                if response.lower() not in ['yes', 'y']:
                    print("Import cancelled.")
                    return

        # Fetch exercises from wger
        wger_exercises = fetch_wger_exercises(limit=limit)
        print(f"\nFetched {len(wger_exercises)} exercises from wger")

        # Transform and import
        imported_count = 0
        skipped_count = 0

        for wger_ex in wger_exercises:
            try:
                exercise_data = transform_wger_exercise(wger_ex)

                if not exercise_data or not exercise_data.get("name"):
                    skipped_count += 1
                    continue

                # Check if exercise with this name already exists
                existing = db.query(Exercise).filter(
                    Exercise.name == exercise_data["name"]
                ).first()

                if existing:
                    skipped_count += 1
                    continue

                # Create new exercise
                exercise = Exercise(**exercise_data)
                db.add(exercise)
                imported_count += 1

                # Commit in batches of 50
                if imported_count % 50 == 0:
                    db.commit()
                    print(f"Imported {imported_count} exercises...")

            except Exception as e:
                print(f"Error importing exercise: {e}")
                skipped_count += 1
                continue

        # Final commit
        db.commit()

        print(f"\n✓ Import complete!")
        print(f"  Imported: {imported_count} exercises")
        print(f"  Skipped: {skipped_count} exercises")

    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("WRXS Exercise Import from wger.de")
    print("=" * 60)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Check for --force flag
    force = "--force" in sys.argv or "-f" in sys.argv

    # Import exercises (limit to 100 for testing, remove limit for all)
    import_exercises(limit=None, skip_existing=True, force=force)
