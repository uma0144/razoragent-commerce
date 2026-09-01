import json
from typing import Dict, Any, List, Optional

class MachineReadableCatalog:
    '''Implements AP2 / UAP agentic commerce catalog schema readable by AI buyer agents.'''
    
    DEFAULT_PRODUCTS = [
        {
            "id": "prod_dev_server",
            "name": "Cloud GPU Inference Cluster (100 GPU-Hours)",
            "category": "Cloud & AI Compute",
            "price_inr": 2499.0,
            "stock": 15,
            "sku": "GPU-INF-100",
            "specifications": {
                "gpus": "NVIDIA H100 SXM5",
                "memory": "80GB HBM3 per node",
                "network": "3.2 Tbps InfiniBand"
            },
            "bundle_options": ["prod_support_pass", "prod_storage_tier"]
        },
        {
            "id": "prod_support_pass",
            "name": "24/7 Priority SLA Engineer Support Pass",
            "category": "Enterprise Support",
            "price_inr": 899.0,
            "stock": 50,
            "sku": "SUPP-PRIO-247",
            "specifications": {
                "sla": "< 15 minutes",
                "channel": "Dedicated Slack & PagerDuty",
                "validity": "30 Days"
            },
            "bundle_options": []
        },
        {
            "id": "prod_storage_tier",
            "name": "Encrypted Vector DB Storage (500GB SSD)",
            "category": "Database & Storage",
            "price_inr": 1299.0,
            "stock": 25,
            "sku": "VEC-STORE-500",
            "specifications": {
                "type": "NVMe PCIe Gen5",
                "encryption": "AES-256 at rest",
                "iops": "1,000,000"
            },
            "bundle_options": ["prod_dev_server"]
        },
        {
            "id": "prod_api_bundle",
            "name": "AI Agent Orchestration API Tier (1M Credits)",
            "category": "API Gateway",
            "price_inr": 1799.0,
            "stock": 100,
            "sku": "API-AGT-1M",
            "specifications": {
                "rate_limit": "5,000 req/min",
                "redundancy": "Multi-region fallback"
            },
            "bundle_options": ["prod_support_pass"]
        }
    ]

    def __init__(self, products: Optional[List[Dict[str, Any]]] = None):
        self.products = products or [dict(p) for p in self.DEFAULT_PRODUCTS]

    def get_protocol_schema(self) -> Dict[str, Any]:
        '''Returns schema compliant with Agentic Commerce Protocol (AP2/UAP).'''
        return {
            "@context": "https://schema.org/AgenticCommerce",
            "@type": "MerchantCatalogProtocol",
            "merchant_id": "merch_razorpay_ai_01",
            "currency": "INR",
            "version": "2.0-UAP",
            "supported_payment_rails": ["Razorpay_UPI", "Razorpay_Cards", "Razorpay_NetBanking", "UPI_Autopay"],
            "catalog": self.products
        }

    def search(self, query: str, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
        '''AI Buyer query filter.'''
        query_lower = query.lower()
        results = []
        for p in self.products:
            if max_price and p["price_inr"] > max_price:
                continue
            if (query_lower in p["name"].lower() or 
                query_lower in p["category"].lower() or 
                query_lower in p["sku"].lower()):
                results.append(p)
        return results

    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

    def lock_inventory(self, product_id: str, quantity: int = 1) -> bool:
        p = self.get_product_by_id(product_id)
        if p and p["stock"] >= quantity:
            p["stock"] -= quantity
            return True
        return False

    def release_inventory(self, product_id: str, quantity: int = 1) -> None:
        p = self.get_product_by_id(product_id)
        if p:
            p["stock"] += quantity
