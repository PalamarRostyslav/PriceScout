from pydantic import BaseModel

class Deal(BaseModel):
    """
    A class to represent a deal with a summary description
    """
    product_description: str
    price: float
    url: str