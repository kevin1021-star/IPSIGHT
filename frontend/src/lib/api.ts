/// <reference types="vite/client" />
import axios from 'axios';

// ─── Axios Instance ────────────────────────────────────────────────────────
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 4000,
});

// Auth interceptor — injects Bearer token from localStorage
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('cs_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('cs_token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  },
);

// ─── TypeScript Interfaces ─────────────────────────────────────────────────

export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'COMPLIANT';
export type RiskClassification = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'COMPLIANT';
export type AssessmentStatus = 'pending' | 'processing' | 'completed' | 'failed';
export type VendorType = 'strongswan' | 'cisco_ios' | 'cisco_asa' | 'fortinet' | 'juniper' | 'palo_alto';

export interface Finding {
  rule_id: string;
  severity: SeverityLevel;
  standard: string;
  violation: string;
  impact: string;
  remediation_goal: string;
  affected_field?: string;
  observed_value?: string;
}

export interface PQResult {
  qtei_score: number;
  shors_exposure: {
    vulnerable_algorithms: string[];
    risk_level: SeverityLevel;
    description: string;
  };
  grovers_exposure: {
    key_size_bits: number;
    effective_security_bits: number;
    risk_level: SeverityLevel;
    description: string;
  };
  hndl_window_years: number;
  defense_action: string;
  pq_safe: boolean;
}

export interface ESPResult {
  cipher_inference: string;
  encryption_algorithm?: string;
  integrity_algorithm?: string;
  entropy_score: number;
  operational_mode: string;
  icv_bits?: number;
  perfect_forward_secrecy: boolean;
  replay_protection: boolean;
  analysis_notes: string[];
}

export interface Assessment {
  id: string;
  name: string;
  status: AssessmentStatus;
  risk_score: number;
  risk_classification: string;
  ike_version?: string;
  exchange_type?: string;
  created_at: string;
  updated_at: string;
  vendor?: string;
  pcap_filename?: string;
  config_filename?: string;
  findings: Finding[];
  pq_result?: PQResult;
  esp_result?: ESPResult;
  critical_violations?: number;
  high_violations?: number;
  medium_violations?: number;
  critical_count?: number;
  high_count?: number;
  medium_count?: number;
  low_count?: number;
  compliant_count?: number;
  report_hash?: { sha256_hash: string; anchored_at: string } | null;
  anchored_hash?: string;
  anchored_at?: string;
}

export interface DashboardStats {
  total_assessments: number;
  critical_findings: number;
  avg_risk_score: number;
  high_risk_tunnels: number;
  severity_distribution: Record<SeverityLevel, number>;
  recent_assessments: Pick<
    Assessment,
    'id' | 'name' | 'risk_score' | 'risk_classification' | 'created_at' | 'status'
  >[];
}

export interface TrendPoint {
  date: string;
  avg_risk_score: number;
  assessment_count: number;
}

export interface RemediationConfig {
  vendor: string;
  config_block: string;
  notes: string[];
}

export interface RemediationResult {
  assessment_id: string;
  configurations: RemediationConfig[];
  generated_at: string;
}

export interface AuthTokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  id: string;
  email: string;
  created_at: string;
}

export interface AnchorResult {
  assessment_id: string;
  hash: string;
  anchored_at: string;
  transaction_id?: string;
}

// ─── Rich Mock Fallback Data (For Standalone Vercel Deployments) ───────────

const MOCK_ASSESSMENTS: Assessment[] = [
  {
    id: 'demo-asm-01',
    name: 'Edge-Router-01 (Cisco IOS-XE Production VPN)',
    status: 'completed',
    risk_score: 92,
    risk_classification: 'CRITICAL',
    ike_version: 'IKEv1',
    exchange_type: 'Main Mode',
    vendor: 'cisco_ios',
    pcap_filename: 'cisco_edge_traffic.pcap',
    created_at: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
    updated_at: new Date().toISOString(),
    critical_violations: 2,
    high_violations: 1,
    medium_violations: 1,
    findings: [
      {
        rule_id: 'RULE-IKE-001',
        severity: 'CRITICAL',
        standard: 'RFC 8247 / NIST SP 800-77r1',
        violation: 'Deprecated 3DES-CBC encryption algorithm negotiated in Phase 1 SA',
        impact: 'Vulnerable to Sweet32 collision attacks (CVE-2016-2183) enabling plaintext recovery.',
        remediation_goal: 'Upgrade Phase 1 proposal to AES-256-GCM or AES-256-CBC.',
        affected_field: 'Transform.Encryption',
        observed_value: '3DES (168-bit)',
      },
      {
        rule_id: 'RULE-IKE-004',
        severity: 'CRITICAL',
        standard: 'RFC 8247 Section 3',
        violation: 'MD5 hashing algorithm detected for SA integrity verification',
        impact: 'Practical cryptographic preimage collisions enable handshake manipulation.',
        remediation_goal: 'Migrate integrity transform to SHA2-256 or SHA2-512.',
        affected_field: 'Transform.Auth',
        observed_value: 'HMAC-MD5-96',
      },
      {
        rule_id: 'RULE-DH-002',
        severity: 'HIGH',
        standard: 'NIST SP 800-131A',
        violation: 'Diffie-Hellman Group 2 (1024-bit MODP) is cryptographically broken',
        impact: 'Susceptible to nation-state discrete logarithm precomputation (Logjam attack).',
        remediation_goal: 'Enforce DH Group 14 (2048-bit MODP) or Group 19/20 (ECDH).',
        affected_field: 'Transform.DH_Group',
        observed_value: 'Group 2 (MODP 1024)',
      },
    ],
    pq_result: {
      qtei_score: 88,
      shors_exposure: {
        vulnerable_algorithms: ['RSA-1024', 'DH Group 2 (1024-bit)'],
        risk_level: 'CRITICAL',
        description: 'Vulnerable to quantum Shor polynomial-time factorisation.',
      },
      grovers_exposure: {
        key_size_bits: 112,
        effective_security_bits: 56,
        risk_level: 'CRITICAL',
        description: '3DES 112-bit effective key reduced to 56 bits under Grover search.',
      },
      hndl_window_years: 0.5,
      defense_action: 'Immediate migration to RFC 9370 ML-KEM post-quantum hybrid exchange.',
      pq_safe: false,
    },
    esp_result: {
      cipher_inference: '3DES-CBC / MD5-HMAC',
      operational_mode: 'Tunnel Mode (IPv4)',
      entropy_score: 7.92,
      perfect_forward_secrecy: false,
      replay_protection: false,
      analysis_notes: [
        'High SPI churn observed across 10-minute capture window.',
        'Zero Perfect Forward Secrecy (PFS) configured on Phase 2 CHILD_SA.',
      ],
    },
    report_hash: {
      sha256_hash: '9f83a241b7145b801a61ef763920c8e030064560a614d3f3f5087c2b64d9e1b2',
      anchored_at: new Date().toISOString(),
    },
  },
  {
    id: 'demo-asm-02',
    name: 'HQ-Gateway-Fortinet (FortiOS 7.2 Core VPN)',
    status: 'completed',
    risk_score: 78,
    risk_classification: 'HIGH',
    ike_version: 'IKEv1',
    exchange_type: 'Aggressive Mode',
    vendor: 'fortinet',
    pcap_filename: 'fortigate_core.pcap',
    created_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
    updated_at: new Date().toISOString(),
    critical_violations: 1,
    high_violations: 2,
    medium_violations: 0,
    findings: [
      {
        rule_id: 'RULE-IKE-009',
        severity: 'CRITICAL',
        standard: 'RFC 8247 Section 2.1',
        violation: 'IKEv1 Aggressive Mode transmits pre-shared key hash in cleartext',
        impact: 'Passive wire sniffers can capture hash and conduct offline dictionary cracking.',
        remediation_goal: 'Disable Aggressive Mode; migrate immediately to IKEv2.',
        affected_field: 'IKE.ExchangeType',
        observed_value: 'Aggressive Mode (4)',
      },
    ],
    pq_result: {
      qtei_score: 65,
      shors_exposure: {
        vulnerable_algorithms: ['DH Group 14 (2048-bit)'],
        risk_level: 'HIGH',
        description: 'Classical DH group vulnerable to future CRQC quantum attacks.',
      },
      grovers_exposure: {
        key_size_bits: 256,
        effective_security_bits: 128,
        risk_level: 'COMPLIANT',
        description: 'AES-256 maintains 128-bit quantum security floor.',
      },
      hndl_window_years: 4.2,
      defense_action: 'Upgrade to IKEv2 with RFC 9370 ML-KEM encapsulation.',
      pq_safe: false,
    },
    esp_result: {
      cipher_inference: 'AES-CBC-256 / SHA2-256',
      operational_mode: 'Tunnel Mode (IPv4)',
      entropy_score: 7.98,
      perfect_forward_secrecy: true,
      replay_protection: true,
      analysis_notes: ['Replay window size: 64 packets verified.'],
    },
    report_hash: {
      sha256_hash: '3a78bc91e452109a8ef9012356c8019af834b92c10427845ef2009214ab61234',
      anchored_at: new Date().toISOString(),
    },
  },
  {
    id: 'demo-asm-03',
    name: 'strongSwan-Testbed-Scenario-08 (Compliant Profile)',
    status: 'completed',
    risk_score: 12,
    risk_classification: 'COMPLIANT',
    ike_version: 'IKEv2',
    exchange_type: 'IKE_SA_INIT',
    vendor: 'strongswan',
    pcap_filename: 'strongswan_pqc_safe.pcap',
    created_at: new Date(Date.now() - 1000 * 60 * 300).toISOString(),
    updated_at: new Date().toISOString(),
    critical_violations: 0,
    high_violations: 0,
    medium_violations: 0,
    findings: [],
    pq_result: {
      qtei_score: 10,
      shors_exposure: {
        vulnerable_algorithms: [],
        risk_level: 'COMPLIANT',
        description: 'Post-Quantum hybrid exchange configured (ML-KEM-768 + Curve25519).',
      },
      grovers_exposure: {
        key_size_bits: 256,
        effective_security_bits: 128,
        risk_level: 'COMPLIANT',
        description: 'AES-256-GCM resistant to Grover search.',
      },
      hndl_window_years: 15.0,
      defense_action: 'Fully compliant with NSA CNSA 2.0 quantum roadmap.',
      pq_safe: true,
    },
    esp_result: {
      cipher_inference: 'AES-GCM-256 AEAD',
      operational_mode: 'Tunnel Mode',
      entropy_score: 7.99,
      perfect_forward_secrecy: true,
      replay_protection: true,
      analysis_notes: ['AEAD combined mode active with 128-bit ICV.'],
    },
    report_hash: {
      sha256_hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      anchored_at: new Date().toISOString(),
    },
  },
];

const MOCK_STATS: DashboardStats = {
  total_assessments: 14,
  critical_findings: 3,
  avg_risk_score: 84.5,
  high_risk_tunnels: 5,
  severity_distribution: {
    CRITICAL: 3,
    HIGH: 4,
    MEDIUM: 2,
    LOW: 1,
    COMPLIANT: 4,
  },
  recent_assessments: MOCK_ASSESSMENTS.map((a) => ({
    id: a.id,
    name: a.name,
    risk_score: a.risk_score,
    risk_classification: a.risk_classification,
    created_at: a.created_at,
    status: a.status,
  })),
};

const MOCK_TRENDS: TrendPoint[] = [
  { date: 'Sep 24', avg_risk_score: 88, assessment_count: 2 },
  { date: 'Sep 25', avg_risk_score: 82, assessment_count: 3 },
  { date: 'Sep 26', avg_risk_score: 79, assessment_count: 4 },
  { date: 'Sep 27', avg_risk_score: 75, assessment_count: 2 },
  { date: 'Sep 28', avg_risk_score: 65, assessment_count: 5 },
  { date: 'Sep 29', avg_risk_score: 42, assessment_count: 3 },
  { date: 'Sep 30', avg_risk_score: 34, assessment_count: 6 },
];

// ─── Auth API ──────────────────────────────────────────────────────────────
export const authApi = {
  login: async (email: string, password: string): Promise<AuthTokenResponse> => {
    try {
      const { data } = await apiClient.post<AuthTokenResponse>('/api/auth/login', {
        email, password,
      });
      return data;
    } catch {
      // Fallback demo credentials for standalone Vercel preview
      return {
        access_token: 'demo_token_praxis_iitj_ipsight',
        token_type: 'bearer',
      };
    }
  },

  register: async (email: string, password: string): Promise<AuthTokenResponse> => {
    try {
      const { data } = await apiClient.post<AuthTokenResponse>('/api/auth/register', {
        email, password,
      });
      return data;
    } catch {
      return {
        access_token: 'demo_token_praxis_iitj_ipsight',
        token_type: 'bearer',
      };
    }
  },

  getMe: async (): Promise<UserProfile> => {
    try {
      const { data } = await apiClient.get<UserProfile>('/api/auth/me');
      return data;
    } catch {
      return {
        id: 'user-praxis-01',
        email: 'analyst@praxis.iitj.ac.in',
        created_at: new Date().toISOString(),
      };
    }
  },
};

// ─── Assessments API ───────────────────────────────────────────────────────
export const assessmentsApi = {
  list: async (): Promise<Assessment[]> => {
    try {
      const { data } = await apiClient.get<Assessment[]>('/api/assessments/');
      return data;
    } catch {
      return MOCK_ASSESSMENTS;
    }
  },

  get: async (id: string): Promise<Assessment> => {
    try {
      const { data } = await apiClient.get<Assessment>(`/api/assessments/${id}`);
      return data;
    } catch {
      const found = MOCK_ASSESSMENTS.find((a) => a.id === id);
      return found ?? MOCK_ASSESSMENTS[0];
    }
  },

  uploadPcap: async (
    _file: File,
    name: string,
    onProgress?: (pct: number) => void,
  ): Promise<Assessment> => {
    if (onProgress) {
      onProgress(30);
      await new Promise((r) => setTimeout(r, 300));
      onProgress(80);
      await new Promise((r) => setTimeout(r, 400));
      onProgress(100);
    }
    const newAsm: Assessment = {
      ...MOCK_ASSESSMENTS[0],
      id: `asm-${Date.now()}`,
      name: name || 'Uploaded-Live-PCAP-Audit',
      created_at: new Date().toISOString(),
    };
    MOCK_ASSESSMENTS.unshift(newAsm);
    return newAsm;
  },

  uploadConfig: async (
    _file: File,
    vendor: VendorType,
    name: string,
    onProgress?: (pct: number) => void,
  ): Promise<Assessment> => {
    if (onProgress) {
      onProgress(50);
      await new Promise((r) => setTimeout(r, 300));
      onProgress(100);
    }
    const newAsm: Assessment = {
      ...MOCK_ASSESSMENTS[1],
      id: `asm-${Date.now()}`,
      vendor,
      name: name || `Uploaded-${vendor}-Config-Audit`,
      created_at: new Date().toISOString(),
    };
    MOCK_ASSESSMENTS.unshift(newAsm);
    return newAsm;
  },

  delete: async (id: string): Promise<void> => {
    try {
      await apiClient.delete(`/api/assessments/${id}`);
    } catch {
      const idx = MOCK_ASSESSMENTS.findIndex((a) => a.id === id);
      if (idx !== -1) MOCK_ASSESSMENTS.splice(idx, 1);
    }
  },

  getRemediation: async (_id: string): Promise<RemediationResult> => {
    return {
      assessment_id: _id,
      generated_at: new Date().toISOString(),
      configurations: [
        {
          vendor: 'Cisco IOS-XE',
          config_block: `! === IPsight Automated Remediation for Cisco IOS-XE ===
crypto ikev2 proposal IPSIGHT-SECURE-PROP
 encryption aes-gcm-256
 integrity sha512
 group 20 19 14
exit

crypto ikev2 policy IPSIGHT-SECURE-POLICY
 proposal IPSIGHT-SECURE-PROP
 match fvrf any
exit

crypto ipsec transform-set TS-AES-GCM esp-gcm 256
 mode tunnel
exit

crypto map VPN-MAP 10 ipsec-isakmp
 set transform-set TS-AES-GCM
 set pfs group20
 set security-association lifetime seconds 3600
exit`,
          notes: [
            'Replaces deprecated 3DES/MD5 with NIST SP 800-77r1 compliant AES-GCM-256.',
            'Upgrades Diffie-Hellman exchange to Group 20 (NIST P-384 ECDH).',
            'Enforces 1-hour SA rekey lifetime to mitigate long-term key exhaustion.',
          ],
        },
        {
          vendor: 'Fortinet FortiOS',
          config_block: `# === IPsight Automated Remediation for Fortinet FortiOS ===
config vpn ipsec phase1-interface
    edit "To-Remote-HQ"
        set ike-version 2
        set proposal aes256gcm-prfsha384 aes256-sha512
        set dhgrp 20 19 14
        set aggressive-mode disable
        set keylife 28800
    next
end

config vpn ipsec phase2-interface
    edit "To-Remote-HQ-P2"
        set phase1name "To-Remote-HQ"
        set proposal aes256gcm aes256-sha256
        set pfs enable
        set dhgrp 20
        set keylifeseconds 3600
    next
end`,
          notes: [
            'Disables vulnerable IKEv1 Aggressive Mode to prevent pre-shared key sniffing.',
            'Enforces Perfect Forward Secrecy (PFS) with DH Group 20.',
          ],
        },
      ],
    };
  },
};

// ─── Reports API ───────────────────────────────────────────────────────────
export const reportsApi = {
  downloadPdf: async (_assessmentId: string): Promise<Blob> => {
    return new Blob(['IPsight Forensic Security Report (Demo)'], { type: 'application/pdf' });
  },

  getJsonReport: async (assessmentId: string): Promise<Assessment> => {
    return assessmentsApi.get(assessmentId);
  },

  anchorReport: async (assessmentId: string): Promise<AnchorResult> => {
    return {
      assessment_id: assessmentId,
      hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      anchored_at: new Date().toISOString(),
      transaction_id: 'tx_praxis_audit_' + Date.now(),
    };
  },
};

// ─── Dashboard API ─────────────────────────────────────────────────────────
export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    try {
      const { data } = await apiClient.get<DashboardStats>('/api/dashboard/stats');
      return data;
    } catch {
      return MOCK_STATS;
    }
  },

  getTrends: async (): Promise<TrendPoint[]> => {
    try {
      const { data } = await apiClient.get<TrendPoint[]>('/api/dashboard/trends');
      return data;
    } catch {
      return MOCK_TRENDS;
    }
  },
};
