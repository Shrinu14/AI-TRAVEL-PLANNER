import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Auth scheme (Bearer token)
bearer_scheme = HTTPBearer(auto_error=False)

# The credentials path used to be hardcoded to a specific developer's
# Windows machine (C:\Users\vaish\Downloads\firebase-credentials.json),
# which meant `import auth.firebase_auth` (and therefore the whole app,
# since backend/main.py imports this at startup) crashed immediately on
# every other machine. It's now read from an env var, and initialization
# is deferred until a request actually needs auth, so the app can still
# start and serve its other (non-auth) endpoints even if Firebase isn't
# configured yet.
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

_firebase_ready = False


def _ensure_firebase_initialized():
    global _firebase_ready
    if _firebase_ready:
        return
    if not FIREBASE_CREDENTIALS_PATH:
        raise HTTPException(
            status_code=503,
            detail="Firebase auth is not configured (set FIREBASE_CREDENTIALS_PATH).",
        )
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
    _firebase_ready = True


# Dependency for verifying token
def verify_token(auth_credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if auth_credentials is None:
        raise HTTPException(status_code=401, detail="Missing Firebase Token")

    _ensure_firebase_initialized()

    token = auth_credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # Contains user info like uid, email, etc.
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase Token")
