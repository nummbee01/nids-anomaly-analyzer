# Argus NIDS - Technical Reference

This technical reference explains the Argus Network Intrusion Detection System for users with basic Python knowledge or those new to network security concepts.

---

## Table of Contents

1. [What is Argus NIDS?](#what-is-argus-nids)
2. [How Does It Work?](#how-does-it-work)
3. [Project Structure](#project-structure)
4. [Understanding Network Basics](#understanding-network-basics)
5. [Data Structures Explained](#data-structures-explained)
6. [Packet Parsing - Breaking Down Network Data](#packet-parsing)
7. [Threat Detection](#threat-detection)
8. [Packet Capture - Listening to the Network](#packet-capture)
9. [The GUI - User Interface](#the-gui)
10. [Configuration System](#configuration-system)

---

## What is Argus NIDS?

**NIDS** stands for **Network Intrusion Detection System**.

Argus functions as a security guard for computer networks. Similar to how a security guard monitors building entry and exit points, Argus monitors all data (called "packets") flowing through the network.

**What does it do?**
- Monitors all network traffic in real-time
- Detects suspicious activities (like hacking attempts)
- Generates alerts when dangerous activity is detected
- Maintains logs of all activity for later review

**Why is it useful?**
- Protects against unauthorized network access attempts
- Detects malware communication with external servers
- Identifies unusual patterns that might indicate security problems
- Provides visibility into network activity

---

## How Does It Work?

The basic flow of Argus operation:

```
Network Traffic → Capture Packets → Parse Packets → Analyze for Threats → Alert User
```

**Step-by-step:**

1. **Capture**: Argus listens to the network interface (analogous to a microphone listening to conversations)
2. **Parse**: Packets are broken down into understandable components (analogous to reading a letter)
3. **Analyze**: Each packet is checked for suspicious patterns using 12 different detection methods
4. **Alert**: When threats are detected, warnings are displayed in the GUI
5. **Log**: All activity is recorded for later review

---

## Project Structure

File organization structure:

```
Argus/
├── main.py                    # CLI testing interface (for developers)
├── requirements.txt           # List of required Python libraries
├── README.md                  # Project overview
├── docs/                      # Documentation folder
│   ├── devlog.md             # Development diary
│   └── technical_reference.md # This file
└── src/                       # Source code folder
    ├── core/                  # Core functionality
    │   ├── packet_capture.py # Captures network packets
    │   ├── packet_parser.py  # Breaks down packets
    │   └── threat_detectors.py # Detects threats
    ├── gui/                   # Graphical interface
    │   └── gui.py            # Tkinter GUI
    ├── utils/                 # Utility files
    │   └── data_structures.py # Data definitions
    └── tests/                 # Test files
        └── test_packet_parser.py
```

**What each folder does:**
- `core/`: The "brain" - does all the important work
- `gui/`: The user interface layer
- `utils/`: Helper tools and definitions
- `tests/`: Code to verify everything works correctly

---

## Understanding Network Basics

Before diving into the code, some basic networking concepts are necessary.

### What is a Network Packet?

A **network packet** is analogous to a postal letter - it's a small piece of data wrapped with addressing information.

**A packet contains:**
- **Source address**: The sender's address (analogous to a return address)
- **Destination address**: The recipient's address
- **Data**: The actual message content
- **Protocol information**: The type of communication method

### Network Layers (Like Layers of an Onion)

Network data is organized in layers, each wrapping the previous one:

```
┌─────────────────────────────────────┐
│  Ethernet Layer (Physical delivery) │  ← Outermost layer
│  ┌───────────────────────────────┐  │
│  │  IP Layer (Addressing)        │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  TCP/UDP (Connection)   │  │  │
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │  Data (Message)   │  │  │  │  ← Innermost layer
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**1. Ethernet Layer** (Physical)
- Contains MAC addresses (unique hardware identifiers)
- Handles physical transmission of data frames

**2. IP Layer** (Internet Protocol)
- Contains IP addresses (like 192.168.1.1)
- Provides routing information for packets across networks

**3. Transport Layer** (TCP/UDP)
- TCP: Reliable delivery with acknowledgments
- UDP: Fast delivery without guarantees
- Contains port numbers to identify applications

**4. Application Layer**
- The actual data content

### Important Network Concepts

**IP Address**: A unique number identifying a device on the network
- Example: `192.168.1.100`
- Used for routing packets to the correct destination

**MAC Address**: A unique hardware identifier burned into network cards
- Example: `aa:bb:cc:dd:ee:ff`
- Used for local network communication within the same subnet

**Port**: A number identifying which application should receive the data
- Example: Port 80 = Web traffic, Port 22 = SSH (remote login)
- Allows multiple applications to use the network simultaneously

**Protocol**: The "language" or rules for communication
- TCP (Protocol 6): Reliable, ordered delivery
- UDP (Protocol 17): Fast, no guarantees
- ICMP (Protocol 1): Network diagnostics (like ping)

---

## Data Structures Explained

Argus uses **NamedTuples** to store packet information. These are immutable data structures with named fields.

### File: `src/utils/data_structures.py`

This file defines the "blueprints" for storing different types of network data.

#### Ethernet Structure

```python
class Ethernet(NamedTuple):
    dst_mac: str
    src_mac: str
    ethertype: str
```

**What it stores:**
- `dst_mac`: Destination MAC address (where it's going)
- `src_mac`: Source MAC address (where it came from)
- `ethertype`: What type of data is inside (like "0800" for IPv4)

**Used in:**
- `packet_parser.py`: `parse_ethernet()` function creates this structure from raw packet bytes
- `packet_capture.py`: Passed to `analyze_packet()` for threat detection
- `threat_detectors.py`: Used in MAC spoofing and ARP spoofing detection

#### IPv4 Structure

```python
class IPv4(NamedTuple):
    protocol: int
    src_ip: str
    dst_ip: str
```

**What it stores:**
- `protocol`: What protocol is being used (6=TCP, 17=UDP, 1=ICMP)
- `src_ip`: Source IP address (like "192.168.1.100")
- `dst_ip`: Destination IP address (like "8.8.8.8")

**Used in:**
- `packet_parser.py`: `parse_ipv4()` function creates this structure from IP header bytes
- `packet_capture.py`: Determines which transport layer parser to use (TCP/UDP/ICMP)
- `threat_detectors.py`: Used in IP spoofing, DDoS, malicious packet, port scan, and brute force detection

#### IPv6 Structure

```python
class IPv6(NamedTuple):
    src_ip: str
    dst_ip: str
```

**What it stores:**
- `src_ip`: Source IPv6 address (longer format, like "2001:0db8:85a3::8a2e:0370:7334")
- `dst_ip`: Destination IPv6 address

**Why IPv6?**: IPv4 addresses are running out, so IPv6 provides many more addresses.

#### TCP Structure

```python
class TCP(NamedTuple):
    src_port: int
    dst_port: int
    seq_num: int
    ack_num: int
```

**What it stores:**
- `src_port`: Source port number (which application sent it)
- `dst_port`: Destination port number (which application should receive it)
- `seq_num`: Sequence number (for ordering packets)
- `ack_num`: Acknowledgment number (confirms receipt)

**Used in:**
- `packet_parser.py`: `parse_tcp()` function creates this structure from TCP header bytes
- `packet_capture.py`: Passed to `analyze_packet()` for threat analysis
- `threat_detectors.py`: Used in SYN flood detection (checks if `ack_num == 0`), port scan detection, and brute force detection

**Special note about `ack_num`:**
- If `ack_num == 0`, this is a **SYN packet** (connection request)
- SYN packets are used to start new connections
- Too many SYN packets = possible attack (SYN flood)

#### UDP Structure

```python
class UDP(NamedTuple):
    src_port: int
    dst_port: int
    length: int
    checksum: int
```

**What it stores:**
- `src_port`: Source port
- `dst_port`: Destination port
- `length`: How long the data is
- `checksum`: Error-checking value

**Difference from TCP**: UDP is faster but doesn't guarantee delivery or ordering.

**Used in:**
- `packet_parser.py`: `parse_udp()` function creates this structure from UDP header bytes
- `packet_capture.py`: Passed to `analyze_packet()` for threat analysis
- `threat_detectors.py`: Used in DNS tunneling detection (checks for port 53) and port scan detection

#### ICMP Structures

```python
class ICMPv4(NamedTuple):
    type: int
    code: int
    checksum: int
    identifier: int
    sequence: int

class ICMPv6(NamedTuple):
    type: int
    code: int
    checksum: int
```

**What it stores:**
- `type`: What kind of ICMP message (8 = ping request, 0 = ping reply)
- `code`: More specific information
- `identifier` & `sequence`: For matching requests with replies

**What is ICMP?**: Used for network diagnostics and error messages (like the "ping" command).

**Used in:**
- `packet_parser.py`: `parse_icmpv4()` and `parse_icmpv6()` functions create these structures
- `packet_capture.py`: Passed to `analyze_packet()` for threat analysis
- `threat_detectors.py`: Used in ICMP flood detection

---

## Packet Parsing - Breaking Down Network Data

Parsing means "reading and understanding" the raw bytes of a packet. It's like opening an envelope and reading the letter inside.

### File: `src/core/packet_parser.py`

This file contains functions that convert raw bytes into our data structures.

#### Helper Function: Converting Bytes to MAC Address

```python
def bytes_to_mac(b: bytes) -> str:
    return ":".join(f"{byte:02x}" for byte in b)
```

**What it does:**
- Takes 6 bytes of raw data
- Converts each byte to hexadecimal (base-16 numbers)
- Joins them with colons

**Example:**
- Input: `b'\xaa\xbb\xcc\xdd\xee\xff'`
- Output: `"aa:bb:cc:dd:ee:ff"`

**Step-by-step breakdown:**
1. `for byte in b` - Loop through each byte
2. `f"{byte:02x}"` - Convert byte to 2-digit hex (like `170` → `"aa"`)
3. `":".join(...)` - Put colons between each pair (like `"aa:bb:cc"`)

#### Helper Function: Converting Bytes to IPv4 Address

```python
def bytes_to_ipv4(b: bytes) -> str:
    return ".".join(str(byte) for byte in b)
```

**What it does:**
- Takes 4 bytes of raw data
- Converts each byte to a decimal number
- Joins them with dots

**Example:**
- Input: `b'\xc0\xa8\x01\x64'`
- Output: `"192.168.1.100"`

**Step-by-step breakdown:**
1. `for byte in b` - Loop through each byte
2. `str(byte)` - Convert byte to string (like `192`)
3. `".".join(...)` - Put dots between numbers

#### Helper Function: Converting Bytes to IPv6 Address

```python
def bytes_to_ipv6(b: bytes) -> str:
    return ":".join(f"{b[i]:02x}{b[i + 1]:02x}" for i in range(0, 16, 2))
```

**What it does:**
- Takes 16 bytes of raw data
- Groups them into pairs
- Converts each pair to hexadecimal
- Joins with colons

**Example:**
- Input: 16 bytes
- Output: `"2001:0db8:85a3:0000:0000:8a2e:0370:7334"`

**Step-by-step breakdown:**
1. `range(0, 16, 2)` - Count from 0 to 16, stepping by 2 (0, 2, 4, 6, ...)
2. `b[i]:02x` and `b[i+1]:02x` - Take two bytes at a time, convert to hex
3. `":".join(...)` - Put colons between each group

#### Parsing Ethernet Layer

```python
def parse_ethernet(raw: bytes) -> Ethernet:
    if len(raw) < 14:
        raise ValueError("Invalid Ethernet frame")
    
    return Ethernet(
        dst_mac=bytes_to_mac(raw[0:6]),
        src_mac=bytes_to_mac(raw[6:12]),
        ethertype=raw[12:14].hex(),
    )
```

**What it does:**
- Reads the first 14 bytes of a packet
- Extracts destination MAC, source MAC, and ethertype
- Returns an Ethernet object

**Byte layout:**
- Bytes 0-5: Destination MAC (6 bytes)
- Bytes 6-11: Source MAC (6 bytes)
- Bytes 12-13: Ethertype (2 bytes)

**Step-by-step breakdown:**
1. Check if we have at least 14 bytes (safety check)
2. Extract bytes 0-5 and convert to destination MAC address
3. Extract bytes 6-11 and convert to source MAC address
4. Extract bytes 12-13 and convert to hex string (like "0800" for IPv4)
5. Create and return an Ethernet object with this information

**Example:**
- If ethertype is `"0800"` → IPv4 packet inside
- If ethertype is `"86dd"` → IPv6 packet inside
- If ethertype is `"0806"` → ARP packet inside

#### Parsing IPv4 Layer

```python
def parse_ipv4(raw: bytes) -> IPv4:
    return IPv4(
        protocol=raw[9],
        src_ip=bytes_to_ipv4(raw[12:16]),
        dst_ip=bytes_to_ipv4(raw[16:20]),
    )
```

**What it does:**
- Reads 20 bytes of IPv4 header
- Extracts protocol number, source IP, and destination IP
- Returns an IPv4 object

**Byte layout:**
- Byte 9: Protocol number (6=TCP, 17=UDP, 1=ICMP)
- Bytes 12-15: Source IP address (4 bytes)
- Bytes 16-19: Destination IP address (4 bytes)

**Step-by-step breakdown:**
1. Get byte 9 for protocol (tells us what's inside: TCP, UDP, or ICMP)
2. Extract bytes 12-15 and convert to source IP address
3. Extract bytes 16-19 and convert to destination IP address
4. Create and return an IPv4 object

**Why these specific bytes?**: The IPv4 header has a fixed format defined by internet standards (RFC 791).

#### Parsing TCP Layer

```python
def parse_tcp(raw: bytes) -> TCP:
    return TCP(
        src_port=int.from_bytes(raw[0:2], "big"),
        dst_port=int.from_bytes(raw[2:4], "big"),
        seq_num=int.from_bytes(raw[4:8], "big"),
        ack_num=int.from_bytes(raw[8:12], "big"),
    )
```

**What it does:**
- Reads 20 bytes of TCP header
- Extracts port numbers and sequence numbers
- Returns a TCP object

**Byte layout:**
- Bytes 0-1: Source port (2 bytes)
- Bytes 2-3: Destination port (2 bytes)
- Bytes 4-7: Sequence number (4 bytes)
- Bytes 8-11: Acknowledgment number (4 bytes)

**Step-by-step breakdown:**
1. `int.from_bytes(raw[0:2], "big")` - Convert 2 bytes to integer (big-endian format)
   - "big-endian" means most significant byte first (like reading left-to-right)
2. Extract source port from bytes 0-1
3. Extract destination port from bytes 2-3
4. Extract sequence number from bytes 4-7 (used for ordering packets)
5. Extract acknowledgment number from bytes 8-11 (used for confirming receipt)

**Important for threat detection:**
- If `ack_num == 0`, this is a SYN packet (connection request)
- Many SYN packets from one source = SYN flood attack

#### Parsing UDP Layer

```python
def parse_udp(raw: bytes) -> UDP:
    return UDP(
        src_port=int.from_bytes(raw[0:2], "big"),
        dst_port=int.from_bytes(raw[2:4], "big"),
        length=int.from_bytes(raw[4:6], "big"),
        checksum=int.from_bytes(raw[6:8], "big"),
    )
```

**What it does:**
- Reads 8 bytes of UDP header (simpler than TCP)
- Extracts port numbers, length, and checksum
- Returns a UDP object

**Byte layout:**
- Bytes 0-1: Source port
- Bytes 2-3: Destination port
- Bytes 4-5: Length of data
- Bytes 6-7: Checksum (for error detection)

**Step-by-step breakdown:**
1. Extract source port from bytes 0-1
2. Extract destination port from bytes 2-3
3. Extract length from bytes 4-5 (tells us how much data follows)
4. Extract checksum from bytes 6-7 (used to detect transmission errors)

**Important for threat detection:**
- If destination port is 53 → DNS traffic (might be DNS tunneling)
- UDP is often used for DDoS attacks because it's faster and doesn't require connection setup

#### Parsing ICMP Layers

```python
def parse_icmpv4(raw: bytes) -> ICMPv4:
    return ICMPv4(
        type=raw[0],
        code=raw[1],
        checksum=int.from_bytes(raw[2:4], "big"),
        identifier=int.from_bytes(raw[4:6], "big"),
        sequence=int.from_bytes(raw[6:8], "big"),
    )

def parse_icmpv6(raw: bytes) -> ICMPv6:
    return ICMPv6(
        type=raw[0],
        code=raw[1],
        checksum=int.from_bytes(raw[2:4], "big"),
    )
```

**What they do:**
- Read ICMP headers (8 bytes for ICMPv4, 4 bytes minimum for ICMPv6)
- Extract type, code, and other fields
- Return ICMP objects

**Byte layout:**
- Byte 0: Type (what kind of ICMP message)
- Byte 1: Code (more specific information)
- Bytes 2-3: Checksum
- Bytes 4-5: Identifier (for matching requests/replies)
- Bytes 6-7: Sequence number

**Common ICMP types:**
- Type 8: Echo Request (ping request)
- Type 0: Echo Reply (ping response)
- Type 3: Destination Unreachable

**Important for threat detection:**
- Too many ICMP packets = ICMP flood attack
- ICMP can be used for network scanning

---

## Threat Detection

This is the most important part of Argus! The threat detection system analyzes packets and identifies 12 different types of attacks.

### File: `src/core/threat_detectors.py`

This file contains all the detection logic and configurable thresholds.

### Configuration Constants (Top of File)

At the very top of the file, we have all the configurable thresholds:

```python
# Port Scan Detection
PORT_SCAN_THRESHOLD = 20  # Number of unique ports to trigger alert
PORT_SCAN_WINDOW = 10  # Time window in seconds

# SYN Flood Detection
SYN_FLOOD_THRESHOLD = 100  # Number of SYN packets to trigger alert
SYN_FLOOD_WINDOW = 5  # Time window in seconds

# DDoS Detection
DDOS_THRESHOLD = 200  # Number of packets to single destination
DDOS_WINDOW = 10  # Time window in seconds

# ... and more
```

**Why configurable?**
- Different networks have different "normal" traffic patterns
- You can tune the sensitivity to reduce false alarms
- Easy to adjust without digging through code

**How to change them:**
- Edit these values directly in the file, OR
- Use the GUI Configuration view to change them and save to JSON

### The State Dictionary

Before detecting threats, we need to remember what we've seen. The `create_state()` function creates a "memory" for the system:

```python
def create_state():
    return {
        "port_scans": {},      # Track which ports each IP has tried
        "syn_floods": {},      # Track SYN packets from each IP
        "ip_macs": {},         # Track which MACs are used with each IP
        "arp_table": {},       # Remember IP-to-MAC mappings
        "ddos": {},            # Track packets to each destination
        "brute_force": {},     # Track login attempts
        "icmp_floods": {},     # Track ICMP packets
        "dns_queries": {},     # Track DNS queries
        "unusual_protos": {},  # Count unusual protocols
        "traffic": {},         # Track total traffic per IP
        "mac_ips": {},         # Track which IPs are used with each MAC
    }
```

**What is state?**
- A dictionary (like a notebook) that stores what we've observed
- Each key tracks a different type of activity
- Gets updated as packets arrive
- Used to detect patterns over time

**Example:**
- If we see IP `192.168.1.100` try port 22, we add it to `port_scans`
- If the same IP tries ports 23, 80, 443, 3389... we detect a port scan!

### Helper Function: Cleaning Old Entries

```python
def clean_old_entries(entries, window):
    """Remove entries older than window seconds"""
    cutoff = time() - window
    return [e for e in entries if e[0] >= cutoff]
```

**What it does:**
- Removes old data that's no longer relevant
- Keeps only recent entries within the time window

**Why is this important?**
- We only care about recent activity (last 5-60 seconds depending on the threat)
- Prevents memory from growing forever
- Makes detection more accurate (old data doesn't interfere)

**Step-by-step breakdown:**
1. `time()` - Get current time in seconds since 1970 (Unix timestamp)
2. `cutoff = time() - window` - Calculate the cutoff time (e.g., 10 seconds ago)
3. `e[0]` - Each entry is a tuple where first element is the timestamp
4. `e[0] >= cutoff` - Keep only entries newer than cutoff
5. Return the filtered list

**Example:**
- Current time: 1000 seconds
- Window: 10 seconds
- Cutoff: 990 seconds
- Entries: `[(985, data), (992, data), (998, data)]`
- Result: `[(992, data), (998, data)]` (removed the 985 entry)

---

### Detection Function 1: Port Scan

```python
def detect_port_scan(state, src_ip, dst_port):
    """Detect same IP trying multiple ports quickly"""
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
```

**What is a port scan?**
- An attacker tries many different ports to find open services
- Like trying every door in a building to see which ones are unlocked
- Common first step in hacking attempts

**How detection works:**
1. Get current time
2. Check if we've seen this IP before; if not, create empty list
3. Remove old port attempts (older than 10 seconds)
4. Add this new port attempt with timestamp
5. Count how many **unique** ports this IP has tried
6. If 20 or more unique ports → **ALERT!**

**Why unique ports?**
- Trying the same port 20 times is normal (like refreshing a webpage)
- Trying 20 different ports is suspicious (scanning for vulnerabilities)

**Real-world example:**
- Normal: `192.168.1.100` connects to port 80 (web) repeatedly
- Suspicious: `192.168.1.100` tries ports 21, 22, 23, 25, 80, 110, 143, 443, 3306, 3389, 5432, 8080...

---

### Detection Function 2: SYN Flood

```python
def detect_syn_flood(state, src_ip):
    """Detect massive SYN packets from same source"""
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
```

**What is a SYN flood?**
- Attacker sends many connection requests (SYN packets) but never completes the connection
- Like calling a restaurant 100 times and hanging up immediately
- Overwhelms the target server, making it unavailable to legitimate users

**How detection works:**
1. Get current time
2. Check if we've seen this IP before; if not, create empty list
3. Remove old SYN packets (older than 5 seconds)
4. Add this new SYN packet timestamp
5. Count total SYN packets in the last 5 seconds
6. If 100 or more SYN packets → **ALERT!**

**Why is this dangerous?**
- Each SYN packet makes the server allocate resources
- Too many = server runs out of resources
- Legitimate users can't connect

**Real-world example:**
- Normal: A user sends 1-2 SYN packets to connect to a website
- Attack: An attacker sends 100+ SYN packets per second to crash the server

---

### Detection Function 3: IP Spoofing

```python
def detect_ip_spoofing(state, src_ip, src_mac):
    """Detect IP used with multiple MAC addresses"""
    # Skip private/DHCP ranges to reduce false positives
    if src_ip.startswith(('169.254.', '0.0.0.0', '255.255.255.255')):
        return None
    
    if src_ip not in state["ip_macs"]:
        state["ip_macs"][src_ip] = set()
    
    state["ip_macs"][src_ip].add(src_mac)
    
    if len(state["ip_macs"][src_ip]) >= SPOOFING_THRESHOLD:
        return f"IP Spoofing: {src_ip} seen with {len(state['ip_macs'][src_ip])} different MACs"
    return None
```

**What is IP spoofing?**
- Attacker pretends to be someone else by using their IP address
- Like wearing a disguise and using someone else's ID
- Used to bypass security or frame someone else

**How detection works:**
1. Skip special IP addresses that legitimately change MACs (like DHCP)
2. Check if we've seen this IP before; if not, create empty set
3. Add this MAC address to the set of MACs seen with this IP
4. Count how many different MACs have used this IP
5. If 3 or more different MACs → **ALERT!**

**Why multiple MACs with one IP is suspicious?**
- Normally, one IP = one device = one MAC address
- If multiple devices claim the same IP, someone is lying
- Exception: DHCP can reassign IPs, so we skip those ranges

**Real-world example:**
- Normal: IP `192.168.1.100` always uses MAC `aa:bb:cc:dd:ee:ff`
- Suspicious: IP `192.168.1.100` uses MACs `aa:bb:cc:dd:ee:ff`, `11:22:33:44:55:66`, `99:88:77:66:55:44`

---

### Detection Function 4: ARP Spoofing

```python
def detect_arp_spoofing(state, ip, mac):
    """Detect IP-MAC binding changes"""
    # Skip broadcast and multicast addresses
    if ip.startswith(('255.', '224.', '169.254.', '0.0.0.0')):
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
```

**What is ARP spoofing?**
- ARP (Address Resolution Protocol) maps IP addresses to MAC addresses
- Attacker sends fake ARP messages to associate their MAC with someone else's IP
- Like changing the address on someone's mailbox to redirect their mail
- Used for man-in-the-middle attacks (intercepting traffic)

**How detection works:**
1. Skip special addresses (broadcast, multicast)
2. Check if we've seen this IP before
3. If yes, check if the MAC has changed
4. If changed, track the change with timestamp
5. Remove old changes (older than 5 minutes)
6. If 3 or more changes in 5 minutes → **ALERT!**
7. Update the ARP table with new MAC

**Why track changes over time?**
- A single MAC change might be legitimate (device replaced, network reconfigured)
- Multiple rapid changes are highly suspicious
- Reduces false positives

**Real-world example:**
- Normal: IP `192.168.1.1` (router) always has MAC `aa:bb:cc:dd:ee:ff`
- Attack: Attacker sends fake ARP saying "192.168.1.1 is now at MAC 11:22:33:44:55:66"
- Result: Your traffic goes to attacker instead of router

---

### Detection Function 5: DDoS (Distributed Denial of Service)

```python
def detect_ddos(state, src_ip, dst_ip):
    """Detect high packet rate to single destination"""
    now = time()
    if dst_ip not in state["ddos"]:
        state["ddos"][dst_ip] = []
    
    state["ddos"][dst_ip] = clean_old_entries(state["ddos"][dst_ip], DDOS_WINDOW)
    state["ddos"][dst_ip].append((now, src_ip))
    
    if len(state["ddos"][dst_ip]) >= DDOS_THRESHOLD:
        sources = len(set(s for _, s in state["ddos"][dst_ip]))
        return f"DDoS: {dst_ip} received {len(state['ddos'][dst_ip])} packets from {sources} sources in {DDOS_WINDOW}s"
    return None
```

**What is DDoS?**
- Many computers flood one target with traffic to overwhelm it
- Like thousands of people calling the same phone number at once
- Makes the target unavailable to legitimate users
- "Distributed" means attacks come from many sources

**How detection works:**
1. Get current time
2. Check if the system is tracking this destination; if not, create empty list
3. Remove old packets (older than 10 seconds)
4. Add this new packet with timestamp and source IP
5. Count total packets to this destination
6. Count how many different sources sent packets
7. If 200+ packets in 10 seconds → **ALERT!**

**Why track sources?**
- Shows if it's a distributed attack (many sources) or single source
- Helps understand the attack pattern
- More sources = harder to block

**Real-world example:**
- Normal: Server receives 50 packets per second from various users
- Attack: Server receives 200+ packets per second, overwhelming it

---

### Detection Function 6: Malicious Packets

```python
def detect_malicious_packet(src_ip, dst_ip):
    """Detect obviously malicious packets"""
    if src_ip == dst_ip:
        return f"Malicious: Land attack {src_ip} -> {dst_ip}"
    if src_ip.startswith("0.") or dst_ip.startswith("0."):
        return f"Malicious: Invalid IP {src_ip} -> {dst_ip}"
    return None
```

**What are malicious packets?**
- Packets that are obviously wrong or impossible
- Violate basic networking rules
- Often used to crash or confuse systems

**Types detected:**

**1. Land Attack:**
- Source IP = Destination IP (packet sent to itself)
- Like mailing a letter to itself at its own address
- Can crash some systems that don't handle this properly

**2. Invalid IP:**
- IPs starting with "0." are reserved and invalid
- Should never appear in real traffic
- Sign of malformed or crafted packets

**How detection works:**
1. Check if source equals destination → Land attack
2. Check if either IP starts with "0." → Invalid IP
3. If either condition is true → **ALERT!**

**Real-world example:**
- Malicious: Packet from `192.168.1.100` to `192.168.1.100` (land attack)
- Malicious: Packet from `0.0.0.1` to anywhere (invalid IP)

---

### Detection Function 7: Brute Force

```python
def detect_brute_force(state, src_ip, dst_port):
    """Detect repeated attempts on auth services"""
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
```

**What is brute force?**
- Attacker tries many passwords/credentials to break into a system
- Like trying every key on a keyring to unlock a door
- Automated tools can try thousands of passwords per minute

**Monitored ports (authentication services):**
- Port 21: FTP (file transfer)
- Port 22: SSH (remote login)
- Port 23: Telnet (old remote login)
- Port 25: SMTP (email)
- Port 110: POP3 (email)
- Port 143: IMAP (email)
- Port 389: LDAP (directory service)
- Port 445: SMB (file sharing)
- Port 3306: MySQL (database)
- Port 3389: RDP (Windows remote desktop)
- Port 5432: PostgreSQL (database)
- Port 5900: VNC (remote desktop)

**How detection works:**
1. Check if destination port is an authentication service; if not, return
2. Get current time
3. Create key combining IP and port (track per-service attempts)
4. Remove old attempts (older than 60 seconds)
5. Add this new attempt
6. If 20+ attempts in 60 seconds → **ALERT!**

**Why per-service tracking?**
- Someone might legitimately connect to SSH and FTP at the same time
- We only care about repeated attempts to the **same** service

**Real-world example:**
- Normal: User tries SSH password 2-3 times (typos happen)
- Attack: Automated tool tries 20+ SSH passwords in one minute

---

### Detection Function 8: ICMP Flood

```python
def detect_icmp_flood(state, src_ip):
    """Detect ICMP flood attacks"""
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
```

**What is ICMP flood?**
- Attacker sends massive amounts of ICMP packets (like ping)
- Overwhelms the target's network bandwidth
- Also called "ping flood"
- Simple but effective DoS attack

**How detection works:**
1. Get current time
2. Check if the system is tracking this IP; if not, create empty list
3. Remove old ICMP packets (older than 5 seconds)
4. Add this new ICMP packet timestamp
5. Count total ICMP packets in last 5 seconds
6. If 100+ ICMP packets → **ALERT!**

**Why is this dangerous?**
- ICMP packets require processing
- Too many = wastes bandwidth and CPU
- Can make network unusable

**Real-world example:**
- Normal: User pings a server once (1 packet)
- Attack: Attacker sends 100+ pings per second

---

### Detection Function 9: DNS Tunneling

```python
def detect_dns_tunneling(state, src_ip, query_length=0):
    """Detect DNS tunneling patterns"""
    now = time()
    if src_ip not in state["dns_queries"]:
        state["dns_queries"][src_ip] = []
    
    state["dns_queries"][src_ip] = clean_old_entries(
        state["dns_queries"][src_ip], DNS_TUNNELING_WINDOW
    )
    state["dns_queries"][src_ip].append((now, query_length))
    
    queries = state["dns_queries"][src_ip]
    long_queries = sum(1 for _, l in queries if l > DNS_TUNNELING_LONG_QUERY_LENGTH)
    
    if len(queries) >= DNS_TUNNELING_QUERY_THRESHOLD or \
       (len(queries) > 10 and long_queries > len(queries) * DNS_TUNNELING_LONG_QUERY_RATIO):
        return f"DNS Tunneling: {src_ip} made {len(queries)} queries ({long_queries} long) in {DNS_TUNNELING_WINDOW}s"
    return None
```

**What is DNS tunneling?**
- DNS normally translates domain names to IP addresses (like "google.com" → "142.250.80.46")
- Attackers abuse DNS to sneak data out of networks
- Encode data in domain names (like "secret-data-here.evil.com")
- Bypasses many firewalls because DNS is usually allowed

**How detection works:**
1. Get current time
2. Check if the system is tracking this IP; if not, create empty list
3. Remove old queries (older than 60 seconds)
4. Add this new query with timestamp and length
5. Count total queries
6. Count "long" queries (over 50 characters)
7. Calculate ratio of long queries
8. If 100+ queries OR more than 60% are long → **ALERT!**

**Why track query length?**
- Normal DNS queries are short: "google.com" (10 chars)
- Tunneling queries are long: "aGVsbG8gd29ybGQgdGhpcyBpcyBzZWNyZXQgZGF0YQ.evil.com" (50+ chars)
- Long queries = likely encoding data

**Real-world example:**
- Normal: User looks up "facebook.com", "youtube.com" (few queries, short names)
- Attack: Malware makes 100+ queries to "base64encodeddata.attacker.com"

---

### Detection Function 10: Unusual Protocol

```python
def detect_unusual_protocol(state, protocol, src_ip):
    """Detect unusual protocol usage"""
    # Common protocols: ICMP, TCP, UDP, ICMPv6, IGMP, ESP, AH, GRE
    common = {1, 2, 6, 17, 41, 47, 50, 51, 58, 89, 132}
    if protocol in common:
        return None
    
    # Only alert after seeing the same unusual protocol multiple times
    state["unusual_protos"][protocol] = state["unusual_protos"].get(protocol, 0) + 1
    
    if state["unusual_protos"][protocol] >= 10:
        return f"Unusual Protocol: {protocol} from {src_ip} (seen {state['unusual_protos'][protocol]} times)"
    return None
```

**What are unusual protocols?**
- Most internet traffic uses just a few protocols (TCP, UDP, ICMP)
- Other protocols exist but are rare
- Seeing unusual protocols might indicate:
  - Specialized applications
  - Tunneling attempts
  - Malware using custom protocols
  - Network misconfiguration

**Common protocols (not alerted):**
- 1: ICMP (ping, errors)
- 2: IGMP (multicast)
- 6: TCP (web, email, most apps)
- 17: UDP (DNS, streaming, games)
- 41: IPv6 encapsulation
- 47: GRE (VPN tunneling)
- 50: ESP (IPsec encryption)
- 51: AH (IPsec authentication)
- 58: ICMPv6 (IPv6 ping)
- 89: OSPF (routing)
- 132: SCTP (streaming)

**How detection works:**
1. Check if protocol is in the common list; if yes, return (no alert)
2. Increment counter for this protocol
3. If seen 10+ times → **ALERT!**

**Why wait for 10 occurrences?**
- A single unusual packet might be legitimate
- Repeated use is more suspicious
- Reduces false positives

**Real-world example:**
- Normal: All traffic is TCP (6), UDP (17), ICMP (1)
- Suspicious: Repeated use of protocol 253 (experimental/private use)

---

### Detection Function 11: Abnormal Traffic

```python
def detect_abnormal_traffic(state, src_ip):
    """Detect abnormally high traffic from single source"""
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
```

**What is abnormal traffic?**
- One device sending way more packets than normal
- Could indicate:
  - Malware infection (sending spam, attacking others)
  - Compromised device (part of botnet)
  - Misconfigured application
  - Data exfiltration (stealing data)

**How detection works:**
1. Get current time
2. Check if the system is tracking this IP; if not, create empty list
3. Remove old packets (older than 60 seconds)
4. Add this new packet timestamp
5. Count total packets from this IP
6. If 2000+ packets in 60 seconds → **ALERT!**

**Why 2000 packets?**
- Normal user: 10-100 packets per minute (web browsing, email)
- Heavy user: 500-1000 packets per minute (streaming video)
- Abnormal: 2000+ packets per minute (likely malicious)

**Real-world example:**
- Normal: Your laptop sends 50 packets per minute (browsing web)
- Abnormal: Your laptop sends 2000+ packets per minute (infected with malware sending spam)

---

### Detection Function 12: MAC Spoofing

```python
def detect_mac_spoofing(state, src_mac, src_ip):
    """Detect MAC used with multiple IPs"""
    # Skip broadcast/multicast MACs
    if src_mac.startswith(('ff:ff:', '01:00:5e:', '33:33:')):
        return None
    
    if src_mac not in state["mac_ips"]:
        state["mac_ips"][src_mac] = set()
    
    state["mac_ips"][src_mac].add(src_ip)
    
    if len(state["mac_ips"][src_mac]) >= SPOOFING_THRESHOLD:
        return f"MAC Spoofing: {src_mac} seen with {len(state['mac_ips'][src_mac])} different IPs"
    return None
```

**What is MAC spoofing?**
- Attacker changes their MAC address to impersonate another device
- Opposite of IP spoofing (one MAC claiming multiple IPs)
- Used to:
  - Bypass MAC address filtering
  - Impersonate authorized devices
  - Evade tracking

**How detection works:**
1. Skip special MACs (broadcast, multicast) that legitimately use multiple IPs
2. Check if we've seen this MAC before; if not, create empty set
3. Add this IP to the set of IPs seen with this MAC
4. Count how many different IPs have used this MAC
5. If 3+ different IPs → **ALERT!**

**Why multiple IPs with one MAC is suspicious?**
- Normally, one device (MAC) = one IP address
- If one MAC claims multiple IPs, something is wrong
- Exception: Routers and special devices, but they use special MAC ranges we skip

**Real-world example:**
- Normal: MAC `aa:bb:cc:dd:ee:ff` always uses IP `192.168.1.100`
- Suspicious: MAC `aa:bb:cc:dd:ee:ff` uses IPs `192.168.1.100`, `192.168.1.101`, `192.168.1.102`

---

### Main Analysis Function

```python
def analyze_packet(state, ethernet=None, ipv4=None, ipv6=None, tcp=None, udp=None, icmp=None):
    """Run all detectors on a packet and return alerts"""
    alerts = []
    
    # Extract basic info
    src_ip = ipv4.src_ip if ipv4 else (ipv6.src_ip if ipv6 else None)
    dst_ip = ipv4.dst_ip if ipv4 else (ipv6.dst_ip if ipv6 else None)
    src_mac = ethernet.src_mac if ethernet else None
    protocol = ipv4.protocol if ipv4 else None
    
    # Run detectors based on available data
    if src_mac and src_ip:
        alert = detect_mac_spoofing(state, src_mac, src_ip)
        if alert: alerts.append(alert)
        
        alert = detect_ip_spoofing(state, src_ip, src_mac)
        if alert: alerts.append(alert)
        
        alert = detect_arp_spoofing(state, src_ip, src_mac)
        if alert: alerts.append(alert)
    
    if src_ip and dst_ip:
        alert = detect_malicious_packet(src_ip, dst_ip)
        if alert: alerts.append(alert)
        
        alert = detect_ddos(state, src_ip, dst_ip)
        if alert: alerts.append(alert)
    
    if src_ip:
        alert = detect_abnormal_traffic(state, src_ip)
        if alert: alerts.append(alert)
    
    if protocol:
        alert = detect_unusual_protocol(state, protocol, src_ip)
        if alert: alerts.append(alert)
    
    if tcp:
        if tcp.ack_num == 0:  # SYN packet
            alert = detect_syn_flood(state, src_ip)
            if alert: alerts.append(alert)
        
        alert = detect_port_scan(state, src_ip, tcp.dst_port)
        if alert: alerts.append(alert)
        
        alert = detect_brute_force(state, src_ip, tcp.dst_port)
        if alert: alerts.append(alert)
    
    if udp:
        if udp.dst_port == 53:  # DNS
            alert = detect_dns_tunneling(state, src_ip)
            if alert: alerts.append(alert)
        
        alert = detect_port_scan(state, src_ip, udp.dst_port)
        if alert: alerts.append(alert)
    
    if icmp:
        alert = detect_icmp_flood(state, src_ip)
        if alert: alerts.append(alert)
    
    return alerts
```

**What this function does:**
- Coordinates all 12 detection functions
- Decides which detectors to run based on packet type
- Collects all alerts into a list
- Returns the list to be displayed

**Step-by-step breakdown:**
1. Create empty alerts list
2. Extract basic information (IPs, MAC, protocol) from packet layers
3. **If we have MAC and IP**: Check for MAC spoofing, IP spoofing, ARP spoofing
4. **If we have source and destination IPs**: Check for malicious packets, DDoS
5. **If we have source IP**: Check for abnormal traffic
6. **If we have protocol**: Check for unusual protocols
7. **If it's TCP**:
   - If `ack_num == 0` (SYN packet): Check for SYN flood
   - Check for port scan
   - Check for brute force
8. **If it's UDP**:
   - If destination port is 53 (DNS): Check for DNS tunneling
   - Check for port scan
9. **If it's ICMP**: Check for ICMP flood
10. Return all collected alerts

**Why conditional checks?**
- Not all packets have all layers (e.g., ICMP doesn't have ports)
- We only run detectors when we have the necessary information
- Prevents errors from missing data

---

## Packet Capture - Listening to the Network

This module handles capturing packets from the network and coordinating the parsing and analysis.

### File: `src/core/packet_capture.py`

This file bridges the gap between raw network capture and our threat detection system.

#### Function: Selecting Network Interface

```python
def select_interface():
    interfaces = get_if_list()
    for index, interface in enumerate(interfaces):
        print(f"{index} - {interface}")
    try:
        choice = int(input("Select an interface: "))
    except ValueError:
        print("Invalid input")
        print(f"Auto-selecting {interfaces[0]} for testing")
        return interfaces[0]
    if choice < 0 or choice >= len(interfaces):
        print("Invalid choice")
        print(f"Auto-selecting {interfaces[0]} for testing")
        return interfaces[0]
    return interfaces[choice]
```

**What is a network interface?**
- A network interface is like a "door" through which network traffic flows
- Examples: `eth0` (Ethernet cable), `wlp8s0` (WiFi), `lo` (loopback - internal)
- Your computer might have multiple interfaces

**What this function does:**
- Lists all available network interfaces
- Asks user to choose one
- Returns the selected interface name

**Step-by-step breakdown:**
1. `get_if_list()` - Get list of all network interfaces from Scapy
2. Loop through interfaces and print them with numbers
3. Ask user to input a number
4. If input is invalid or out of range, auto-select interface 2 (usually a real network interface)
5. Return the chosen interface name

**Real-world example:**
```
Available interfaces:
0 - lo (loopback, internal only)
1 - docker0 (Docker virtual network)
2 - eth0 (Ethernet cable)
3 - wlp8s0 (WiFi)

User selects: 2
Returns: "eth0"
```

#### Function: Creating Packet Handler

```python
def create_packet_handler(state, callback=None):
    packet_count = [0]
    
    def packet_handler(packet):
        packet_count[0] += 1
        
        try:
            raw = bytes(packet)
            if len(raw) < 14:
                return
            
            # Parse Ethernet layer
            ethernet = parse_ethernet(raw[:14])
            remaining = raw[14:]
            ethertype = ethernet.ethertype
            
            ipv4 = None
            ipv6 = None
            tcp = None
            udp = None
            icmp = None
            
            if ethertype == "0800" and len(remaining) >= 20:
                ipv4 = parse_ipv4(remaining[:20])
                remaining = remaining[20:]
                proto = ipv4.protocol
                
                if proto == 6 and len(remaining) >= 20:
                    tcp = parse_tcp(remaining[:20])
                elif proto == 17 and len(remaining) >= 8:
                    udp = parse_udp(remaining[:8])
                elif proto == 1 and len(remaining) >= 8:
                    icmp = parse_icmpv4(remaining[:8])
            
            elif ethertype == "86dd" and len(remaining) >= 40:
                ipv6 = parse_ipv6(remaining[:40])
                remaining = remaining[40:]
                if remaining and remaining[0] == 58 and len(remaining) >= 8:
                    icmp = parse_icmpv6(remaining[:8])
            
            alerts = analyze_packet(
                state,
                ethernet=ethernet,
                ipv4=ipv4,
                ipv6=ipv6,
                tcp=tcp,
                udp=udp,
                icmp=icmp,
            )
            
            if callback:
                packet_info = {
                    'packet_num': packet_count[0],
                    'ethernet': ethernet,
                    'ipv4': ipv4,
                    'ipv6': ipv6,
                    'tcp': tcp,
                    'udp': udp,
                    'icmp': icmp,
                }
                callback(packet_info, alerts)
        
        except Exception as e:
            pass
    
    return packet_handler
```

**What this function does:**
- Creates a handler function that processes each captured packet
- Parses the packet into layers
- Runs threat detection
- Calls a callback function with results

**Why use a callback?**
- Separates packet processing from display logic
- Makes it easy to use with GUI or CLI
- GUI can update its display when callback is called

**Step-by-step breakdown:**
1. Initialize packet counter (using list so it can be modified inside nested function)
2. Define inner function `packet_handler` that will be called for each packet
3. Increment packet counter
4. Convert packet to raw bytes
5. Check if packet is at least 14 bytes (minimum for Ethernet header)
6. Parse Ethernet layer (first 14 bytes)
7. Get remaining bytes after Ethernet header
8. Initialize all layer variables to None
9. **If ethertype is "0800" (IPv4)**:
   - Parse IPv4 layer
   - Check protocol number
   - If protocol 6 (TCP): Parse TCP layer
   - If protocol 17 (UDP): Parse UDP layer
   - If protocol 1 (ICMP): Parse ICMP layer
10. **If ethertype is "86dd" (IPv6)**:
    - Parse IPv6 layer
    - Check for ICMPv6 (protocol 58)
11. Call `analyze_packet()` with all parsed layers
12. If callback function was provided, call it with packet info and alerts
13. If any error occurs, silently ignore (prevents crashes from malformed packets)
14. Return the handler function

**Why try-except?**
- Some packets might be malformed or incomplete
- We don't want one bad packet to crash the entire system
- Better to skip a bad packet than stop monitoring

#### Function: Starting Capture

```python
def start_capture(interface, state, callback=None, count=0):
    handler = create_packet_handler(state, callback)
    sniff(
        iface=interface,
        prn=handler,
        count=count if count > 0 else 0,
        store=False,
    )
```

**What this function does:**
- Starts capturing packets from the specified network interface
- Processes each packet with the handler
- Runs until stopped or count is reached

**Parameters:**
- `interface`: Which network interface to listen on (like "eth0")
- `state`: The state dictionary for tracking threats
- `callback`: Optional function to call with results
- `count`: How many packets to capture (0 = infinite)

**Step-by-step breakdown:**
1. Create packet handler using `create_packet_handler()`
2. Call Scapy's `sniff()` function with:
   - `iface=interface` - Which interface to listen on
   - `prn=handler` - Function to call for each packet ("prn" = print/process)
   - `count=count` - How many packets to capture (0 = infinite)
   - `store=False` - Don't store packets in memory (saves RAM)

**Why `store=False`?**
- Storing packets uses lots of memory
- We process them immediately and don't need to keep them
- Important for long-running monitoring

---

## The GUI - User Interface

The GUI (Graphical User Interface) is the visual interface for interacting with Argus. It's built using Tkinter, Python's standard GUI library.

### File: `src/gui/gui.py`

This file contains all the GUI code - windows, buttons, text areas, etc.

### Main Components

#### 1. Color Scheme

```python
colors = {
    'bg_dark': '#1e1e1e',      # Dark background
    'bg_medium': '#2d2d2d',    # Medium background
    'bg_light': '#3d3d3d',     # Light background
    'accent': '#007acc',       # Blue accent color
    'text': '#ffffff',         # White text
    'text_dim': '#cccccc',     # Dimmed text
    'success': '#4caf50',      # Green (for success)
    'warning': '#ff9800',      # Orange (for warnings)
    'danger': '#f44336',       # Red (for danger)
}
```

**What this does:**
- Defines a consistent color scheme for the entire GUI
- Dark theme (easier on the eyes)
- Color-coded alerts (red = danger, green = safe, etc.)

#### 2. Sidebar Menu

The sidebar contains:
- **ARGUS** logo at the top
- **Dashboard** button (shows main monitoring view)
- **Configuration** button (shows settings)

**How switching works:**
- Clicking a button calls `switch_view()` function
- Hides current view, shows selected view
- Updates button colors to show which is active

#### 3. Dashboard View

The dashboard is the main monitoring screen with several sections:

**Control Buttons:**
- **Start/Stop**: Dynamic button that toggles between starting and stopping capture
  - Green "▶ Start" when stopped
  - Red "⏹ Stop" when running
  - Updates status indicator
- **Clear Logs**: Clears all displayed logs and alerts
- **Export Logs**: Saves logs and alerts to JSON file

**Filter System:**
- Text input for Wireshark-style filters (placeholder shows examples)
- Apply button to activate filters
- Uses placeholder functionality (text disappears on focus)

**Two-Column Layout:**
- **Left: Packet Logs** - Shows all captured packets with timestamps, IPs, ports, protocols
- **Right: Threat Alerts** - Shows detected threats in red

**Statistics:**
- Dashboard shows real-time statistics
- Will show total packets and threats detected

**Statistics Cards:**
- 12 cards showing different threat counts
- Color-coded: green (safe), orange (warning), red (danger), blue (info)
- Cards include:
  - Total Packets
  - Total Alerts
  - Port Scans
  - SYN Floods
  - Brute Force
  - DDoS Attacks
  - IP Spoofing
  - MAC Spoofing
  - ARP Spoofing
  - DNS Tunneling
  - ICMP Floods
  - Unusual Protocols

#### 4. Configuration View

The configuration view provides controls for adjusting detection thresholds:

**Sections:**
- Port Scan Detection
- SYN Flood Detection
- DDoS Detection
- Brute Force Detection
- ICMP Flood Detection
- DNS Tunneling Detection
- Abnormal Traffic Detection
- IP/MAC Spoofing Detection
- Network Interface
- Capture Settings

**Each field shows:**
- Field name (like "PORT_SCAN_THRESHOLD")
- Description (what it does)
- Input box with current value

**Save Button:**
- Saves all configuration values to `src/config.json`
- Shows success message with file path

#### 5. Footer

Simple footer showing: "Made by Binam Adhikari 2026"

### Utility Functions

#### Saving Configuration

```python
def save_config_to_json(entry_widgets):
    config_data = {}
    
    for field_name, entry in entry_widgets.items():
        value = entry.get()
        try:
            if '.' in value:
                config_data[field_name] = float(value)
            elif value.lower() in ('true', 'false'):
                config_data[field_name] = value.lower() == 'true'
            else:
                config_data[field_name] = int(value)
        except ValueError:
            config_data[field_name] = value
    
    config_data['last_updated'] = datetime.now().isoformat()
    
    config_path = Path(__file__).parent.parent / 'config.json'
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        messagebox.showinfo("Success", f"Configuration saved to:\n{config_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
```

**What this does:**
- Collects all values from configuration input fields
- Converts them to appropriate types (int, float, bool, string)
- Adds timestamp
- Saves to JSON file
- Shows success or error message

**Type conversion logic:**
- If value contains a dot → float (like "0.6")
- If value is "true" or "false" → boolean
- Otherwise, try to convert to int
- If all fail, keep as string

#### Exporting Logs

```python
def export_logs_to_json(logs_text, alerts_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"argus_logs_{timestamp}.json"
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialfile=default_filename
    )
    
    if not filepath:
        return
    
    logs_content = logs_text.get("1.0", "end-1c")
    alerts_content = alerts_text.get("1.0", "end-1c")
    
    logs_list = [line.strip() for line in logs_content.split('\n') if line.strip()]
    alerts_list = [line.strip() for line in alerts_content.split('\n') if line.strip()]
    
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "total_packets": len(logs_list),
        "total_alerts": len(alerts_list),
        "packet_logs": logs_list,
        "threat_alerts": alerts_list
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=4)
        messagebox.showinfo("Success", f"Logs exported to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export logs:\n{str(e)}")
```

**What this does:**
- Creates default filename with current timestamp
- Opens file save dialog
- Gets all text from logs and alerts areas
- Splits into individual lines
- Creates JSON structure with metadata
- Saves to file
- Shows success or error message

**JSON structure:**
```json
{
  "export_timestamp": "2026-01-30T20:53:00",
  "total_packets": 1234,
  "total_alerts": 3,
  "packet_logs": [
    "[00:01:23] 192.168.1.100:54321 → 192.168.1.1:80 | TCP | SYN",
    ...
  ],
  "threat_alerts": [
    "[00:01:30] Port Scan: 192.168.1.100 tried 25 ports in 10s",
    ...
  ]
}
```

---

## Configuration System

Argus has two ways to configure detection thresholds:

### Method 1: Edit Source Code

Open `src/core/threat_detectors.py` and edit the constants at the top:

```python
PORT_SCAN_THRESHOLD = 20  # Change this number
PORT_SCAN_WINDOW = 10     # Change this number
```

**Pros:**
- Direct and simple
- Changes take effect immediately on restart

**Cons:**
- Need to edit code
- Easy to make syntax errors

### Method 2: Use GUI Configuration View

1. Run the GUI: `python src/gui/gui.py`
2. Click "Configuration" in the sidebar
3. Edit the values in the input fields
4. Click "Save" button
5. Configuration is saved to `src/config.json`

**Pros:**
- User-friendly
- No code editing required
- Can't break syntax

**Cons:**
- Currently, the saved config isn't automatically loaded (future feature)
- Need to manually update the Python file or add config loading code

### Configuration File Format

Saving configuration creates `src/config.json`:

```json
{
  "PORT_SCAN_THRESHOLD": 20,
  "PORT_SCAN_WINDOW": 10,
  "SYN_FLOOD_THRESHOLD": 100,
  "SYN_FLOOD_WINDOW": 5,
  ...
  "last_updated": "2026-01-30T20:53:00"
}
```


---

**Made by Binam Adhikari 2026**
**Made with love in Arch Linux btw ❤️**
