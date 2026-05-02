from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user: str
    amount: float