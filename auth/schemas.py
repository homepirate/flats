from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    login: str
    page: int
    name: str
    surname: str
    phonenumber: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    title: str
    verified: Optional[bool] = False
    yearsw: int = None
    companyname: str = None
    yearsw: int = None
    website: Optional[str] = None
    statusid: int
    login: str
    page: int
    name: str
    surname: str
    phonenumber: int
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


# class UserUpdate(schemas.BaseUserUpdate):
#     pass

'''
class UserCreateOwner(UserCreate):
    title: str = "owner"
    verified: Optional[bool] = False


class UserCreateRealtor(UserCreate):
    title: str = "realtor"
    yearsw: int


class UserCreateCompany(UserCreate):
    title: str = "company"
    companyname: str
    yearsw: int
    website: Optional[str]

'''