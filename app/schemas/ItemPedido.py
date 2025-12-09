from pydantic import BaseModel, field_validator
from fastapi import HTTPException
from app.models.order_models import ItemPedido

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float


    @field_validator("quantidade")
    def quantidade_validator(cls, quantidade):
        if quantidade <= 0:
            raise HTTPException(status_code=400,detail="Campo quantidade não pode ser menor ou igual a 0")
        return quantidade
    

    @field_validator("sabor")
    def sabor_validator(cls, sabor):
        sabores = ItemPedido("","", 0)

        if not sabor in sabores.SABORES:
            raise HTTPException(status_code=400,detail="Esse sabor não existe em nosso cardápio")
        return sabor
    

    @field_validator("tamanho")
    def tamanho_validator(cls, tamanho):
        tamanhos = ItemPedido("","", 0)

        if not tamanho in tamanhos.TAMANHOS:
            raise HTTPException(status_code=400,detail="Esse Tamanho não existe em nosso cardápio")
        return tamanho
    

    @field_validator("preco_unitario")
    def preco_unitario_validator(cls, preco_unitario):
        if preco_unitario <= 0:
            raise HTTPException(status_code=400,detail="Campo preço não pode ser menor ou igual a 0")
        return preco_unitario

    class Config():
        from_attributes = True
