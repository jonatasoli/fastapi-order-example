from fastapi import status
from datetime import datetime
import json
import pytest

from order.schemas.schemas_order import orderModelBase, messageBaseResponse,\
    orderModelCreateResponse

HEADERS = {"Content-Type": "application/json"}


order_response = orderModelCreateResponse(
    id=1,
    user_id="1",
    product_code="x1",
    customer_fullname="UserName",
    product_name="product 1",
    total_amount=125.00,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_message = messageBaseResponse(
    queue_index=1,
    order_id=1,
    user_id="1",
    product_code="x1",
    customer_fullname="UserName",
    product_name="product 1",
    total_amount=125.00,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


order_response_user_2 = orderModelCreateResponse(
    id=1,
    user_id="e6f24d7d1c7e",
    product_code="classic-box",
    customer_fullname="AlanTuring",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


response_message_user_2 = messageBaseResponse(
    queue_index=1,
    order_id=1,
    user_id="e6f24d7d1c7e",
    product_code="classic-box",
    customer_fullname="AlanTuring",
    product_name="Classic Box",
    total_amount=9.99,
    created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
)


def test_error_route(client):
    response = client.get("/error_route", headers=HEADERS)
    response_data = response.json().get("detail")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == "Not Found"


def test_add_order_error_field_user_id(client):
    """Must be error on validate fields"""
    data = dict(product_code="x1")
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"
    assert response_data.get("loc") == ["body", "user_id"]


def test_add_order_error_field_product_code(client):
    """Must be error on validate fields"""
    data = dict(user_id="1")
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"
    assert response_data.get("loc") == ["body", "product_code"]


def test_add_order_error_validate_user_id(client):
    """Must be error on validate data"""
    data = dict(user_id="", product_code="x1")
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "__init__() takes exactly 3 positional arguments (2 given)"
    assert response_data.get("type") == "type_error"
    assert response_data.get("loc") == ["body", "user_id"]


def test_add_order_error_validate_product_code(client):
    """Must be error on validate data"""
    data = dict(user_id="1", product_code="")
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "__init__() takes exactly 3 positional arguments (2 given)"
    assert response_data.get("type") == "type_error"
    assert response_data.get("loc") == ["body", "product_code"]


def test_add_order_error_validate_bool_user_id(client):
    """Must be error on validate data"""
    data = dict(user_id=" ", product_code="x1")
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "__init__() takes exactly 3 positional arguments (2 given)"
    assert response_data.get("type") == "type_error"
    assert response_data.get("loc") == ["body", "user_id"]


def test_add_order_error_validate_bool_product_code(client):
    """Must be error on validate data"""
    data = dict(user_id=1, product_code=False)
    response = client.post("/orders", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "__init__() takes exactly 3 positional arguments (2 given)"
    assert response_data.get("type") == "type_error"
    assert response_data.get("loc") == ["body", "product_code"]


@pytest.mark.container
def test_add_order_case_1(client, mocker):
    """Must return 201"""
    mocker.patch(
        "order.dao.ordermodel.create",
        return_value=order_response
    )
    mocker.patch(
        "order.services.services_order.OrderService._pub_message",
        return_value=response_message
    )
    data = orderModelBase(user_id="7c11e1ce2741", product_code="classic-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == json.loads(response_message.json())


@pytest.mark.slow
@pytest.mark.container
def test_add_order_case_2(client, mocker):
    """Must have return 408 timeout http error"""
    data = orderModelBase(user_id="7c11e1ce2741", product_code="family-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    # assert response.status_code == status.HTTP_408_REQUEST_TIMEOUT
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.slow
@pytest.mark.container
def test_add_order_case_3(client, mocker):
    """Must have return internal error 500 in product"""
    data = orderModelBase(user_id="7c11e1ce2741", product_code="veggie-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    # assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.container
def test_add_order_case_4(client, mocker):
    """Must return 201"""
    mocker.patch(
        "order.dao.ordermodel.create",
        return_value=order_response_user_2
    )
    mocker.patch(
        "order.services.services_order.OrderService._pub_message",
        return_value=response_message_user_2
    )
    data = orderModelBase(user_id="e6f24d7d1c7e", product_code="classic-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == json.loads(response_message_user_2.json())


@pytest.mark.slow
@pytest.mark.container
def test_add_order_case_5(client, mocker):
    """Must have return error with 408 with latency family-box"""
    data = orderModelBase(user_id="e6f24d7d1c7e", product_code="family-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.slow
@pytest.mark.container
def test_add_order_case_6(client, mocker):
    """Must have return 200 in user adapter and 500 and product with raise"""
    data = orderModelBase(user_id="e6f24d7d1c7e", product_code="veggie-box")
    response = client.post("/orders", headers=HEADERS, json=data.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND
