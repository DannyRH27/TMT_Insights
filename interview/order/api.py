### Challenge 3 Embargo Date:
# Write an endpoint that lists orders that are between a particular start and embargo date.

# params would be particular start date
# edge cases: 
# if start date is not provided, return no orders
# if start date is after embargo date, return no orders
# if invalid date, return no orders
# otherwise return all orders between start date and embargo date serialized as dictionary
# assume start date is a string in the format YYYY-MM-DD
# convert start date to date object and then compare to embargo date
# nvm found the OrderSerializer, so we can use that to serialize the orders
# also could use the date_validation_utils if we don't want to instantiate an OrderSerializer everytime, but since i am going to serialize orders anyways, i think it is okay.

from interview.order.models import Order
from interview.order.serializers import OrderSerializer
from datetime import datetime
from rest_framework.response import Response
from rest_framework.request import Request


def get_orders_by_start_date(request: Request) -> list[dict]:

    start_date = request.query_params.get('start_date')
    if start_date is None:
        return []

    # check if start date is a valid date
    # use util function so we don't have to instantiate an OrderSerializer unless we have orders
    if not is_valid_date(start_date):
        return Response(error="Start date is not valid.", status=400)
        
    
    # check if start date is in the future
    # actually, we don't need to check if it is in the future, because the start dates can be in the future, so as long as it is before embargo date it is okay.
    # if is_future_date(start_date):
    #     return []

    # happy case
    orders = Order.objects.filter(start_date__gte=start_date, embargo_date__gte=start_date)

    # No matching orders found
    if not orders.exists():
        return Response(error=f"No orders found before start date: {start_date}.", status=404)

    # do i need many?? Yeah, bc i return as list. worst case it's a list of 1
    serialized_orders = OrderSerializer(orders, many=True).data

    return Response(serialized_orders, status=200)




def is_valid_date(date_str, format = None):
    if format:
        valid = datetime.strptime(date_str, format)
    else:
        valid = datetime.strptime(date_str, '%Y-%m-%d')

    return valid
