from pydantic import BaseModel, ConfigDict, field_validator



class User(BaseModel):
    id: int
    username: str
    role: str
    model_config = ConfigDict(from_attributes=True)

# Схемы для пользователя
class UserCreate(BaseModel):
    username: str
    password: str
    password2: str
    
    # Валидатор для проверки совпадения паролей
    
    @field_validator("password2")
    def passwords_match(cls, password2, values):
        if password2 != values.get("password"):
            raise ValueError("Passwords do not match")
        return password2

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Схемы для заметок
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    body: str
    owner_id: int

    class Config:
        orm_mode = True
