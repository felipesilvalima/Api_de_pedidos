from fastapi import APIRouter, Depends, HTTPException
from app.models.order_models import Pedidos
from app.helpers.dependicies import pegar_sessao, verify_token
from sqlalchemy.orm import Session
from app.schemas.Pedido import PedidoSchema
from app.schemas.ItemPedido import ItemPedidoSchema
from app.models.order_models import Pedidos, Usuario, ItemPedido



order_router = APIRouter(prefix="/api", tags=['api'],dependencies=[Depends(verify_token)]) #criando objeto da minha rota passando o prefixo


@order_router.get("/pedidos") #criando meu endpoint pedidos do tipo get. Lista todos os pedidos
async def Listar_Pedidos(session = Depends(pegar_sessao), usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar essa operação")
    else:

        pedidos = session.query(Pedidos).all() # pegando todos os pedidos

        if not pedidos:
            raise HTTPException(status_code=404,detail="Nenhum pedido encontrado") # aviso no caso de não exister pedidos
        else:
            return {"pedidos" : pedidos}, 200 

 
@order_router.post("/pedidos") #criando meu endpoint pedidos do tipo post. Criar novo pedido
async def Criar_Pedido(pedido_schema: PedidoSchema ,session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.id ==  pedido_schema.usuario_id).first() # verificando se exister o usuario

    if not usuario:
        raise HTTPException(status_code=400, detail="Não foi possivel criar pedido. Usuário não existe") # aviso no caso de não achar o usuario
    else:
        novoPedido = Pedidos(pedido_schema.usuario_id) # chamando meu modelo pedidos passando parametro
        session.add(novoPedido) # add do pedido
        session.commit() # commit para banco
        return {"mensagem" : f"Pedido criado com sucesso. ID do pedido {novoPedido.id}"}, 201


@order_router.get("/pedidos/{pedido_id}") #criando meu endpoint pedidos do tipo get. buscar um pedido
async def Buscar_Pedido(pedido_id, session = Depends(pegar_sessao),usuario: Usuario = Depends(verify_token)):
    if not usuario.admin:
         raise HTTPException(status_code=401, detail="Você não tem autorização para acessar essa operação")
    else:

        pedido = session.query(Pedidos).filter(Pedidos.id == pedido_id).first() #verificando se existe o pedido

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado") # aviso no caso de não achar o pedido
        else:
            return {"pedido" : pedido}, 200


@order_router.post("/pedidos/cancelar/{pedido_id}") #criando meu endpoint pedidos do tipo get. buscar um pedido
async def Cancelar_Pedido(pedido_id: int, session = Depends(pegar_sessao),usuario: Usuario = Depends(verify_token)):

    pedido = session.query(Pedidos).filter(Pedidos.id == pedido_id).first() #verificando se existe o pedido

    if not usuario.admin or usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    else:

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado") # aviso no caso de não achar o pedido  
        else:
            pedido.status = "CANCELADO"
            session.commit() # commit para banco
            return {
                "mensagem" : f"Pedido do Número: {pedido.id} foi Cancelado com sucesso!",
                "pedido" : pedido
            }, 200


@order_router.post("/pedidos/adicionar-item/{id_pedido}")
async def Adicionar_Pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session = Depends(pegar_sessao), usuario: Usuario = Depends(verify_token)):

    pedido = session.query(Pedidos).filter(Pedidos.id == id_pedido).first()

    if not pedido:
       raise HTTPException(status_code=400, detail="Pedido não existente")
    elif not usuario.admin or usuario.id != pedido.usuario_id: 
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    else:
        item_pedido = ItemPedido(item_pedido_schema.sabor, item_pedido_schema.tamanho, id_pedido, item_pedido_schema.preco_unitario, item_pedido_schema.quantidade)
    
        session.add(item_pedido)
        pedido.calcularPreco()
        session.commit()

        return {
            "mensagem" : "Item criado com sucesso",
            "item_id" : item_pedido.id,
            "preco_pedido": pedido.preco
        }
    
@order_router.post("/pedidos/remover-item/{id_item_pedido}")
async def Remover_Item_Pedido(id_item_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verify_token)):

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()

    if not item_pedido:
       raise HTTPException(status_code=400, detail="Item no pedido não existente")
    
    pedido = session.query(Pedidos).filter(Pedidos.id == item_pedido.pedido_id).first()
    
    if not usuario.admin or usuario.id != pedido.usuario_id: 
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    else:
        session.delete(item_pedido)
        pedido.calcularPreco()
        session.commit()
        return {
            "mensagem" : "Item removido com sucesso",
            "quantidade_itens_pedido" : len(pedido.item),
            "pedido" : pedido
        }