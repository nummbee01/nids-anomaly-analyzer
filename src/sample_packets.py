from scapy.all import *

# Create various sample packets
packets = []

# 1. HTTP request (TCP to port 80)
http_packet = Ether()/IP(src="192.168.1.100", dst="93.184.216.34")/TCP(sport=54321, dport=80, flags="S")
packets.append(http_packet)

# 2. HTTPS request (TCP to port 443)
https_packet = Ether()/IP(src="192.168.1.100", dst="142.250.185.46")/TCP(sport=54322, dport=443, flags="PA")
packets.append(https_packet)

# 3. DNS query (UDP to port 53)
dns_packet = Ether()/IP(src="192.168.1.100", dst="8.8.8.8")/UDP(sport=53241, dport=53)
packets.append(dns_packet)

# 4. ICMP ping
icmp_packet = Ether()/IP(src="192.168.1.100", dst="1.1.1.1")/ICMP()
packets.append(icmp_packet)

# 5. SSH connection (TCP to port 22)
ssh_packet = Ether()/IP(src="192.168.1.100", dst="192.168.1.50")/TCP(sport=54323, dport=22, flags="S")
packets.append(ssh_packet)

# 6. Suspicious packet with payload
malicious_packet = Ether()/IP(src="10.0.0.50", dst="192.168.1.100")/TCP(sport=12345, dport=80)/Raw(load="<script>alert('xss')</script>")
packets.append(malicious_packet)

# Save to file
wrpcap("sample_packets.pcap", packets)
print("Sample packets saved to sample_packets.pcap")
