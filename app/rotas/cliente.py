from fastapi import APIRouter

from app.modelos.cliente import Cliente

router = APIRouter(prefix="/clientes")


@router.get("/", response_model=list[Cliente])
async def listar_clientes():
    clientes_list = [
        Cliente(nome="Raphael", email="raphael@rossi.com", telefone="123456789"),
        Cliente(nome="João", email="joao@rossi.com", telefone="123456789"),
    ]

    return clientes_list
