import os.path

from sqlalchemy import MetaData, ForeignKey, select, delete, func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, with_polymorphic, selectin_polymorphic
from sqlalchemy.orm import declarative_base

from sqlalchemy import INTEGER, String, Column, FLOAT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import ConcreteBase


BASE_DIR = os.path.dirname(os.path.abspath(__name__))
db_path = os.path.join(BASE_DIR, 'database')
if not os.path.exists(db_path):
    os.makedirs(db_path)

DATABASE_URL = f'sqlite:///./database/test.db'

Base = declarative_base()

# metadata = MetaData()

engine = create_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, expire_on_commit=False)


def get_async_session():
    with async_session_maker() as session:
        yield session

# ConcreteBase
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
        'polymorphic_identity': 'realtor',
        # 'concrete': True
    }

    def __repr__(self):
        return str(self.__dict__)


class Owner(Status):
    __tablename__ = "owner"

    statusid = Column(INTEGER, ForeignKey("status.id"), primary_key=True)
    verified = Column(BOOLEAN, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'owner',
        # 'concrete': True
    }


    def __repr__(self):
        return str(self.__dict__)


class User(Base):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True)
    statusid = Column(INTEGER, ForeignKey("status.id"))
    # page = Column(INTEGER, nullable=False)
    # login = Column(String, nullable=False)
    # password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    # surname = Column(String, nullable=False)
    # email = Column(String, nullable=False)
    # phonenumber = Column(INTEGER, nullable=False)
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
    Ceilingheight = Column(FLOAT, nullable=False)
    balcony = Column(INTEGER, nullable=True)
    numberofelevators = Column(INTEGER, nullable=True)
    # apartamentnumber = Column(INTEGER, nullable=False)
    user = relationship("User", back_populates="realestate")
    address = relationship("Address", back_populates="realestate", uselist=False)


# Base.metadata.create_all(engine)


def add():
    a = get_async_session()
    session = next(a)
    session.add(Realtor(title="realtor", yearsw=2000))
    r = len(session.query(Status).all())
    session.add(User(name="dasha", statusid=r))
    session.add(Owner(title="owner", verified=True))
    r = len(session.query(Status).all())
    session.add(User(name="Pasha", statusid=r))
    session.commit()


# add()

def get():
    a = get_async_session()
    session = next(a)
    session.add(Address(city="VOSW", district="dfdfd", street="ssf", housenumber="11"))
    session.add(Address(city="VOadaSW", district="dadafdfd", street="ssssf", housenumber="111"))
    # r = session.query(User, with_polymorphic(Status, [Owner, Realtor, Company])) \
    #     .join(with_polymorphic(Status, [Owner, Realtor, Company]), User.statusid == Status.id).all()
    session.add(Realestate(userid=2, addressid=1, name="name",
                           numberofrooms=1, price=1, floor=1, square=1, yearofconstruction=1,
                           numberofbathrooms=1, balcony=1, Ceilingheight=1, numberofelevators=1))

    session.add(Realestate(userid=2, addressid=1, name="nam2222e",
                           numberofrooms=1, price=1, floor=1, square=1, yearofconstruction=1,
                           numberofbathrooms=1, balcony=1, Ceilingheight=1, numberofelevators=1))

    # r = session.query(with_polymorphic(Status, [Owner, Realtor, Company])).all()
    # r = session.query(User, Realestate.name).where(User.name == "Pasha").join(Realestate, User.id == Realestate.userid).all()
    # q = select(Address)
    # address = session.execute(q)
    # address = address.all()
    # print(address)
    # address_array = [f'{i[0].city}, {i[0].district}, {i[0].street}, {i[0].housenumber}' for i in address]
    # print(address_array)
    # q = select(User, Realestate).where(User.name == "Pasha").join(Realestate, User.id == Realestate.userid)
    # q = select(User, Realestate).where(User.name == "Pasha").join(User.realestate)
    # r = session.execute(q)
    # r = r.all()
    # print(r)
    # data = [{"id": i[0].id, "name": i[0].name,
    #         "rename": i[1].name} for i in r]
    # print(data)
    #
    # q = select(Realestate, Address).join(Address, Realestate.addressid == Address.id).order_by(Realestate.price)
    # resp = session.execute(q)
    # resp = resp.all()
    # for i in resp:
    #     print(i[0].name, i[1].city)
    # for i in r:
    #     print(i[0], i[0].id, i[1])

    # ow = Owner(title="owner", verified=True)
    # session.add(ow)
    # session.commit()
    # session.refresh(ow)
    #
    # u = User(name="BOSS", statusid=ow.id)
    # session.add(u)
    # session.commit()
    # session.refresh(u)
    # uid = u.id
    # print(session.query(User).where(User.name=="BOSS").all())

    # print(f'{uid=}')
    # print(session.query(User).where(User.id==uid).delete())
    # print(session.query(User).all())
    #
    # q = delete(User).where(User.id==3)
    # session.execute(q)
    # print(session.query(User).all())
    # print(session.query(User).where(User.id==uid).all())
    # session.commit()
    # print(session.query(Status).all())

    # q = select(User.statusid).where(User.id == 1)
    # resp = session.execute(q)
    # resp = resp.first()
    # print(resp[0])
    #
    # q = select(User)
    # resp = session.execute(q)
    # resp = resp.all()
    # for i in resp:
    #     print(i[0])

    stmt = select(User, with_polymorphic(Status, [Owner, Realtor, Company])) \
        .join(with_polymorphic(Status, [Owner, Realtor, Company]), User.statusid == Status.id)

    stmt = session.execute(stmt)
    stmt = stmt.all()
    for i in stmt:
        print(i[0].status.yearsw)
    # r = select(Realestate).join(Realestate.address)
    # r = session.execute(r)
    # r = r.all()
    # print(r)
    # print(r[0].status)
    # for u in r:
    #     print(u)
    #     # if u.title == "owner":
    #     #     print(u.verified)
    #     # elif u.title == 'realtor':
    #     #     print(u.yearsw)
    #     print("-----------------")
    # r = session.query(Status).all()
    # for st in r:
    #     print(st.title, st.id,)

    # r = session.query(User).all()
    # print(r[1].status.companyname)
get()
