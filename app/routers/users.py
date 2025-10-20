"""
User management endpoints with role-based access control.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User, UserRole
from app.crud.user import get_user, get_users, update_user, delete_user
from app.dependencies import get_current_active_user, require_admin, require_moderator


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get current logged-in user's information.
    
    This is a common endpoint that allows users to get their own data.
    Requires authentication but no special role.
    
    Usage:
        GET /users/me
        Authorization: Bearer <access_token>
    
    Returns:
        Current user's profile data
    """
    return current_user


@router.get("", response_model=List[UserRead])
async def read_users(
    current_user: Annotated[User, Depends(require_moderator)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get list of all users (admin/moderator only).
    
    Supports pagination with skip and limit parameters.
    Only accessible by moderators and admins.
    
    Query Parameters:
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100)
    
    Returns:
        List of users
    """
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific user by ID.
    
    Users can view their own profile.
    Admins and moderators can view any user.
    Regular users cannot view other users.
    
    Authorization Logic:
    - If user_id matches current user → Allow
    - If current user is admin/moderator → Allow
    - Otherwise → Deny (403 Forbidden)
    """
    # Check if user is requesting their own data
    if current_user.id == user_id:
        return current_user
    
    # Check if user is admin or moderator
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view other users"
        )
    
    # Get requested user
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_endpoint(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update user information.
    
    Authorization:
    - Users can update their own profile (except role and is_active)
    - Admins can update any user including role and status
    
    Restricted Fields (for non-admins):
    - role: Only admins can change roles
    - is_active: Only admins can activate/deactivate accounts
    """
    # Check if user exists
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Authorization check
    is_self = current_user.id == user_id
    is_admin = current_user.role == UserRole.ADMIN
    
    if not is_self and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user"
        )
    
    # Restrict certain fields for non-admins
    if not is_admin:
        if user_update.role is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change user roles"
            )
        if user_update.is_active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change account status"
            )
    
    # Update user
    updated_user = update_user(db, user_id=user_id, user_update=user_update)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    current_user: Annotated[User, Depends(require_admin)],
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a user (admin only).
    
    Hard delete removes user from database.
    Consider using soft delete (is_active=False) instead.
    
    Security:
    - Only admins can delete users
    - Cannot delete yourself (prevent lockout)
    - Returns 204 No Content on success
    """
    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user
    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return None


"""
USER ENDPOINTS EXPLAINED:

1. GET /users/me
   - Returns current user's profile
   - Requires authentication only
   - Most common endpoint for frontend

2. GET /users
   - Lists all users with pagination
   - Moderator/Admin only
   - Used for user management dashboards

3. GET /users/{user_id}
   - Get specific user by ID
   - Users can view themselves
   - Mods/Admins can view anyone

4. PATCH /users/{user_id}
   - Update user information
   - Users can update their own profile
   - Admins can update anyone
   - Some fields restricted to admins

5. DELETE /users/{user_id}
   - Delete user (admin only)
   - Cannot delete yourself
   - Consider soft delete instead

ROLE-BASED ACCESS CONTROL (RBAC):

Permission Matrix:
┌──────────────┬──────┬───────────┬───────┐
│ Endpoint     │ User │ Moderator │ Admin │
├──────────────┼──────┼───────────┼───────┤
│ GET /me      │  ✓   │     ✓     │   ✓   │
│ GET /users   │  ✗   │     ✓     │   ✓   │
│ GET /{id}    │ self │     ✓     │   ✓   │
│ PATCH /{id}  │ self │    self   │   ✓   │
│ DELETE /{id} │  ✗   │     ✗     │   ✓   │
└──────────────┴──────┴───────────┴───────┘

AUTHORIZATION PATTERNS:

1. Self-or-Admin:
   if user_id != current_user.id and current_user.role != UserRole.ADMIN:
       raise HTTPException(403, "Not authorized")

2. Role-Based:
   current_user: User = Depends(require_admin)
   current_user: User = Depends(require_moderator)

3. Resource-Based:
   if resource.owner_id != current_user.id:
       raise HTTPException(403, "Not authorized")

4. Combined:
   is_owner = resource.owner_id == current_user.id
   is_admin = current_user.role == UserRole.ADMIN
   if not (is_owner or is_admin):
       raise HTTPException(403, "Not authorized")

HTTP STATUS CODES:

200 OK - Successful GET/PATCH
201 Created - Successful POST
204 No Content - Successful DELETE
400 Bad Request - Invalid input/self-deletion
401 Unauthorized - Not authenticated
403 Forbidden - Authenticated but not authorized
404 Not Found - Resource doesn't exist
422 Unprocessable Entity - Validation error

FRONTEND INTEGRATION:

// Get current user
const me = await fetch('/api/v1/users/me', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Get all users (admin)
const users = await fetch('/api/v1/users?skip=0&limit=50', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Update profile
await fetch(`/api/v1/users/${userId}`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    full_name: 'New Name',
    email: 'newemail@example.com'
  })
});

// Delete user (admin)
await fetch(`/api/v1/users/${userId}`, {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${token}` }
});

SOFT DELETE PATTERN (RECOMMENDED):

Instead of DELETE endpoint, use PATCH to set is_active=False:

@router.patch("/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    user.is_active = False
    db.commit()
    return user

Benefits:
- Preserves data for auditing
- Can reactivate accounts
- Maintains referential integrity
- Complies with GDPR (right to be forgotten via anonymization)

PRODUCTION ENHANCEMENTS:

1. Search & Filtering:
   @router.get("/search")
   async def search_users(
       q: str,
       role: Optional[UserRole] = None,
       is_active: Optional[bool] = None
   )

2. Bulk Operations:
   @router.post("/bulk/deactivate")
   async def bulk_deactivate(user_ids: List[int])

3. User Activity:
   @router.get("/{user_id}/activity")
   async def get_user_activity(user_id: int)

4. Profile Picture Upload:
   @router.post("/me/avatar")
   async def upload_avatar(file: UploadFile)

5. Password Change:
   @router.post("/me/change-password")
   async def change_password(
       old_password: str,
       new_password: str
   )
"""