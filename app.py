import os
import time
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from core.config import Config
from core.catalog_protocol import MachineReadableCatalog
from core.safety_gate import BoundedSafetyGate
from core.razorpay_client import RazorpayClient
from core.growth_engine import MerchantGrowthEngine
from core.failure_sentinel import FailureSentinel
from core.agent_buyer import AutonomousBuyerAgent

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RazorAgent Commerce ? Autonomous AI Merchant Engine",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Fintech Dark Glassmorphic Theme)
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .agent-step {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #38bdf8;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "catalog" not in st.session_state:
    st.session_state.catalog = MachineReadableCatalog()
if "sentinel" not in st.session_state:
    st.session_state.sentinel = FailureSentinel()
if "safety_gate" not in st.session_state:
    st.session_state.safety_gate = BoundedSafetyGate(
        max_single_tx=Config.DEFAULT_MAX_TX_LIMIT,
        session_budget=Config.DEFAULT_SESSION_BUDGET
    )
if "growth_engine" not in st.session_state:
    st.session_state.growth_engine = MerchantGrowthEngine(st.session_state.catalog)
if "simulation_result" not in st.session_state:
    st.session_state.simulation_result = None

# Sidebar Controls
with st.sidebar:
    st.markdown("## ??? Bounded Money Controls")
    st.caption("The Razorpay Bar: Every money action is bounded, explainable, and gated.")
    
    max_tx_slider = st.slider(
        "Max Single Transaction Cap (?)",
        min_value=1000.0,
        max_value=10000.0,
        value=5000.0,
        step=500.0
    )
    st.session_state.safety_gate.max_single_tx = max_tx_slider
    
    session_budget_slider = st.slider(
        "Cumulative Session Budget (?)",
        min_value=5000.0,
        max_value=30000.0,
        value=15000.0,
        step=1000.0
    )
    st.session_state.safety_gate.session_budget = session_budget_slider
    
    st.markdown("---")
    st.markdown("## ?? Razorpay Test Mode API")
    rzp_key = st.text_input("Razorpay Key ID", value=Config.RAZORPAY_KEY_ID, placeholder="rzp_test_...", type="password")
    rzp_secret = st.text_input("Razorpay Key Secret", value=Config.RAZORPAY_KEY_SECRET, placeholder="Key Secret", type="password")
    
    rzp_client = RazorpayClient(key_id=rzp_key, key_secret=rzp_secret)
    if rzp_client.is_live_configured:
        st.success("?? Connected to Live Razorpay Test API")
    else:
        st.info("?? Running in **Smart Sandbox Mode** (Simulated Rails & UPI QR)")

    st.markdown("---")
    st.markdown("## ?? Session Financials")
    spent = st.session_state.safety_gate.spent_total
    rem = max(0.0, st.session_state.safety_gate.session_budget - spent)
    st.metric("Total Settled Spend", f"?{spent:,.2f}")
    st.metric("Remaining Budget", f"?{rem:,.2f}")

# Main Header
st.markdown('<div class="main-title">?? RazorAgent Commerce</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Autonomous Agent-to-Agent Commerce & Dynamic Merchant Checkout Engine on Razorpay Rails</div>', unsafe_allow_html=True)

# Tabs
tab_sim, tab_checkout, tab_growth, tab_failure, tab_audit, tab_catalog = st.tabs([
    "?? Autonomous AI Buyer Simulator",
    "?? Razorpay Checkout & Dynamic QR",
    "?? Merchant Growth & Upsell Engine",
    "? Graceful Failure & Rollback",
    "?? Immutable Audit Trail",
    "?? Machine-Readable Catalog (AP2)"
])

# 1. Autonomous AI Buyer Simulator Tab
with tab_sim:
    st.markdown("### ?? Autonomous Agent-to-Agent Purchase Scenario")
    st.write("Configure an autonomous procurement intent and trigger the AI buyer agent to negotiate, verify safety gating, and checkout.")
    
    s_col1, s_col2 = st.columns([2, 1])
    
    with s_col1:
        buyer_intent = st.selectbox(
            "AI Buyer Agent Intent",
            options=[
                "Deploy Cloud GPU Cluster for LLM Training (Target: GPU Cluster)",
                "Procure Enterprise 24/7 Priority SLA Support Pass",
                "Expand Vector DB Storage Tier for RAG Embeddings",
                "Acquire 1M Agent Orchestration API Credits Tier"
            ]
        )
        
        intent_query_map = {
            "Deploy Cloud GPU Cluster for LLM Training (Target: GPU Cluster)": "GPU",
            "Procure Enterprise 24/7 Priority SLA Support Pass": "Support",
            "Expand Vector DB Storage Tier for RAG Embeddings": "Storage",
            "Acquire 1M Agent Orchestration API Credits Tier": "API"
        }
        
    with s_col2:
        allow_upsell = st.checkbox("Allow Autonomous Cross-sell Negotiation", value=True)
        agent_budget = st.number_input("Buyer Agent Allocation (?)", min_value=1000.0, max_value=25000.0, value=8000.0, step=500.0)

    launch_btn = st.button("?? Trigger Autonomous Agent Transaction", type="primary", use_container_width=True)

    if launch_btn:
        buyer_agent = AutonomousBuyerAgent(
            catalog=st.session_state.catalog,
            safety_gate=st.session_state.safety_gate,
            razorpay_client=rzp_client,
            growth_engine=st.session_state.growth_engine,
            failure_sentinel=st.session_state.sentinel
        )
        
        with st.spinner("Autonomous AI Buyer executing protocol discovery & bounded checkout..."):
            time.sleep(0.4)
            res = buyer_agent.run_agentic_purchase_flow(
                intent_query=intent_query_map[buyer_intent],
                user_budget=agent_budget,
                accept_upsell=allow_upsell
            )
            st.session_state.simulation_result = res

    if st.session_state.simulation_result:
        res = st.session_state.simulation_result
        st.markdown("---")
        
        if res["success"]:
            st.success(f"? Autonomous Commerce Transaction Succeeded! Total: **?{res['total_amount_inr']:,.2f}**")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Razorpay Order ID", res["order"]["order_id"])
            with c2:
                st.metric("Total Amount", f"?{res['total_amount_inr']:,.2f}")
            with c3:
                st.metric("Items in Cart", len(res["cart"]))
            with c4:
                st.metric("Gate Risk Score", f"{res['gate_evaluation']['risk_score']} / 100")

            trace_col, qr_col = st.columns([2, 1])
            with trace_col:
                st.markdown("#### ?? Agentic Execution Trace")
                for step in res["trace"]:
                    st.markdown(f'<div class="agent-step"><b>{step["step"]}</b><br/>{step["detail"]}</div>', unsafe_allow_html=True)
                    
            with qr_col:
                st.markdown("#### ?? Dynamic UPI QR (NPCI UAP)")
                st.image(res["qr_code_image"], caption="Scan & Pay via any UPI App", width=220)
                st.markdown(f"[?? Open Razorpay Payment Link]({res['payment_link']['short_url']})")
        else:
            st.error(f"? Transaction Stopped by Sentinel at {res['stage']} Stage: {res['error']}")
            st.markdown("#### ?? Execution Trace")
            for step in res["trace"]:
                st.markdown(f'<div class="agent-step"><b>{step["step"]}</b><br/>{step["detail"]}</div>', unsafe_allow_html=True)

# 2. Razorpay Checkout & Dynamic QR Tab
with tab_checkout:
    st.markdown("### ?? Razorpay Payment Rails & Smart Checkout")
    st.write("Generate dynamic Razorpay orders and inspect real-time transaction payloads.")
    
    co_col1, co_col2 = st.columns(2)
    with co_col1:
        custom_amt = st.number_input("Custom Payment Amount (?)", min_value=100.0, max_value=20000.0, value=2499.0, step=100.0)
        custom_desc = st.text_input("Order Description", value="AI Agent Server Allocation")
        if st.button("Generate Razorpay Order & QR"):
            order_info = rzp_client.create_order(custom_amt, f"rcpt_{int(time.time())}")
            plink_info = rzp_client.create_payment_link(custom_amt, custom_desc)
            qr_data = rzp_client.generate_upi_qr_code(custom_amt, order_info["order_id"])
            
            st.session_state.last_order = {
                "order": order_info,
                "plink": plink_info,
                "qr": qr_data,
                "amount": custom_amt
            }
            st.session_state.sentinel.record_event("MANUAL_ORDER_CREATED", "SUCCESS", order_info)
            
    with co_col2:
        if "last_order" in st.session_state:
            lo = st.session_state.last_order
            st.markdown("#### Generated Payment Assets")
            st.markdown(f"**Order ID:** `{lo['order']['order_id']}`")
            st.markdown(f"**Payment Link:** [{lo['plink']['short_url']}]({lo['plink']['short_url']})")
            st.image(lo["qr"], caption=f"Dynamic UPI QR for ?{lo['amount']:.2f}", width=200)

# 3. Merchant Growth & Upsell Engine Tab
with tab_growth:
    st.markdown("### ?? Revenue Growth & Dynamic Upsell Analytics")
    st.write("Demonstrates autonomous merchant basket optimization and checkout abandonment recovery.")
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### ?? Active Bundle Strategy")
        st.info("?? **GPU Cluster + 24/7 SLA Support:** 15% Bundle Discount automatically applied when AI buyer agent detects SLA dependencies.")
        st.info("?? **Vector DB + GPU Compute:** 10% Bundle Discount for high-throughput RAG workloads.")
        
    with g_col2:
        st.markdown("#### ?? Abandonment Recovery Engine")
        st.write("Simulate checkout drop-off and trigger autonomous bounded win-back intervention.")
        if st.button("Trigger Drop-off Recovery Sequence"):
            sample_cart = [{"id": "prod_dev_server", "price_inr": 2499.0, "quantity": 1}]
            recovery_data = st.session_state.growth_engine.trigger_dropoff_recovery(sample_cart, "User paused at payment screen")
            st.json(recovery_data)
            st.session_state.sentinel.record_event("RECOVERY_DISCOUNT_APPLIED", "SUCCESS", recovery_data)

# 4. Graceful Failure & Rollback Tab
with tab_failure:
    st.markdown("### ? The Razorpay Bar: Graceful Failure & Inventory Rollback")
    st.write("Demonstrates how RazorAgent handles payment degradation, budget breaches, and stock exhaustion gracefully without orphan locks.")
    
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("#### Simulate Payment Degradation")
        if st.button("Simulate Bank Gateway Outage"):
            rec_res = st.session_state.sentinel.handle_payment_degradation("order_deg_101", "GATEWAY_TIMEOUT", 2499.0)
            st.warning(f"?? {rec_res['message']}")
            st.json(rec_res["audit_entry"])
            
    with f2:
        st.markdown("#### Simulate Stock Lock Rollback")
        if st.button("Simulate Order Abort & Inventory Rollback"):
            rb_res = st.session_state.sentinel.execute_inventory_rollback(st.session_state.catalog, "prod_dev_server", 1, "Simulated Buyer Cancel")
            st.success("? Inventory Rollback Succeeded! Stock cleanly restored.")
            st.json(rb_res["audit_entry"])

# 5. Immutable Audit Trail Tab
with tab_audit:
    st.markdown("### ?? Real-time Immutable Audit Trail")
    st.write("Chronological audit logs of every protocol query, safety evaluation, money settlement, and error rollback.")
    
    logs = st.session_state.sentinel.audit_log
    if logs:
        st.dataframe(logs, use_container_width=True)
    else:
        st.info("No audit events recorded yet. Trigger a transaction to populate.")

# 6. Machine-Readable Catalog Tab
with tab_catalog:
    st.markdown("### ?? Machine-Readable Catalog (AP2 / UAP Schema)")
    st.write("Machine-readable JSON schema exposed to AI buyer agents for autonomous discovery and negotiation.")
    st.json(st.session_state.catalog.get_protocol_schema())
