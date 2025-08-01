import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from datetime import date
from unittest.mock import Mock

from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory
from interview.order.api import retrieve_orders_by_tag


def test_tag_does_not_exist():
    """Test when tag doesn't exist in database"""
    mock_tag = Mock()
    mock_tag.id = 999  # Non-existent ID
    
    result = retrieve_orders_by_tag(mock_tag)
    
    assert result.status == 404
    assert result.data.get("error", "") == "OrderTag with ID 999 does not exist."


def test_tag_exists_with_orders():
    # Create test data
    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    tag = OrderTag.objects.create(name="Test Tag")
    
    order1 = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    order1.tags.add(tag)
    
    order2 = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 20),
        embargo_date=date(2024, 2, 20),
        is_active=True
    )
    order2.tags.add(tag)
    
    result = retrieve_orders_by_tag(tag)
    
    assert result.status == 200
    data = result.data.get("response", {})
    assert len(data) == 2
    assert data[0]['id'] == order1.id
    assert data[1]['id'] == order2.id


def test_tag_exists_without_orders():
    tag = OrderTag.objects.create(name="Empty Tag")
    
    result = retrieve_orders_by_tag(tag)
    
    assert result.status == 404
    assert result.data.get("error", "") == f"Orders associated with OrderTag with ID {tag.id} does not exist."


def test_tag_with_one_order():
    inventory = Inventory.objects.create(
        name="Test Movie",
        description="Test description"
    )
    
    tag = OrderTag.objects.create(name="Single Order Tag")
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=date(2024, 1, 15),
        embargo_date=date(2024, 2, 15),
        is_active=True
    )
    order.tags.add(tag)
    
    result = retrieve_orders_by_tag(tag)
    
    assert result.status == 200
    data = result.data.get("response", [])
    assert len(data) == 1
    assert data[0]['id'] == order.id


if __name__ == "__main__":
    # NOTE: HACKY Teardown
    # Delete Inventory and OrderTag since OrderTags do not cascade
    
    # Run all tests
    test_tag_does_not_exist()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    test_tag_exists_with_orders()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    test_tag_exists_without_orders()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    test_tag_with_one_order()
    Inventory.objects.all().delete()
    OrderTag.objects.all().delete()
    
    print("All tests passed!") 