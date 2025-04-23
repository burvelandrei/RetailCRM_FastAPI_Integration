from pydantic import BaseModel
from typing import List, Dict


class OrdersRequest(BaseModel):
    customer_id: int


class Order(BaseModel):
    class Config:
        extra = "allow"


class OrdersResponse(BaseModel):
    success: bool
    orders: List[Order]
    pagination: Dict | None = None


class OrderItemRequest(BaseModel):
    productName: str
    quantity: float
    price: float


class CreateOrderRequest(BaseModel):
    site: str
    customerId: int
    number: str
    items: List[OrderItemRequest]


class CreateOrderResponse(BaseModel):
    success: bool
    id: int
    errorMsg: str | None = None


class CreatePaymentRequest(BaseModel):
    site: str
    orderId: int
    amount: float
    type: str
    status: str | None = "paid"
    externalId: str | None = None


class CreatePaymentResponse(BaseModel):
    success: bool
    id: int
    errorMsg: str | None = None
