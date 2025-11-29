from fastapi import FastAPI #importando meu fastApi
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # VARIVEIS DE AMBEINTES
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI() #instanciando fastApi

ouath2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from app.routers.order_routes import order_router #importando minhas order_router
from app.routers.auth_routes import auth_router #importando minhas auth_router

app.include_router(auth_router) #incluindo minha rotas no meu objeto
app.include_router(order_router) #incluindo minha rotas no meu objeto


# rodar servidor: uvicorn app.main:app --reload
