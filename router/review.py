from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models.review import Review
from models.customer import Customer
from schema.review import ReviewCreate, ReviewUpdate, ReviewOut

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewOut)
def add_review(
    data: ReviewCreate,
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    review = Review(
        rating=data.rating,
        comment=data.comment,
        product_id=data.product_id,
        customer_id=customer_id
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return ReviewOut(
        id=review.id,
        rating=review.rating,
        comment=review.comment,
        customer_name=customer.name,
        created_at=review.created_at
    )

@router.get("/product/{product_id}", response_model=list[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()

    return [
        ReviewOut(
            id=r.id,
            rating=r.rating,
            comment=r.comment,
            customer_name=r.customer.name,
            created_at=r.created_at
        ) for r in reviews
    ]

@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.rating = data.rating
    review.comment = data.comment
    db.commit()
    db.refresh(review)

    return ReviewOut(
        id=review.id,
        rating=review.rating,
        comment=review.comment,
        customer_name=review.customer.name,
        created_at=review.created_at
    )
