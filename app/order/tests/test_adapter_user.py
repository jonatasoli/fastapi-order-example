import pytest
from fastapi import status, HTTPException

from order.api.adapters.user import get_user


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_user_success(mocker):
    response_obj = dict(
        firstName="Ada",
        user_id="7c11e1ce2741",
        lastName="Lovelace",
        customer_fullname="AdaLovelace"
    )
    output = await get_user(user_id="7c11e1ce2741")
    assert output.dict() == response_obj


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_user_success_resilient(mocker):
    """Must have return object User because retry decorator"""
    response_obj = dict(
        firstName="Alan",
        user_id="e6f24d7d1c7e",
        lastName="Turing",
        customer_fullname="AlanTuring"
    )
    output = await get_user(user_id="e6f24d7d1c7e")
    assert output.dict() == response_obj


@pytest.mark.container
@pytest.mark.asyncio
async def test_get_user_not_found(mocker):
    with pytest.raises(HTTPException) as exc_info:
        await get_user(user_id="errorid1")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
