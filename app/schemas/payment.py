from pydantic import BaseModel
from typing import Optional


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    user_id: int
    amount: float
    status: str
    payment_gateway: str
    transaction_id: Optional[str]

    class Config:
        from_attributes = True
