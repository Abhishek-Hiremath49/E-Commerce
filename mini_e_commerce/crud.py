from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal
from . import models, schema

def create_product(db: Session, product: schema.ProductCreate):
    prod = models.Product(name=product.name, price=product.price, stock=product.stock)
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

def list_products(db: Session):
    return db.query(models.Product).all()

def create_customer(db: Session, customer: schema.CustomerCreate):
    if db.query(models.Customer).filter_by(email=customer.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    cust = models.Customer(name=customer.name, email=customer.email)
    db.add(cust)
    db.commit()
    db.refresh(cust)
    return cust

def place_order(db: Session, order: schema.OrderCreate):
    customer = db.query(models.Customer).filter_by(id=order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    total = Decimal("0.00")
    products = {}
    for item in order.items:
        prod = db.query(models.Product).filter_by(id=item.product_id).with_for_update().first()
        if not prod:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if prod.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
        products[item.product_id] = prod
        total += Decimal(str(prod.price)) * Decimal(str(item.quantity))

    order_db = models.Order(customer_id=order.customer_id, total=total, status=models.OrderStatus.placed)
    db.add(order_db)
    db.flush()

    for item in order.items:
        prod = products[item.product_id]
        prod.stock -= item.quantity
        db.add(models.OrderItem(order_id=order_db.id, product_id=prod.id, quantity=item.quantity, price=prod.price))

    db.commit()
    db.refresh(order_db)
    return order_db

def update_order_status(db: Session, order_id: int, status_value: schema.StatusUpdate):
    order = db.query(models.Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_value.status
    db.commit()
    db.refresh(order)
    return order

def get_customer_orders(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter_by(id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.query(models.Order).filter_by(customer_id=customer_id).all()

def list_customers(db: Session):
    return db.query(models.Customer)

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter_by(id=customer_id).first()

def delete_products(db: Session, product_id:int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted_product = product
    db.delete(product)
    db.commit()
    return deleted_product

def get_cart_by_customer(db: Session, customer_id: int):
    cart = db.query(models.Cart).filter(models.Cart.customer_id == customer_id).first()
    if not cart:
        cart = models.Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_or_update_cart_item(db: Session, customer_id: int, item_in: schema.CartItemCreate):
    cart = get_cart_by_customer(db, customer_id)
    
    product = db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < item_in.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for product")

    # Check if item already in cart
    cart_item = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id, models.CartItem.product_id == item_in.product_id).first()
    if cart_item:
        cart_item.quantity += item_in.quantity
    else:
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_cart_item(db: Session, item_id: int):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()

def clear_cart(db: Session, customer_id: int):
    cart = get_cart_by_customer(db, customer_id)
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()

def update_cart_item_quantity(db: Session, item_id: int, quantity: int):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if quantity <= 0:
        db.delete(cart_item)
    else:
        product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()
        if product.stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock for product")
        cart_item.quantity = quantity
        db.add(cart_item)
    db.commit()
    if quantity > 0:
        db.refresh(cart_item)
        return cart_item
    else:
        return None

    