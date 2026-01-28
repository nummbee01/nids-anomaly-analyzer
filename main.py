import argparse  # CLI argument parser
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.packet_capture import select_interface, sniffing_interface
from core.packet_parser import print_packet_info
from utils.data_structures import Alert, DetectionState


def main():
    # Shown in --help
    parser = argparse.ArgumentParser(
        description="Argus NIDS - Network Intrusion Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive interface selection
  python main.py -i eth0                 # Use specific interface
  python main.py -i eth0 -c 100           # Capture 100 packets
  python main.py --list-interfaces       # Show available interfaces
        """,
    )

    parser.add_argument("-i", "--interface", help="Network interface to capture from")
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=5,
        help="Number of packets to capture (default: 5)",
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available network interfaces",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # List interfaces and exit
    if args.list_interfaces:
        from scapy.all import get_if_list

        interfaces = get_if_list()
        print("Available network interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  {i} - {iface}")
        return

    # Select interface
    if args.interface:
        interface = args.interface
        if args.verbose:
            print(f"Using interface: {interface}")
    else:
        interface = select_interface()

    if args.verbose:
        print(f"Starting packet capture on {interface}")
        print(f"Capturing {args.count} packets...")
        print("Press Ctrl+C to stop early\n")

    try:
        # Start packet capture
        sniffing_interface(interface, count=args.count)

    except KeyboardInterrupt:
        print("\nPacket capture stopped by user")
    except PermissionError:
        print("Error: Permission denied. Try running with sudo:")
        print(f"sudo python3 {sys.argv[0]} {' '.join(sys.argv[1:])}")
    except Exception as e:
        print(f"Error during packet capture: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
