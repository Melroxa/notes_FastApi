from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import database, models
from app.logger import log_action
from app.models import Note, User
from .auth import get_current_user, get_user_role

templates = Jinja2Templates(directory="app/templates")
user_router = APIRouter(prefix="/user", tags=["user"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])


# Маршрут для отображения списка заметок
@user_router.get("/notes", response_class=HTMLResponse)
def list_notes(
    request: Request,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("User")),
):
    notes = (
        db.query(Note)
        .filter(Note.owner_id == user.id, Note.is_deleted == False)
        .order_by(Note.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        "user_notes.html", {"request": request, "user": user, "notes": notes}
    )


# Переход на страницу создания заметки
@user_router.get("/notes/create", response_class=HTMLResponse)
def create_note_page(request: Request):
    return templates.TemplateResponse("notes_create.html", {"request": request})


@user_router.get("/notes/search", response_class=HTMLResponse)
def search_notes_by_title(
    request: Request,
    note_title: Optional[str] = "",  
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("User")),
):
    if not note_title:
        notes = (
            db.query(Note)
            .filter(Note.owner_id == user.id, Note.is_deleted == False)
            .order_by(Note.id.desc())
            .all()
        )
    else:
        notes = (
            db.query(Note)
            .filter(
                Note.owner_id == user.id,
                Note.is_deleted == False,
                Note.title.ilike(f"%{note_title}%"),
            )
            .order_by(Note.id.desc())
            .all()
        )

    return templates.TemplateResponse(
        "user_notes.html", {"request": request, "user": user, "notes": notes}
    )


# Создание новой заметки
@user_router.post("/notes")
def create_note(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    new_note = Note(
        title=title,
        content=content,
        owner_id=current_user.id,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    log_action(f"Пользователь: {current_user.username}. Сделал заметку!")

    return RedirectResponse(url="/user/user/notes", status_code=303)


# Переход на страницу редактирования заметки
@user_router.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def edit_note_page(
    note_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("User")),
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse(
        "notes_edit.html", {"request": request, "note": note}
    )


# Обновление заметки
@user_router.post("/notes/{note_id}")
def update_note(
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("User")),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == user.id, Note.is_deleted == False)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = title
    note.content = content
    db.commit()
    log_action(f"Пользователь: {user.username}. Отредактировал заметку {note_id}!")

    return RedirectResponse(url="/user/user/notes", status_code=303)


# Удаление заметки
@user_router.post("/notes/{note_id}/delete")
def delete_note(
    note_id: int,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("User")),
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.is_deleted = True
    db.commit()
    log_action(f"Пользователь: {user.username}. Удалил заметку под id: {note_id}!")

    return RedirectResponse(url="/user/user/notes", status_code=303)


# Рендеринг шаблона для администратора
@admin_router.get("/notes", response_class=HTMLResponse)
def admin_notes_page(
    request: Request,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("Admin")),
):
    notes = db.query(Note).join(User, Note.owner_id == User.id).all()
    users = db.query(User).all()

    return templates.TemplateResponse(
        "admin_notes.html",
        {
            "request": request,
            "notes": notes,
            "users": users,
            "user": user,
        },  
    )


@admin_router.get("/notes/user/{user_id}")
def list_user_notes(
    user_id: int,
    db: Session = Depends(database.get_db),
    admin: User = Depends(get_user_role("Admin")),
):
    notes = db.query(Note).filter(Note.owner_id == user_id).all()
    log_action(f"Admin {admin.username} listed notes of user {user_id}")
    return notes


@admin_router.post("/notes/{note_id}/permanent_delete")
def permanent_delete_note(
    note_id: int,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("Admin")),
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")


    db.delete(note)
    db.commit()


    log_action(
        f"Администратор {user.username} перманентно удалил заметку под id: {note_id}!"
    )

    return RedirectResponse(url="/admin/admin/notes", status_code=303)


# Восстановление удаленной заметки
@admin_router.post("/notes/{note_id}/restore")
def restore_deleted_note(
    note_id: int,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("Admin")),
):
    note = db.query(Note).filter(Note.id == note_id, Note.is_deleted == True).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or not deleted")
    note.is_deleted = False
    db.commit()
    log_action(f"Администратор {user.username}. Востоновил запись под id: {note_id}!")
    return RedirectResponse(url="/admin/admin/notes", status_code=303)


@admin_router.get("/notes/search", response_class=HTMLResponse)
def search_note_by_id(
    request: Request,
    note_id_input: Optional[str] = "",  
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("Admin")),
):
    users = db.query(User).all()

    if not note_id_input:
        notes = (
            db.query(Note)
            .join(User, Note.owner_id == User.id)
            .filter(Note.is_deleted == False)
            .all()
        )
        return templates.TemplateResponse(
            "admin_notes.html",
            {"request": request, "notes": notes, "users": users, "user": user},
        )

    # Попытка преобразовать note_id_input в число
    try:
        note_id = int(note_id_input)
    except ValueError:
        return templates.TemplateResponse(
            "admin_notes.html",
            {
                "request": request,
                "notes": [],
                "users": users,
                "error": "Введите корректный ID заметки.",
                "user": user,
            },
        )

    # Поиск заметки по ID
    note = (
        db.query(Note)
        .join(User, Note.owner_id == User.id)
        .filter(Note.id == note_id)
        .first()
    )

    if not note:
        return templates.TemplateResponse(
            "admin_notes.html",
            {
                "request": request,
                "notes": [],
                "users": users,
                "error": f"Заметка с ID {note_id} не найдена.",
                "user": user,
            },
        )
    log_action(f"Администратор {user.username}. Поисик по заметки по id: {note_id}!")
    return templates.TemplateResponse(
        "admin_notes.html",
        {"request": request, "notes": [note], "users": users, "user": user},
    )


@admin_router.get("/notes/filter/user", response_class=HTMLResponse)
def filter_notes_by_user(
    user_id: str,
    request: Request,
    db: Session = Depends(database.get_db),
    user: User = Depends(get_user_role("Admin")),
):
    users = db.query(User).all()

    try:
        user_id = int(user_id)
    except ValueError:
        return templates.TemplateResponse(
            "admin_notes.html",
            {
                "request": request,
                "notes": [],
                "users": users,
                "error": "Выберите корректного пользователя или 'all'.",
                "user": user,
            },
        )

    # Убираем фильтрацию по is_deleted
    notes = (
        db.query(Note)
        .join(User, Note.owner_id == User.id)
        .filter(Note.owner_id == user_id)
        .all()
    )

    if not notes:
        return templates.TemplateResponse(
            "admin_notes.html",
            {
                "request": request,
                "notes": [],
                "users": users,
                "error": f"У пользователя с ID {user_id} нет заметок.",
                "user": user,
            },
        )

    log_action(
        f"Администратор: {user.username}. Просмотрел заметки пользователя с ID: {user_id}"
    )
    return templates.TemplateResponse(
        "admin_notes.html",
        {"request": request, "notes": notes, "users": users, "user": user},
    )


@admin_router.post("/notes")
def redirect_to_all_notes(user: User = Depends(get_user_role("Admin"))):
    log_action(f"Администратор {user.username} вернулся ко всем заметкам")
    return RedirectResponse(url="/admin/admin/notes", status_code=302)
