# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                ▀█▀ █░█ █▀█ █▀▀ ▄▀█ ▀█▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █▀█ █▀█ █▀                 │
# │                ░█░ █▀█ █▀▄ ██▄ █▀█ ░█░    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █▄█ █▀▄ ▄█                 │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                                  █ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀ █▀                                  │
# │                                  █ █░▀░█ █▀▀ █▄█ █▀▄  █  ▄█                                  │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
from time import time

# ╔───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                                               │
# │ █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ █▄▄ █░░ █▀▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█    ▀█▀ █░█ █▀█ █▀▀ █▀ █░█ █▀█ █░░ █▀▄ █▀ │
# │ █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ █▄█ █▄▄ ██▄    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█    ░█░ █▀█ █▀▄ ██▄ ▄█ █▀█ █▄█ █▄▄ █▄▀ ▄█ │
# │                                                                                                                               │
# ╚───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╝

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │           █▀█ █▀█ █▀█ ▀█▀    █▀ █▀▀ ▄▀█ █▄░█    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█           │
# │           █▀▀ █▄█ █▀▄ ░█░    ▄█ █▄▄ █▀█ █░▀█    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█           │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
PORT_SCAN_THRESHOLD = 20  # Number of unique ports to trigger alert
PORT_SCAN_WINDOW = 10  # Time window in seconds

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │           █▀ ▀▄▀ █▄░█    █▀▀ █░░ █▀█ █▀█ █▀▄    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█           │
# │           ▄█ ░█░ █░▀█    █▀░ █▄▄ █▄█ █▄█ █▄▀    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█           │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
SYN_FLOOD_THRESHOLD = 100  # Number of SYN packets to trigger alert
SYN_FLOOD_WINDOW = 5  # Time window in seconds

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                     █▀▄ █▀▄ █▀█ █▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█                     │
# │                     █▄▀ █▄▀ █▄█ ▄█    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█                     │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
DDOS_THRESHOLD = 200  # Number of packets to single destination
DDOS_WINDOW = 10  # Time window in seconds

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │       █▄▄ █▀█ █░█ ▀█▀ █▀▀    █▀▀ █▀█ █▀█ █▀▀ █▀▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█       │
# │       █▄█ █▀▄ █▄█ ░█░ ██▄    █▀░ █▄█ █▀▄ █▄▄ ██▄    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█       │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
BRUTE_FORCE_THRESHOLD = 20  # Number of attempts to trigger alert
BRUTE_FORCE_WINDOW = 60  # Time window in seconds
BRUTE_FORCE_PORTS = {21, 22, 23, 25, 110, 143, 389, 445, 3306, 3389, 5432, 5900}

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │         █ █▀▀ █▀▄▀█ █▀█    █▀▀ █░░ █▀█ █▀█ █▀▄    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█         │
# │         █ █▄▄ █░▀░█ █▀▀    █▀░ █▄▄ █▄█ █▄█ █▄▀    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█         │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
ICMP_FLOOD_THRESHOLD = 100  # Number of ICMP packets to trigger alert
ICMP_FLOOD_WINDOW = 5  # Time window in seconds

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │  █▀▄ █▄░█ █▀    ▀█▀ █░█ █▄░█ █▄░█ █▀▀ █░░ █ █▄░█ █▀▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█   │
# │  █▄▀ █░▀█ ▄█    ░█░ █▄█ █░▀█ █░▀█ ██▄ █▄▄ █ █░▀█ █▄█    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█   │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
DNS_TUNNELING_QUERY_THRESHOLD = 100  # Number of DNS queries to trigger alert
DNS_TUNNELING_WINDOW = 60  # Time window in seconds
DNS_TUNNELING_LONG_QUERY_LENGTH = 50  # Character length considered "long"
DNS_TUNNELING_LONG_QUERY_RATIO = 0.6  # Ratio of long queries to trigger alert

# ╔───────────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                       │
# │ ▄▀█ █▄▄ █▄░█ █▀█ █▀█ █▀▄▀█ ▄▀█ █░░    ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀ █ █▀▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█ │
# │ █▀█ █▄█ █░▀█ █▄█ █▀▄ █░▀░█ █▀█ █▄▄    ░█░ █▀▄ █▀█ █▀░ █▀░ █ █▄▄    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█ │
# │                                                                                                       │
# ╚───────────────────────────────────────────────────────────────────────────────────────────────────────╝
ABNORMAL_TRAFFIC_THRESHOLD = 2000  # Number of packets from single source
ABNORMAL_TRAFFIC_WINDOW = 60  # Time window in seconds

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │ █ █▀█ / █▀▄▀█ ▄▀█ █▀▀    █▀ █▀█ █▀█ █▀█ █▀▀ █ █▄░█ █▀▀    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█ │
# │ █ █▀▀ / █░▀░█ █▀█ █▄▄    ▄█ █▀▀ █▄█ █▄█ █▀░ █ █░▀█ █▄█    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █▄█ █░▀█ │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝
SPOOFING_THRESHOLD = 3  # Number of different MACs/IPs before alerting
SPOOFING_WINDOW = 300  # Time window to track changes (5 minutes)


# ╔──────────────────────────────────────────────────────────────────────────────╗
# │                                                                              │
# │             █▀▀ █▀█ █▀▀ █▀█ ▀█▀ █ █▀█ █▀█    █▀ ▀█▀ █▀█ ▀█▀ █▀▀              │
# │             █▄▄ █▀▄ ██▄ █▀█  █  █ █ █ █▄█    ▄█  █  █▀█  █  ██▄              │
# │                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────╝
def create_state():
    return {
        "port_scans": {},
        "syn_floods": {},  # ip -> [time, ...]
        "ip_macs": {},  # ip -> {mac1, mac2, ...}
        "arp_table": {},  # ip -> mac
        "ddos": {},  # dst_ip -> [(time, src_ip), ...]
        "brute_force": {},  # (ip, port) -> [time, ...]
        "icmp_floods": {},  # ip -> [time, ...]
        "dns_queries": {},  # ip -> [(time, length), ...]
        "unusual_protos": {},  # protocol -> count
        "traffic": {},  # ip -> [time, ...]
        "mac_ips": {},  # mac -> {ip1, ip2, ...}
    }


# ╔──────────────────────────────────────────────────────────────────────────────╗
# │                                                                              │
# │          █▀▀ █   █▀▀ █▀█ █▀█ █ █▀█ █▀█    █▀▀ █▀█ ▀█▀ █▀█ █ █▀▀ █▀           │
# │          █▄▄ █▄▄ ██▄ █▀█ █ █ █ █ █ █▄█    ██▄ █ █  █  █▀▄ █ ██▄ ▄█           │
# │                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────╝
def clean_old_entries(entries, window):
    cutoff = time() - window
    return [e for e in entries if e[0] >= cutoff]


# ╔──────────────────────────────────────────────────────────────────────────────╗
# │                                                                              │
# │    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▀█ █▀█    █▀█ █▀█ █▀█ ▀█▀    █▀ █▀▀ █▀█ █▀█    │
# │    █▄▀ ██▄  █  ██▄ █▄▄  █  █ █ █ █▄█    █▀▀ █▄█ █▀▄  █     ▄█ █▄▄ █▀█ █ █    │
# │                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────╝
def detect_port_scan(state, src_ip, dst_port):
    now = time()
    if src_ip not in state["port_scans"]:
        state["port_scans"][src_ip] = []

    # Clean old entries
    state["port_scans"][src_ip] = clean_old_entries(
        state["port_scans"][src_ip], PORT_SCAN_WINDOW
    )
    state["port_scans"][src_ip].append((now, dst_port))

    # Check unique ports
    unique_ports = len(set(p for _, p in state["port_scans"][src_ip]))
    if unique_ports >= PORT_SCAN_THRESHOLD:
        return f"Port Scan: {src_ip} tried {unique_ports} ports in {PORT_SCAN_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │             █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █▀ ▀▄▀ █▄░█ ░ █▀▀ █░░ █▀█ █▀█ █▀▄               │
# │             █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ ▄█ ░█░ █░▀█ ░ █▀░ █▄▄ █▄█ █▄█ █▄▀               │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_syn_flood(state, src_ip):
    now = time()
    if src_ip not in state["syn_floods"]:
        state["syn_floods"][src_ip] = []

    state["syn_floods"][src_ip] = [
        t for t in state["syn_floods"][src_ip] if t >= now - SYN_FLOOD_WINDOW
    ]
    state["syn_floods"][src_ip].append(now)

    if len(state["syn_floods"][src_ip]) >= SYN_FLOOD_THRESHOLD:
        return f"SYN Flood: {src_ip} sent {len(state['syn_floods'][src_ip])} SYN packets in {SYN_FLOOD_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │           █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █ █▀█ ░ █▀ █▀█ █▀█ █▀█ █▀▀ █ █▄░█ █▀▀             │
# │           █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █ █▀▀ ░ ▄█ █▀▀ █▄█ █▄█ █▀░ █ █░▀█ █▄█             │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_ip_spoofing(state, src_ip, src_mac):
    # Skip private/DHCP ranges to reduce false positives
    if src_ip.startswith(("169.254.", "0.0.0.0", "255.255.255.255")):
        return None

    if src_ip not in state["ip_macs"]:
        state["ip_macs"][src_ip] = set()

    state["ip_macs"][src_ip].add(src_mac)

    if len(state["ip_macs"][src_ip]) >= SPOOFING_THRESHOLD:
        return f"IP Spoofing: {src_ip} seen with {len(state['ip_macs'][src_ip])} different MACs"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │        █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ ▄▀█ █▀█ █▀█ ░ █▀ █▀█ █▀█ █▀█ █▀▀ █ █▄░█ █▀▀          │
# │        █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▀█ █▀▄ █▀▀ ░ ▄█ █▀▀ █▄█ █▄█ █▀░ █ █░▀█ █▄█          │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_arp_spoofing(state, ip, mac):
    # Skip broadcast and multicast addresses
    if ip.startswith(("255.", "224.", "169.254.", "0.0.0.0")):
        return None

    if ip in state["arp_table"]:
        if state["arp_table"][ip] != mac:
            # Track changes instead of alerting immediately
            if "arp_changes" not in state:
                state["arp_changes"] = {}
            if ip not in state["arp_changes"]:
                state["arp_changes"][ip] = []

            now = time()
            state["arp_changes"][ip] = [
                t for t in state["arp_changes"][ip] if t >= now - SPOOFING_WINDOW
            ]
            state["arp_changes"][ip].append(now)

            # Only alert if multiple changes in short time
            if len(state["arp_changes"][ip]) >= 3:
                old_mac = state["arp_table"][ip]
                state["arp_table"][ip] = mac
                return f"ARP Spoofing: {ip} changed MAC {len(state['arp_changes'][ip])} times (now {mac})"

            state["arp_table"][ip] = mac
    else:
        state["arp_table"][ip] = mac

    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                      █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █▀▄ █▀▄ █▀█ █▀                         │
# │                      █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▄▀ █▄▀ █▄█ ▄█                         │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_ddos(state, src_ip, dst_ip):
    now = time()
    if dst_ip not in state["ddos"]:
        state["ddos"][dst_ip] = []

    state["ddos"][dst_ip] = clean_old_entries(state["ddos"][dst_ip], DDOS_WINDOW)
    state["ddos"][dst_ip].append((now, src_ip))

    if len(state["ddos"][dst_ip]) >= DDOS_THRESHOLD:
        sources = len(set(s for _, s in state["ddos"][dst_ip]))
        return f"DDoS: {dst_ip} received {len(state['ddos'][dst_ip])} packets from {sources} sources in {DDOS_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │█▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █▀▄▀█ ▄▀█ █░░ █ █▀▀ █ █▀█ █░█ █▀ ░ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ ▀█▀   │
# │█▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █░▀░█ █▀█ █▄▄ █ █▄▄ █ █▄█ █▄█ ▄█ ░ █▀▀ █▀█ █▄▄ █░█ ██▄ ░█░   │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_malicious_packet(src_ip, dst_ip):
    if src_ip == dst_ip:
        return f"Malicious: Land attack {src_ip} -> {dst_ip}"
    if src_ip.startswith("0.") or dst_ip.startswith("0."):
        return f"Malicious: Invalid IP {src_ip} -> {dst_ip}"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │         █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █▄▄ █▀█ █░█ ▀█▀ █▀▀ ░ █▀▀ █▀█ █▀█ █▀▀ █▀▀           │
# │         █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▄█ █▀▄ █▄█ ░█░ ██▄ ░ █▀░ █▄█ █▀▄ █▄▄ ██▄           │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_brute_force(state, src_ip, dst_port):
    if dst_port not in BRUTE_FORCE_PORTS:
        return None

    now = time()
    key = (src_ip, dst_port)
    if key not in state["brute_force"]:
        state["brute_force"][key] = []

    state["brute_force"][key] = [
        t for t in state["brute_force"][key] if t >= now - BRUTE_FORCE_WINDOW
    ]
    state["brute_force"][key].append(now)

    if len(state["brute_force"][key]) >= BRUTE_FORCE_THRESHOLD:
        return f"Brute Force: {src_ip} made {len(state['brute_force'][key])} attempts on port {dst_port} in {BRUTE_FORCE_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │           █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █ █▀▀ █▀▄▀█ █▀█ ░ █▀▀ █░░ █▀█ █▀█ █▀▄             │
# │           █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █ █▄▄ █░▀░█ █▀▀ ░ █▀░ █▄▄ █▄█ █▄█ █▄▀             │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_icmp_flood(state, src_ip):
    now = time()
    if src_ip not in state["icmp_floods"]:
        state["icmp_floods"][src_ip] = []

    state["icmp_floods"][src_ip] = [
        t for t in state["icmp_floods"][src_ip] if t >= now - ICMP_FLOOD_WINDOW
    ]
    state["icmp_floods"][src_ip].append(now)

    if len(state["icmp_floods"][src_ip]) >= ICMP_FLOOD_THRESHOLD:
        return f"ICMP Flood: {src_ip} sent {len(state['icmp_floods'][src_ip])} ICMP packets in {ICMP_FLOOD_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │    █▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █▄▀ █▄░█ █▀ ░ ▀█▀ █░█ █▄░█ █▄░█ █▀▀ █░░ █ █▄░█ █▀▀       │
# │    █▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▄▀ █░▀█ ▄█ ░ ░█░ █▄█ █░▀█ █░▀█ ██▄ █▄▄ █ █░▀█ █▄█       │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_dns_tunneling(state, src_ip, query_length=0):
    now = time()
    if src_ip not in state["dns_queries"]:
        state["dns_queries"][src_ip] = []

    state["dns_queries"][src_ip] = clean_old_entries(
        state["dns_queries"][src_ip], DNS_TUNNELING_WINDOW
    )
    state["dns_queries"][src_ip].append((now, query_length))

    queries = state["dns_queries"][src_ip]
    long_queries = sum(1 for _, l in queries if l > DNS_TUNNELING_LONG_QUERY_LENGTH)

    if len(queries) >= DNS_TUNNELING_QUERY_THRESHOLD or (
        len(queries) > 10
        and long_queries > len(queries) * DNS_TUNNELING_LONG_QUERY_RATIO
    ):
        return f"DNS Tunneling: {src_ip} made {len(queries)} queries ({long_queries} long) in {DNS_TUNNELING_WINDOW}s"
    return None


# ╔────────────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                        │
# │█▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ █░█ █▄░█ █░█ █▀ █░█ ▄▀█ █░░ ░ █▀█ █▀█ █▀█ ▀█▀ █▀█ █▀▀ █▀█ █░░      │
# │█▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▄█ █░▀█ █▄█ ▄█ █▄█ █▄█ █▀█ █▄▄ ░ █▀▀ █▀▄ █▄█ ░█░ █▄█ █▄█ █▄█ █▄▄  │
# │                                                                                                        │
# ╚────────────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_unusual_protocol(state, protocol, src_ip):
    # Common protocols: ICMP, TCP, UDP, ICMPv6, IGMP, ESP, AH, GRE
    common = {1, 2, 6, 17, 41, 47, 50, 51, 58, 89, 132}
    if protocol in common:
        return None

    # Only alert after seeing the same unusual protocol multiple times
    state["unusual_protos"][protocol] = state["unusual_protos"].get(protocol, 0) + 1

    if state["unusual_protos"][protocol] >= 10:
        return f"Unusual Protocol: {protocol} from {src_ip} (seen {state['unusual_protos'][protocol]} times)"
    return None


# ╔────────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                    │
# │█▀▄ █▀▀ ▀█▀ █▀▀ █▀▀ ▀█▀ █ █▄░█ █▀▀ ░ ▄▀█ █▄█ █▄░█ █▀█ █▀█ █▀▄▀█ ▄▀█ █░░ ░ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀ █ █▀▀ │
# │█▄▀ ██▄ ░█░ ██▄ █▄▄ ░█░ █ █░▀█ █▄█ ░ █▀█ █▄█ █░▀█ █▄█ █▀▄ █░▀░█ █▀█ █▄▄ ░ ░█░ █▀▄ █▀█ █▀░ █▀░ █ █▄▄ │
# │                                                                                                    │
# ╚────────────────────────────────────────────────────────────────────────────────────────────────────╝
def detect_abnormal_traffic(state, src_ip):
    now = time()
    if src_ip not in state["traffic"]:
        state["traffic"][src_ip] = []

    state["traffic"][src_ip] = [
        t for t in state["traffic"][src_ip] if t >= now - ABNORMAL_TRAFFIC_WINDOW
    ]
    state["traffic"][src_ip].append(now)

    if len(state["traffic"][src_ip]) >= ABNORMAL_TRAFFIC_THRESHOLD:
        return f"Abnormal Traffic: {src_ip} sent {len(state['traffic'][src_ip])} packets in {ABNORMAL_TRAFFIC_WINDOW}s"
    return None


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                  ▄▀█ █▄░█ ▄▀█ █░░ ▀▄▀ ▀█ █ █▄░█ █▀▀ ░ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ ▀█▀                    │
# │                  █▀█ █░▀█ █▀█ █▄▄ ░█░ █▄ █ █░▀█ █▄█ ░ █▀▀ █▀█ █▄▄ █░█ ██▄ ░█░                    │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def analyze_packet(
    state, ethernet=None, ipv4=None, ipv6=None, tcp=None, udp=None, icmp=None
):
    alerts = []

    src_ip = ipv4.src_ip if ipv4 else (ipv6.src_ip if ipv6 else None)
    dst_ip = ipv4.dst_ip if ipv4 else (ipv6.dst_ip if ipv6 else None)
    src_mac = ethernet.src_mac if ethernet else None
    protocol = ipv4.protocol if ipv4 else None

    # Run detectors
    if src_mac and src_ip:
        # COMMENTED OUT: MAC Spoofing detection disabled
        # alert = detect_mac_spoofing(state, src_mac, src_ip)
        # if alert:
        #     alerts.append(alert)

        alert = detect_ip_spoofing(state, src_ip, src_mac)
        if alert:
            alerts.append(alert)

    if src_ip and dst_ip:
        alert = detect_malicious_packet(src_ip, dst_ip)
        if alert:
            alerts.append(alert)

        alert = detect_ddos(state, src_ip, dst_ip)
        if alert:
            alerts.append(alert)

    if src_ip:
        alert = detect_abnormal_traffic(state, src_ip)
        if alert:
            alerts.append(alert)

    if protocol and src_ip:
        alert = detect_unusual_protocol(state, protocol, src_ip)
        if alert:
            alerts.append(alert)

    if tcp and src_ip:
        is_syn = tcp.ack_num == 0
        if is_syn:
            alert = detect_syn_flood(state, src_ip)
            if alert:
                alerts.append(alert)

        alert = detect_port_scan(state, src_ip, tcp.dst_port)
        if alert:
            alerts.append(alert)

        alert = detect_brute_force(state, src_ip, tcp.dst_port)
        if alert:
            alerts.append(alert)

    if udp and src_ip:
        if udp.dst_port == 53:
            alert = detect_dns_tunneling(state, src_ip)
            if alert:
                alerts.append(alert)

        alert = detect_port_scan(state, src_ip, udp.dst_port)
        if alert:
            alerts.append(alert)

    if icmp and src_ip:
        alert = detect_icmp_flood(state, src_ip)
        if alert:
            alerts.append(alert)

    return alerts
