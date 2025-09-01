from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schema, crud
from ..deps import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schema.ProductRead, status_code=201)
def add_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/", response_model=list[schema.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return crud.list_products(db)
