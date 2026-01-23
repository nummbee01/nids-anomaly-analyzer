from scapy.all import *
import sys

def select_interface():
    interfaces = get_if_list()
    for index, interface in enumerate(interfaces):
        print(f"{index} - {interface}")
    
    # Auto-select first interface for testing (change if needed)
    if len(interfaces) > 0:
        print(f"Auto-selecting {interfaces[2]} for testing")
        return interfaces[2]
    
    print("No interfaces found!")
    return None


def parse_ethernet(raw_data):
    """
    Parse Ethernet frame header from raw bytes

    Ethernet frame structure (14 bytes):
    Bytes 0-5: Destination MAC (6 bytes)
    Bytes 6-11: Source MAC (6 bytes)
    Bytes 12-13: EtherType (2 bytes) - 0x0800 = IPv4

    Returns: dict with src_mac, dst_mac, ethertype
    """
    if len(raw_data) < 14:
        raise ValueError("Invalid Ethernet frame")

    dst_mac = convert_bytes_to_mac(raw_data[:6])
    src_mac = convert_bytes_to_mac(raw_data[6:12])
    ethertype = raw_data[12:14].hex()
    return {"dst_mac": dst_mac, "src_mac": src_mac, "ethertype": ethertype}


def convert_bytes_to_mac(bytes):
    return ":".join(f"{byte:02x}" for byte in bytes)


def test_parse_ethernet():
    """Test with dummy data"""
    raw = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x08\x00"  # IPv4 EtherType

    result = parse_ethernet(raw)

    assert result["dst_mac"] == "00:01:02:03:04:05"
    assert result["src_mac"] == "06:07:08:09:0a:0b"
    assert result["ethertype"] == "0800"

    print("✓ Ethernet parsing test passed")


def process_and_print_packet(packet):
    """
    This function is called for each captured packet.
    It tests our parse_ethernet() function with real data.
    """
    try:
        # Convert Scapy packet to raw bytes
        raw_bytes = bytes(packet)
        
        # Ensure we have enough bytes
        if len(raw_bytes) < 14:
            return
        
        # Parse Ethernet header using OUR function
        eth_info = parse_ethernet(raw_bytes[:14])
        
        # Get Scapy's version for comparison
        if Ether in packet:
            scapy_src = packet[Ether].src
            scapy_dst = packet[Ether].dst
            scapy_type = hex(packet[Ether].type)
        else:
            scapy_src = scapy_dst = scapy_type = "N/A"
        
        # Print comparison
        print("\n" + "="*60)
        print("📦 PACKET ANALYSIS:")
        print("-"*60)
        
        print(f"OUR PARSER:")
        print(f"  Source MAC: {eth_info['src_mac']}")
        print(f"  Dest MAC:   {eth_info['dst_mac']}")
        print(f"  EtherType:  0x{eth_info['ethertype']}")
        
        print(f"\nSCAPY PARSER:")
        print(f"  Source MAC: {scapy_src}")
        print(f"  Dest MAC:   {scapy_dst}")
        print(f"  EtherType:  {scapy_type}")
        
        # Check if they match
        if Ether in packet:
            our_mac = eth_info['src_mac'].lower()
            scapy_mac = scapy_src.lower()
            
            if our_mac == scapy_mac:
                print("\n✅ SUCCESS: Our parser matches Scapy!")
            else:
                print(f"\n❌ MISMATCH: Our MAC: {our_mac}, Scapy MAC: {scapy_mac}")
        
        # Also show packet summary
        print(f"\n📋 Packet summary: {packet.summary()}")
        
        # Decode EtherType
        eth_type = int(eth_info['ethertype'], 16)
        if eth_type == 0x0800:
            print("🔍 Protocol: IPv4")
        elif eth_type == 0x0806:
            print("🔍 Protocol: ARP")
        elif eth_type == 0x86DD:
            print("🔍 Protocol: IPv6")
        else:
            print(f"🔍 Protocol: Unknown (0x{eth_type:04x})")
            
    except Exception as e:
        print(f"❌ Error processing packet: {e}")


def sniff_and_parse(interface, count=5):
    """
    Sniff packets and parse them using our custom parser
    """
    print(f"\n🚀 Starting packet capture on {interface}")
    print(f"Will capture {count} packets to test our parser")
    print("Press Ctrl+C to stop early\n")
    
    try:
        # Sniff packets and process each one
        sniff(
            iface=interface,
            prn=process_and_print_packet,
            count=count,
            store=False,
            timeout=30
        )
        print(f"\n✅ Successfully captured and parsed {count} packets!")
        
    except Exception as e:
        print(f"\n❌ Error during capture: {e}")


def main():
    print("="*60)
    print("ARGUS NIDS - PARSER TEST SCRIPT")
    print("="*60)
    
    # First, run unit test with dummy data
    print("\n🧪 Running unit test with dummy data...")
    try:
        test_parse_ethernet()
    except AssertionError:
        print("❌ Unit test failed! Fix parser first.")
        return
    
    # Select interface
    IFACE = select_interface()
    if IFACE is None:
        return
    
    # Ask how many packets to capture
    try:
        count = int(input("\nHow many packets to capture for testing? (Default: 5) ") or "5")
    except ValueError:
        count = 5
    
    # Start sniffing and parsing
    sniff_and_parse(IFACE, count)
    
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    # Run with sudo/administrator privileges
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_parse_ethernet()
    else:
        main()
