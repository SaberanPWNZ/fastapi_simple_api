from sqlalchemy import Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

ItemBase = declarative_base()


class Item(ItemBase):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=False)
    partner_price: Mapped[float] = mapped_column(Float, nullable=False)
    rrp_price: Mapped[float] = mapped_column(Float, nullable=False)
    EAN: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default='in stock')
    warranty: Mapped[int] = mapped_column(Integer, default=12)
