from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    db = SessionLocal() # Mở kết nối MySQL
    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )
        db.add(new_product) # Thêm vào session
        db.commit()
        db.refresh(new_product)
        
        return {
            "message": "Product prepared successfully", 
            "data": {"sku": new_product.sku, "name": new_product.name}
        }
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail="Product sku already exists"
        )
    finally:
        db.close()