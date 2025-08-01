from interview.order.models import Order
from interview.order.serializers import OrderTagSerializer

from rest_framework.response import Response
from rest_framework.request import Request

# if order doesn't exist, don't grab tags and don't instantiate serializer

def retrieve_tags_by_order(order: Order) -> Response:
    if not Order.objects.filter(id=order.id).exists():
        return Response(f"Order with Order ID {order.id} does not exist", status=404)

    tags = Order.tags.all()

    if not tags:
        return Response(f"No tags associated with Order ID {order.id}", status=404)

    return Response(OrderTagSerializer(tags, many=True).data, status=200)