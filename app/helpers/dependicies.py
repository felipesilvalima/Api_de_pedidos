from app.models.order_models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from app.models.order_models import Usuario
from jose import jwt, JWTError
from app.main import SECRET_KEY, ALGORITHM,ouath2_schema

def pegar_sessao():
    try:
        session = sessionmaker(bind=db)
        session = session()
        return session
    finally:
        session.close() 


def verify_token(token: str = Depends(ouath2_schema), session: Session = Depends(pegar_sessao)): # função para verificar token
    try:
        dic_inf =  jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
        usuario_id = int(dic_inf.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401,detail="Acesso negado, verifique a data de expiração do token")

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario