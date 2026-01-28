from scapy.all import *

from .packet_parser import *


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


def main():
    IFACE = select_interface()
    sniffing_interface(IFACE)


if __name__ == "__main__":
    main()
