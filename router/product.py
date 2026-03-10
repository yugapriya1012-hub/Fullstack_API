import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, status,HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from models.product import Product
from models.seller import Seller
from schema.product import ProductResponse


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

UPLOAD_DIR = "images/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    seller_name: str = Form(...), 
    product_name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    places: str = Form(...),
    discount: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
   
    seller = db.query(Seller).filter(Seller.name == seller_name).first()
    
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found. Please check the name."
        )

   
    file_path = f"{UPLOAD_DIR}/{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

  
    new_product = Product(
        seller_id=seller.id, 
        product_name=product_name,
        description=description,
        price=price,
        places=places,
        discount=discount,
        image=image.filename
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



@router.get("/")
def get_products(db: Session = Depends(get_db)):
  
    products = db.query(Product).all() 
    
    
    result = []
    for product in products:
        seller = db.query(Seller).filter(Seller.id == product.seller_id).first()
        product_dict = product.__dict__
        product_dict['seller_name'] = seller.name if seller else "Unknown"
        result.append(product_dict)
        
    return result


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    seller_id: int = Form(...),
    product_name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    places: str = Form(...),
    discount: int = Form(...),
    image: UploadFile = File(None),  
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.seller_id == seller_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not authorized")

    if image:
        old_image_path = f"{UPLOAD_DIR}/{product.image}"
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

        new_image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(new_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        product.image = image.filename

   
    product.product_name = product_name
    product.description = description
    product.price = price
    product.places = places
    product.discount = discount

    db.commit()
    db.refresh(product)

    return product



@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    seller_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.seller_id == seller_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not authorized")

    # 🔹 Delete image from folder
    image_path = f"{UPLOAD_DIR}/{product.image}"
    if os.path.exists(image_path):
        os.remove(image_path)

    db.delete(product)
    db.commit()

    return None

    