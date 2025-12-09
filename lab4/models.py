from typing import Optional, List
from datetime import date
from sqlalchemy import String, Integer, Float, Date, ForeignKey, create_engine, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = 'Orders'

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    product: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "product": self.product,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "order_date": self.order_date.isoformat(),
            "status": self.status
        }

class TopCustomer(Base):
    __tablename__ = 'top_customers'

    customer_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_spent: Mapped[float] = mapped_column(Float, nullable=False)

    def to_dict(self):
        return {
            "customer_name": self.customer_name,
            "total_spent": round(self.total_spent, 2)
        }