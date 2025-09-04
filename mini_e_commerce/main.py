from fastapi import FastAPI
from .database import Base, engine
from .routers import products, customers, orders, cart

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce Backend")

@app.get("/",tags=["Welcome Message"])
def root():
    return {"message": "Mini E-Commerce Backend is running"}

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(cart.router)
app.include_router(orders.router)