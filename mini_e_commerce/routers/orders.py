from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schema, crud
from ..deps import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schema.OrderRead, status_code=201)
def place_order(order: schema.OrderCreate, db: Session = Depends(get_db)):
    return crud.place_order(db, order)

@router.patch("/{order_id}/status", response_model=schema.OrderRead)
def update_status(order_id: int, status_in: schema.StatusUpdate, db: Session = Depends(get_db)):
    return crud.update_order_status(db, order_id, status_in)