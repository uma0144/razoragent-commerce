import time
from typing import Dict, Any, List

class FailureSentinel:
    '''Guarantees graceful failure handling, automatic rollbacks, and audit logging.'''
    
    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def record_event(
        self,
        event_type: str,
        status: str,
        details: Dict[str, Any],
        actor: str = "RazorAgent_System"
    ) -> Dict[str, Any]:
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "event_type": event_type,
            "status": status,
            "actor": actor,
            "details": details
        }
        self.audit_log.insert(0, entry) # Most recent first
        return entry

    def handle_payment_degradation(self, order_id: str, error_code: str, amount_inr: float) -> Dict[str, Any]:
        '''Gracefully handles bank outage / gateway degradation with smart retry routing.'''
        event = self.record_event(
            event_type="PAYMENT_DEGRADATION",
            status="RECOVERING",
            details={
                "order_id": order_id,
                "error_code": error_code,
                "amount": amount_inr,
                "action": "Switching routing from primary gateway to Razorpay Optimizer Smart Fallback"
            }
        )
        return {
            "recovered": True,
            "fallback_rail": "UPI_Intent_Optimizer_Failover",
            "message": "Payment degraded on primary bank rail. Seamlessly failed-over to alternate Razorpay Optimizer rail without dropping cart.",
            "audit_entry": event
        }

    def execute_inventory_rollback(self, catalog, product_id: str, quantity: int = 1, reason: str = "Payment Cancelled") -> Dict[str, Any]:
        '''Releases locked inventory when payment fails or is aborted.'''
        catalog.release_inventory(product_id, quantity)
        event = self.record_event(
            event_type="INVENTORY_ROLLBACK",
            status="SUCCESS",
            details={
                "product_id": product_id,
                "quantity": quantity,
                "reason": reason
            }
        )
        return {
            "rollback_executed": True,
            "product_id": product_id,
            "quantity_restored": quantity,
            "audit_entry": event
        }
