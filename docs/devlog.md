This project was initialized on 7th January 2026.

# Setting up Git and Github

Commands used:

```bash
# Creating directory
mkdir nids-anomaly-analyzer
cd nids-anomaly-analyzer
# Setting up Git
git init
git branch -M main
touch README.md
git add .
git commit -m "Added README file"
# Pushing to Github
git remote add origin https://github.com/nummbee01/nids-anomaly-analyzer.git
git push -u origin main
# Adding a virtual environment
python3 -m venv venv
source venv/bin/activate.fish # because I am using fish shell
pip install -r requirements.txt
```

# Day 1

NIDS is a system that tracks the network traffic and detect malicious activities.

I'll use Streamlit + Scapy for this. In Streamlit, there is a menu bar with buttons : start, stop, clear logs. Then, dropdown to filter threats. Others are Status, and Statistics, which include Total Packets, Threats Detected, Blocked IPs, and current rate. The main page will have a graph that changes dynamically based on the selected time range. There's live packets and alert log below.

## Things to learn:

- Streamlit
- Scapy

# Day 2

Applied git branching using the following commands:

```bash
git switch -c testing
git push -u origin testing

git branch # too see current branch
```

Learned the basics of Scapy, including how to make packets, send packets, sniff packets, and filter packets, and analyze them.

## Logic behind the NIDS

1. Sniffs packets
2. Analyzes packets
3. Detects anomalies
4. Blocks malicious traffic
5. Logs alerts

## Cases that triggers alerts

- Same IP tries multiple ports in short time
- Massive SYN packets being sent
- IP spoofing
- ARP spoofing (impersonates another device on local network)
- DDoS attacks
- Malicious packets
- Brute force attacks
- ICMP flood
- DNS Tunneling
- Unusual protocol usage
- Abnormal traffic patterns
- MAC spoofing

# Day 3 

Parsed the data successfully and created custom data structures to store the information.

Next, I'll implement the rule-based detection system.

# Day 4

- Implemented rule-based threat detection system with 12 detection algorithms
- Made all detection thresholds configurable via constants at the top of threat_detectors.py
- Reduced false positives by adding filtering logic for spoofing detection and increasing threshold values
- Refactored packet_capture.py to use callback architecture for GUI integration
- Built complete Tkinter GUI with:
  - Dashboard: packet logs, threat alerts, statistics, matplotlib graph placeholder
  - Configuration view: editable threshold fields
  - Dynamic Start/Stop button, Clear Logs button, Export Logs button
- Added JSON export for logs and configuration save functionality
- Cleaned up code by removing excessive comments
- Created .gitignore file
- Switched from CLI-focused to GUI-focused architecture

# Day 5

- Fixed Stop button functionality by implementing AsyncSniffer instead of blocking sniff()
  - Modified packet_capture.py to return AsyncSniffer object for controllable start/stop
  - Updated GUI to store sniffer object and call .stop() method when stopping
  - Stop button now properly terminates packet capture immediately
- Changed default network interface to wlan0 (wireless) with fallback logic
  - Prefers wlan0 if available, otherwise uses first available interface
  - Falls back to eth0 if no interfaces detected
- Disabled MAC Spoofing detection due to excessive false positives
  - Commented out detect_mac_spoofing() function in threat_detectors.py
  - Removed MAC spoofing from GUI statistics display (11 threat categories instead of 12)
  - False positives caused by legitimate routers, gateways, DHCP servers, and NAT devices
- Implemented thread-safety improvements in GUI
  - Wrapped all GUI updates in root.after(0, update_gui) to ensure main thread execution
  - Prevents race conditions and crashes from cross-thread widget access
- Fixed blank timestamp lines in packet logs
  - Modified gui_callback() to only insert log entries when IPv4 or IPv6 data exists
  - Filters out non-IP packets (ARP, malformed packets) for cleaner log output
- Integrated GUI with main.py as primary entry point
  - Removed all CLI functionality from main.py
  - Application now launches GUI directly with python3 main.py
- Added network interface dropdown menu in Configuration view
  - Replaced text entry with Combobox widget showing all available interfaces
  - Read-only mode prevents invalid interface names
- Updated documentation101.md with all recent changes
  - Integrated AsyncSniffer documentation in Packet Capture section
  - Documented MAC Spoofing disable with explanation in Threat Detection section
  - Added GUI improvements sections for thread-safety, interface selection, and log filtering
  - Removed changelog section and integrated information into appropriate technical sections
