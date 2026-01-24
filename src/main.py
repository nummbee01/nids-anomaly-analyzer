from scapy.all import *


def select_interface():
    interfaces = get_if_list()
    for index, interface in enumerate(interfaces):
        print(f"{index} - {interface}")
    try:
        choice = int(input("Select an interface: "))
    except ValueError:
        print("Invalid input")
        print(f"Auto-selecting {interfaces[2]} for testing")
        return interfaces[2]
    if choice < 0 or choice >= len(interfaces):
        print("Invalid choice")
        print(f"Auto-selecting {interfaces[2]} for testing")
        return interfaces[2]
    return interfaces[choice]


def show_summary(pkt):
    print(pkt.summary())


def sniffing_interface(interface):
    sniff(iface=interface, prn=print_packet_info, count=5, store=False)


# Converting raw data


def convert_bytes_to_mac(bytes):
    return ":".join(f"{byte:02x}" for byte in bytes)


def convert_bytes_to_ipv4(bytes):
    return ".".join(f"{byte}" for byte in bytes)


def convert_bytes_to_ipv6(bytes):
    return ":".join(f"{byte:02x}" for byte in bytes)


# Parse Ethernet


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


# Parse IPv4


def parse_ipv4(raw_data):
    """
    Parse IPv4 header from raw bytes

    IPv4 Header (20 bytes minimum):
    Byte 0: Version (4 bits) + Header Length (4 bits)
    Byte 1: Type of Service
    Bytes 2-3: Total Length
    Bytes 4-5: Identification
    Bytes 6-7: Flags + Fragment Offset
    Byte 8: Time to Live (TTL)
    Byte 9: Protocol (6=TCP, 17=UDP, 1=ICMP)
    Bytes 10-11: Header Checksum
    Bytes 12-15: Source IP (4 bytes)
    Bytes 16-19: Destination IP (4 bytes)

    Returns: dict with version, ihl, protocol, src_ip, dst_ip, ttl, total_length
    """

    src_ip = convert_bytes_to_ipv4(raw_data[12:16])
    dst_ip = convert_bytes_to_ipv4(raw_data[16:20])
    protocol = int(raw_data[9])
    return {
        "protocol": protocol,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    }


def parse_ipv6(raw_data):
    """
    Parse IPv6 header from raw bytes

    IPv6 Header (40 bytes fixed):
    Bytes 0-3: Version (4 bits) + Traffic Class (8 bits) + Flow Label (20 bits)
    Bytes 4-5: Payload Length (16 bits)
    Byte 6: Next Header (8 bits) -> same as IPv4 protocol
    Byte 7: Hop Limit (8 bits) -> same as TTL
    Bytes 8-23: Source Address (128 bits, 16 bytes)
    Bytes 24-39: Destination Address (128 bits, 16 bytes)

    Returns: dict with version, payload_length, next_header, hop_limit, src_ip, dst_ip
    """
    src_ip = convert_bytes_to_ipv6(raw_data[8:24])
    dst_ip = convert_bytes_to_ipv6(raw_data[24:40])
    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    }


# Print Packet Information


def print_packet_info(pkt):
    raw_bytes = bytes(pkt)
    eth_info = parse_ethernet(raw_bytes[:14])

    print("=" * 40)
    print(f"Source MAC: {eth_info['src_mac']}")
    print(f"Destination MAC: {eth_info['dst_mac']}")
    print(f"EtherType: 0x{eth_info['ethertype']}")

    # Decode EtherType
    eth_type = int(eth_info["ethertype"], 16)

    if eth_type == 0x0800:
        print("🔍 Protocol: IPv4")
        ip_info = parse_ipv4(raw_bytes[14:34])
        print(f"IPv4: {ip_info['src_ip']} -> {ip_info['dst_ip']}")
    elif eth_type == 0x86DD:
        print("🔍 Protocol: IPv6")
        ip_info = parse_ipv6(raw_bytes[14:54])
        print(f"IPv6: {ip_info['src_ip']} -> {ip_info['dst_ip']}")
    elif eth_type == 0x0806:
        print("🔍 Protocol: ARP")
    else:
        print(f"🔍 Protocol: Unknown (0x{eth_type:04x})")


def main():
    IFACE = select_interface()
    sniffing_interface(IFACE)


if __name__ == "__main__":
    main()
