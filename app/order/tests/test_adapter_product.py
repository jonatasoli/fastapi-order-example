import pytest
from fastapi import status, HTTPException

from order.api.adapters.product import get_product
from order.schemas.schemas_product import productBase


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_product_success(mocker):
    response_obj = productBase(
        product_code="classic-box",
        product_name="Classic Box",
        price=9.99
    )
    response = await get_product(product_code="classic-box")
    assert response.dict() == response_obj


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_product_not_found(mocker):
    with pytest.raises(HTTPException) as exc_info:
        await get_product(product_code="error-box")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    # assert exc_info.value.detail == "Internal Error\n 404 Client Error: Not Found for url: http://localhost:8081/products/error-box\nFor more information check: https://httpstatuses.com/404"


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_product_request_timeout(mocker):
    with pytest.raises(HTTPException) as exc_info:
        await get_product(product_code="family-box")
    assert exc_info.value.status_code == status.HTTP_408_REQUEST_TIMEOUT


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_product_internal_error(mocker):
    with pytest.raises(HTTPException) as exc_info:
        await get_product(product_code="veggie-box")
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
