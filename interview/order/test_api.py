from datetime import datetime, date

from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory
from interview.order.api import get_orders_by_start_date, is_valid_date
from rest_framework.response import Response
from rest_framework.request import Request

def test_missing_start_date_parameter():
    request = Request()
    request.query_params = {}
    
    result = get_orders_by_start_date(request)
    
    assert result == []


def test_invalid_date_format():
    # Fresh setup
    Inventory.objects.all().delete()
    Order.objects.all().delete()
    
    request = Request()
    request.query_params = {'start_date': 'invalid-date'}
    
    result = get_orders_by_start_date(request)
    
    assert result.get('error') == 'Start date is not valid.'
    assert result.get('status') == 400


def test_valid_date_with_matching_orders():
    # Fresh setup
    Inventory.objects.all().delete()
    Order.objects.all().delete()

    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    
    request = Request()
    request.query_params = {'start_date': '2024-01-10'}
    
    result = get_orders_by_start_date(request)
    
    assert isinstance(result, dict)
    assert result.get('status') == 200
    data = result.get('data', [])
    assert len(data) == 1
    order_data = data[0]
    order_start_date = datetime.strptime(order_data['start_date'], '%Y-%m-%d').date()
    provided_start_date = datetime.strptime('2024-01-10', '%Y-%m-%d').date()
    assert order_start_date >= provided_start_date
    

def test_valid_date_with_no_matching_orders():
    # Fresh setup
    Inventory.objects.all().delete()
    Order.objects.all().delete()

    request = Request()
    request.query_params = {'start_date': '2024-03-01'}
    
    result = get_orders_by_start_date(request)

    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 3, 15),
        embargo_date=date(2024, 6, 15),
        is_active=True
    )
    
    assert isinstance(result, dict)
    assert result.get('error') == 'No orders found before start date: 2024-03-01.'
    assert result.get('status') == 404


def test_is_valid_date_function():
    result = is_valid_date('2024-01-15')
    assert isinstance(result, datetime)
    
    try:
        is_valid_date('invalid-date')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

if __name__ == "__main__":
    test_missing_start_date_parameter()
    test_invalid_date_format()
    test_valid_date_with_matching_orders()
    test_valid_date_with_no_matching_orders()
    test_is_valid_date_function()
    
    print("All tests passed!")