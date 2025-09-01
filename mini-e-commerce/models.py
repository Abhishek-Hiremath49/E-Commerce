from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum as PyEnum


class OrderStatus(str, PyEnum):
    placed = "placed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(scale=2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total = Column(Numeric(scale=2), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.placed)

    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(scale=2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
