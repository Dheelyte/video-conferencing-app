"""
Database session configuration using SQLAlchemy 2.0.
Creates database engine and session factory.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Create database engine
# For SQLite: connects to local file
# For PostgreSQL: would be postgresql://user:pass@host/db
engine = create_engine(
   settings.DATABASE_URL,
   connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
   pool_pre_ping=True,  # Verify connections before using
   echo=False  # Set to True to see SQL queries (useful for debugging)
)

# Create session factory
# Each request gets its own session
SessionLocal = sessionmaker(
   autocommit=False,
   autoflush=False,
   bind=engine
)

# Base class for all ORM models
Base = declarative_base()


def get_db():
   """
   Dependency function that provides a database session.
   
   Yields a database session and ensures it's closed after use.
   Used as a FastAPI dependency with Depends().
   
   Usage:
      @app.get("/items")
      def read_items(db: Session = Depends(get_db)):
         return db.query(Item).all()
   
   Why this pattern?
   ----------------
   - Creates new session per request
   - Automatically closes session after request
   - Handles exceptions and rollback
   - Thread-safe (each request has its own session)
   """
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()


"""
DATABASE CONFIGURATION EXPLAINED:

1. ENGINE
   - Manages connection pool to database
   - SQLite: Single file, no pooling needed
   - PostgreSQL: Connection pooling for performance
   - pool_pre_ping: Checks if connection is alive before using

2. SESSION
   - Represents a "conversation" with the database
   - autocommit=False: Must explicitly commit changes
   - autoflush=False: Don't auto-flush on query (more control)
   - Each request gets its own session (thread-safe)

3. BASE
   - All models inherit from Base
   - Provides metadata for table creation
   - Used by Alembic for migrations

SWITCHING TO POSTGRESQL:

1. Update .env:
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname

2. Install driver:
   pip install psycopg2-binary

3. Remove SQLite-specific connect_args:
   engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

4. Run migrations:
   alembic upgrade head

BEST PRACTICES:

1. Always use dependency injection for sessions
2. Never create global session
3. Let FastAPI handle session lifecycle
4. Use transactions for multi-step operations
5. Configure connection pooling for PostgreSQL
6. Enable pool_pre_ping to handle stale connections

SESSION LIFECYCLE:

1. Request arrives
2. get_db() creates new session
3. Session injected into route handler
4. Route performs database operations
5. Response sent to client
6. Session closed automatically (finally block)
7. Exceptions trigger rollback

COMMON PITFALLS:

❌ Don't do this:
   db = SessionLocal()  # Global session
   user = db.query(User).first()

✅ Do this:
   def get_user(db: Session = Depends(get_db)):
       return db.query(User).first()
"""