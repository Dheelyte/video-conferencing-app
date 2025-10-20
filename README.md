# Video Conferencing Application


### Access API Documentation

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

## Role-Based Access Control

### Roles

- **Admin**: Full access to all resources
- **Moderator**: Can view and moderate content
- **User**: Standard user permissions

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
