from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates
from .routers.notes import user_router, admin_router
from .routers.auth import router as auth_router
from .database import engine
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes Management API")



router = APIRouter()


templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router)
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "errors": {}})


app.include_router(router) 
