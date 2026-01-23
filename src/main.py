from scapy.all import *


def select_interface():
    interfaces = get_if_list()
    for index, interface in enumerate(interfaces):
        print(f"{index} - {interface}")
    try:
        choice = int(input("Select an interface: "))
    except ValueError:
        print("Invalid input")
        return select_interface()
    if choice < 0 or choice >= len(interfaces):
        print("Invalid choice")
        return select_interface()
    return interfaces[choice]


def show_summary(pkt):
    print(pkt.summary())


def sniffing_interface(interface):
    sniff(iface=interface, prn=show_summary, store=False)


def main():
    IFACE = select_interface()
    sniffing_interface(IFACE)


if __name__ == "__main__":
    main()
