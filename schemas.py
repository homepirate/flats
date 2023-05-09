from pydantic import BaseModel


class ReModel(BaseModel):
    name: str
    numberofrooms: int
    price: int
    floor: int
    square: int
    yearofconstruction: int
    numberofbathrooms: int
    сeilingheight: float
    balcony: int
    numberofelevators: int