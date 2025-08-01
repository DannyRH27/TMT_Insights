from interview.order.models import Order
from interview.order.serializers import OrderTagSerializer

# if order doesn't exist, don't grab tags and don't instantiate serializer

def retrieve_tags_by_order(order: Order) ->list[dict]:
    if not Order.objects.filter(id=order.id).exists():
        return []

    tags = Order.tags.all()

    return OrderTagSerializer(tags, many=True).data