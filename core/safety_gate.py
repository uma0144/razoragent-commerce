import time
from typing import Dict, Any, List, Tuple

class BoundedSafetyGate:
    '''Enforces financial constraints: spending caps, velocity limits, 2FA triggers, and risk scoring.'''
    
    def __init__(
        self,
        max_single_tx: float = 5000.0,
        session_budget: float = 15000.0,
        velocity_limit_per_min: int = 3
    ):
        self.max_single_tx = max_single_tx
        self.session_budget = session_budget
        self.velocity_limit = velocity_limit_per_min
        self.spent_total = 0.0
        self.tx_history: List[Dict[str, Any]] = []

    def evaluate_transaction(
        self,
        amount_inr: float,
        merchant_id: str,
        item_name: str,
        agent_role: str = "Procurement_Agent_01"
    ) -> Dict[str, Any]:
        '''Evaluates if transaction satisfies bounded gating rules.'''
        current_time = time.time()
        
        # 1. Single Transaction Cap Check
        exceeds_single_cap = amount_inr > self.max_single_tx
        
        # 2. Cumulative Session Budget Check
        exceeds_budget = (self.spent_total + amount_inr) > self.session_budget
        
        # 3. Velocity Limit (Transactions in the last 60 seconds)
        recent_txs = [tx for tx in self.tx_history if (current_time - tx["timestamp"]) < 60]
        exceeds_velocity = len(recent_txs) >= self.velocity_limit
        
        # Risk Score Calculation (0 to 100)
        risk_score = 10
        risk_factors = []
        if exceeds_single_cap:
            risk_score += 45
            risk_factors.append(f"Amount ?{amount_inr:.2f} exceeds single tx cap ?{self.max_single_tx:.2f}")
        if exceeds_budget:
            risk_score += 50
            risk_factors.append(f"Projected spend ?{self.spent_total + amount_inr:.2f} exceeds budget ?{self.session_budget:.2f}")
        if exceeds_velocity:
            risk_score += 30
            risk_factors.append(f"Velocity spike: {len(recent_txs)+1} txs in under 60 seconds")
            
        risk_score = min(100, risk_score)
        
        # Decision Logic
        if exceeds_budget:
            status = "BLOCKED"
            reason = "Session budget exhausted. Money action prevented by Safety Gate."
            requires_2fa = True
        elif exceeds_single_cap:
            status = "NEEDS_APPROVAL"
            reason = "Single transaction limit exceeded. Human-in-the-loop 2FA approval required."
            requires_2fa = True
        elif exceeds_velocity:
            status = "RATE_LIMITED"
            reason = "Velocity threshold breached. Cooldown enforced."
            requires_2fa = True
        else:
            status = "APPROVED"
            reason = "Complies with all bounded financial policies and risk thresholds."
            requires_2fa = False
            
        return {
            "status": status,
            "approved": (status == "APPROVED"),
            "amount_inr": amount_inr,
            "risk_score": risk_score,
            "requires_2fa": requires_2fa,
            "reason": reason,
            "risk_factors": risk_factors,
            "explainability_breakdown": {
                "max_single_cap": self.max_single_tx,
                "current_spent": self.spent_total,
                "session_budget": self.session_budget,
                "remaining_budget": max(0.0, self.session_budget - self.spent_total),
                "recent_velocity_count": len(recent_txs)
            }
        }

    def record_settled_transaction(self, tx_id: str, amount_inr: float, description: str) -> None:
        self.spent_total += amount_inr
        self.tx_history.append({
            "tx_id": tx_id,
            "amount_inr": amount_inr,
            "description": description,
            "timestamp": time.time()
        })
