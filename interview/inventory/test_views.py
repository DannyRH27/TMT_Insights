import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from rest_framework.test import APIClient
from datetime import datetime
from django.utils import timezone
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


def test_invalid_date():
    """Test when invalid date provided"""
    client = APIClient()
    
    response = client.get('/inventory/after-day/11-03-022/')
    assert response.status_code == 400


def test_valid_date():
    """Test when valid date provided"""
    client = APIClient()
    
    _type = InventoryType.objects.create(name="Test Type1")
    language = InventoryLanguage.objects.create(name="Test_Lang1")
    # Create test inventory
    Inventory.objects.create(
        name="Test Item",
        language=language,
        type=_type,
        metadata={},
        created_at=timezone.make_aware(datetime(2024, 2, 1, 12, 0, 0))
    )
    
    response = client.get('/inventory/after-day/2024-01-01/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_no_results():
    """Test when no items found"""
    client = APIClient()

    _type = InventoryType.objects.create(name="Test Type2")
    language = InventoryLanguage.objects.create(name="Test_Lang2")
    # Create test inventory
    inventory=Inventory.objects.create(
        name="Test Item",
        type=_type,
        language=language,
        metadata={},
        created_at=timezone.make_aware(datetime(2024, 2, 1, 12, 0, 0))
    )
    
    inventory.created_at = timezone.make_aware(datetime(2024, 2, 1, 12, 0, 0))
    inventory.save()

    response = client.get('/inventory/after-day/2024-03-01/')
    assert response.status_code == 200
    assert len(response.data) == 0


def test_date_before_all_items():
    """Test when date is before all inventory items"""
    client = APIClient()
    
    _type = InventoryType.objects.create(name="Test Type3")
    language = InventoryLanguage.objects.create(name="Test_Lang3")
    # Create test inventory
    inventory=Inventory.objects.create(
        name="Test Item",
        type=_type,
        language=language,
        metadata={},
    )
    inventory.created_at = timezone.make_aware(datetime(2024, 2, 1, 12, 0, 0))
    inventory.save()
    
    response = client.get('/inventory/after-day/2023-12-01/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_exact_date_match():
    """Test when date exactly matches an item's created date"""
    client = APIClient()
    
    _type = InventoryType.objects.create(name="Test Type4")
    language = InventoryLanguage.objects.create(name="Test_Lang4")
    # Create test inventory
    inventory = Inventory.objects.create(
        name="Test Item",
        type=_type,
        metadata={},
        language=language,
    )
    inventory.created_at = timezone.make_aware(datetime(2024, 2, 1, 12, 0, 0))
    inventory.save()

    
    response = client.get('/inventory/after-day/2024-02-01/')
    assert response.status_code == 200
    assert len(response.data) == 1


if __name__ == "__main__":
    Inventory.objects.all().delete()
    InventoryLanguage.objects.all().delete()
    InventoryType.objects.all().delete()
    # Run all tests
    test_invalid_date()
    Inventory.objects.all().delete()
    test_valid_date()
    Inventory.objects.all().delete()
    test_no_results()
    Inventory.objects.all().delete()
    test_date_before_all_items()
    Inventory.objects.all().delete()
    test_exact_date_match()
    Inventory.objects.all().delete()
    
    print("All tests passed!") 