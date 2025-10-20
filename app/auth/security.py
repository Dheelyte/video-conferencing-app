"""
Password hashing and verification using bcrypt.
"""
# from passlib.context import CryptContext
from pwdlib import PasswordHash


# Create password context with bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    
    Args:
        plain_password: The password provided by the user
        hashed_password: The hashed password stored in the database
        
    Returns:
        True if the password matches, False otherwise
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plaintext password
        
    Returns:
        The hashed password string
    """
    return password_hash.hash(password)