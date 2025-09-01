from pydantic import BaseModel
from typing import List
from .deal import Deal

class DealSelection(BaseModel):
    """
    A class to represent a list of deals
    """
    deals: List[Deal]