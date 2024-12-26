from tempfile import template
import bcrypt
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import models, database
from .auth_utils import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Функция для верификации JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


# Получение пользователя из токена (если токен существует)
def get_current_user(request: Request, db: Session = Depends(database.get_db)):

    token = request.cookies.get("access_token")  
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # Декодируем токен
        user = db.query(models.User).filter(models.User.id == payload["sub"]).first()
        if not user:
            raise HTTPException(
                status_code=404, detail="User not found"
            )  # Проверка наличия пользователя
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired"
        )  # Обрабатываем ошибки токена
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )



