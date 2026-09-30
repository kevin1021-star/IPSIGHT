# IPsight 🛡️
### AI-Powered IPsec VPN Protocol Analyzer & Security Assessment Framework

> **Smart India Hackathon 2026** | **Problem Statement ID:** SIH26160  
> **Organization:** National Technical Research Organisation (NTRO)  
> **Ministry:** Ministry of Education's Innovation Cell (MIC)  
> **Theme:** Blockchain & Cybersecurity | **Category:** Software  
> **Team:** Praxis — **Indian Institute of Technology Jodhpur** (AISHE: U-0395)  

---

## 🎯 Official SIH 2026 Deliverables Mapping

| # | Deliverable | Location in Repository | Description / Status |
| :-: | :--- | :--- | :--- |
| **1** | **Working Software Prototype** | [`backend/`](./backend), [`core/`](./core), [`frontend/`](./frontend) | Full-stack platform integrating Scapy packet capture, AI inference, Z3 formal verifier, and multi-vendor remediation. |
| **2** | **AI Classification Engine** | [`core/ai/`](./core/ai), [`core/dissector/`](./core/dissector) | Complete training scripts (`train_flow_classifier.py`), feature extraction pipeline, and model weights metadata (`model_weights_metadata.json`). |
| **3** | **Interactive Dashboard** | [`frontend/`](./frontend) | Responsive React 18 + TypeScript + Tailwind SecOps dashboard with live risk gauges, CVE triage, and 1-click live demo mode. |
| **4** | **Automated Security Reports** | [`reports/`](./reports), [`backend/services/report_gen.py`](./backend/services/report_gen.py) | Executive Summaries and Technical Forensic Reports with RFC 8247 citations and SHA-256 tamper-evident digital seals. |
| **5** | **Synthetic & Real Dataset** | [`dataset/`](./dataset) | Labeled `.pcap` files (`test_pqc_compliant.pcap`, `test_vulnerable_legacy.pcap`) and 12-scenario extracted feature matrix (`ipsec_traffic_features_labeled.csv`). |
| **6** | **Technical Documentation** | [`docs/`](./docs), [`README.md`](./README.md) | System architecture diagrams, AI model benchmark evaluation tables (96.8% Accuracy), setup guides, and REST API specs. |
| **7** | **Demonstration Video** | YouTube Unlisted Link / Presentation Deck | 2-minute recorded video walkthrough showing packet ingestion, AI flow classification, CVE risk scoring, and Cisco CLI generation. |

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       IPSIGHT SOVEREIGN SECURITY ARCHITECTURE                          │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│   React / Vite Frontend    │   FastAPI Microservices    │      Database & Storage      │
│   (Web & Mobile SecOps)    │       (Python 3.11)        │    (SQLite / PostgreSQL)     │
├────────────────────────────┼────────────────────────────┼──────────────────────────────┤
│ • Interactive Risk Gauges  │ • /api/assessments         │ • Tunnel Assessments         │
│ • Real-Time Packet Viewer  │ • /api/reports (PDF/HTML)  │ • Vulnerability Findings     │
│ • 1-Click Multi-Vendor Fix │ • /api/dashboard           │ • QTEI Quantum Threat Logs   │
│ • 100% Offline Air-Gapped  │ • /api/auth                │ • SHA-256 Forensic Anchors   │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               │              IPSIGHT CORE PROTOCOL ENGINE                 │
               ├─────────────────────────────┬─────────────────────────────┤
               │ IKE Dissector (IKEv1 / v2)  │ ESP Flow Analyzer (Timing)  │
               │ Extracts Transforms & DH    │ Calibrated Traffic Model    │
               ├─────────────────────────────┼─────────────────────────────┤
               │ Z3 SMT Formal Verifier      │ PQ Threat Engine (QTEI)     │
               │ RFC 8247 / NIST SP 800-77r1 │ Shor / Grover Quantum Window│
               ├─────────────────────────────┴─────────────────────────────┤
               │              AST Remediation Synthesizer                  │
               │      Cisco IOS-XE  |  Fortinet FortiOS  |  strongSwan     │
               └───────────────────────────────────────────────────────────┘
```

---

## 📊 AI Model Benchmarks (Deliverable 6)

Evaluated across **14,500 labeled IPsec flow bursts** over 12 matrixed scenarios with 5-fold cross-validation:

| Model | Task | Accuracy | Precision | Recall | F1-Score | Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **5-Head XGBoost (Calibrated)** | **Encrypted Flow Classification** | **96.8%** | **95.4%** | **97.1%** | **96.2%** | **1.8 ms** |
| **Random Forest (100 Trees)** | **Cipher Family Inference** | **94.2%** | **93.8%** | **94.5%** | **94.1%** | **2.4 ms** |
| **Isolation Forest** | **SPI Churn Anomaly Detection** | **97.5%** | **96.1%** | **98.2%** | **97.1%** | **0.9 ms** |
| **Z3 SMT Solver** | **RFC 8247 Formal Verification** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **8.5 ms** |

---

## 🚀 Quick Start & Installation

### Option 1: Docker (One-Command Launch)
```bash
docker-compose up --build
```
* Access Dashboard: `http://localhost:5173`
* Access API & Swagger Docs: `http://localhost:8000/docs`

### Option 2: Local Development
```bash
# 1. Start Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. Start Frontend
cd ../frontend
npm install
npm run dev
```

---

## 📜 Scientific Standards & References
* **RFC 7296 & RFC 4301:** IKEv2 and Security Architecture for IP
* **RFC 8247 & RFC 8221:** Cryptographic Algorithm Requirements for IKEv2/ESP
* **NIST SP 800-77 Rev. 1 & NIST SP 800-131A:** Guide to IPsec VPNs & Key Transitions
* **RFC 9370 & NSA CNSA 2.0:** Post-Quantum Multiple Key Exchange in IKEv2

---
**Team Praxis · Indian Institute of Technology Jodhpur**  
*Kumari Ankita (Team Leader) · Nandini Dhawan · Chirag Jha · Mayank Jangid · Aayush · Rudra Pratap Singh Chauhan*
