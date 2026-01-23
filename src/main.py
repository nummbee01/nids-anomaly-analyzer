import json  # for saving packet data
import os  # for file operations
from datetime import datetime  # for timestamps of packets

from scapy.all import *

# Disable verbose output to keep console clean
conf.verb = 0

# Most commonly attacked ports
suspicious_ports = [22, 23, 25, 80, 443]

# Example blacklists
blacklisted_ips = ["192.168.1.1", "192.168.1.2"]

# Initialize variables
total_packets = 0
threats_detected = 0
blocked_ips = set()


# Save packet to log file
def save_packet_log(packet_info):
    try:
        with open("packet_log.json", "a") as f:
            json.dump(packet_info, f)
            f.write("\n")
    except Exception as e:
        print(f"Error saving packet log: {e}")


# Save alert to log file
def save_alert_log(alert):
    try:
        with open("alert_log.json", "a") as f:
            f.write(f"{alert}\n")
    except Exception as e:
        print(f"Error saving alert: {e}")


# Analyze packets
def analyze_threats(packet_info):
    return
