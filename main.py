# from fastapi import FastAPI
# from router import customer,seller,product,order,order_items,cart,discount,payment,review
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from db.database import Base,engine
# import os

# app = FastAPI(title="E-Commerce API")

# # create tables
# Base.metadata.create_all(bind=engine)

# # static images
# if os.path.exists("images/products"):
#     app.mount("/images", StaticFiles(directory="images/products"), name="images")

# origins = [
#     "http://localhost",
#     "http://127.0.0.1:5500", 
#     "https://your-frontend-domain.vercel.app", 
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(customer.router)
# app.include_router(seller.router)
# app.include_router(product.router)
# app.include_router(order.router)
# app.include_router(order_items.router)
# app.include_router(cart.router)
# app.include_router(payment.router)
# app.include_router(discount.router)
# app.include_router(review.router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to the E-Commerce API"}

from fastapi import FastAPI
from router import customer, seller, product, order, order_items, cart, discount, payment, review
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db.database import Base, engine
import os

app = FastAPI(title="Doughlightful E-Commerce API")

Base.metadata.create_all(bind=engine)

IMAGE_PATH = "images/products"
# if os.path.exists(IMAGE_PATH):
#     app.mount("/images/products", StaticFiles(directory="images/products"), name="images")
if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including Routers
app.include_router(customer.router)
app.include_router(seller.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(order_items.router)
app.include_router(cart.router)
# app.include_router(payment.router)
# app.include_router(discount.router)
# app.include_router(review.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Doughlightful API",
        "status": "Online",
        "docs": "/docs"
    }