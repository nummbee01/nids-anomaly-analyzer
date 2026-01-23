import json
from datetime import datetime

from scapy.all import conf, sniff


def packet_callback(pkt):
    if pkt.haslayer("IP"):
        entry = {
            "time": datetime.now().isoformat(),
            "src": pkt["IP"].src,
            "dst": pkt["IP"].dst,
            "proto": pkt["IP"].proto,
            "summary": pkt.summary(),
        }
        # Save immediately (append mode)
        with open("captured_packets.json", "a") as f:
            json.dump(entry, f)
            f.write("\n")  # newline for JSON Lines format
        print(pkt.summary())


def main():
    conf.verb = 0
    print("Sniffing... Ctrl+C to stop\n")

    try:
        sniff(prn=packet_callback, store=0)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
