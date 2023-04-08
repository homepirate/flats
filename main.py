from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from models import Realestate, User, Address
from router import *

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


app.include_router(router_users)


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
