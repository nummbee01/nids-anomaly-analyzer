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

    Returns: protocol, src_ip, dst_ip
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

    Returns: src_ip, dst_ip
    """
    src_ip = convert_bytes_to_ipv6(raw_data[8:24])
    dst_ip = convert_bytes_to_ipv6(raw_data[24:40])
    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    }


def parse_tcp(raw_data):
    """
    Parse TCP header from raw bytes

    TCP Header (minimum 20 bytes):
    Bytes 0-1: Source Port (16 bits)
    Bytes 2-3: Destination Port (16 bits)
    Bytes 4-7: Sequence Number (32 bits)
    Bytes 8-11: Acknowledgment Number (32 bits)
    Byte 12: Data Offset (4 bits) + Reserved (4 bits)
    Byte 13: Flags (8 bits)
    Bytes 14-15: Window Size (16 bits)
    Bytes 16-17: Checksum (16 bits)
    Bytes 18-19: Urgent Pointer (16 bits)

    Returns: dict with src_port, dst_port, seq_num, ack_num
    """

    src_port = int.from_bytes(raw_data[0:2], byteorder="big")
    dst_port = int.from_bytes(raw_data[2:4], byteorder="big")
    seq_num = int.from_bytes(raw_data[4:8], byteorder="big")
    ack_num = int.from_bytes(raw_data[8:12], byteorder="big")

    return {
        "src_port": src_port,
        "dst_port": dst_port,
        "seq_num": seq_num,
        "ack_num": ack_num,
    }


def parse_udp(raw_data):
    """
    Parse UDP header from raw bytes

    UDP Header (8 bytes):
    Bytes 0-1: Source Port (16 bits)
    Bytes 2-3: Destination Port (16 bits)
    Bytes 4-5: Length (16 bits)
    Bytes 6-7: Checksum (16 bits)

    Returns: dict with src_port, dst_port, length, checksum
    """

    src_port = int.from_bytes(raw_data[0:2], byteorder="big")
    dst_port = int.from_bytes(raw_data[2:4], byteorder="big")
    length = int.from_bytes(raw_data[4:6], byteorder="big")
    checksum = int.from_bytes(raw_data[6:8], byteorder="big")

    return {
        "src_port": src_port,
        "dst_port": dst_port,
        "length": length,
        "checksum": checksum,
    }


def parse_icmpv4(raw_data):
    """
    Parse ICMP message from raw bytes

    ICMP Header (8 bytes minimum):
    Byte 0: Type (8 bits)
    Byte 1: Code (8 bits)
    Bytes 2-3: Checksum (16 bits)
    Bytes 4-5: Identifier (16 bits) - for Echo Request/Reply
    Bytes 6-7: Sequence Number (16 bits) - for Echo Request/Reply

    Returns: dict with type, code, checksum, identifier, sequence
    """

    type = raw_data[0]
    code = raw_data[1]
    checksum = int.from_bytes(raw_data[2:4], byteorder="big")
    identifier = int.from_bytes(raw_data[4:6], byteorder="big")
    sequence = int.from_bytes(raw_data[6:8], byteorder="big")

    return {
        "type": type,
        "code": code,
        "checksum": checksum,
        "identifier": identifier,
        "sequence": sequence,
    }


def parse_icmpv6(raw_data):
    """
    Parse ICMPv6 message from raw bytes

    ICMPv6 Header (8 bytes minimum):
    Byte 0: Type (8 bits)
    Byte 1: Code (8 bits)
    Bytes 2-3: Checksum (16 bits)
    Bytes 4-7: Reserved (32 bits)

    Returns: dict with type, code, checksum
    """

    type = raw_data[0]
    code = raw_data[1]
    checksum = int.from_bytes(raw_data[2:4], byteorder="big")

    return {
        "type": type,
        "code": code,
        "checksum": checksum,
    }


def print_packet_info(packet):
    return


def main():
    IFACE = select_interface()
    sniffing_interface(IFACE)


if __name__ == "__main__":
    main()
