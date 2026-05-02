from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add Transaction
@app.post("/add")
def add_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
    new_txn = models.Transaction(user=txn.user, amount=txn.amount)
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return {"message": "Transaction added", "data": new_txn}

# Get All Transactions
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

# Analytics API
@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    data = db.query(models.Transaction).all()

    total = sum([d.amount for d in data])
    count = len(data)
    avg = total / count if count > 0 else 0

    return {
        "total": total,
        "count": count,
        "average": avg
    }
@app.put("/update/{id}")
def update_transaction(id: int, txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
    data = db.query(models.Transaction).filter(models.Transaction.id == id).first()
    
    if not data:
        return {"error": "Data not found"}
    
    data.user = txn.user
    data.amount = txn.amount
    db.commit()
    
    return {"message": "Updated successfully"}