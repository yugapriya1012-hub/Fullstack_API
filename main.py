from fastapi import FastAPI
from router import customer,seller,product,order,order_items,cart,discount,payment,review
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db.database import Base,engine



# Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="E-Commerce API")
app = FastAPI()
origins = ["http://127.0.0.1:5500","http://localhost:5500",]

app.mount("/images",StaticFiles(directory="images"),name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

