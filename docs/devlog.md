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
