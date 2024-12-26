from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from .. import models, database, auth_utils
from app.utils import hash_password, verify_password, get_current_user

# Указываем путь к папке с шаблонами
templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_role(required_role: str):
    def role_dependency(user: models.User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="У вас недостаточно прав для выполнения этого действия",
            )
        return user

    return role_dependency


# Роут для страницы регистрации
@router.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "errors": []}
    )


# Роут для обработки регистрации пользователя
@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(database.get_db),
):
    # Проверка, что пароли совпадают
    if password != password2:
        errors = {"password2": "Пароли не совпадают"}
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "errors": errors, "username": username},
        )

    # Проверка на существующего пользователя
    existing_user = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if existing_user:
        errors = {"username": "Пользователь с таким логином уже существует"}
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "errors": errors, "username": username},
        )

    # Хеширование пароля и добавление пользователя в базу данных
    hashed_password = hash_password(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # После успешной регистрации перенаправление на страницу входа
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "message": "Регистрация прошла успешно!",
            "errors": {},  
        },
    )


# Роут для страницы входа
@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})


# Роут для обработки логина
@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db),
):
    # Проверка наличия пользователя
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        errors = {"credentials": "Неверный логин или пароль"}
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )

    token = auth_utils.create_access_token({"sub": db_user.id})

    # Определяем путь в зависимости от роли пользователя
    redirect_url = (
        "/admin/admin/notes" if db_user.role == "Admin" else "/user/user/notes"
    )

    # Устанавливаем токен в cookie
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False, 
    )
    return response


# Роут для выхода
@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/")  
    response.delete_cookie("access_token")  
    return response



