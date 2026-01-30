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
