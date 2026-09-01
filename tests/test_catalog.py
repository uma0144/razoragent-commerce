import pytest
from core.catalog_protocol import MachineReadableCatalog

def test_catalog_search_and_filter():
    cat = MachineReadableCatalog()
    items = cat.search("GPU")
    assert len(items) >= 1
    assert "GPU" in items[0]["name"]

def test_inventory_lock_and_release():
    cat = MachineReadableCatalog()
    p = cat.get_product_by_id("prod_dev_server")
    initial_stock = p["stock"]
    
    assert cat.lock_inventory("prod_dev_server", 2) is True
    assert p["stock"] == initial_stock - 2
    
    cat.release_inventory("prod_dev_server", 2)
    assert p["stock"] == initial_stock
