from scapy.all import *


def get_interface():
    interfaces = get_if_list()
    for i, interface in enumerate(interfaces):
        print(f"{i}: {interface}")


def start_capture(interface, callback):
    sniff(iface=interface, prn=callback)


def stop_capture():
    pass


get_interface()
