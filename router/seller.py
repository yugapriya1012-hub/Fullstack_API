from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from models.seller import Seller
from schema.seller import SellerCreate, SellerResponse,SellerLogin

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/seller",
    tags=["Seller"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def seller_signup(data: SellerCreate, db: Session = Depends(get_db)):

    existing_seller = db.query(Seller).filter(Seller.email == data.email).first()
    if existing_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(data.password)

    new_seller = Seller(
        name=data.name,
        email=data.email,
        password=hashed_password,
        phone=data.phone
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return {
        "message": "Seller created successfully"
    }


@router.post("/login")
def seller_login(data: SellerLogin, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.email == data.email).first()
   
    return {
        "message": "Login successful",
        "seller_id": seller.id,  
        "name": seller.name,
        "email": seller.email,
        "phone": seller.phone
    }


@router.post("/", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
def create_seller(seller: SellerCreate, db: Session = Depends(get_db)):

    existing_seller = db.query(Seller).filter(Seller.email == seller.email).first()
    if existing_seller:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_seller = Seller(
        name=seller.name,
        email=seller.email,
        password=seller.password  
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return new_seller


@router.get("/", response_model=List[SellerResponse])
def get_all_sellers(db: Session = Depends(get_db)):
    sellers = db.query(Seller).all()
    return sellers

@router.get("/{seller_id}", response_model=SellerResponse)
def get_seller_by_id(seller_id: int, db: Session = Depends(get_db)):

    seller = db.query(Seller).filter(Seller.id == seller_id).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    return seller

@router.post("/login")
def seller_login(data: SellerLogin, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.email == data.email).first()
    if not seller:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(data.password, seller.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "message": "Login successful",
        "seller_id": seller.id,
        "name": seller.name,
        "email": seller.email,
        "phone": seller.phone
    }

@router.get("/{seller_id}/phone")
def get_seller_phone(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return {
        "seller_id": seller.id,
        "name": seller.name,
        "phone": seller.phone
    }