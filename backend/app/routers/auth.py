from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = auth.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = auth.get_user_by_username(db, username=user_data.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Create new user
    hashed_password = auth.get_password_hash(user_data.password)
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check for unique username/email if updating
    if user_update.username is not None and user_update.username != current_user.username:
        existing = auth.get_user_by_username(db, username=user_update.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_update.username

    if user_update.email is not None and user_update.email != current_user.email:
        existing = auth.get_user_by_email(db, email=user_update.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email

    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.weight_kg is not None:
        current_user.weight_kg = user_update.weight_kg
    if user_update.height_cm is not None:
        current_user.height_cm = user_update.height_cm
    if user_update.fitness_level is not None:
        current_user.fitness_level = user_update.fitness_level
    if user_update.fitness_goals is not None:
        current_user.fitness_goals = user_update.fitness_goals
    if user_update.weight_unit is not None:
        current_user.weight_unit = user_update.weight_unit
    if user_update.distance_unit is not None:
        current_user.distance_unit = user_update.distance_unit
    if user_update.measurement_unit is not None:
        current_user.measurement_unit = user_update.measurement_unit
    if user_update.age is not None:
        current_user.age = user_update.age
    if user_update.sex is not None:
        current_user.sex = user_update.sex
    if user_update.location is not None:
        current_user.location = user_update.location

    db.commit()
    db.refresh(current_user)
    return current_user
