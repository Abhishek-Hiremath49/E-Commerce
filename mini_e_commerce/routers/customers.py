from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schema, crud
from ..deps import get_db

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=schema.CustomerRead, status_code=201)
def register_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@router.get("/{customer_id}", response_model=schema.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with id {customer_id}")
    return customer

@router.get("/{customer_id}/orders", response_model=list[schema.OrderRead])
def get_orders(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_orders(db, customer_id)

@router.get("/", response_model=list[schema.CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return crud.list_customers(db).all()