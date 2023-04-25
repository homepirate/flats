from database import Base

from sqlalchemy import INTEGER, String, Column, FLOAT, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable


class Status(Base):
    __tablename__ = 'status'

    id = Column(INTEGER, primary_key=True)
    title = Column(String)
    rating = Column(INTEGER, nullable=True)
    user = relationship("User", back_populates="status", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'status',
        # 'concrete': True
        'polymorphic_on': 'title'

    }

    def __repr__(self):
        return str(self.__dict__)


class Company(Status):
    __tablename__ = "company"

    statusid = Column(INTEGER, ForeignKey("status.id"), primary_key=True)
    companyname = Column(String, nullable=False)
    website = Column(String, nullable=True)
    yearsw = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'company',
        # 'concrete': True
    }


class Realtor(Status):
    __tablename__ = "realtor"

    statusid = Column(INTEGER, ForeignKey("status.id"), primary_key=True)
    yearsw = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'realtor'
    }

    def __repr__(self):
        return str(self.__dict__)


class Owner(Status):
    __tablename__ = "owner"

    statusid = Column(INTEGER, ForeignKey("status.id"), primary_key=True)
    verified = Column(BOOLEAN, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'owner'
    }

    def __repr__(self):
        return str(self.__dict__)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True)
    statusid = Column(INTEGER, ForeignKey("status.id"))
    page = Column(INTEGER, nullable=False)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phonenumber = Column(INTEGER, nullable=False)
    is_active = Column(BOOLEAN, default=True, nullable=False)
    is_superuser = Column(BOOLEAN, default=False, nullable=False)
    is_verified = Column(BOOLEAN, default=False, nullable=False)
    status = relationship("Status", back_populates="user", uselist=False)
    realestate = relationship("Realestate", back_populates="user")

    def __repr__(self):
        return str(self.__dict__)


class Address(Base):
    __tablename__ = "address"

    id = Column(INTEGER, primary_key=True)
    city = Column(String, nullable=False)
    district = Column(String, nullable=True)
    street = Column(String, nullable=False)
    housenumber = Column(String, nullable=False)
    realestate = relationship("Realestate", back_populates="address")


class Realestate(Base):
    __tablename__ = "realestate"

    id = Column(INTEGER, primary_key=True)
    userid = Column(INTEGER, ForeignKey("user.id"))
    addressid = Column(INTEGER, ForeignKey("address.id"))
    name = Column(String, nullable=False)
    numberofrooms = Column(INTEGER, nullable=False)
    price = Column(INTEGER, nullable=False)
    floor = Column(INTEGER, nullable=True)
    square = Column(INTEGER, nullable=False)
    yearofconstruction = Column(INTEGER, nullable=False)
    numberofbathrooms = Column(INTEGER, nullable=False)
    сeilingheight = Column(FLOAT, nullable=False)
    balcony = Column(INTEGER, nullable=True)
    numberofelevators = Column(INTEGER, nullable=True)
    user = relationship("User", back_populates="realestate")
    address = relationship("Address", back_populates="realestate", uselist=False)