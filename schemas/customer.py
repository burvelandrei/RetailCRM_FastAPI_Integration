from pydantic import BaseModel
from typing import Dict, List

class Customer(BaseModel):
    class Config:
        extra = "allow"

    id: int
    firstName: str | None = None
    email: str| None = None
    createdAt: str | None = None

class CustomersResponse(BaseModel):
    success: bool
    customers: List[Customer]
    pagination: Dict | None = None

class CreateCustomer(BaseModel):
    firstName: str
    lastName: str | None = None
    patronymic: str | None = None
    email: str | None = None
    phone: str | None = None
    externalId: str | None = None

class CreateCustomerRequest(BaseModel):
    site: str
    customer: CreateCustomer

class CreateCustomerResponse(BaseModel):
    success: bool
    id: int | None = None
    errorMsg: str | None = None