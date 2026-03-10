from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db
from models.customer import Customer
from schema.customer import CustomerCreate, CustomerOut, CustomerLogin
from passlib.context import CryptContext

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED)
def signup(data: CustomerCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Customer).filter(Customer.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = pwd_context.hash(data.password)
    new_customer = Customer(
        name=data.name,
        email=data.email,
        password=hashed_password,
        phone=data.phone
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer created successfully"}


@router.post("/login")
def login(data: CustomerLogin, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == data.email).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(data.password, customer.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "message": "Login successful",
        "customer_id": customer.id,  
        "name": customer.name,
        "email": customer.email
    }


@router.get("/by-email")
def get_customer_by_email(email: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# ✅ Get all customers
@router.get("/", response_model=list[CustomerOut])
def get_all_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer