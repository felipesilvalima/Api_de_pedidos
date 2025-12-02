from pydantic import BaseModel
from typing import List
from app.schemas.ItemPedido import ItemPedidoSchema


class PedidoSchema(BaseModel):
    usuario_id: int

    class Config():
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    item: List[ItemPedidoSchema]
    class Config():
        from_attributes = True

