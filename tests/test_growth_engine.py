import pytest
from core.catalog_protocol import MachineReadableCatalog
from core.growth_engine import MerchantGrowthEngine

def test_dynamic_upsell_generation():
    cat = MachineReadableCatalog()
    growth = MerchantGrowthEngine(cat)
    cart = [{"id": "prod_dev_server", "bundle_options": ["prod_support_pass"], "price_inr": 2499.0}]
    
    upsell = growth.generate_dynamic_upsell(cart)
    assert upsell is not None
    assert upsell["discount_percent"] == 15
    assert upsell["recommended_product"]["id"] == "prod_support_pass"

def test_dropoff_recovery():
    cat = MachineReadableCatalog()
    growth = MerchantGrowthEngine(cat)
    cart = [{"id": "prod_dev_server", "price_inr": 2000.0, "quantity": 1}]
    recovery = growth.trigger_dropoff_recovery(cart, "Payment Timeout")
    assert recovery["savings_inr"] == 200.0
