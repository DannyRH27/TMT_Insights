from interview.order.serializers import OrderSerializer
from interview.order.models import OrderTag
from rest_framework.response import Response
from rest_framework.request import Request


def retrieve_orders_by_tag(tag:OrderTag) -> Response:
    # check if the tag exists first
    if not OrderTag.objects.filter(id=tag.id).exists():
        return Response(f"OrderTag with ID {Ordertag.id} does not exist.", status=404)

    orders = tag.orders.all()

    if not orders:
        return Response(f"Orders associated with OrderTag with ID {tag.id} does not exist.", status=404)

    return Response(OrderSerializer(orders, many=True).data, status=200)