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

    # Check duplicate email
    existing_seller = db.query(Seller).filter(Seller.email == data.email).first()
    if existing_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(data.password)

    # Create seller
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


# @router.post("/login")
# def seller_login(data: SellerLogin, db: Session = Depends(get_db)):

#     seller = db.query(Seller).filter(Seller.email == data.email).first()

#     if not seller:
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     # Verify password
#     if not pwd_context.verify(data.password, seller.password):
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     return {
#         "message": "Login successful"
#     }

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
        password=seller.password   # later hash this
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return new_seller


# 🔹 GET ALL SELLERS
@router.get("/", response_model=List[SellerResponse])
def get_all_sellers(db: Session = Depends(get_db)):
    sellers = db.query(Seller).all()
    return sellers


# 🔹 GET SELLER BY ID
@router.get("/{seller_id}", response_model=SellerResponse)
def get_seller_by_id(seller_id: int, db: Session = Depends(get_db)):

    seller = db.query(Seller).filter(Seller.id == seller_id).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    return seller

# @router.post("/logout")
# def seller_logout(seller_id: int):
#     """
#     This route handles the ACT of logging out.
#     """
#     import datetime
#     logout_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     # Store the info in our history list
#     entry = {"seller_id": seller_id, "logout_at": logout_time}
#     logout_history.append(entry)
    
#     print(f"Server Log: Seller {seller_id} logged out at {logout_time}")
    
#     return {
#         "status": "success", 
#         "message": "Logged out successfully",
#         "data": entry
#     }
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
# 🔹 2. THE VIEW: Get Logout History (GET)
# @router.get("/logout-history")
# def get_logout_history():
#     """
#     This route allows you to SEE who has logged out.
#     """
#     return {
#         "total_logouts": len(logout_history),
#         "history": logout_history
    # }
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