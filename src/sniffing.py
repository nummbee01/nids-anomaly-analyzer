from scapy.all import *

def analyze_packet(pkt):
    print(pkt.summary())
    if Ether in pkt:
        print(f"MAC Src: {pkt[Ether].src} -> Dst: {pkt[Ether].dst}")
    if IP in pkt:
        print(f"IP Src: {pkt[IP].src} -> Dst: {pkt[IP].dst}")
        proto = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(pkt[IP].proto, "Other")
        print(f"Protocol: {proto}")
    if TCP in pkt:
        print(f"Ports: {pkt[TCP].sport} -> {pkt[TCP].dport}")
    elif UDP in pkt:
        print(f"Ports: {pkt[UDP].sport} -> {pkt[UDP].dport}")
    print("-" * 40)

print("Sniffing 5 packets...")
packets = sniff(count=5)  # Add iface="your_interface" if needed
for i, pkt in enumerate(packets, 1):
    print(f"\nPacket {i}:")
    analyze_packet(pkt)
