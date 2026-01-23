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


# Parsing Data


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
    elif eth_type == 0x0806:
        print("🔍 Protocol: ARP")
    elif eth_type == 0x86DD:
        print("🔍 Protocol: IPv6")
    else:
        print(f"🔍 Protocol: Unknown (0x{eth_type:04x})")


def main():
    IFACE = select_interface()
    sniffing_interface(IFACE)


if __name__ == "__main__":
    main()
