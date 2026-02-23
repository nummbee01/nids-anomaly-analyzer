from scapy.all import AsyncSniffer, get_if_list

from .packet_parser import (
    parse_ethernet,
    parse_ipv4,
    parse_ipv6,
    parse_tcp,
    parse_udp,
    parse_icmpv4,
    parse_icmpv6,
)
from .threat_detectors import analyze_packet


def select_interface():
    interfaces = get_if_list()
    for index, interface in enumerate(interfaces):
        print(f"{index} - {interface}")
    try:
        choice = int(input("Select an interface: "))
    except ValueError:
        print("Invalid input")
        print(f"Auto-selecting {interfaces[0]} for testing")
        return interfaces[0]
    if choice < 0 or choice >= len(interfaces):
        print("Invalid choice")
        print(f"Auto-selecting {interfaces[0]} for testing")
        return interfaces[0]
    return interfaces[choice]


def create_packet_handler(state, callback=None):
    packet_count = [0]
    
    def packet_handler(packet):
        packet_count[0] += 1
        
        try:
            raw = bytes(packet)
            if len(raw) < 14:
                return
            
            # Parse Ethernet layer
            ethernet = parse_ethernet(raw[:14])
            remaining = raw[14:]
            ethertype = ethernet.ethertype
            
            ipv4 = None
            ipv6 = None
            tcp = None
            udp = None
            icmp = None
            
            if ethertype == "0800" and len(remaining) >= 20:
                ipv4 = parse_ipv4(remaining[:20])
                remaining = remaining[20:]
                proto = ipv4.protocol
                
                if proto == 6 and len(remaining) >= 20:
                    tcp = parse_tcp(remaining[:20])
                elif proto == 17 and len(remaining) >= 8:
                    udp = parse_udp(remaining[:8])
                elif proto == 1 and len(remaining) >= 8:
                    icmp = parse_icmpv4(remaining[:8])
            
            elif ethertype == "86dd" and len(remaining) >= 40:
                ipv6 = parse_ipv6(remaining[:40])
                remaining = remaining[40:]
                if remaining and remaining[0] == 58 and len(remaining) >= 8:
                    icmp = parse_icmpv6(remaining[:8])
            
            alerts = analyze_packet(
                state,
                ethernet=ethernet,
                ipv4=ipv4,
                ipv6=ipv6,
                tcp=tcp,
                udp=udp,
                icmp=icmp,
            )
            
            if callback:
                packet_info = {
                    'packet_num': packet_count[0],
                    'ethernet': ethernet,
                    'ipv4': ipv4,
                    'ipv6': ipv6,
                    'tcp': tcp,
                    'udp': udp,
                    'icmp': icmp,
                }
                callback(packet_info, alerts)
        
        except Exception as e:
            pass
    
    return packet_handler


def start_capture(interface, state, callback=None, count=0):
    """Start packet capture and return AsyncSniffer object for control"""
    handler = create_packet_handler(state, callback)
    sniffer = AsyncSniffer(
        iface=interface,
        prn=handler,
        count=count if count > 0 else 0,
        store=False,
    )
    sniffer.start()
    return sniffer
