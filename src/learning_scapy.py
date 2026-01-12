from scapy.all import *

# Most basic packet

# p = IP()
# p.show()

# Packet with source and destination IP addresses

# p = IP(src="192.168.1.1", dst="192.168.1.2")
# p.show()
# print(p.summary())  # one line output

# Packet sniffing

# packets = sniff(filter="ip", count=3)

# for packet in packets:
#     print(packet.show())

# Filtering packets while sniffing

# packets = sniff(filter="ip", count=3, prn=lambda x: x.summary())

# Writing packets to a file

# pkts = sniff(filter="ip", count=3)
# wrpcap("packets.pcap", pkts)

# Reading packets from a file

# packets = rdpcap("packets.pcap")
# packets.show()

# Basic detection


def detect_syn_scan(pkt):
    if pkt.haslayer(TCP) and pkt[TCP].flags == "S":
        print(f"SYN scan? {pkt[IP].src} → {pkt[IP].dst}:{pkt[TCP].dport}")


sniff(iface="lo", filter="tcp", prn=detect_syn_scan, store=0)
