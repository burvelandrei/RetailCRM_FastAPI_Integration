import json
from fastapi import APIRouter, Query
from typing import Dict, Any
from schemas.order import (
    OrdersResponse,
    OrdersRequest,
    CreateOrderRequest,
    CreateOrderResponse,
    CreatePaymentRequest,
    CreatePaymentResponse,
)
from services.retailcrm_client import RetailCRMClient
from config import settings


router = APIRouter(prefix="/orders")


@router.get(
        "/",
        response_model=OrdersResponse,
        summary="Получение списка заказов клиента",
)
async def get_customer_orders(
    customer_data: OrdersRequest,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Получение списка заказов клиента"""
    params: Dict[str, Any] = {
        "page": page,
        "limit": limit
    }
    params["filter[customerId]"] = customer_data.customer_id
    async with RetailCRMClient(
        subdomain=settings.RETAILCRM_SUBDOMAIN,
        api_key=settings.RETAILCRM_API_KEY,
    ) as client:
        data = await client.get("orders", params=params)
    return OrdersResponse(
        success=data["success"],
        orders=data.get("orders", []),
        pagination=data.get("pagination")
    )


@router.post(
        "/create/",
        response_model=CreateOrderResponse,
        summary="Создание нового заказа для клиента"
)
async def create_order(
    order_data: CreateOrderRequest,
):
    """Создание нового заказа для клиента"""
    order = {
        "number": order_data.number,
        "customer": {
            "id": order_data.customerId,
        },
        "items": [
            {
                "productName": item.productName,
                "quantity": item.quantity,
                "initialPrice": item.price,
            } for item in order_data.items
        ]
    }
    payload = {
        "site": order_data.site,
        "order": json.dumps(order)
    }
    async with RetailCRMClient(
        subdomain=settings.RETAILCRM_SUBDOMAIN,
        api_key=settings.RETAILCRM_API_KEY,
    ) as client:
        data = await client.post("orders/create", data=payload)
    return CreateOrderResponse(
        success=data["success"],
        id=data.get("id"),
        errorMsg=data.get("errorMsg")
    )


@router.post(
        "/payments/create/",
        response_model=CreatePaymentResponse,
        summary="Создание и привязка платежа к заказу",
)
async def add_payment(payment_data: CreatePaymentRequest):
    """Создание и привязка платежа к заказу"""
    payment = {
        "amount": payment_data.amount,
        "order": {
            "id": payment_data.orderId
        },
        "type": payment_data.type,
        "status": payment_data.status,
        "externalId": payment_data.externalId
    }
    payload = {
        "site": payment_data.site,
        "payment": json.dumps(payment)
    }
    async with RetailCRMClient(
        subdomain=settings.RETAILCRM_SUBDOMAIN,
        api_key=settings.RETAILCRM_API_KEY,
    ) as client:
        data = await client.post("orders/payments/create", data=payload)
    return CreatePaymentResponse(
        success=True,
        id=data.get("id"),
        errorMsg=data.get("errorMsg")
    )
