# WRXS Architecture Documentation

## System Overview

WRXS is a full-stack web application designed with a modern, containerized architecture.

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│   Nginx     │────▶│   Backend    │
│  (Frontend) │     │   FastAPI    │
└─────────────┘     └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   Database   │
                    └──────────────┘
```

## Component Architecture

### Backend (FastAPI)

**Location**: `/backend`

#### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── seed_data.py         # Database seeding
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── exercises.py     # Exercise CRUD
│       ├── workout_plans.py # Workout plan CRUD
│       ├── workout_logs.py  # Logging and stats
│       └── ai_suggestions.py# AI recommendations
├── Dockerfile
└── requirements.txt
```

#### Key Components

**Models** (`models.py`):
- `User`: User accounts and fitness profiles
- `Exercise`: Exercise library (system and user-created)
- `WorkoutPlan`: User workout plans
- `WorkoutLog`: Workout history and progress
- `workout_exercise_association`: Many-to-many relationship table

**Authentication** (`auth.py`):
- JWT token generation and validation
- Password hashing (bcrypt)
- OAuth2 password bearer flow
- User dependency injection

**API Routers**:
Each router handles a specific domain:
- Auth: Registration, login, profile management
- Exercises: CRUD operations with filtering
- Workout Plans: Plan creation and management
- Workout Logs: Progress tracking and statistics
- AI Suggestions: Intelligent workout recommendations

### Frontend (React)

**Location**: `/frontend`

#### Directory Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js             # React entry point
│   ├── index.css            # Global styles
│   ├── App.js               # Main app component
│   └── components/
│       ├── Login.js
│       ├── Register.js
│       ├── Dashboard.js
│       ├── Exercises.js
│       ├── WorkoutPlans.js
│       ├── WorkoutLogs.js
│       ├── Profile.js
│       └── AISuggestions.js
├── Dockerfile
├── nginx.conf
└── package.json
```

#### Component Hierarchy

```
App
├── Router
    ├── Login / Register (unauthenticated)
    └── Authenticated Routes
        ├── Dashboard
        ├── Exercises
        ├── WorkoutPlans
        ├── WorkoutLogs
        ├── Profile
        └── AISuggestions
```

#### State Management

- Local component state (useState)
- Token stored in localStorage
- User profile fetched on mount
- No Redux (intentionally kept simple)

### Database (PostgreSQL)

#### Schema Design

**Users Table**:
```sql
users (
  id SERIAL PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  username VARCHAR UNIQUE NOT NULL,
  hashed_password VARCHAR NOT NULL,
  full_name VARCHAR,
  is_active BOOLEAN,
  created_at TIMESTAMP,
  -- Fitness profile
  weight_kg FLOAT,
  height_cm FLOAT,
  fitness_level VARCHAR,
  fitness_goals JSON
)
```

**Exercises Table**:
```sql
exercises (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  description TEXT,
  category VARCHAR NOT NULL,  -- strength, cardio, flexibility
  muscle_groups JSON NOT NULL,
  equipment JSON,
  difficulty VARCHAR NOT NULL,
  instructions TEXT,
  video_url VARCHAR,
  image_url VARCHAR,
  is_template BOOLEAN,
  created_by_id INTEGER FK,
  created_at TIMESTAMP
)
```

**Workout Plans Table**:
```sql
workout_plans (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  description TEXT,
  user_id INTEGER FK NOT NULL,
  is_template BOOLEAN,
  difficulty VARCHAR NOT NULL,
  duration_weeks INTEGER,
  days_per_week INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**Workout Logs Table**:
```sql
workout_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER FK NOT NULL,
  workout_plan_id INTEGER FK,
  exercise_id INTEGER FK NOT NULL,
  date TIMESTAMP,
  sets_completed INTEGER NOT NULL,
  reps JSON NOT NULL,
  weight_kg JSON,
  duration_seconds INTEGER,
  distance_km FLOAT,
  notes TEXT,
  difficulty_rating INTEGER
)
```

**Association Table**:
```sql
workout_exercise_association (
  workout_plan_id INTEGER FK,
  exercise_id INTEGER FK,
  sets INTEGER,
  reps INTEGER,
  rest_seconds INTEGER,
  order INTEGER,
  notes TEXT
)
```

## Data Flow

### Authentication Flow

```
1. User registers/logs in
   ├─▶ Frontend sends credentials
   ├─▶ Backend validates
   ├─▶ Backend generates JWT token
   └─▶ Frontend stores token in localStorage

2. Authenticated requests
   ├─▶ Frontend includes token in Authorization header
   ├─▶ Backend validates token
   ├─▶ Backend extracts user from token
   └─▶ Backend processes request with user context
```

### Workout Logging Flow

```
1. User logs workout
   ├─▶ Select exercise from library
   ├─▶ Enter performance data (sets, reps, weight)
   ├─▶ Frontend sends to POST /api/workout-logs
   ├─▶ Backend validates and creates log entry
   └─▶ Database stores with timestamp

2. View statistics
   ├─▶ Frontend requests GET /api/workout-logs/stats
   ├─▶ Backend aggregates data (SQL queries)
   └─▶ Frontend displays charts and summaries
```

### AI Suggestions Flow

```
1. OpenAI Available:
   ├─▶ User submits preferences
   ├─▶ Backend builds context from user profile + history
   ├─▶ Backend calls OpenAI API
   ├─▶ Backend parses AI response
   └─▶ Frontend displays suggestions

2. OpenAI Unavailable (Fallback):
   ├─▶ User submits preferences
   ├─▶ Backend uses rule-based algorithm
   │   ├─ Filter by fitness level
   │   ├─ Filter by equipment
   │   ├─ Avoid recently performed exercises
   │   └─ Select diverse muscle groups
   └─▶ Frontend displays suggestions
```

## Security Architecture

### Authentication
- JWT tokens with HS256 algorithm
- Bcrypt password hashing (12 rounds)
- Token expiration (7 days default)
- Secure token storage (localStorage)

### Authorization
- User-scoped data isolation
- Ownership checks on resources
- Template vs user-created content separation

### Data Protection
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (React auto-escaping)
- CORS configuration
- Environment variable secrets

## Deployment Architecture

### Docker Compose Services

```yaml
services:
  postgres:     # Database (port 5432)
  backend:      # API (port 8000)
  frontend:     # UI (port 3000/80)
```

### Container Communication
- Backend connects to postgres via service name
- Frontend proxies API requests through nginx
- Containers share Docker network

### Volume Persistence
- `postgres_data`: Persistent database storage
- Backend/Frontend: Development volume mounts

## Performance Considerations

### Backend
- Database connection pooling (SQLAlchemy)
- Async/await support (FastAPI + uvicorn)
- Indexed database columns (email, username)
- Query pagination (limit/offset)

### Frontend
- Code splitting (React lazy loading potential)
- Minimal dependencies
- Nginx gzip compression
- Static asset caching

### Database
- Proper indexing on foreign keys
- JSON columns for flexible data
- Timestamp indexes for log queries

## Scalability Path

### Current Limitations
- Single database instance
- No caching layer
- Stateful JWT in localStorage

### Future Enhancements
- **Horizontal Scaling**: Add load balancer, stateless API
- **Database**: Read replicas, connection pooling
- **Caching**: Redis for sessions and frequent queries
- **CDN**: Static asset distribution
- **Object Storage**: Exercise images/videos (S3)
- **Background Jobs**: Celery for async tasks
- **Monitoring**: Prometheus + Grafana

## Extension Points

### Adding New Features

1. **New Exercise Types**:
   - Add category to exercise model
   - Update seed data
   - Add filter in frontend

2. **Social Features**:
   - Add workout sharing table
   - Create social router
   - Build social component

3. **Mobile App**:
   - API already supports mobile clients
   - Implement React Native or native apps
   - Same authentication flow

4. **Advanced Analytics**:
   - Add analytics router
   - Implement more complex SQL queries
   - Create visualization components

5. **Coach/Admin Role**:
   - Add role column to users
   - Implement RBAC middleware
   - Create admin dashboard
