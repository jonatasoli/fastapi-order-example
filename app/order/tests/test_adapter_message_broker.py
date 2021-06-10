import pytest
import json
from datetime import datetime
from config import settings
from order.api.adapters.publisher import publish_queue
from order.schemas.schemas_order import orderModelBrokerMessage,\
    orderMessage, orderPayload


@pytest.mark.container
@pytest.mark.asyncio
async def test_create_message(mocker):
    _order_message = orderMessage(
        order_id=1,
        customer_fullname="AdaLovelace",
        product_name="product 1",
        total_amount=99.99,
        created_at=datetime(2021, 5, 25, 10, 20, 30, 0)
    )
    _order_payload = orderPayload(order=_order_message)
    _order_broker_message = orderModelBrokerMessage(
        producer="service-order",
        sent_at=datetime.now(),
        type="created-order",
        payload=_order_payload
    )
    _body = _order_broker_message.json().encode("utf-8")
    response = await publish_queue(
        broker_queue='test',
        broker_exchange=settings.BROKER_EXCHANGE_ORDERS,
        body_queue=_body,
        exchange_type='direct'
    )
    assert isinstance(response.index, int)

