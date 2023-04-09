from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from .auth import get_user_db
from models import User, Owner, Company, Realtor, Status
from config import SECRET_TO_UM
from database import get_async_session

SECRET = SECRET_TO_UM


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        session = Depends(get_async_session)
        title = user_dict.pop("title")
        if title == "owner":
            user_dict.pop("companyname")
            user_dict.pop("website")
            user_dict.pop("yearsw")
            verified = user_dict.pop("verified")
            session.add(Owner(title=title, verified=verified))
        elif title == "realtor":
            user_dict.pop("companyname")
            user_dict.pop("website")
            user_dict.pop("verified")
            yearsw = user_dict.pop("yearsw")
            session.add(Realtor(title=title, yearsw=yearsw))
        else:
            user_dict.pop("verified")
            companyname = user_dict.pop("companyname")
            website = user_dict.pop("website")
            yearsw = user_dict.pop("yearsw")
            session.add(Company(title=title, companyname=companyname, website=website, yearsw=yearsw))

        stid = len(session.query(Status).all())

        user_dict["statusid"] = stid
        session.commit()
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
