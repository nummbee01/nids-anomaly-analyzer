from core.packet_parser import *
from utils.data_structures import Ethernet, IPv4, IPv6, TCP, UDP, ICMPv4, ICMPv6


def test_bytes_to_mac():
    assert bytes_to_mac(b"\x01\x02\x03\x04\x05\x06") == "01:02:03:04:05:06"


def test_bytes_to_ipv4():
    assert bytes_to_ipv4(b"\x7f\x00\x00\x01") == "127.0.0.1"


def test_bytes_to_ipv6():
    ip6_bytes = b"\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x34"
    expected = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert bytes_to_ipv6(ip6_bytes) == expected


def test_parse_ethernet():
    raw = b"\x01\x02\x03\x04\x05\x06\x11\x12\x13\x14\x15\x16\x08\x00"
    expected = Ethernet(
        dst_mac="01:02:03:04:05:06",
        src_mac="11:12:13:14:15:16", 
        ethertype="0800"
    )
    assert parse_ethernet(raw) == expected


def test_parse_ipv4():
    raw = b"\x45\x00\x00\x14\x00\x00\x40\x00\x40\x06\xa6\xec\x7f\x00\x00\x01\x7f\x00\x00\x01"
    expected = IPv4(
        protocol=6,
        src_ip="127.0.0.1",
        dst_ip="127.0.0.1"
    )
    assert parse_ipv4(raw) == expected


def test_parse_ipv6():
    raw = (
        b"\x60\x00\x00\x00\x00\x08\x3a\x40"
        + b"\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x34"
        + b"\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x35"
    )
    expected = IPv6(
        src_ip="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        dst_ip="2001:0db8:85a3:0000:0000:8a2e:0370:7335"
    )
    assert parse_ipv6(raw) == expected


def test_parse_tcp():
    raw = b"\x00P\x00P\x00\x00\x00\x01\x00\x00\x00\x02\x50\x18\x71\x10\x00\x00\x00\x00"
    expected = TCP(
        src_port=80,
        dst_port=80,
        seq_num=1,
        ack_num=2
    )
    assert parse_tcp(raw) == expected


def test_parse_udp():
    raw = b"\x00P\x00P\x00\x08\x12\x34"
    expected = UDP(
        src_port=80,
        dst_port=80,
        length=8,
        checksum=0x1234
    )
    assert parse_udp(raw) == expected


def test_parse_icmpv4():
    raw = b"\x08\x00\xf7\xff\x12\x34\x00\x01"
    expected = ICMPv4(
        type=8,
        code=0,
        checksum=0xF7FF,
        identifier=0x1234,
        sequence=1
    )
    assert parse_icmpv4(raw) == expected


def test_parse_icmpv6():
    raw = b"\x80\x00\xf7\xff\x00\x00\x00\x00"
    expected = ICMPv6(
        type=128,
        code=0,
        checksum=0xF7FF
    )
    assert parse_icmpv6(raw) == expected


if __name__ == "__main__":
    test_bytes_to_mac()
    test_bytes_to_ipv4()
    test_bytes_to_ipv6()
    test_parse_ethernet()
    test_parse_ipv4()
    test_parse_ipv6()
    test_parse_tcp()
    test_parse_udp()
    test_parse_icmpv4()
    test_parse_icmpv6()
    print("All tests passed.")