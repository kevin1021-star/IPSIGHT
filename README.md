# CIPHER-SENTINEL 🛡️
### AI-Powered IPsec VPN Protocol Analyzer & Security Assessment Framework

> **SIH26160** | National Technical Research Organisation (NTRO) | Ministry of Education's Innovation Cell  
> **Theme:** Blockchain & Cybersecurity

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CIPHER-SENTINEL PLATFORM                    │
├────────────────────┬────────────────────┬───────────────────────┤
│   React Frontend   │   FastAPI Backend  │    Neon PostgreSQL     │
│   (Vite + TS)      │   (Python 3.11)    │    (Assessments DB)    │
├────────────────────┼────────────────────┼───────────────────────┤
│   Dashboard        │   /api/assessments │    assessments         │
│   Upload PCAP/Cfg  │   /api/reports     │    findings            │
│   Risk Gauge       │   /api/dashboard   │    pq_results          │
│   Findings Table   │   /api/auth        │    esp_results         │
│   Remediation      │                   │    report_hashes        │
└────────────────────┴────────────────────┴───────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │        Supabase             │
              │  Auth + PCAP/Config Storage │
              └─────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │          CORE ENGINE (Python)          │
         ├────────────────┬──────────────────────┤
         │ IKE Dissector  │ ESP Analyzer (PECF)  │
         │ (IKEv1/v2)     │ Patent Claim 1       │
         ├────────────────┼──────────────────────┤
         │ Z3 SMT Verifier│ PQ Threat Engine     │
         │ (NIST/CNSA 2.0)│ (HNDL / QTEI)       │
         ├────────────────┴──────────────────────┤
         │     Remediation Synthesizer           │
         │  Cisco / StrongSwan / Fortinet        │
         └───────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- A [Neon](https://neon.tech) PostgreSQL database
- A [Supabase](https://supabase.com) project

### 1. Clone & Configure

```bash
git clone <repo>
cd vpn

# Backend environment
cp backend/.env.example backend/.env
# Fill in: DATABASE_URL, SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY, SECRET_KEY
```

### 2. Set up Supabase

1. Create a new Supabase project at https://supabase.com
2. Go to **Storage** → **New Bucket** → name it `cipher-sentinel-uploads` (set to private)
3. Go to **Authentication** → enable **Email** provider
4. Copy your **Project URL** and **anon key** and **service_role key** to `.env`

### 3. Set up Neon

1. Create a project at https://neon.tech
2. Copy the **Connection string** to `DATABASE_URL` in `.env`
3. Run migrations:

```bash
cd vpn
pip install alembic psycopg2-binary
alembic upgrade head
```

### 4. Backend

```bash
cd vpn
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 5. Frontend

```bash
cd vpn/frontend
cp .env.example .env.local
# Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY
npm install
npm run dev
```

Dashboard available at: http://localhost:5173

---

## Docker (Full Stack)

```bash
# Set env vars in backend/.env first
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Core Engine Usage (CLI)

```bash
# Analyze a PCAP file
python cipher_sentinel_cli.py sample.pcap

# Analyze with remediation export
python cipher_sentinel_cli.py sample.pcap --remediate

# Generate sample PCAP for testing
python demo_pcap_generator.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Authenticate |
| POST | `/api/auth/register` | Register new user |
| GET | `/api/auth/me` | Current user |
| POST | `/api/assessments/upload-pcap` | Upload & analyze PCAP |
| POST | `/api/assessments/upload-config` | Upload & analyze config |
| GET | `/api/assessments/` | List all assessments |
| GET | `/api/assessments/{id}` | Assessment detail + findings |
| POST | `/api/assessments/{id}/remediate` | Generate vendor patches |
| GET | `/api/reports/{id}/pdf` | Download PDF report |
| GET | `/api/reports/{id}/json` | Download JSON report |
| POST | `/api/reports/{id}/anchor` | Anchor report hash (blockchain MVP) |
| GET | `/api/dashboard/stats` | Dashboard statistics |
| GET | `/api/dashboard/trends` | Risk score trends (30 days) |

---

## Security Checks Performed

| Category | Check | Standard |
|----------|-------|----------|
| 🔴 Crypto | DES / 3DES / Blowfish | NIST SP 800-77r1 / CVE-2016-2183 |
| 🔴 Crypto | CBC without AEAD/EtM | BSI TR-02102-3 |
| 🔴 Key Exchange | DH Group 1/2/5 (768-1536 bit) | NIST SP 800-77r1 (Logjam) |
| 🟠 Key Exchange | MODP < 2048 bit | NIST SP 800-131A |
| 🔴 Hash | MD5 PRF / Integrity | NIST SP 800-77r1 |
| 🟠 Hash | SHA-1 | NIST SP 800-131A |
| 🔴 Protocol | IKEv1 Aggressive Mode | NTRO Defense Mandate |
| 🟡 PQC | No ML-KEM / Kyber hybrid | NSA CNSA 2.0 / RFC 9370 |
| 🔵 ESP | Cipher inference (no keys needed) | Patent Claim 1 (PECF) |

---

## Risk Scoring

```
Score 90-100  →  DEFENSE_GRADE   ✅
Score 70-89   →  ACCEPTABLE      🟡
Score 40-69   →  VULNERABLE      🟠
Score 0-39    →  COMPROMISED     🔴
```

**Penalty weights:** CRITICAL: -35 | HIGH: -15 | MEDIUM: -5 | LOW: -2

---

## Compliance Mappings

- NIST SP 800-77 Rev 1 (IPsec Guide)
- NIST SP 800-131A (Algorithm transitions)
- NSA CNSA 2.0 (Commercial National Security Algorithm Suite)
- BSI TR-02102-3 (German Federal Office for IT Security)
- RFC 8247 (IKEv2 Algorithm Implementation Requirements)
- RFC 9370 (Post-Quantum Hybrid KEM)
- ISO 27001 (Information Security Management)

---

## Supported Vendors (Remediation Output)

| Vendor | Remediation Config |
|--------|--------------------|
| StrongSwan | `swanctl.conf` (IKEv2 + PQC) |
| Cisco IOS-XE | `crypto ikev2` / `ipsec profile` |
| Fortinet FortiOS 7.x | Phase1/Phase2 interface config |
| Generic | Ansible hardening playbook |

---

## Blockchain Anchoring (MVP)

Each assessment report can be SHA-256 hashed and stored in the `report_hashes` table, providing a tamper-evident audit trail. Future versions will anchor to Hyperledger Fabric.

```bash
POST /api/reports/{id}/anchor
→ { "sha256_hash": "a3f9...", "anchored_at": "2026-09-29T..." }
```

---

## Project Structure

```
vpn/
├── core/                        # Core analysis engine (existing)
│   ├── dissector/
│   │   ├── ike_parser.py        # IKEv1/v2 binary dissector
│   │   └── esp_analyzer.py      # ESP side-channel analyzer (PECF)
│   ├── formal/
│   │   └── z3_verifier.py       # SMT compliance verifier
│   ├── ai/
│   │   └── pq_threat_engine.py  # Post-quantum QTEI calculator
│   └── remediation/
│       └── patch_generator.py   # Multi-vendor config synthesizer
├── backend/                     # FastAPI backend
│   ├── main.py
│   ├── database.py              # Neon async SQLAlchemy
│   ├── supabase_client.py       # Auth + file storage
│   ├── models.py                # ORM + Pydantic schemas
│   ├── routers/
│   │   ├── auth.py
│   │   ├── assessments.py
│   │   ├── reports.py
│   │   └── dashboard.py
│   ├── services/
│   │   ├── analyzer.py          # Core engine bridge
│   │   └── report_gen.py        # PDF generator
│   ├── alembic/                 # DB migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # React dashboard
│   ├── src/
│   │   ├── pages/               # Dashboard, Upload, Assessment, Reports, Login
│   │   ├── components/          # RiskGauge, FindingsTable, SeverityBadge, etc.
│   │   └── lib/                 # API client, auth context
│   ├── package.json
│   └── Dockerfile
├── pcap_samples/                # Test PCAP files
├── cipher_sentinel_cli.py       # CLI analyzer
├── demo_pcap_generator.py       # Test data generator
├── docker-compose.yml
└── alembic.ini
```

---

## License

For academic/competition use — SIH 2026. Contact NTRO/MIC for production licensing.
