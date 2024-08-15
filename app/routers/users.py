from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def hello_world():
    return {"hello": "world"}
