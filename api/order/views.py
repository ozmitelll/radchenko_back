from datetime import datetime
from urllib.parse import unquote

from fastapi import APIRouter, Depends, Query
from tortoise.exceptions import DoesNotExist

from api.user.views import get_current_user
from models.app_models import OrderModel, User_Pydantic, OrderDTO, User

router = APIRouter()


async def generate_order_number(user_id: int):
    order_number = f"N{user_id:02d}-{datetime.now().microsecond}"
    return order_number


@router.get('')
async def get_orders(
        skip: int = Query(1, alias="page", ge=0),
        limit: int = Query(10, le=100),
        current_user=Depends(get_current_user),
        unit: str = None
):
    user = await User.get(id=current_user.id)
    decoded_unit = unquote(unit) if unit else None
    try:
        if user.is_admin:
            query = await OrderModel.all().offset((skip - 1) * limit).limit(limit).all()
        else:
            query = await user.orders.offset((skip - 1) * limit).limit(limit).all()

        if decoded_unit:
            query = [order for order in query if order.unit in decoded_unit]

        total_count = await OrderModel.all().count()
        total_pages = -(-total_count // limit)  # Calculate total pages (ceiling division)
        return {"data": query, "currentPage": skip, "totalPages": total_pages, "totalCount": total_count}
    except Exception as e:
        return {"error": str(e)}


@router.get('/{order_id}')
async def get_order(current_user=Depends(get_current_user),
                    order_id: int = None):
    try:
        order = await OrderModel.get(id=order_id)
        return {"order": order.number_order}
    except DoesNotExist:
        return {"order": "Not found!"}


@router.post('/create')
async def create_order(current_user=Depends(get_current_user),
                       order: OrderDTO = None):
    try:
        user = await User.get(id=current_user.id)
        order_number = await generate_order_number(current_user.id)
        await OrderModel.create(
            number_order=order_number,
            unit=user.unit,
            customer_id=current_user.id,
            technics=order.technics,
            time_of_execution=datetime.now()
        )
        return {'result': "order created successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.delete('/{order_id}')
async def delete_order(current_user=Depends(get_current_user),
                       order_id: int = None):
    try:
        order = await OrderModel.get(id=order_id)
        await order.delete()
        return {'result': "order deleted successfully"}
    except DoesNotExist:
        return {"result": "order not found!"}
