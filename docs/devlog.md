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
```

# Day 1

NIDS is a system that tracks the network traffic and detect malicious activities.

I'll use Streamlit + Scapy for this. In Streamlit, there is a menu bar with buttons : start, stop, clear logs. Then, dropdown to filter threats. Others are Status, and Statistics, which include Total Packets, Threats Detected, Blocked IPs, and current rate. The main page will have a graph that changes dynamically based on the selected time range. There's live packets and alert log below.

## Things to learn:

- Streamlit
- Scapy
