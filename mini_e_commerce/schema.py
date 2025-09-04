from pydantic import BaseModel, Field, EmailStr, field_validator
from decimal import Decimal
from typing import List, Annotated
from .models import OrderStatus

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: Annotated[float,Field(strict=True,gt=0)]
    stock: Annotated[int,Field(strict=True,ge=0)]

class ProductRead(ProductCreate):
    id: int
    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr

class CustomerRead(CustomerCreate):
    id: int
    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    product_id: int
    name : str
    quantity: Annotated[float,Field(strict=True,gt=0)]

class OrderCreate(BaseModel):
    customer_id: int
    name: str
    items: List[OrderItemCreate]

    @field_validator("items")
    def check_items(cls, v):
        if not v:
            raise ValueError("Order must contain at least one item.")
        return v

class OrderItemRead(BaseModel):
    product_id: int
    quantity: int
    price: Decimal
    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    customer_id: int
    total: Decimal
    status: OrderStatus
    items: List[OrderItemRead]
    class Config:
        orm_mode = True

class StatusUpdate(BaseModel):
    status: OrderStatus

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(...,gt=0)

class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    
    class Config:
        orm = True

class CartRead(BaseModel):
    id: int
    customer_id: int
    items: List[CartItemRead]

    class Config:
        orm_mode = True