from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio
from app.modelos.usuario import UsuarioCriarAtualizar

router = APIRouter(prefix="/registro")

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registro.html",
        context={"request": request},
    )


@router.post("/")
async def registrar_usuario(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
    request: Request,
    nome=Form(...),  # noqa: B008
    email=Form(...),  # noqa: B008
    senha=Form(...),  # noqa: B008
    confirma_senha=Form(...),  # noqa: B008
):
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha,
    }

    # Verificar se todos os campos obrigatórios foram preenchidos
    if not all([email, senha, nome, confirma_senha]):
        return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "request": request,
                "error": "Campos obrigatórios faltantes",
                **data,
            },
        )

    # Verificar se as senhas coincidem
    if senha != confirma_senha:
        return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "request": request,
                "error": "As senhas não coincidem",
                **data,
            },
        )

    # Verificar se o e-mail já está cadastrado
    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)

    if usuario_existente:
        return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "request": request,
                "error": "Email já cadastrado",
                **data,
            },
        )

    # Criar o usuário no banco de dados
    usuario_criar = UsuarioCriarAtualizar(
        nome=nome,
        email=email,
        senha=senha,
    )

    usuario = await usuario_repositorio.criar_usuario(usuario_criar)

    if usuario:
        return RedirectResponse(url="/login", status_code=303)
