import unittest
from scapy.all import *
import sys
import os

# Add the core directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from packet_parser import (
    parse_ethernet, parse_ipv4, parse_ipv6, parse_tcp, parse_udp, 
    parse_icmpv4, parse_icmpv6
)


class TestPacketParsing(unittest.TestCase):
    """Test packet parsing functions against Scapy's built-in parsing"""

    def setUp(self):
        """Create test packets for comparison"""
        # Create a simple TCP packet
        self.tcp_packet = Ether()/IP(src="192.168.1.1", dst="10.0.0.1")/TCP(sport=12345, dport=80)/Raw(b"test data")
        
        # Create a UDP packet
        self.udp_packet = Ether()/IP(src="192.168.1.2", dst="10.0.0.2")/UDP(sport=54321, dport=53)/Raw(b"dns query")
        
        # Create an ICMP packet
        self.icmp_packet = Ether()/IP(src="192.168.1.3", dst="10.0.0.3")/ICMP(type=8, code=0)/Raw(b"ping data")
        
        # Create an IPv6 packet
        self.ipv6_packet = Ether()/IPv6(src="2001:db8::1", dst="2001:db8::2")/TCP(sport=80, dport=443)

    def test_parse_ethernet_comparison(self):
        """Test Ethernet parsing against Scapy"""
        raw = bytes(self.tcp_packet)
        manual_result = parse_ethernet(raw[:14])
        
        self.assertEqual(manual_result["src_mac"], self.tcp_packet[Ether].src)
        self.assertEqual(manual_result["dst_mac"], self.tcp_packet[Ether].dst)
        self.assertEqual(manual_result["ethertype"], "0800")  # IPv4

    def test_parse_ipv4_comparison(self):
        """Test IPv4 parsing against Scapy"""
        raw = bytes(self.tcp_packet)
        # Skip Ethernet header (14 bytes) to get to IP
        ip_data = raw[14:]
        manual_result = parse_ipv4(ip_data[:20])
        
        self.assertEqual(manual_result["src_ip"], self.tcp_packet[IP].src)
        self.assertEqual(manual_result["dst_ip"], self.tcp_packet[IP].dst)
        self.assertEqual(manual_result["protocol"], self.tcp_packet[IP].proto)

    def test_parse_ipv6_comparison(self):
        """Test IPv6 parsing against Scapy"""
        raw = bytes(self.ipv6_packet)
        # Skip Ethernet header (14 bytes) to get to IPv6
        ipv6_data = raw[14:]
        manual_result = parse_ipv6(ipv6_data[:40])
        
        self.assertEqual(manual_result["src_ip"], self.ipv6_packet[IPv6].src)
        self.assertEqual(manual_result["dst_ip"], self.ipv6_packet[IPv6].dst)

    def test_parse_tcp_comparison(self):
        """Test TCP parsing against Scapy"""
        raw = bytes(self.tcp_packet)
        # Skip Ethernet (14) + IP (20) = 34 bytes to get to TCP
        tcp_data = raw[34:]
        manual_result = parse_tcp(tcp_data[:20])
        
        self.assertEqual(manual_result["src_port"], self.tcp_packet[TCP].sport)
        self.assertEqual(manual_result["dst_port"], self.tcp_packet[TCP].dport)
        self.assertEqual(manual_result["seq_num"], self.tcp_packet[TCP].seq)
        self.assertEqual(manual_result["ack_num"], self.tcp_packet[TCP].ack)

    def test_parse_udp_comparison(self):
        """Test UDP parsing against Scapy"""
        raw = bytes(self.udp_packet)
        # Skip Ethernet (14) + IP (20) = 34 bytes to get to UDP
        udp_data = raw[34:]
        manual_result = parse_udp(udp_data[:8])
        
        self.assertEqual(manual_result["src_port"], self.udp_packet[UDP].sport)
        self.assertEqual(manual_result["dst_port"], self.udp_packet[UDP].dport)
        self.assertEqual(manual_result["length"], self.udp_packet[UDP].len)
        self.assertEqual(manual_result["checksum"], self.udp_packet[UDP].chksum)

    def test_parse_icmpv4_comparison(self):
        """Test ICMPv4 parsing against Scapy"""
        raw = bytes(self.icmp_packet)
        # Skip Ethernet (14) + IP (20) = 34 bytes to get to ICMP
        icmp_data = raw[34:]
        manual_result = parse_icmpv4(icmp_data[:8])
        
        self.assertEqual(manual_result["type"], self.icmp_packet[ICMP].type)
        self.assertEqual(manual_result["code"], self.icmp_packet[ICMP].code)
        self.assertEqual(manual_result["checksum"], self.icmp_packet[ICMP].chksum)
        self.assertEqual(manual_result["identifier"], self.icmp_packet[ICMP].id)
        self.assertEqual(manual_result["sequence"], self.icmp_packet[ICMP].seq)

    def compare_with_scapy(self, packet, manual):
        """
        Compare manual parsing results with Scapy's built-in parsing
        
        Args:
            packet: Scapy packet object
            manual: dict with manually parsed packet information
            
        Returns:
            bool: True if all fields match, False otherwise
        """
        try:
            # Ethernet
            if packet.haslayer(Ether):
                eth = packet[Ether]
                if manual.get("src_mac") != eth.src or manual.get("dst_mac") != eth.dst:
                    return False

            # IPv4
            if packet.haslayer(IP):
                ip = packet[IP]
                if manual.get("src_ip") != ip.src or manual.get("dst_ip") != ip.dst:
                    return False
                if manual.get("protocol") != ip.proto:
                    return False

            # IPv6
            if packet.haslayer(IPv6):
                ip6 = packet[IPv6]
                if manual.get("src_ip") != ip6.src or manual.get("dst_ip") != ip6.dst:
                    return False

            # TCP
            if packet.haslayer(TCP):
                tcp = packet[TCP]
                if (
                    manual.get("src_port") != tcp.sport
                    or manual.get("dst_port") != tcp.dport
                ):
                    return False
                if manual.get("seq_num") != tcp.seq or manual.get("ack_num") != tcp.ack:
                    return False

            # UDP
            if packet.haslayer(UDP):
                udp = packet[UDP]
                if (
                    manual.get("src_port") != udp.sport
                    or manual.get("dst_port") != udp.dport
                ):
                    return False

            # ICMPv4
            if packet.haslayer(ICMP):
                icmp = packet[ICMP]
                if manual.get("type") != icmp.type or manual.get("code") != icmp.code:
                    return False

            # ICMPv6
            if packet.haslayer(ICMPv6EchoRequest) or packet.haslayer(ICMPv6EchoReply):
                icmp6 = packet.getlayer(ICMPv6EchoRequest) or packet.getlayer(
                    ICMPv6EchoReply
                )
                if manual.get("type") != icmp6.type or manual.get("code") != icmp6.code:
                    return False

            return True

        except Exception:
            return False

    def test_full_packet_comparison_tcp(self):
        """Test complete packet comparison for TCP packet"""
        raw = bytes(self.tcp_packet)
        remaining = raw
        
        # Parse manually
        eth = parse_ethernet(remaining[:14])
        remaining = remaining[14:]
        ip = parse_ipv4(remaining[:20])
        remaining = remaining[20:]
        tcp = parse_tcp(remaining[:20])
        
        manual_data = {**eth, **ip, **tcp}
        
        # Test comparison function
        self.assertTrue(self.compare_with_scapy(self.tcp_packet, manual_data))

    def test_full_packet_comparison_udp(self):
        """Test complete packet comparison for UDP packet"""
        raw = bytes(self.udp_packet)
        remaining = raw
        
        # Parse manually
        eth = parse_ethernet(remaining[:14])
        remaining = remaining[14:]
        ip = parse_ipv4(remaining[:20])
        remaining = remaining[20:]
        udp = parse_udp(remaining[:8])
        
        manual_data = {**eth, **ip, **udp}
        
        # Test comparison function
        self.assertTrue(self.compare_with_scapy(self.udp_packet, manual_data))

    def test_full_packet_comparison_icmp(self):
        """Test complete packet comparison for ICMP packet"""
        raw = bytes(self.icmp_packet)
        remaining = raw
        
        # Parse manually
        eth = parse_ethernet(remaining[:14])
        remaining = remaining[14:]
        ip = parse_ipv4(remaining[:20])
        remaining = remaining[20:]
        icmp = parse_icmpv4(remaining[:8])
        
        manual_data = {**eth, **ip, **icmp}
        
        # Test comparison function
        self.assertTrue(self.compare_with_scapy(self.icmp_packet, manual_data))


if __name__ == '__main__':
    unittest.main()