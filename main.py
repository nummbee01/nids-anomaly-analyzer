import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.packet_capture import select_interface, start_capture
from core.threat_detectors import create_state


def main():
    """
    CLI interface for Argus NIDS (for testing purposes).
    For production use, run the GUI: python src/gui/gui.py
    """
    parser = argparse.ArgumentParser(
        description="Argus NIDS - Network Intrusion Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -i eth0
  python main.py -i eth0 -c 100
  python main.py --list-interfaces
        """,
    )

    parser.add_argument("-i", "--interface", help="Network interface to capture from")
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=0,
        help="Number of packets to capture (default: 0 = infinite)",
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available network interfaces",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--show-packets",
        action="store_true",
        help="Show detailed packet information",
    )

    args = parser.parse_args()

    if args.list_interfaces:
        from scapy.all import get_if_list
        interfaces = get_if_list()
        print("Available network interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  {i} - {iface}")
        return

    interface = args.interface if args.interface else select_interface()

    print(f"\n{'=' * 80}")
    print(f"  Argus NIDS - Network Intrusion Detection System")
    print(f"{'=' * 80}")
    print(f"Interface: {interface}")
    print(f"Packet count: {'Infinite (Ctrl+C to stop)' if args.count == 0 else args.count}")
    print(f"Verbose mode: {'ON' if args.verbose else 'OFF'}")
    print(f"Show packets: {'ON' if args.show_packets else 'OFF'}")
    print(f"{'=' * 80}\n")

    state = create_state()
    packet_count = [0]
    threat_count = [0]

    def cli_callback(packet_info, alerts):
        packet_count[0] = packet_info['packet_num']
        
        if args.show_packets:
            print(f"\n[Packet #{packet_count[0]}]")
            ipv4 = packet_info['ipv4']
            ipv6 = packet_info['ipv6']
            tcp = packet_info['tcp']
            udp = packet_info['udp']
            icmp = packet_info['icmp']
            
            if ipv4:
                print(f"  {ipv4.src_ip} → {ipv4.dst_ip}", end="")
                if tcp:
                    print(f" | TCP {tcp.src_port}→{tcp.dst_port}")
                elif udp:
                    print(f" | UDP {udp.src_port}→{udp.dst_port}")
                elif icmp:
                    print(f" | ICMP type={icmp.type}")
                else:
                    print()
            elif ipv6:
                print(f"  {ipv6.src_ip} → {ipv6.dst_ip}")
        
        if alerts:
            threat_count[0] += len(alerts)
            print(f"\n{'!' * 80}")
            print(f"⚠️  THREAT DETECTED - Packet #{packet_count[0]}")
            print(f"{'!' * 80}")
            for alert in alerts:
                print(f"  → {alert}")
            print(f"{'!' * 80}\n")
        elif not args.verbose and packet_count[0] % 100 == 0:
            print(f"[{packet_count[0]} packets analyzed, {threat_count[0]} threats detected]")

    try:
        print("🔍 Starting packet capture and threat detection...")
        print("   (Press Ctrl+C to stop)\n")

        start_capture(interface=interface, state=state, callback=cli_callback, count=args.count)

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 80}")
        print("📊 Session Summary")
        print(f"{'=' * 80}")
        print(f"Total packets analyzed: {packet_count[0]}")
        print(f"Total threats detected: {threat_count[0]}")
        print(f"{'=' * 80}")
        print("\n✓ Packet capture stopped by user")
    except PermissionError:
        print("\n❌ Error: Permission denied. Try running with sudo:")
        print(f"   sudo python3 {sys.argv[0]} {' '.join(sys.argv[1:])}")
    except Exception as e:
        print(f"\n❌ Error during packet capture: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
