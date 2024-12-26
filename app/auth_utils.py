from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"  


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": str(data["sub"])})  

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not isinstance(sub, str):
            raise jwt.InvalidSubjectError("Subject must be a string")
        return payload
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")
