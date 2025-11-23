# WRXS - Workout & Fitness Tracker

A self-hosted, multi-user fitness and workout planning application with AI-powered workout suggestions.

## Features

- **User Authentication**: Secure registration and login system
- **Exercise Library**: Comprehensive database of exercises with filtering by category, difficulty, and muscle groups
- **Workout Plans**: Create and manage custom workout plans with templates
- **Progress Tracking**: Log workouts, track sets/reps/weight over time with detailed statistics
- **AI Suggestions**: Get personalized workout recommendations based on your fitness level, available equipment, and goals
- **Multi-User Support**: Multiple users can use the same instance with isolated data
- **Self-Hosted**: Full control over your data with Docker deployment

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: ORM for database operations
- **JWT Authentication**: Secure token-based authentication
- **OpenAI API**: Optional AI-powered workout suggestions

### Frontend
- **React**: Modern UI library
- **React Router**: Client-side routing
- **Recharts**: Data visualization

### Deployment
- **Docker & Docker Compose**: Containerized deployment
- **Nginx**: Reverse proxy for frontend

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- (Optional) OpenAI API key for AI suggestions

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd wrxs
```

2. Copy the environment file and configure:
```bash
cp .env.example .env
```

3. Edit `.env` and set your configurations:
   - Generate a secure `SECRET_KEY` (use `openssl rand -hex 32`)
   - (Optional) Add your `OPENAI_API_KEY` for AI features
   - Modify database credentials if desired

4. Build and start the application:
```bash
docker-compose up -d
```

5. Seed the database with sample exercises:
```bash
docker-compose exec backend python -m app.seed_data
```

6. Access the application:
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## Usage

### First Time Setup

1. Navigate to http://localhost:3000
2. Click "Register" to create a new account
3. Fill in your profile information (weight, height, fitness level, goals)
4. Start exploring exercises and creating workout plans

### Creating a Workout Plan

1. Go to "Workout Plans" in the navigation
2. Click "Create New Plan"
3. Fill in plan details (name, difficulty, duration)
4. (Future enhancement: Add exercises to the plan)

### Logging Workouts

1. Navigate to "Workout Logs"
2. Click "Log New Workout"
3. Select an exercise
4. Enter sets, reps, weight, and notes
5. Submit to track your progress

### Getting AI Suggestions

1. Go to "AI Suggestions"
2. Select your fitness level, available equipment, and target muscle groups
3. Specify time available
4. Click "Get AI Suggestions" to receive personalized recommendations

Note: AI suggestions work without OpenAI API using a rule-based fallback system. For enhanced suggestions, add your OpenAI API key to the `.env` file.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | postgresql://wrxs_user:wrxs_password@postgres:5432/wrxs |
| `SECRET_KEY` | JWT secret key | your-secret-key-change-in-production |
| `OPENAI_API_KEY` | OpenAI API key (optional) | - |
| `REACT_APP_API_URL` | Backend API URL | http://localhost:8000 |

### Security Recommendations

For production deployment:

1. **Change default credentials**: Update PostgreSQL username and password
2. **Generate strong SECRET_KEY**: Use `openssl rand -hex 32`
3. **Use HTTPS**: Set up SSL/TLS certificates
4. **Configure CORS**: Update `CORS_ORIGINS` in backend/app/config.py
5. **Backup database**: Regularly backup PostgreSQL data

## API Documentation

Once the application is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Main Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user profile
- `GET /api/exercises` - List exercises with filters
- `POST /api/exercises` - Create custom exercise
- `GET /api/workout-plans` - List workout plans
- `POST /api/workout-plans` - Create workout plan
- `GET /api/workout-logs` - List workout logs
- `POST /api/workout-logs` - Log a workout
- `GET /api/workout-logs/stats` - Get workout statistics
- `POST /api/ai/suggest-workout` - Get AI workout suggestions

## Development

### Running Locally (Development Mode)

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm start
```

### Database Migrations

The application uses SQLAlchemy and Alembic for database migrations. To create a new migration:

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
```

### Adding Custom Exercises

You can add exercises through:
1. The web interface (Exercises page)
2. Direct API calls
3. Modifying `backend/app/seed_data.py` and re-running the seed script

## Troubleshooting

### Application won't start

- Check if ports 3000, 8000, and 5432 are available
- Verify Docker is running
- Check logs: `docker-compose logs`

### Database connection errors

- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Verify DATABASE_URL in `.env` matches docker-compose.yml

### Frontend can't connect to backend

- Check REACT_APP_API_URL in `.env`
- Verify backend is running: `curl http://localhost:8000/health`
- Check browser console for CORS errors

### AI suggestions not working

- AI suggestions work without OpenAI API (rule-based fallback)
- For enhanced AI features, add OPENAI_API_KEY to `.env`
- Check backend logs for errors

## Data Backup

To backup your PostgreSQL data:

```bash
docker-compose exec postgres pg_dump -U wrxs_user wrxs > backup.sql
```

To restore:

```bash
cat backup.sql | docker-compose exec -T postgres psql -U wrxs_user wrxs
```

## Updating

To update the application:

```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

## License

MIT License - Feel free to use and modify for your needs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
