"""
Initialize database with first superuser.
"""
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.models.user import UserRole


def init_db(db: Session) -> None:
    """
    Initialize database with first superuser.
    
    Creates admin account if it doesn't exist.
    """
    # Check if first superuser already exists
    user = get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_SUPERUSER_FULL_NAME,
        )
        user = create_user(db, user=user_in, role=UserRole.ADMIN)
        print(f"✓ Created first superuser: {user.email}")
    else:
        print(f"✓ First superuser already exists: {user.email}")