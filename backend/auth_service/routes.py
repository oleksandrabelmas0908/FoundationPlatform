from fastapi import APIRouter


router = APIRouter(tags=["auth"])


@router.get("/token")
async  def get_token():
    pass