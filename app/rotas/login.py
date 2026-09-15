from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/login")


@router.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request},
    )


@router.post("/")
async def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    if email == "admin@techlog.com.br" and senha == "senha123":
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)
        return response
    else:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "email": email,
                "senha": senha,
                "error": "Credenciais inválidas",
            },
        )
