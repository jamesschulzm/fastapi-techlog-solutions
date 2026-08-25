from pydantic import BaseModel


class Cliente(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str


class ClienteCriarAtualizar(BaseModel):
    nome: str
    email: str
    telefone: str
