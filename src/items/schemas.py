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

    # class Config:
    #
    #     from_attributes = True
