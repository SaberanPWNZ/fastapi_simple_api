from typing import Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    article: str
    partner_price: float
    rrp_price: float
    EAN: str
    category: str
    status: str
    warranty: int

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    article: Optional[str] = None
    partner_price:  Optional[float] = None
    rrp_price:  Optional[float] = None
    EAN: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    warranty: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    title: str
    article: str
    partner_price: float
    rrp_price: float
    EAN: str
    category: str
    status: str
    warranty: int


