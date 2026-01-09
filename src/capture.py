from scapy.all import *


def main():
    print("Program started...")
    # packet = IP()
    packet = IP(src="192.168.1.5", dst="192.168.1.1")
    packet.show()


if __name__ == "__main__":
    main()
