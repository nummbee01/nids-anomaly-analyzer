from dataclasses import asdict
from scapy.all import *
from src.utils.data_structures import *


def bytes_to_mac(b: bytes) -> str:
    return ":".join(f"{byte:02x}" for byte in b)


def bytes_to_ipv4(b: bytes) -> str:
    return ".".join(str(byte) for byte in b)


def bytes_to_ipv6(b: bytes) -> str:
    return ":".join(f"{b[i]:02x}{b[i + 1]:02x}" for i in range(0, 16, 2))


def parse_ethernet(raw: bytes) -> Ethernet:
    if len(raw) < 14:
        raise ValueError("Invalid Ethernet frame")

    return Ethernet(
        dst_mac=bytes_to_mac(raw[0:6]),
        src_mac=bytes_to_mac(raw[6:12]),
        ethertype=raw[12:14].hex(),
    )


def parse_ipv4(raw: bytes) -> IPv4:
    return IPv4(
        protocol=raw[9],
        src_ip=bytes_to_ipv4(raw[12:16]),
        dst_ip=bytes_to_ipv4(raw[16:20]),
    )


def parse_ipv6(raw: bytes) -> IPv6:
    return IPv6(
        src_ip=bytes_to_ipv6(raw[8:24]),
        dst_ip=bytes_to_ipv6(raw[24:40]),
    )


def parse_tcp(raw: bytes) -> TCP:
    return TCP(
        src_port=int.from_bytes(raw[0:2], "big"),
        dst_port=int.from_bytes(raw[2:4], "big"),
        seq_num=int.from_bytes(raw[4:8], "big"),
        ack_num=int.from_bytes(raw[8:12], "big"),
    )


def parse_udp(raw: bytes) -> UDP:
    return UDP(
        src_port=int.from_bytes(raw[0:2], "big"),
        dst_port=int.from_bytes(raw[2:4], "big"),
        length=int.from_bytes(raw[4:6], "big"),
        checksum=int.from_bytes(raw[6:8], "big"),
    )


def parse_icmpv4(raw: bytes) -> ICMPv4:
    return ICMPv4(
        type=raw[0],
        code=raw[1],
        checksum=int.from_bytes(raw[2:4], "big"),
        identifier=int.from_bytes(raw[4:6], "big"),
        sequence=int.from_bytes(raw[6:8], "big"),
    )


def parse_icmpv6(raw: bytes) -> ICMPv6:
    return ICMPv6(
        type=raw[0],
        code=raw[1],
        checksum=int.from_bytes(raw[2:4], "big"),
    )


def compare_with_scapy(packet, manual) -> bool:
    try:
        if isinstance(manual, Ethernet) and packet.haslayer(Ether):
            eth = packet[Ether]
            return (
                manual.src_mac == eth.src
                and manual.dst_mac == eth.dst
                and manual.ethertype == f"{eth.type:04x}"
            )

        if isinstance(manual, IPv4) and packet.haslayer(IP):
            ip = packet[IP]
            return (
                manual.src_ip == ip.src
                and manual.dst_ip == ip.dst
                and manual.protocol == ip.proto
            )

        if isinstance(manual, IPv6) and packet.haslayer(IPv6):
            ip6 = packet[IPv6]
            return manual.src_ip == ip6.src and manual.dst_ip == ip6.dst

        if isinstance(manual, TCP) and packet.haslayer(TCP):
            tcp = packet[TCP]
            return (
                manual.src_port == tcp.sport
                and manual.dst_port == tcp.dport
                and manual.seq_num == tcp.seq
                and manual.ack_num == tcp.ack
            )

        if isinstance(manual, UDP) and packet.haslayer(UDP):
            udp = packet[UDP]
            return manual.src_port == udp.sport and manual.dst_port == udp.dport

        if isinstance(manual, ICMPv4) and packet.haslayer(ICMP):
            icmp = packet[ICMP]
            return manual.type == icmp.type and manual.code == icmp.code

        if isinstance(manual, ICMPv6):
            icmp6 = packet.getlayer(ICMPv6EchoRequest) or packet.getlayer(
                ICMPv6EchoReply
            )
            return icmp6 and manual.type == icmp6.type and manual.code == icmp6.code

        return False

    except Exception:
        return False


def print_packet_info(packet):
    try:
        print("*" * 80)
        raw = bytes(packet)
        remaining = raw

        # Ethernet
        eth = parse_ethernet(remaining[:14])
        remaining = remaining[14:]
        print("[Ethernet]")
        print(f"dst_mac: {eth.dst_mac}")
        print(f"src_mac: {eth.src_mac}")
        print(f"ethertype: {eth.ethertype}")

        ethertype = eth.ethertype

        # IPv4
        if ethertype == "0800" and len(remaining) >= 20:
            ip = parse_ipv4(remaining[:20])
            remaining = remaining[20:]
            print(f"src_ip: {ip.src_ip}")
            print(f"dst_ip: {ip.dst_ip}")
            print(f"protocol: {ip.protocol}")

            proto = ip.protocol

            if proto == 6 and len(remaining) >= 20:  # TCP
                tcp = parse_tcp(remaining[:20])
                remaining = remaining[20:]
                print("[TCP]")
                print(f"src_port: {tcp.src_port}")
                print(f"dst_port: {tcp.dst_port}")
                print(f"seq_num: {tcp.seq_num}")
                print(f"ack_num: {tcp.ack_num}")

            elif proto == 17 and len(remaining) >= 8:  # UDP
                udp = parse_udp(remaining[:8])
                remaining = remaining[8:]
                print("[UDP]")
                print(f"src_port: {udp.src_port}")
                print(f"dst_port: {udp.dst_port}")
                print(f"length: {udp.length}")
                print(f"checksum: {udp.checksum}")

            elif proto == 1 and len(remaining) >= 8:  # ICMPv4
                icmp = parse_icmpv4(remaining[:8])
                remaining = remaining[8:]
                print("[ICMPv4]")
                print(f"type: {icmp.type}")
                print(f"code: {icmp.code}")
                print(f"checksum: {icmp.checksum}")
                print(f"identifier: {icmp.identifier}")
                print(f"sequence: {icmp.sequence}")

        # IPv6
        elif ethertype == "86dd" and len(remaining) >= 40:
            ip6 = parse_ipv6(remaining[:40])
            remaining = remaining[40:]
            print("[IPv6]")
            print(f"src_addr: {ip6.src_ip}")
            print(f"dst_addr: {ip6.dst_ip}")

            # Next header
            next_header = remaining[0] if remaining else None
            if next_header == 58 and len(remaining) >= 8:  # ICMPv6
                icmp6 = parse_icmpv6(remaining[:8])
                remaining = remaining[8:]
                print("[ICMPv6]")
                print(f"type: {icmp6.type}")
                print(f"code: {icmp6.code}")
                print(f"checksum: {icmp6.checksum}")

    except Exception as e:
        print(f"[Error parsing packet] {e}")
