from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import declarative_base

# criando conexao com banco de dados
db = create_engine("mysql+pymysql://root:@localhost:3306/banco_db")

# criar base do banco de dados
base = declarative_base()

#criar classes/tabelas do banco
#usuarios
class Usuario(base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    senha = Column(String(90), nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# =====================
# Tabela Pedidos
# =====================
class Pedidos(base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = ("PEDENTE", "CANCELADO", "FINALIZADO")

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column(Enum(*STATUS_PEDIDOS, name="status_enum"), default="PEDENTE", nullable=False)
    preco = Column(Float, default=0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    def __init__(self, usuario_id, status="PEDENTE", preco=0):
        self.usuario_id = usuario_id
        self.status = status
        self.preco = preco

# =====================
# Tabela ItensPedido
# =====================
class ItemPedido(base):
    __tablename__ = "itens_pedido"

    SABORES = ("CALABRESA", "MEXICANA", "NORDESTINA", "FRANGO", "PORTUGUESA")
    TAMANHOS = ("PEQUENA", "MEDIA", "GRANDE")

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quantidade = Column(Integer, default=0)
    sabor = Column(Enum(*SABORES, name="sabor_enum"), nullable=False)
    tamanho = Column(Enum(*TAMANHOS, name="tamanho_enum"), nullable=False)
    preco_unitario = Column(Float, default=0)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

    def __init__(self, sabor, tamanho, pedido_id, preco_unitario=0, quantidade=0):
        self.sabor = sabor
        self.tamanho = tamanho
        self.pedido_id = pedido_id
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade




#executar a criação dos metadados do seu banco de dados