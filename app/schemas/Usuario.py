from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import HTTPException
import re
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    @field_validator("nome")
    def nome_validator(cls, nome):
        if len(nome) > 30:
            raise HTTPException(status_code=400,detail="Campo nome dever ter no máximo 30 caracteres")
        return nome
    

    @field_validator("email")
    def email_validator(cls, email):

        regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if len(email) > 30:
            raise HTTPException(status_code=400,detail="Campo email dever ter no máximo 30 caracteres")
        
        if not re.match(regex,email):
            raise HTTPException(status_code=400,detail="Campo email inválido")
        
        return email
    
    @field_validator("senha")
    def senha_validator(cls, senha):
         
        regex = "^(?=.*[A-Z])(?=(?:.*\d){2,}).+$"

        if len(senha) > 12:
            raise HTTPException(status_code=400,detail="Campo senha dever ter no máximo 12 caracteres")
        
        if not re.match(regex,senha):
            raise HTTPException(status_code=400,detail="Campo senha deve ter no minimo um caracter maiúsculo e dois números inteiros")
        
        return senha

    class Config():
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config():
        from_attributes = True