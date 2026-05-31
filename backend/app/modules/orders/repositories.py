from datetime import datetime
from decimal import Decimal
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.orders.models import Order, OrderItem

class OrderRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, user_id: int, **data):
        items_data = data.pop("items", None) or data.pop("order_items", None) or []

        allowed_fields = {
            "cafe_id",
            "status",
            "total_price",
            "note",
        }

        order_data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        order = Order(
            user_id=user_id,
            **order_data,
        )

        self.db.add(order)
        self.db.flush()

        for item in items_data:
            if hasattr(item, "dict"):
                item = item.dict()

            quantity = item.get("quantity", 1)
            unit_price = item.get("unit_price") or item.get("price") or 0
            total_price = item.get("total_price") or Decimal(str(unit_price)) * quantity

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item["menu_item_id"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
            )

            self.db.add(order_item)

        self.db.commit()
        self.db.refresh(order)

        return order

    def get_by_id(self, order_id: int):
        return (
            self.db.query(Order)
            .filter(Order.id == order_id, Order.deleted_at.is_(None))
            .first()
        )

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id, Order.deleted_at.is_(None))
            .order_by(Order.created_at.desc())
            .all()
        )

    def has_user_ordered_from_cafe(self, user_id: int, cafe_id: int) -> bool:
        order = (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
                Order.cafe_id == cafe_id,
                Order.deleted_at.is_(None),
            )
            .first()
        )

        return order is not None

    def update(self, order, data: dict):
        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)

        self.db.commit()
        self.db.refresh(order)

        return order

    def delete(self, order):
        order.deleted_at = datetime.utcnow()

        self.db.commit()
        return order