from fastapi import APIRouter , Depends, HTTPException
from app.models.order_models import Usuario
from app.helpers.dependicies import pegar_sessao, verify_token
from app.core.secury import bcrypt_context, verify_senha
from app.schemas.Usuario import UsuarioSchema,LoginSchema
from sqlalchemy.orm import Session
from jose import jwt
from datetime import timezone, timedelta, datetime
from app.main import ACESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=['auth']) #criando instancia da minha rota passando o prefixo


def generate_token(id_usuario, duracao_toke=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)): #função de gerar token
    
    data_expiracao = datetime.now(timezone.utc) + duracao_toke #data de expiração
    payload = {"sub" : str(id_usuario), "exp" : data_expiracao} # payload
    jwt_codificado = jwt.encode(payload,SECRET_KEY, ALGORITHM) # codificado 
    return jwt_codificado


def autenticarUsuario(email, senha, session): #função para autenticar usuarios
     
     usuario = session.query(Usuario).filter(Usuario.email == email).first() #consultando usuario

     if not usuario: # se não existir
         return False
     elif not verify_senha(senha, usuario.senha): #se senha for falsa
         return False
     else: # se usuario e senha for válidos 
        return usuario


@auth_router.get("/home")
async def home():
    return {"aqui e home"}


@auth_router.post("/criar_conta") #criando meu endpoint criar conta do tipo post. Criar um novo usuário
async def criarConta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao),usuario_logado: Usuario = Depends(verify_token)):
    try:
        usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
        
        if usuario:
            raise HTTPException(status_code=400, detail="já existe um usuário com esse email")
        else:
            if usuario_logado.admin != True and usuario_schema.admin == True:
                raise HTTPException(status_code=400, detail="Esse usuário não pode criar conta administradora") 
            else:  
                senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
                novoUsuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
                session.add(novoUsuario)
                session.commit()
                return {"mensagem" : f"Usuário cadastrado com sucesso {novoUsuario.email}"}, 201
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error interno no servidor: " + error) 


@auth_router.post("/login") #criando meu endpoint autenticação do tipo post. Fazer login
async def Login(logi_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    try:
        usuario = autenticarUsuario(email=logi_schema.email, senha=logi_schema.senha, session=session) # retorno da autenticação do usuario

        if usuario:  # se autenticar

            access_token = generate_token(usuario.id) #gerar um token de acesso
            refresh_token = generate_token(usuario.id,duracao_toke=timedelta(days=7))

            return {
                "access_token" : access_token,
                "refresh_token" : refresh_token,
                "type_token" : "Bearer"
            }, 200
        else: # se não autenticar
            raise HTTPException(status_code=403, detail="Email ou Senha inválida")
        
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error interno no servidor: " + error) 
    


@auth_router.post("/login-form") #criando meu endpoint autenticação do tipo post. Fazer login
async def Login(dados_formualario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    try:
        usuario = autenticarUsuario(email=dados_formualario.username, senha=dados_formualario.password, session=session) # retorno da autenticação do usuario

        if usuario:  # se autenticar

            access_token = generate_token(usuario.id) #gerar um token de acesso

            return {
                "access_token" : access_token,
                "type_token" : "Bearer"
            }
        else: # se não autenticar
            raise HTTPException(status_code=403, detail="Email ou Senha inválida")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error interno no servidor: " + error)  



@auth_router.get("/refresh") #criando meu endpoint refresh do tipo get. gerar novo token
async def User_Refresh_token(usuario: Usuario = Depends(verify_token)):

    acess_token = generate_token(usuario.id)

    return {
        "acess_token" : acess_token,
        "type_token" : "Bearer"
    }, 200  
           
   