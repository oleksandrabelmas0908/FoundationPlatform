from pydantic import BaseModel
from datetime import datetime


class PaymentSchema(BaseModel):
    id: int
    amount: float
    payment_date: datetime
    
    user_id: int
    found_id: int
