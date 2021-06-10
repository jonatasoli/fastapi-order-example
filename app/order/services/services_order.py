from datetime import datetime

from loguru import logger
from config import settings

from order.dao import ordermodel
from order.schemas.schemas_order import (
    orderMessage,
    orderPayload,
    orderModelBrokerMessage,
    orderModelCreate,
    messageBaseResponse,
)
from order.api.adapters.user import get_user
from order.api.adapters.product import get_product
from order.api.adapters.publisher import publish_queue


class OrderService():
    async def add_ordermodel(self, ordermodel_data):
        try:
            _order_message = await self._pub_message(
                await ordermodel.create(
                    obj_in=await self._create_model_obj(ordermodel_data)
                )
            )
            return _order_message
        except Exception as e:
            logger.error(f"Error in add ordermodel {e}")
            raise e

    @staticmethod
    async def _create_model_obj(data):
        try:
            _user = await get_user(user_id=data.user_id)
            _product = await get_product(product_code=data.product_code)

            if not _user or not _product:
                raise ValueError(f"User or Product not found.\n User {_user} - Product {_product}")

            return orderModelCreate(
                user_id=_user.user_id,
                product_code=_product.product_code,
                customer_fullname=_user.customer_fullname,
                product_name=_product.product_name,
                total_amount=_product.price
            )
        except Exception as e:
            logger.error(f"Error in create_model_object {e}")
            raise e

    @staticmethod
    async def _pub_message(message):
        try:
            _order_message = orderMessage(
                order_id=message.id,
                product_code=message.product_code,
                customer_fullname=message.customer_fullname,
                product_name=message.product_name,
                total_amount=message.total_amount,
                created_at=message.created_at
            )
            _order_payload = orderPayload(order=_order_message)
            _order_broker_message = orderModelBrokerMessage(
                producer="service-order",
                sent_at=datetime.now(),
                type="created-order",
                payload=_order_payload,
            )

            _output = await publish_queue(
                broker_queue=settings.BROKER_QUEUE_CREATE_ORDER,
                broker_exchange=settings.BROKER_EXCHANGE_ORDERS,
                body_queue=_order_broker_message.json().encode("utf-8")
            )

            if not hasattr(_output, "index"):
                raise Exception("Order not queue")
            return messageBaseResponse(
                queue_index=_output.index,
                order_id=message.id,
                user_id=message.user_id,
                product_code=message.product_code,
                customer_fullname=message.customer_fullname,
                product_name=message.product_name,
                total_amount=message.total_amount,
                created_at=message.created_at,
            )
        except Exception as e:
            logger.error(f"Error in send message to broker {e}")
            raise e
