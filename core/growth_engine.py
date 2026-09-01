from typing import Dict, Any, List, Optional
from core.catalog_protocol import MachineReadableCatalog

class MerchantGrowthEngine:
    '''Optimizes merchant basket size via dynamic bundle recommendations & abandonment recovery.'''
    
    def __init__(self, catalog: MachineReadableCatalog):
        self.catalog = catalog

    def generate_dynamic_upsell(self, cart_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        '''Recommends tailored cross-sell bundles based on current cart.'''
        if not cart_items:
            return None
            
        cart_ids = {item["id"] for item in cart_items}
        
        for item in cart_items:
            bundle_options = item.get("bundle_options", [])
            for rec_id in bundle_options:
                if rec_id not in cart_ids:
                    rec_product = self.catalog.get_product_by_id(rec_id)
                    if rec_product and rec_product["stock"] > 0:
                        discounted_price = round(rec_product["price_inr"] * 0.85, 2)
                        return {
                            "recommended_product": rec_product,
                            "original_price": rec_product["price_inr"],
                            "bundle_discount_price": discounted_price,
                            "discount_percent": 15,
                            "pitch": f"Bundle '{rec_product['name']}' with your order to save 15% immediately!"
                        }
        return None

    def trigger_dropoff_recovery(self, cart_items: List[Dict[str, Any]], dropoff_reason: str) -> Dict[str, Any]:
        '''Generates automated bounded win-back intervention for abandoned AI checkouts.'''
        total_value = sum(item["price_inr"] * item.get("quantity", 1) for item in cart_items)
        recovery_discount = 10.0 # 10% bounded coupon
        recovered_value = round(total_value * 0.90, 2)
        
        return {
            "recovery_strategy": "Autonomous Bounded Incentive",
            "trigger_event": dropoff_reason,
            "incentive_applied": f"{recovery_discount}% Dynamic Instant Discount",
            "original_total": total_value,
            "new_recovery_total": recovered_value,
            "savings_inr": round(total_value - recovered_value, 2),
            "recovery_message": "Agentic checkout stalled. Auto-applying 10% merchant coupon to close the transaction."
        }
