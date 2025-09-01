from fastapi import FastAPI
from .database import Base, engine
# from .routers import products, customers, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce Backend")

# app.include_router(products.router)
# app.include_router(customers.router)
# app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Mini E-Commerce Backend is running"}
