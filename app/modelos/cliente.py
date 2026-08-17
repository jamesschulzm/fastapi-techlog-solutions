from pydantic import BaseModel


class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str
