mkdir -p fastapi-jwt-auth
cd fastapi-jwt-auth

# Create all directories
mkdir -p app/api/v1 app/auth app/core app/db app/models app/schemas app/crud
mkdir -p tests alembic/versions

# Create __init__.py files
touch app/__init__.py app/api/__init__.py app/api/v1/__init__.py
touch app/auth/__init__.py app/core/__init__.py app/db/__init__.py
touch app/models/__init__.py app/schemas/__init__.py app/crud/__init__.py
touch tests/__init__.py