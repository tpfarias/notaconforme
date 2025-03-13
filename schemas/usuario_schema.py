from typing import Optional
from pydantic import BaseModel, EmailStr

class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    ativo: bool = True


    class Config:
        from_attributes = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha: str

class UsuarioSchemaUpdate(UsuarioSchema):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    ativo: Optional[bool]

