from fastapi import APIRouter, Request, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_polymorphic

from database import get_async_session
from models import User, Status, Company, Address, Realtor, Owner
from starlette.templating import Jinja2Templates


router_users = APIRouter(
    prefix='/users',
    tags=["Users"]
)

templates = Jinja2Templates(directory="templates")


@router_users.get("/")
async def get_all_users(request: Request, session: AsyncSession = Depends(get_async_session)):
    stmt = select(User, with_polymorphic(Status, [Owner, Realtor, Company])) \
        .join(with_polymorphic(Status, [Owner, Realtor, Company]), User.statusid == Status.id)

    response = await session.execute(stmt)
    if len(response.all()) == 0:
        return templates.TemplateResponse(
            "miss_page.html",
            {
                "request": request,
            },
            status_code=404
        )
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": response.all()
        },
        status_code=200
    )


@router_users.get("/{page}")
async def get_user(request: Request, page: int, session: AsyncSession = Depends(get_async_session)):
    # response = session.query(User, with_polymorphic(Status, [Owner, Realtor, Company]))\
    #     .join(with_polymorphic(Status, [Owner, Realtor, Company]), User.statusid == Status.id).where(User.id == page)\
    #     .first()
    stmt = select(User, with_polymorphic(Status, [Owner, Realtor, Company]))\
        .join(with_polymorphic(Status, [Owner, Realtor, Company]), User.statusid == Status.id).where(User.page == page)

    response = await session.execute(stmt)
    if response is None:
        return templates.TemplateResponse(
            "miss_page.html",
            {
                "request": request,
            },
            status_code=404
        )

    return templates.TemplateResponse(
        "user_page.html",
        {
            "request": request,
            "user": response.first()
         },
        status_code=200
    )


@router_users.delete("/{id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_async_session)):
    user = session.query(User).where(User.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    await session.delete(user)
    await session.commit()
    return


@router_users.put("/{id}/edit")
async def edit_user(id: int, data= Body(), session: AsyncSession = Depends(get_async_session)):
    user = session.query(User).where(User.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    if data["name"]: user.name = data["name"]
    if data["surname"]: user.surname = data["surname"]
    if data["login"]: user.login = data["login"]
    if data["password"]: user.password = data["password"]
    if data["email"]: user.email = data["email"]
    await session.commit()
    await session.refresh(user)
    return user


# @router_users.post("/")
# async def create_user(data = Body(), session: AsyncSession = Depends(get_async_session)):
#     person = User(login=data["login"], password=data["password"], name=data["name"], surname=data["surname"],
#                   email=data["email"])
#     session.add(person)
#     await session.commit()
#     await session.refresh(person)
#     return person
