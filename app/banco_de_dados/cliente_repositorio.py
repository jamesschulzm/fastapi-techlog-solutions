from app.banco_de_dados.local import BancoDeDadosLocal
from app.modelos.cliente import Cliente


class ClienteRepositorio:
    def __init__(self, database: BancoDeDadosLocal):
        self.db = database

    async def listar_clientes(self) -> list[Cliente]:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            linhas = cursor.fetchall()
            clientes = [
                Cliente(id=linha[0], nome=linha[1], email=linha[2], telefone=linha[3])
                for linha in linhas
            ]
            return clientes

    async def obter_cliente(self, cliente_id: int) -> Cliente | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, telefone FROM clientes WHERE id = ?",
                (cliente_id,),
            )
            linha = cursor.fetchone()
            if linha:
                return Cliente(
                    id=linha[0], nome=linha[1], email=linha[2], telefone=linha[3]
                )
            return None
