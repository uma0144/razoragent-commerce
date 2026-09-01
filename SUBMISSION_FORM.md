# ?? Razorpay AI Builder Internship 2026 ? Google Form Submission Answers

Copy and paste these exact, polished responses into your **Razorpay Google Form**:

---

### **1. Selected Track \***
**Track 1: AI Growth & Agentic Commerce**

---

### **2. Project Name / Title \***
`RazorAgent Commerce ? Autonomous Agent-to-Agent Commerce & Dynamic Merchant Checkout Engine on Razorpay Rails`

---

### **3. Project Objectives (What does it solve?) \***
```text
With NPCI's Universal Agentic Protocol (UAP) and global agentic standards (AP2/x402), commerce is shifting from human-driven websites to Autonomous AI Buyer Agents. However, merchants currently lack machine-readable catalogs, dynamic negotiation protocols, and bounded financial safeguards to transact safely with AI bots.

RazorAgent Commerce solves this by:
1. Exposing machine-readable dynamic product catalogs (AP2/JSON-LD protocol) for autonomous AI discovery.
2. Integrating a Merchant Growth Engine that autonomously offers dynamic bundle cross-sells and recovers abandoned checkouts.
3. Enforcing 'The Razorpay Bar': every money action is bounded by spending caps, session budgets, velocity checks, and explainable risk scores.
4. Implementing resilient failure recovery: automated inventory rollbacks and gateway degradation failover via Razorpay Optimizer.
5. Generating instant Razorpay Orders, short payment links, and dynamic UPI QR codes for end-to-end settlement.
```

---

### **4. Architecture & Technical Implementation \***
```text
? Architecture Layers:
1. Machine-Readable Catalog Protocol (AP2/UAP): Standardized JSON-LD catalog schema enabling autonomous AI agents to query specifications, stock, and volume discounts.
2. Bounded Money Safety Gate: Financial guardrails enforcing single-transaction caps (max ?5,000), cumulative session budgets (max ?15,000), velocity rate limits (max 3 tx/min), and 2FA risk scoring (0-100).
3. Razorpay Payment Rails Client: Direct integration with Razorpay Orders API, Payment Links API, and dynamic UPI QR code generator with smart sandbox fallback.
4. Merchant Growth & Upsell Engine: AI-driven basket optimization triggering 15% bundle discounts and automated checkout drop-off recovery sequences.
5. Failure & Rollback Sentinel: Atomic inventory locking with automatic rollback on payment aborts and seamless failover to alternate payment rails on gateway degradation.
6. Real-Time Immutable Audit Trail: Chronological logging of every financial thought, protocol message, and risk assessment.

? Tech Stack: Python 3.11+, Streamlit, Razorpay SDK, Google Gemini / OpenAI APIs, Plotly, Pytest.
```

---

### **5. GitHub Repository Link \***
`https://github.com/uma0144/razoragent-commerce`

---

### **6. Live / Demo Link of the Working MVP \***
`https://github.com/uma0144/razoragent-commerce` *(or your Streamlit Community Cloud live link)*
*(Includes an interactive Zero-Config Demo Mode with pre-configured AI buyer intents, dynamic UPI QR generation, failure simulations, and real-time audit logs).*

---

### **7. 5-Minute Video Pitch Script / Talking Points \***
```text
[0:00-0:45] Intro & Problem: The rise of Agentic Commerce (UAP/AP2) and why merchants must become transactable by AI buyer agents while keeping money actions bounded.
[0:45-2:00] Live Demo: Trigger autonomous buyer agent purchase -> AI searches AP2 catalog -> Growth engine negotiates 15% GPU bundle discount -> Safety Gate verifies budget caps -> Live Razorpay Order & UPI QR generated.
[2:00-3:15] The Razorpay Bar (Failure & Rollbacks): Demonstrate budget limit breach prevention, gateway degradation failover, and automatic inventory rollback.
[3:15-4:15] Technical Deep-Dive: Explain the BoundedSafetyGate, Razorpay Orders API client, and real-time immutable audit trail.
[4:15-5:00] Conclusion: How RazorAgent Commerce empowers Razorpay merchants to monetize the $100B+ agentic economy safely.
```
