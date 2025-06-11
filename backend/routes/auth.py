from fastapi import APIRouter, Header, HTTPException
from auth.firebase_auth import verify_token

router = APIRouter()

@router.get("/protected")
def protected_route(authorization: str = Header(...)):
    uid = verify_token(authorization.replace("Bearer ", ""))
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"uid": uid, "message": "You are logged in"}
