from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Numeric,
    Enum,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import OrderStatus

class Menu(Base, BaseModelMixin):
    __tablename__ = "menus"

    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    cafe = relationship("Cafe", back_populates="menus")
    items = relationship("MenuItem", back_populates="menu")

class MenuItem(Base, BaseModelMixin):
    __tablename__ = "menu_items"

    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    image_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)

    menu = relationship("Menu", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")

class Order(Base, BaseModelMixin):
    __tablename__ = "orders"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    note = Column(Text, nullable=True)

    user = relationship("User", back_populates="orders")
    cafe = relationship("Cafe", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base, BaseModelMixin):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")