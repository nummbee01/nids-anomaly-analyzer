from scapy.all import *

def analyze_packet(packet):
    print("=" * 60)

    # Ethernet layer
    if packet.haslayer(Ether):
        print(f"Ethernet: {packet[Ether].src} -> {packet[Ether].dst}")

    # IP layer
    if packet.haslayer(IP):
        print(f"IP: {packet[IP].src} -> {packet[IP].dst}")
        print(f"Protocol: {packet[IP].proto}")
        print(f"TTL: {packet[IP].ttl}")

    # TCP layer
    if packet.haslayer(TCP):
        print(f"TCP: Port {packet[TCP].sport} -> {packet[TCP].dport}")
        print(f"Flags: {packet[TCP].flags}")
        print(f"Seq: {packet[TCP].seq}, Ack: {packet[TCP].ack}")

    # UDP layer
    if packet.haslayer(UDP):
        print(f"UDP: Port {packet[UDP].sport} -> {packet[UDP].dport}")
        print(f"Length: {packet[UDP].len}")

    # ICMP layer
    if packet.haslayer(ICMP):
        print(f"ICMP: Type {packet[ICMP].type}, Code {packet[ICMP].code}")

    # Raw payload
    if packet.haslayer(Raw):
        payload = packet[Raw].load
        print(f"Payload (bytes): {len(payload)}")
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
            print(f"Payload (text): {payload_str}")
        except:
            print("Payload: [Binary data]")

    print()

# Read packets from file
print("Reading packets from sample_packets.pcap...\n")
packets = rdpcap("sample_packets.pcap")

print(f"Total packets captured: {len(packets)}\n")

# Analyze each packet
for i, packet in enumerate(packets, 1):
    print(f"PACKET #{i}")
    analyze_packet(packet)
