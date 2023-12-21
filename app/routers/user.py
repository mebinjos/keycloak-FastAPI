from fastapi import APIRouter, Depends
from ..dependencies import get_current_user
from ..schemas import User

router = APIRouter()

@router.get("/profile")
async def read_profile(current_user: User = Depends(get_current_user)):
    # Return user profile
    return current_user
