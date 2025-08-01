import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from rest_framework.test import APIClient
from datetime import datetime
from django.utils import timezone
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


def test_deactivate_existing_order():
    """Test deactivating an existing active order"""
    client = APIClient()
    
    # Create test data
    inventory_type = InventoryType.objects.create(name="Test Type")
    inventory_language = InventoryLanguage.objects.create(name="Test Language")
    inventory = Inventory.objects.create(
        name="Test Item",
        type=inventory_type,
        language=inventory_language,
        metadata={}
    )
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=timezone.now().date(),
        embargo_date=timezone.now().date(),
        is_active=True
    )
    
    response = client.post(f'/orders/{order.id}/deactivate/')
    assert response.status_code == 201
    assert response.data['is_active'] == False
    
    # Verify order is deactivated in database
    order.refresh_from_db()
    assert order.is_active == False


def test_deactivate_already_inactive_order():
    """Test deactivating an order that's already inactive"""
    client = APIClient()
    
    # Create test data
    inventory_type = InventoryType.objects.create(name="Test Type")
    inventory_language = InventoryLanguage.objects.create(name="Test Language")
    inventory = Inventory.objects.create(
        name="Test Item",
        type=inventory_type,
        language=inventory_language,
        metadata={}
    )
    
    order = Order.objects.create(
        inventory=inventory,
        start_date=timezone.now().date(),
        embargo_date=timezone.now().date(),
        is_active=False
    )
    
    response = client.post(f'/orders/{order.id}/deactivate/')
    assert response.status_code == 201
    assert response.data['is_active'] == False


def test_deactivate_nonexistent_order():
    """Test deactivating a non-existent order"""
    client = APIClient()
    
    response = client.post('/orders/999/deactivate/')
    assert response.status_code == 404


def test_deactivate_order_with_invalid_id():
    """Test deactivating with invalid order ID"""
    client = APIClient()
    
    response = client.post('/orders/invalid/deactivate/')
    assert response.status_code == 404




if __name__ == "__main__":
    # Clean up before running tests
    Order.objects.all().delete()
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()
    
    # Run all tests
    test_deactivate_existing_order()
    Order.objects.all().delete()
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()
    
    test_deactivate_already_inactive_order()
    Order.objects.all().delete()
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()
    
    test_deactivate_nonexistent_order()
    Order.objects.all().delete()
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()

    test_deactivate_order_with_invalid_id()
    Order.objects.all().delete()
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()
    
    print("All tests passed!") 
