
from datetime import datetime, date
from unittest.mock import Mock

from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory
from interview.order.api import retrieve_tags_by_order


def test_order_does_not_exist():
    # Create a mock order that doesn't exist in database
    mock_order = Mock()
    mock_order.id = 999
    
    result = retrieve_tags_by_order(mock_order)
    
    assert result.status == 404
    error = result.data.get("error", "")
    assert "Order with Order ID 999 does not exist" == error


def test_order_exists_with_tags():
    """Test when order exists and has tags"""
    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    
    tag1 = OrderTag.objects.create(name="Test Tag 1")
    tag2 = OrderTag.objects.create(name="Test Tag 2")
    order.tags.add(tag1, tag2)
    
    result = retrieve_tags_by_order(order)
    
    assert result.status == 200
    data = result.data.get("response", [])
    assert len(data) == 2
    assert data[0]['name'] == "Test Tag 1"
    assert data[1]['name'] == "Test Tag 2"


def test_order_exists_without_tags():
    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    
    result = retrieve_tags_by_order(order)
    
    assert result.status == 404
    error = result.data.get("error", "")
    assert f"No tags associated with Order ID {order.id}" == error


def test_order_with_one_tag():
    
    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    
    # Add one tag
    tag = OrderTag.objects.create(name="Single Tag")
    order.tags.add(tag)
    
    result = retrieve_tags_by_order(order)
    
    assert result.status == 200
    data = result.data.get("response", [])
    assert len(data) == 1
    assert data[0]['name'] == "Single Tag"


if __name__ == "__main__":
    # NOTE: HACKY TEARDOWN 
    # Delete Inventory which will cascade delete the Orders
    # Delete Tags as well because Tags are not cascade deleted.

    test_order_does_not_exist()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()

    test_order_exists_with_tags()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()

    test_order_exists_without_tags()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    
    test_order_with_one_tag()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    
    print("All tests passed!")