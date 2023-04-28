from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from auth.auth import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from models import Realestate, Address, User
from router import *

app = FastAPI()


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


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


@app.get("/reg-auth")
def registration(request: Request):
    return templates.TemplateResponse(
        'reg.html',
        {
            "request": request,
        },
        status_code=200
    )


@app.get("/place-an-advertisement")
def protected_route(request: Request, user: User = Depends(current_user)):
    if user:
        return templates.TemplateResponse(
            "new_flat.html",
            {
                "request": request,
            },
            status_code=200
        )
    return templates.TemplateResponse(
            "notauth.html",
            {
                "request": request,
            },
            status_code=404
        )


@app.get("/flat-{re_page}")
async def get_real_estate_page(request: Request, re_page: int, session: AsyncSession = Depends(get_async_session)):
    q = select(Realestate).filter(Realestate.id == re_page)
    real_estate = await session.execute(q)
    real_estate = real_estate.first()
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
async def home_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    q = select(Realestate)
    real_estate = await session.execute(q)
    return templates.TemplateResponse(
        'index.html',
        {
            "request": request,
            "real_estate": real_estate.all(),
        },
        status_code=200
    )


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, user"

