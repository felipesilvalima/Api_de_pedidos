from pydantic import BaseModel


class PedidoSchema(BaseModel):
    usuario_id: int

    class Config():
        from_attributes = True

