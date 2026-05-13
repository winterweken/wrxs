from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/gym-profiles", tags=["gym-profiles"])


@router.get("/", response_model=List[schemas.GymProfile])
def get_gym_profiles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all gym profiles for the current user"""
    profiles = db.query(models.GymProfile).filter(
        models.GymProfile.user_id == current_user.id
    ).all()
    return profiles


@router.post("/", response_model=schemas.GymProfile, status_code=status.HTTP_201_CREATED)
def create_gym_profile(
    profile_data: schemas.GymProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new gym profile"""
    gym_profile = models.GymProfile(
        user_id=current_user.id,
        name=profile_data.name,
        gym_chain=profile_data.gym_chain,
        equipment=profile_data.equipment
    )
    db.add(gym_profile)
    db.commit()
    db.refresh(gym_profile)
    return gym_profile


@router.get("/{profile_id}", response_model=schemas.GymProfile)
def get_gym_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get a specific gym profile"""
    profile = db.query(models.GymProfile).filter(
        models.GymProfile.id == profile_id,
        models.GymProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Gym profile not found")

    return profile


@router.put("/{profile_id}", response_model=schemas.GymProfile)
def update_gym_profile(
    profile_id: int,
    profile_update: schemas.GymProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update a gym profile"""
    profile = db.query(models.GymProfile).filter(
        models.GymProfile.id == profile_id,
        models.GymProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Gym profile not found")

    if profile_update.name is not None:
        profile.name = profile_update.name
    if profile_update.gym_chain is not None:
        profile.gym_chain = profile_update.gym_chain
    if profile_update.equipment is not None:
        profile.equipment = profile_update.equipment

    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gym_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Delete a gym profile"""
    profile = db.query(models.GymProfile).filter(
        models.GymProfile.id == profile_id,
        models.GymProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Gym profile not found")

    db.delete(profile)
    db.commit()
    return None
