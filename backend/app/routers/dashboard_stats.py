from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app import models, auth
from app.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/weekly-streak")
def get_weekly_streak(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Returns workout status for current week (Mon-Sun)"""
    # Calculate current week boundaries
    today = datetime.utcnow()
    monday = today - timedelta(days=today.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    sunday = monday + timedelta(days=6, hours=23, minutes=59)

    # Query workouts grouped by date
    logs = db.query(
        func.date(models.WorkoutLog.date).label('date'),
        func.count(models.WorkoutLog.id).label('count')
    ).filter(
        and_(
            models.WorkoutLog.user_id == current_user.id,
            models.WorkoutLog.date >= monday,
            models.WorkoutLog.date <= sunday
        )
    ).group_by(func.date(models.WorkoutLog.date)).all()

    # Build 7-day array
    workout_dates = {log.date: log.count for log in logs}
    days = []
    for i in range(7):
        day_date = (monday + timedelta(days=i)).date()
        days.append({
            "date": day_date.isoformat(),
            "day_name": day_date.strftime("%A"),
            "has_workout": day_date in workout_dates,
            "workout_count": workout_dates.get(day_date, 0)
        })

    return {
        "week_start": monday.date().isoformat(),
        "week_end": sunday.date().isoformat(),
        "days": days,
        "total_workout_days": len([d for d in days if d['has_workout']]),
        "total_workouts": sum(d['workout_count'] for d in days)
    }


@router.get("/current-streak")
def get_current_streak(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Calculates consecutive days with workouts"""
    # Get distinct workout dates
    workout_dates = db.query(
        func.date(models.WorkoutLog.date).label('date')
    ).filter(
        models.WorkoutLog.user_id == current_user.id
    ).distinct().order_by(
        func.date(models.WorkoutLog.date).desc()
    ).all()

    if not workout_dates:
        return {"current_streak": 0, "longest_streak": 0, "streak_status": "none"}

    dates = [d.date for d in workout_dates]
    today = datetime.utcnow().date()

    # Calculate current streak
    current_streak = 0
    if dates[0] == today or dates[0] == today - timedelta(days=1):
        current_streak = 1
        for i in range(1, len(dates)):
            if (dates[i-1] - dates[i]).days == 1:
                current_streak += 1
            else:
                break

    # Calculate longest streak (full historical scan)
    longest_streak = current_streak
    temp_streak = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    return {
        "current_streak": current_streak,
        "longest_streak": max(longest_streak, current_streak),
        "last_workout_date": dates[0].isoformat(),
        "streak_status": "active" if current_streak > 0 else "broken"
    }


@router.get("/week-comparison")
def get_week_comparison(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Compare current week vs previous week stats"""
    today = datetime.utcnow()

    # Current week
    curr_monday = today - timedelta(days=today.weekday())
    curr_monday = curr_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    curr_sunday = curr_monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Previous week
    prev_monday = curr_monday - timedelta(days=7)
    prev_sunday = curr_sunday - timedelta(days=7)

    def get_week_stats(start, end):
        logs = db.query(models.WorkoutLog).filter(
            and_(
                models.WorkoutLog.user_id == current_user.id,
                models.WorkoutLog.date >= start,
                models.WorkoutLog.date <= end
            )
        ).all()

        total_workouts = len(logs)
        total_sets = sum(log.sets_completed for log in logs)

        # Calculate volume
        total_volume = 0
        for log in logs:
            if log.weight_kg and log.reps:
                for w, r in zip(log.weight_kg, log.reps):
                    total_volume += w * r

        workout_days = len(set(log.date.date() for log in logs))
        unique_exercises = len(set(log.exercise_id for log in logs))

        return {
            "total_workouts": total_workouts,
            "total_sets": total_sets,
            "total_volume_kg": round(total_volume, 1),
            "workout_days": workout_days,
            "unique_exercises": unique_exercises
        }

    current = get_week_stats(curr_monday, curr_sunday)
    previous = get_week_stats(prev_monday, prev_sunday)

    # Calculate changes
    def calc_change(curr, prev):
        change = curr - prev
        percent = (change / prev * 100) if prev > 0 else 0
        return {"change": change, "percent": round(percent, 1)}

    return {
        "current_week": {**current, "start_date": curr_monday.date().isoformat()},
        "previous_week": {**previous, "start_date": prev_monday.date().isoformat()},
        "comparison": {
            "workouts": calc_change(current['total_workouts'], previous['total_workouts']),
            "sets": calc_change(current['total_sets'], previous['total_sets']),
            "volume": calc_change(current['total_volume_kg'], previous['total_volume_kg']),
            "workout_days": calc_change(current['workout_days'], previous['workout_days'])
        }
    }


@router.get("/frequency-chart")
def get_frequency_chart(
    weeks: int = Query(default=12, ge=1, le=52),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Weekly workout frequency over time"""
    today = datetime.utcnow()
    start_date = today - timedelta(weeks=weeks)

    # Query workouts grouped by week
    logs = db.query(
        func.date_trunc('week', models.WorkoutLog.date).label('week_start'),
        func.count(models.WorkoutLog.id).label('workout_count'),
        func.count(func.distinct(func.date(models.WorkoutLog.date))).label('workout_days')
    ).filter(
        and_(
            models.WorkoutLog.user_id == current_user.id,
            models.WorkoutLog.date >= start_date
        )
    ).group_by('week_start').order_by('week_start').all()

    # Format for Recharts
    weekly_data = []
    for log in logs:
        weekly_data.append({
            "week_start": log.week_start.date().isoformat(),
            "week_label": log.week_start.strftime("%b %d"),
            "workout_count": log.workout_count,
            "workout_days": log.workout_days
        })

    # Calculate trend
    if len(weekly_data) >= 2:
        first_half_avg = sum(w['workout_count'] for w in weekly_data[:len(weekly_data)//2]) / max(len(weekly_data)//2, 1)
        second_half_avg = sum(w['workout_count'] for w in weekly_data[len(weekly_data)//2:]) / max(len(weekly_data) - len(weekly_data)//2, 1)

        if second_half_avg > first_half_avg * 1.1:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "stable"

    return {
        "weeks": weekly_data,
        "period_weeks": weeks,
        "trend": trend
    }
