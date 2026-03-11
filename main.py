from fastapi import FastAPI
from router import customer,seller,product,order,order_items,cart,discount,payment,review
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db.database import Base,engine



Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.mount("/images",StaticFiles(directory="images"),name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(customer.router)
app.include_router(seller.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(order_items.router)
app.include_router(cart.router)
app.include_router(payment.router)
app.include_router(discount.router)
app.include_router(review.router)




# # Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce API"}

