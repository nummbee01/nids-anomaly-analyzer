from scapy.all import sniff, wrpcap

print("[*] Capturing 100 packets...")
packets = sniff(iface="wlp8s0", count=100)
wrpcap("captured.pcap", packets)
print(f"[*] Captured {len(packets)} packets and saved to captured.pcap")
