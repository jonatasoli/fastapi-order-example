import pytest
from fastapi import status, HTTPException
from datetime import datetime
from order.services.services_order import OrderService
from order.schemas.schemas_order import (
    orderModelCreateResponse,
    orderModelBase,
    orderModelCreate,
    messageBaseResponse,
)


response_obj = orderModelCreateResponse(
    id = 1,
    user_id="1",
    product_code="x1",
    customer_fullname="UserName",
    product_name="product 1",
    total_amount=125.00,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_message = messageBaseResponse(
    queue_index=1,
    order_id = 1,
    user_id="1",
    product_code="x1",
    customer_fullname="UserName",
    product_name="product 1",
    total_amount=125.00,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)

response_obj_container = orderModelCreateResponse(
    id = 1,
    user_id="7c11e1ce2741",
    product_code="classic-box",
    customer_fullname="AdaLoveLace",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_message_container = messageBaseResponse(
    queue_index=1,
    order_id = 1,
    user_id="7c11e1ce2741",
    product_code="classic-box",
    customer_fullname="AdaLoveLace",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_obj_container_user_2 = orderModelCreateResponse(
    id = 1,
    user_id="e6f24d7d1c7e",
    product_code="classic-box",
    customer_fullname="AlanTuring",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_message_container_user_2 = messageBaseResponse(
    queue_index=1,
    order_id = 1,
    user_id="e6f24d7d1c7e",
    product_code="classic-box",
    customer_fullname="AlanTuring",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


@pytest.mark.asyncio
async def test_add_ordermodel(mocker):
    mocker.patch(
        "order.dao.ordermodel.create",
        return_value=response_obj
    )
    mocker.patch(
        "order.services.services_order.OrderService._pub_message",
        return_value=response_message
    )
    data = orderModelBase(user_id="7c11e1ce2741", product_code="classic-box")
    order = OrderService()
    response = await order.add_ordermodel(ordermodel_data=data)
    assert response == response_message


@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_1(mocker):
    """Must have return object"""
    mocker.patch(
        "order.dao.ordermodel.create",
        return_value=response_obj_container
    )
    mocker.patch(
        "order.services.services_order.OrderService._pub_message",
        return_value=response_message_container
    )
    data =  orderModelBase(user_id="7c11e1ce2741", product_code="classic-box")
    order = OrderService()
    response = await order.add_ordermodel(ordermodel_data=data)
    assert response == response_message_container


@pytest.mark.slow
@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_2(mocker):
    """Must have return timeout http error"""
    data =  orderModelBase(user_id="7c11e1ce2741", product_code="family-box")
    order = OrderService()
    with pytest.raises(HTTPException) as exc_info:
        response = await order.add_ordermodel(ordermodel_data=data)
    assert exc_info.value.status_code == status.HTTP_408_REQUEST_TIMEOUT


@pytest.mark.slow
@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_3(mocker):
    """Must have return internal error 500 in product"""
    data = orderModelBase(user_id="7c11e1ce2741", product_code="veggie-box")
    order = OrderService()
    with pytest.raises(HTTPException) as exc_info:
        response = await order.add_ordermodel(ordermodel_data=data)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_4(mocker):
    """Must return 200"""
    mocker.patch(
        "order.dao.ordermodel.create",
        return_value=response_obj_container
    )
    mocker.patch(
        "order.services.services_order.OrderService._pub_message",
        return_value=response_message_container_user_2
    )
    data =  orderModelBase(user_id="e6f24d7d1c7e", product_code="classic-box")
    order = OrderService()
    response = await order.add_ordermodel(ordermodel_data=data)
    assert response == response_message_container_user_2


@pytest.mark.slow
@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_6(mocker):
    """Must have return 200 in user adapter and 500 and product with raise"""
    data =  orderModelBase(user_id="e6f24d7d1c7e", product_code="veggie-box")
    order = OrderService()
    with pytest.raises(HTTPException) as exc_info:
        response = await order.add_ordermodel(ordermodel_data=data)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.slow
@pytest.mark.container
@pytest.mark.asyncio
async def test_add_ordermodel_container_case_5(mocker):
    """Must have return error with 408 with latency family-box"""
    data = orderModelBase(user_id="e6f24d7d1c7e", product_code="family-box")
    order = OrderService()
    with pytest.raises(HTTPException) as exc_info:
        response = await order.add_ordermodel(ordermodel_data=data)
    assert exc_info.value.status_code == status.HTTP_408_REQUEST_TIMEOUT


@pytest.mark.asyncio
@pytest.mark.skip
async def test_add_ordermodel_data(mocker):
    mocker.patch(
        "order.api.adapters.publisher.publish_queue",
        return_value=dict(index=1)
    )
    data =  orderModelBase(user_id="7c11e1ce2741", product_code="classic-box")
    order = OrderService()
    response = await order.add_ordermodel(ordermodel_data=data)
    from loguru import logger
    logger.debug(response.dict())
    assert isinstance(response.dict(), dict)
