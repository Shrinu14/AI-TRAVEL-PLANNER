import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\vaish\\Downloads\\firebase-credentials.json")
    firebase_admin.initialize_app(cred)

# Auth scheme (Bearer token)
bearer_scheme = HTTPBearer(auto_error=False)

# Dependency for verifying token
def verify_token(auth_credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if auth_credentials is None:
        raise HTTPException(status_code=401, detail="Missing Firebase Token")

    token = auth_credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # ✅ Contains user info like uid, email, etc.
    except Exception as e:
        # Optional: log the error for debugging
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase Token")
