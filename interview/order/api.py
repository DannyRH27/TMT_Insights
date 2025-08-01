from interview.order.serializers import OrderSerializer
from interview.order.models import Order, OrderTag



def retrieve_orders_by_tag(tag:OrderTag) -> list[dict]:
    # check if the tag exists first
    if not OrderTag.objects.filter(id=tag.id).exists():
        return []

    orders = tag.orders.all()

    return OrderSerializer(orders, many=True).data