# Development Guide

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Local Development (Without Docker)

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database locally or use Docker:
```bash
docker run -d \
  --name wrxs-postgres \
  -e POSTGRES_DB=wrxs \
  -e POSTGRES_USER=wrxs_user \
  -e POSTGRES_PASSWORD=wrxs_password \
  -p 5432:5432 \
  postgres:15-alpine
```

5. Create `.env` file in backend directory:
```bash
DATABASE_URL=postgresql://wrxs_user:wrxs_password@localhost:5432/wrxs
SECRET_KEY=$(openssl rand -hex 32)
```

6. Run database migrations and seed data:
```bash
python -m app.seed_data
```

7. Start development server:
```bash
uvicorn app.main:app --reload --port 8000
```

Backend API will be available at http://localhost:8000

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
REACT_APP_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm start
```

Frontend will be available at http://localhost:3000

## Code Style & Standards

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions focused and small

Example:
```python
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by username.

    Args:
        db: Database session
        username: Username to search for

    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()
```

### Frontend (JavaScript/React)

- Use functional components with hooks
- Follow component naming conventions (PascalCase)
- Keep components focused (single responsibility)
- Extract reusable logic into custom hooks

Example:
```javascript
function ExerciseCard({ exercise, onSelect }) {
  return (
    <div className="exercise-card">
      <h3>{exercise.name}</h3>
      <p>{exercise.description}</p>
      <button onClick={() => onSelect(exercise)}>
        Select
      </button>
    </div>
  );
}
```

## Testing

### Backend Tests

Create test files in `backend/tests/`:

```bash
pytest
```

Example test:
```python
def test_create_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

### Frontend Tests

```bash
npm test
```

## Database Management

### Creating Migrations

1. Make changes to models in `backend/app/models.py`

2. Generate migration:
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add new field to User"
```

3. Review the generated migration in `backend/alembic/versions/`

4. Apply migration:
```bash
docker-compose exec backend alembic upgrade head
```

### Rolling Back Migrations

```bash
docker-compose exec backend alembic downgrade -1
```

### Seeding Data

Modify `backend/app/seed_data.py` and run:
```bash
docker-compose exec backend python -m app.seed_data
```

## API Development

### Adding New Endpoints

1. Create or modify router in `backend/app/routers/`

2. Define Pydantic schemas in `backend/app/schemas.py`

3. Update models if needed in `backend/app/models.py`

4. Register router in `backend/app/main.py`:
```python
from app.routers import new_router
app.include_router(new_router.router)
```

### API Testing

Use the interactive docs at http://localhost:8000/docs

Or use curl:
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=test&password=test123"

# Use token
curl http://localhost:8000/api/exercises \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Frontend Development

### Adding New Pages

1. Create component in `frontend/src/components/`

2. Add route in `frontend/src/App.js`:
```javascript
<Route path="/new-page" element={<NewPage token={token} />} />
```

3. Add navigation link in navbar

### State Management

For simple state, use useState:
```javascript
const [data, setData] = useState([]);
```

For complex state, consider useReducer:
```javascript
const [state, dispatch] = useReducer(reducer, initialState);
```

### API Calls

Create reusable API functions:
```javascript
const fetchExercises = async (token) => {
  const response = await fetch('http://localhost:8000/api/exercises', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

## Debugging

### Backend Debugging

Add print statements or use Python debugger:
```python
import pdb; pdb.set_trace()
```

View logs:
```bash
docker-compose logs -f backend
```

### Frontend Debugging

Use browser DevTools:
- Console for logs
- Network tab for API calls
- React DevTools extension

View logs:
```bash
docker-compose logs -f frontend
```

### Database Debugging

Connect to PostgreSQL:
```bash
docker-compose exec postgres psql -U wrxs_user -d wrxs
```

Useful queries:
```sql
-- List all tables
\dt

-- Describe table
\d users

-- Query data
SELECT * FROM users LIMIT 10;
```

## Performance Optimization

### Backend

1. **Database Queries**:
   - Use eager loading for relationships
   - Add indexes on frequently queried columns
   - Implement pagination

2. **Caching**:
   - Cache exercise library (rarely changes)
   - Consider Redis for session storage

### Frontend

1. **React Performance**:
   - Use React.memo for expensive components
   - Implement lazy loading for routes
   - Debounce search/filter inputs

2. **API Calls**:
   - Implement request caching
   - Use React Query or SWR
   - Batch requests when possible

## Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Errors

1. Check PostgreSQL is running:
```bash
docker-compose ps
```

2. Check connection string in `.env`

3. Reset database:
```bash
docker-compose down -v
docker-compose up -d
```

### CORS Errors

1. Check `CORS_ORIGINS` in `backend/app/config.py`
2. Verify frontend URL matches allowed origins
3. Clear browser cache

### Frontend Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Git Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes

### Commit Messages

Follow conventional commits:
```
feat: Add exercise filtering by equipment
fix: Resolve login token expiration issue
docs: Update API documentation
refactor: Simplify workout log component
test: Add tests for user registration
```

### Pull Request Process

1. Create feature branch
2. Make changes and commit
3. Write tests
4. Update documentation
5. Create PR with description
6. Address review comments
7. Merge after approval

## Deployment

### Building for Production

Backend:
```bash
cd backend
docker build -t wrxs-backend:latest .
```

Frontend:
```bash
cd frontend
npm run build
docker build -t wrxs-frontend:latest .
```

### Environment Configuration

Production `.env` example:
```bash
# Strong secret key
SECRET_KEY=$(openssl rand -hex 32)

# Production database
DATABASE_URL=postgresql://user:password@db-host:5432/wrxs

# Optional OpenAI
OPENAI_API_KEY=sk-...

# Production URL
REACT_APP_API_URL=https://api.yourdomain.com
```

### Docker Compose Production

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'
services:
  postgres:
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    restart: always
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  frontend:
    restart: always
```

Run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
