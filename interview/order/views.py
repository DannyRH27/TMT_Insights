from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:

        _id = kwargs["id"]
        status = kwargs["status"]
        order = self.get_queryset(_id)
        if not order:
            return Response({"error": f"No Order found with ID {order}."}, status=404)

        data = {'is_active': True if status == 'activate' else False}
        serializer = self.serializer_class(instance=order, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get_queryset(self, id):
        return self.queryset.all().filter(id=id)
