from fastapi import Body, APIRouter
from api.auth.dto import UserDto
from api.auth.auth_handler import signJWT

router = APIRouter()


@router.post("/user/token")
async def get_token(user: UserDto = Body(...)):
    # todo check with recruiter if I need to store users
    return signJWT(user.email)
