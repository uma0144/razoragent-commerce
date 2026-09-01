import time
import json
from typing import Dict, Any, List
from core.catalog_protocol import MachineReadableCatalog
from core.safety_gate import BoundedSafetyGate
from core.razorpay_client import RazorpayClient
from core.growth_engine import MerchantGrowthEngine
from core.failure_sentinel import FailureSentinel

class AutonomousBuyerAgent:
    '''Simulates an autonomous AI buyer executing end-to-end commerce transactions.'''
    
    def __init__(
        self,
        catalog: MachineReadableCatalog,
        safety_gate: BoundedSafetyGate,
        razorpay_client: RazorpayClient,
        growth_engine: MerchantGrowthEngine,
        failure_sentinel: FailureSentinel
    ):
        self.catalog = catalog
        self.safety_gate = safety_gate
        self.rzp = razorpay_client
        self.growth = growth_engine
        self.sentinel = failure_sentinel

    def run_agentic_purchase_flow(
        self,
        intent_query: str,
        user_budget: float,
        accept_upsell: bool = True
    ) -> Dict[str, Any]:
        '''Executes complete discovery -> evaluation -> safety gating -> order creation workflow.'''
        
        execution_trace = []
        
        # 1. Discover Products
        execution_trace.append({"step": "1. Catalog Discovery", "detail": f"AI Buyer queried AP2 protocol catalog for: '{intent_query}'"})
        matching_products = self.catalog.search(intent_query, max_price=user_budget)
        
        if not matching_products:
            self.sentinel.record_event("DISCOVERY_EMPTY", "NO_MATCH", {"query": intent_query, "budget": user_budget})
            return {
                "success": False,
                "stage": "Discovery",
                "error": "No products found matching autonomous buyer intent and budget constraints.",
                "trace": execution_trace
            }
            
        selected_product = matching_products[0]
        execution_trace.append({"step": "2. Product Selected", "detail": f"Selected '{selected_product['name']}' at ?{selected_product['price_inr']:.2f}"})
        
        cart = [{"id": selected_product["id"], "name": selected_product["name"], "price_inr": selected_product["price_inr"], "quantity": 1, "bundle_options": selected_product.get("bundle_options", [])}]
        
        # 2. Check Dynamic Upsell
        upsell_offer = self.growth.generate_dynamic_upsell(cart)
        if upsell_offer and accept_upsell:
            rec_p = upsell_offer["recommended_product"]
            cart.append({
                "id": rec_p["id"],
                "name": f"{rec_p['name']} (15% Bundle Discount)",
                "price_inr": upsell_offer["bundle_discount_price"],
                "quantity": 1
            })
            execution_trace.append({"step": "3. Upsell Bundle Accepted", "detail": f"Agent auto-accepted cross-sell bundle: {rec_p['name']} at ?{upsell_offer['bundle_discount_price']:.2f}"})
        
        total_amount = sum(item["price_inr"] * item.get("quantity", 1) for item in cart)
        
        # 3. Lock Inventory
        for item in cart:
            locked = self.catalog.lock_inventory(item["id"], item.get("quantity", 1))
            if not locked:
                # Graceful Rollback
                for rollback_item in cart:
                    self.sentinel.execute_inventory_rollback(self.catalog, rollback_item["id"], 1, "Stock Exhaustion")
                return {
                    "success": False,
                    "stage": "Inventory Lock",
                    "error": f"Insufficient stock for {item['name']}. Automatic inventory rollback executed gracefully.",
                    "trace": execution_trace
                }
                
        execution_trace.append({"step": "4. Inventory Locked", "detail": f"Stock reserved for {len(cart)} item(s) pending payment clearance"})
        
        # 4. Bounded Money Safety Gate Evaluation
        gate_result = self.safety_gate.evaluate_transaction(
            amount_inr=total_amount,
            merchant_id="merch_razorpay_ai_01",
            item_name=selected_product["name"]
        )
        
        execution_trace.append({
            "step": "5. Bounded Safety Gate",
            "detail": f"Status: {gate_result['status']} | Risk Score: {gate_result['risk_score']}/100 | {gate_result['reason']}"
        })
        
        if not gate_result["approved"]:
            # Rollback inventory
            for item in cart:
                self.sentinel.execute_inventory_rollback(self.catalog, item["id"], 1, "Safety Gate Block")
            self.sentinel.record_event("SAFETY_GATE_BLOCK", "BLOCKED", gate_result)
            return {
                "success": False,
                "stage": "Safety Gate",
                "gate_evaluation": gate_result,
                "error": gate_result["reason"],
                "trace": execution_trace
            }
            
        # 5. Create Razorpay Order & Payment Link
        receipt_id = f"rcpt_{int(time.time())}"
        order = self.rzp.create_order(total_amount, receipt_id, {"buyer_agent": "Autonomous_Procurement_Agent"})
        plink = self.rzp.create_payment_link(total_amount, f"Payment for {selected_product['name']}", "Autonomous AI Buyer")
        qr_code = self.rzp.generate_upi_qr_code(total_amount, order["order_id"])
        
        # Record settled tx
        self.safety_gate.record_settled_transaction(order["order_id"], total_amount, f"Purchase of {selected_product['name']}")
        self.sentinel.record_event("ORDER_SETTLED", "SUCCESS", {
            "order_id": order["order_id"],
            "amount_inr": total_amount,
            "items": [i["name"] for i in cart]
        })
        
        execution_trace.append({
            "step": "6. Razorpay Order & UPI Rail Created",
            "detail": f"Order ID: {order['order_id']} | Payment Link & Dynamic UPI QR Generated"
        })
        
        return {
            "success": True,
            "order": order,
            "payment_link": plink,
            "qr_code_image": qr_code,
            "cart": cart,
            "total_amount_inr": total_amount,
            "gate_evaluation": gate_result,
            "trace": execution_trace
        }
