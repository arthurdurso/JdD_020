from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import create_product, get_products, get_product, update_product, delete_product

router = APIRouter()


@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db=db, product=product)
    return db_product

@router.get("/products/", response_model=list[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    products = get_products(db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return db_product