from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schema, crud
from ..deps import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/items", response_model=schema.CartItemRead)
def add_to_cart(customer_id:int, item: schema.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_or_update_cart_item(db, customer_id, item)

@router.get("/", response_model=schema.CartRead)
def get_cart(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_cart_by_customer(db, customer_id)

@router.delete("/items/{item_id}", status_code=204)
def remove_cart_item(item_id: int, db: Session = Depends(get_db)):
    crud.remove_cart_item(db, item_id)
    return {"message": "Item removed"}
