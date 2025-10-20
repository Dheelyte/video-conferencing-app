# FastAPI JWT Authentication & RBAC

Production-grade FastAPI application with JWT authentication, role-based access control, and SQLAlchemy ORM.

## Features

- ✅ JWT Authentication (Access & Refresh Tokens)
- ✅ Role-Based Access Control (Admin, Moderator, User)
- ✅ Password Hashing with bcrypt
- ✅ SQLAlchemy ORM with SQLite/PostgreSQL
- ✅ Alembic Database Migrations
- ✅ Pydantic Validation & Settings
- ✅ Comprehensive Test Suite
- ✅ Auto-Generated API Documentation
- ✅ CORS Configuration
- ✅ Clean Architecture & Code Organization

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd fastapi-jwt-auth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Generate a secure secret key
openssl rand -hex 32

# Edit .env and set your SECRET_KEY and other variables
nano .env
```

**Required Environment Variables:**
- `SECRET_KEY`: JWT signing key (use `openssl rand -hex 32`)
- `FIRST_SUPERUSER_PASSWORD`: Initial admin password

### 3. Database Setup

```bash
# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Or use automatic table creation (development only)
# Tables will be created on first run
```

### 4. Create First Admin User

```python
# Run this script to create initial admin
python -c "
from app.db.session import SessionLocal
from app.db.init_db import init_db

db = SessionLocal()
init_db(db)
db.close()
"
```

### 5. Run the Application

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login (get tokens) | No |
| POST | `/api/v1/auth/refresh` | Refresh access token | No |

### Users

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/v1/users/me` | Get current user | Yes | Any |
| GET | `/api/v1/users` | List all users | Yes | Mod/Admin |
| GET | `/api/v1/users/{id}` | Get user by ID | Yes | Self/Mod/Admin |
| PATCH | `/api/v1/users/{id}` | Update user | Yes | Self/Admin |
| DELETE | `/api/v1/users/{id}` | Delete user | Yes | Admin |

## Authentication Flow

### 1. Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Authenticated Request
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"
```

### 4. Refresh Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login_success

# Verbose output
pytest -v

# Show print statements
pytest -s
```

## Project Structure

```
fastapi-jwt-auth/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── auth.py          # Auth endpoints
│   │       └── users.py         # User endpoints
│   ├── auth/
│   │   ├── jwt.py               # JWT token handling
│   │   └── security.py          # Password hashing
│   ├── core/
│   │   └── config.py            # Settings management
│   ├── crud/
│   │   └── user.py              # Database operations
│   ├── db/
│   │   ├── base.py              # Import all models
│   │   ├── init_db.py           # Initialize database
│   │   └── session.py           # Database session
│   ├── models/
│   │   └── user.py              # SQLAlchemy models
│   ├── schemas/
│   │   ├── token.py             # Token schemas
│   │   └── user.py              # User schemas
│   └── main.py                  # FastAPI app
├── tests/
│   ├── conftest.py              # Test fixtures
│   ├── test_auth.py             # Auth tests
│   └── test_users.py            # User tests
├── alembic/                     # Database migrations
├── .env                         # Environment variables
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Role-Based Access Control

### Roles

- **Admin**: Full access to all resources
- **Moderator**: Can view and moderate content
- **User**: Standard user permissions

### Permission Matrix

| Action | User | Moderator | Admin |
|--------|------|-----------|-------|
| Register | ✓ | ✓ | ✓ |
| Login | ✓ | ✓ | ✓ |
| View own profile | ✓ | ✓ | ✓ |
| Update own profile | ✓ | ✓ | ✓ |
| View all users | ✗ | ✓ | ✓ |
| View other users | ✗ | ✓ | ✓ |
| Update other users | ✗ | ✗ | ✓ |
| Change user roles | ✗ | ✗ | ✓ |
| Delete users | ✗ | ✗ | ✓ |

## Security Best Practices

### Implemented

✅ Password hashing with bcrypt  
✅ JWT token expiration  
✅ Refresh token rotation  
✅ Email validation  
✅ Role-based authorization  
✅ No password leakage in responses  
✅ Secure secret key management  
✅ CORS configuration  

### Recommended for Production

- [ ] HTTPS only (configure reverse proxy)
- [ ] Rate limiting (use slowapi)
- [ ] Email verification
- [ ] Password reset flow
- [ ] Two-factor authentication
- [ ] Token blacklist/revocation (use Redis)
- [ ] Account lockout after failed attempts
- [ ] Security headers (use fastapi-security)
- [ ] Database connection pooling
- [ ] Logging and monitoring
- [ ] Input sanitization
- [ ] SQL injection prevention (ORM handles this)

## Database

### SQLite (Development)

Default configuration uses SQLite for easy local development.

```env
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL (Production)

For production, switch to PostgreSQL:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

3. Run migrations:
```bash
alembic upgrade head
```

## Alembic Migrations

```bash
# Create migration (auto-detect changes)
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View history
alembic history

# View current version
alembic current
```

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with Docker:
```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PROJECT_NAME` | Application name | FastAPI JWT Auth | No |
| `VERSION` | API version | 1.0.0 | No |
| `API_V1_STR` | API prefix | /api/v1 | No |
| `SECRET_KEY` | JWT signing key | - | **Yes** |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | 30 | No |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | 7 | No |
| `DATABASE_URL` | Database connection | sqlite:///./app.db | No |
| `BACKEND_CORS_ORIGINS` | Allowed origins | localhost | No |
| `FIRST_SUPERUSER_EMAIL` | Admin email | admin@example.com | No |
| `FIRST_SUPERUSER_PASSWORD` | Admin password | - | **Yes** |
| `FIRST_SUPERUSER_FULL_NAME` | Admin name | Admin User | No |

## Frontend Integration

### React Example

```javascript
// authService.js
const API_URL = 'http://localhost:8000/api/v1';

export const register = async (email, password, fullName) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name: fullName })
  });
  return response.json();
};

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password })
  });
  const data = await response.json();
  
  // Store tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
};

export const getMe = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/users/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};

export const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  const response = await fetch(`${API_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  const data = await response.json();
  
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};
```

### Axios Interceptor

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auto-refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const { data } = await axios.post(
          'http://localhost:8000/api/v1/auth/refresh',
          { refresh_token: refreshToken }
        );
        
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        
        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

## Troubleshooting

### Common Issues

**1. "SECRET_KEY not set" error**
```bash
# Generate a secure key
openssl rand -hex 32

# Add to .env
SECRET_KEY=your_generated_key_here
```

**2. Database locked (SQLite)**
```bash
# Switch to PostgreSQL for production
# Or ensure only one process accesses SQLite
```

**3. CORS errors**
```python
# Add your frontend URL to .env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**4. Tests failing**
```bash
# Ensure test database is clean
pytest --cache-clear

# Check fixtures in conftest.py
pytest -v
```

**5. Alembic migration conflicts**
```bash
# Reset migrations (development only!)
rm -rf alembic/versions/*
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

## Performance Optimization

### Database Connection Pooling (PostgreSQL)

```python
# app/db/session.py
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,          # Number of persistent connections
    max_overflow=10,        # Additional connections when pool full
    pool_pre_ping=True,     # Verify connections
    pool_recycle=3600       # Recycle connections after 1 hour
)
```

### Caching User Data (Redis)

```python
# Install: pip install redis
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_user(func):
    @wraps(func)
    async def wrapper(user_id: int, *args, **kwargs):
        cache_key = f"user:{user_id}"
        cached = redis_client.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        user = await func(user_id, *args, **kwargs)
        redis_client.setex(cache_key, 300, json.dumps(user))
        return user
    
    return wrapper
```

### Rate Limiting

```python
# Install: pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...
```

## Monitoring and Logging

### Structured Logging

```python
# app/core/logging.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info("User logged in", extra={"user_id": user.id, "email": user.email})
logger.error("Login failed", extra={"email": email, "reason": "invalid_password"})
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check for load balancer.
    Checks database connection.
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.VERSION
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write docstrings for all functions
- Add tests for new features
- Update documentation
- Keep commits atomic and meaningful

## License

MIT License - see LICENSE file for details

## Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)

### Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### Tutorials
- [FastAPI Authentication Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues and documentation
- Review test files for usage examples

## Changelog

### v1.0.0 (2024-01-01)
- Initial release
- JWT authentication
- Role-based access control
- User CRUD operations
- Comprehensive test suite
- API documentation

---

**Built with ❤️ using FastAPI**