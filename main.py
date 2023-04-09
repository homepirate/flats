from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers
from starlette.staticfiles import StaticFiles

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from models import Realestate, Address, User
from router import *

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(router_users)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/{re_page}")
def get_real_estate_page(request: Request, re_page: int, session: AsyncSession = Depends(get_async_session)):
    real_estate = session.query(Realestate).filter(Realestate.id == re_page).first()
    if real_estate is None:
        return templates.TemplateResponse(
            "miss_page.html",
            {
                "request": request,
            },
            status_code=404
        )
    return templates.TemplateResponse(
        "re_page.html",
        {
            "request": request,
            "real_estate": real_estate,
        },
        status_code=200
    )


@app.get("/")
def home_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    real_estate = session.query(Realestate).all()
    return templates.TemplateResponse(
        'index.html',
        {
            "request": request,
            "real_estate": real_estate,
        },
        status_code=200
    )



# @app.get("/registration")
