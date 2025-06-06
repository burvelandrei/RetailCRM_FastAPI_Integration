import json
from fastapi import APIRouter, Query
from datetime import date
from typing import Dict, Any
from schemas.customer import (
    CustomersResponse,
    CreateCustomerRequest,
    CreateCustomerResponse,
)
from services.retailcrm_client import RetailCRMClient
from config import settings


router = APIRouter(prefix="/customers")


@router.get(
        "/",
        response_model=CustomersResponse,
        summary="Получение списка клиентов",
)
async def get_customers(
    name: str | None = Query(None, alias="filter[name]"),
    email: str | None = Query(None, alias="filter[email]"),
    date_from: date | None = Query(None, alias="filter[dateFrom]"),
    date_to: date | None = Query(None, alias="filter[dateTo]"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Получения списка клиентов"""
    params: Dict[str, Any] = {
        "page": page,
        "limit": limit
    }
    if name:
        params["filter[name]"] = name
    if email:
        params["filter[email]"] = email
    if date_from:
        params["filter[dateFrom]"] = date_from.isoformat()
    if date_to:
        params["filter[dateTo]"] = date_to.isoformat()
    async with RetailCRMClient(
        subdomain=settings.RETAILCRM_SUBDOMAIN,
        api_key=settings.RETAILCRM_API_KEY,
    ) as client:
        data = await client.get("customers", params=params)
    return CustomersResponse(
        success=data["success"],
        customers=data.get("customers", []),
        pagination=data.get("pagination")
    )


@router.post(
        "/create/",
        response_model=CreateCustomerResponse,
        summary="Создание клиента",
)
async def create_customer(
    customer_data: CreateCustomerRequest,
):
    """Создание клиента"""
    payload = customer_data.dict()
    payload["customer"] = json.dumps(payload["customer"], ensure_ascii=False)
    async with RetailCRMClient(
        subdomain=settings.RETAILCRM_SUBDOMAIN,
        api_key=settings.RETAILCRM_API_KEY,
    ) as client:
        data = await client.post("customers/create", data=payload)
    return CreateCustomerResponse(
        success=data["success"],
        id=data.get("id"),
        errorMsg=data.get("errorMsg")
    )
