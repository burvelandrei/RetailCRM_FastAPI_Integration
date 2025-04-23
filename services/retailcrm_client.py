import httpx
import logging
import logging.config
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from utils.logger import logging_config


logging.config.dictConfig(logging_config)
logger = logging.getLogger("retailcrm_client")


class RetailCRMClient:
    def __init__(self, subdomain: str, api_key: str):
        """Инициализация клиента"""
        self.subdomain = subdomain
        self.api_key = api_key
        self.base_url = f"https://{subdomain}.retailcrm.ru/api/v5"
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
    ):
        """Выполнение GET-запроса"""
        params = params or {}
        params["apiKey"] = self.api_key
        try:
            response = await self._client.get(
                url=f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("success"):
                error_msg = (
                    f"RetailCRM API error: {
                        data.get('errorMsg', 'Unknown error')
                    }"
                )
                logger.error(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            logger.info(f"GET request successful: {response.status_code}")
            return data
        except httpx.HTTPStatusError as e:
            error_msg = (
                f"HTTP error: {e.response.status_code} - {e.response.text}"
            )
            logger.error(error_msg)
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_msg
            )
        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )

    async def post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        """Выполнение POST-запроса"""
        params = params or {}
        params["apiKey"] = self.api_key
        try:
            response = await self._client.post(
                url=f"{self.base_url}/{endpoint}",
                params=params,
                json=data,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("success"):
                error_msg = (
                    f"RetailCRM API error: {
                        data.get('errorMsg', 'Unknown error')
                    }"
                )
                logger.error(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            logger.info(f"POST request successful: {response.status_code}")
            return data
        except httpx.HTTPStatusError as e:
            error_msg = (
                f"HTTP error: {e.response.status_code} - {e.response.text}"
            )
            logger.error(error_msg)
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_msg
            )
        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
