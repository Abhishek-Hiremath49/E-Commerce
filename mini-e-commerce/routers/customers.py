from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schema, crud
from ..deps import get_db

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=schema.CustomerRead, status_code=201)
def register_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@router.get("/{customer_id}/orders", response_model=list[schema.OrderRead])
def get_orders(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_orders(db, customer_id)
