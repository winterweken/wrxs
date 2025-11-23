from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, exercises, workout_plans, workout_logs, ai_suggestions

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WRXS - Workout & Fitness Tracker",
    description="Self-hosted multi-user fitness and workout planning application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(workout_plans.router)
app.include_router(workout_logs.router)
app.include_router(ai_suggestions.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to WRXS - Workout & Fitness Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
