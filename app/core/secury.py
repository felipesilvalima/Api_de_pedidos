from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_senha(senha: str, senha_hash: str):
    return bcrypt_context.verify(senha, senha_hash)