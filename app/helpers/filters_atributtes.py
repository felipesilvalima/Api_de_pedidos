from app.models.order_models import Pedidos
from fastapi import HTTPException

def filterPedido(atributos: str,session, pedido_id: str = None):

     colunas_permitidas = {
        "id": Pedidos.id,
        "status": Pedidos.status,
        "preco": Pedidos.preco,
        "usuario_id": Pedidos.usuario_id
    }
     
     # ✅ separa os atributos:
     lista_atributos = atributos.split(",")

    # ✅ valida e transforma em colunas reais do model
     colunas = []
     for attr in lista_atributos:
        coluna = colunas_permitidas.get(attr)
        if not coluna:
            raise HTTPException(status_code=400,detail=f"Coluna {attr} não é permitida")
        colunas.append(coluna)

    # ✅ monta a query com múltiplas colunas
     if pedido_id:
          pedido = session.query(*colunas).filter(Pedidos.id == pedido_id).first()
          resultado = dict(zip(lista_atributos, pedido))

     else:
          pedidos = session.query(*colunas).all()

          resultado = []
          for linha in pedidos:
               item = {}
          for i, nome in enumerate(lista_atributos):
               item[nome] = linha[i]
          resultado.append(item)

     return resultado