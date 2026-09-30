"""
CIPHER-SENTINEL: Standalone Pure-Python PCAP Generator
Synthesizes standard Libpcap binary files containing:
1. Vulnerable Legacy IKEv1/3DES/MD5/DH2 Handshake + ESP
2. Modern but Quantum-Vulnerable IKEv2/AES-128-CBC/DH14 Handshake
3. Defense-Grade Post-Quantum Hybrid (ML-KEM + AES-256-GCM)
4. Pure Opaque ESP Stream (for Patent Claim 1 testing)
"""

import struct
import os
import random
import time

def make_pcap_global_header() -> bytes:
    # magic 0xa1b2c3d4, version 2.4, thiszone 0, sigfigs 0, snaplen 65535, network 1 (Ethernet)
    return struct.pack("!IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)

def make_pcap_packet_header(pkt_len: int, ts_sec: int, ts_usec: int) -> bytes:
    return struct.pack("!IIII", ts_sec, ts_usec, pkt_len, pkt_len)

def make_ethernet_ip_udp(src_ip: str, dst_ip: str, src_port: int, dst_port: int, payload: bytes) -> bytes:
    # 14-byte Ethernet Header (IPv4 = 0x0800)
    eth_hdr = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\x08\x00'
    
    # 20-byte IPv4 Header (UDP = 17)
    src_bytes = bytes(map(int, src_ip.split('.')))
    dst_bytes = bytes(map(int, dst_ip.split('.')))
    ip_tot_len = 20 + 8 + len(payload)
    ip_hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_tot_len, 54321, 0, 64, 17, 0, src_bytes, dst_bytes)
    
    # 8-byte UDP Header
    udp_len = 8 + len(payload)
    udp_hdr = struct.pack("!HHHH", src_port, dst_port, udp_len, 0)
    
    return eth_hdr + ip_hdr + udp_hdr + payload

def make_ethernet_ip_esp(src_ip: str, dst_ip: str, spi: int, seq: int, esp_payload: bytes) -> bytes:
    eth_hdr = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\x08\x00'
    src_bytes = bytes(map(int, src_ip.split('.')))
    dst_bytes = bytes(map(int, dst_ip.split('.')))
    
    # ESP Protocol = 50
    esp_hdr = struct.pack("!II", spi, seq)
    full_esp = esp_hdr + esp_payload
    ip_tot_len = 20 + len(full_esp)
    ip_hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_tot_len, 12345, 0, 64, 50, 0, src_bytes, dst_bytes)
    return eth_hdr + ip_hdr + full_esp

def build_ikev2_init_packet(transforms: list) -> bytes:
    """Builds an RFC 7296 compliant IKE_SA_INIT packet binary."""
    initiator_spi = b"\x1a\x2b\x3c\x4d\x5e\x6f\x7a\x8b"
    responder_spi = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    next_payload = 33 # SA Payload
    version = (2 << 4) | 0
    exchange_type = 34 # IKE_SA_INIT
    flags = 0x08 # Initiator
    msg_id = 0
    
    # Build Proposal
    # Proposal header: next(0), res(0), prop_len, prop_num(1), proto(1=IKE), spi_sz(0), num_transforms
    transforms_bin = b""
    for i, t in enumerate(transforms):
        t_next = 3 if i < len(transforms) - 1 else 0
        t_type = t["type"] # 1:Enc, 2:PRF, 3:Integ, 4:DH
        t_id = t["id"]
        key_len = t.get("key_len")
        if key_len:
            # Transform with Key Length Attribute (type 14)
            t_attr = struct.pack("!HH", 0x800e, key_len)
            t_len = 8 + len(t_attr)
            transforms_bin += struct.pack("!BBHBBH", t_next, 0, t_len, t_type, 0, t_id) + t_attr
        else:
            transforms_bin += struct.pack("!BBHBBH", t_next, 0, 8, t_type, 0, t_id)
            
    prop_len = 8 + len(transforms_bin)
    prop_bin = struct.pack("!BBHBBBB", 0, 0, prop_len, 1, 1, 0, len(transforms)) + transforms_bin
    
    # SA Payload header: next(0), res(0), sa_len
    sa_len = 4 + len(prop_bin)
    sa_bin = struct.pack("!BBH", 0, 0, sa_len) + prop_bin
    
    tot_len = 28 + len(sa_bin)
    ike_hdr = struct.pack("!8s8sBBBBII", initiator_spi, responder_spi, next_payload, version, exchange_type, flags, msg_id, tot_len)
    return ike_hdr + sa_bin

def generate_sample_pcaps(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Vulnerable Legacy PCAP (3DES + MD5 + DH2)
    vuln_path = os.path.join(output_dir, "test_vulnerable_legacy.pcap")
    with open(vuln_path, "wb") as f:
        f.write(make_pcap_global_header())
        ts = int(time.time())
        
        # IKE Packet
        vuln_transforms = [
            {"type": 1, "id": 5}, # 3DES-CBC
            {"type": 2, "id": 1}, # HMAC-MD5
            {"type": 3, "id": 1}, # HMAC-MD5-96
            {"type": 4, "id": 2}, # DH Group 2 (MODP-1024)
        ]
        ike_pkt = make_ethernet_ip_udp("192.168.10.1", "192.168.20.1", 500, 500, build_ikev2_init_packet(vuln_transforms))
        f.write(make_pcap_packet_header(len(ike_pkt), ts, 100))
        f.write(ike_pkt)
        
        # Accompanying ESP packets (8-byte block aligned, 3DES padded)
        for i in range(1, 20):
            # 8-byte block alignment + 12-byte MD5 ICV
            raw_inner = random.randbytes(64 + (i % 5) * 8)
            esp_pkt = make_ethernet_ip_esp("192.168.10.1", "192.168.20.1", 0x00A1B2C3, i, raw_inner)
            f.write(make_pcap_packet_header(len(esp_pkt), ts, 200 + i * 10))
            f.write(esp_pkt)
            
    # 2. Modern Post-Quantum Compliant PCAP (ML-KEM + AES-256-GCM + SHA384)
    pqc_path = os.path.join(output_dir, "test_pqc_compliant.pcap")
    with open(pqc_path, "wb") as f:
        f.write(make_pcap_global_header())
        ts = int(time.time())
        pqc_transforms = [
            {"type": 1, "id": 20, "key_len": 256}, # AES-GCM-256
            {"type": 2, "id": 6},                   # HMAC-SHA384
            {"type": 3, "id": 13},                  # HMAC-SHA384-192
            {"type": 4, "id": 1024},                # ML-KEM-768 / Hybrid
        ]
        ike_pkt = make_ethernet_ip_udp("10.0.0.1", "10.0.0.2", 500, 500, build_ikev2_init_packet(pqc_transforms))
        f.write(make_pcap_packet_header(len(ike_pkt), ts, 100))
        f.write(ike_pkt)
        
        # ESP packets (AEAD stream continuous lengths, high entropy)
        for i in range(1, 25):
            raw_inner = random.randbytes(100 + (i * 13) % 400)
            esp_pkt = make_ethernet_ip_esp("10.0.0.1", "10.0.0.2", 0x00F9E8D7, i, raw_inner)
            f.write(make_pcap_packet_header(len(esp_pkt), ts, 200 + i * 10))
            f.write(esp_pkt)

    print(f"Generated sample PCAPs successfully in: {output_dir}")

if __name__ == "__main__":
    generate_sample_pcaps(os.path.join(os.getcwd(), "pcap_samples"))
