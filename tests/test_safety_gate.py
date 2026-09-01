import pytest
from core.safety_gate import BoundedSafetyGate

def test_safety_gate_approval():
    gate = BoundedSafetyGate(max_single_tx=5000, session_budget=15000)
    res = gate.evaluate_transaction(2500, "merch_1", "Test Product")
    assert res["approved"] is True
    assert res["status"] == "APPROVED"
    assert res["requires_2fa"] is False

def test_safety_gate_single_tx_cap_breach():
    gate = BoundedSafetyGate(max_single_tx=5000, session_budget=15000)
    res = gate.evaluate_transaction(6000, "merch_1", "Luxury Server")
    assert res["approved"] is False
    assert res["status"] == "NEEDS_APPROVAL"
    assert res["requires_2fa"] is True

def test_safety_gate_session_budget_exhaustion():
    gate = BoundedSafetyGate(max_single_tx=5000, session_budget=10000)
    gate.record_settled_transaction("tx_1", 8000, "Initial batch")
    res = gate.evaluate_transaction(3000, "merch_1", "Additional compute")
    assert res["approved"] is False
    assert res["status"] == "BLOCKED"
