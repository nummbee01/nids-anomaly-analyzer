import tkinter as tk
from tkinter import scrolledtext
from scapy.all import sniff, conf
import json
from datetime import datetime
import threading

running = False
stop_event = threading.Event()
output_text = None

def packet_callback(pkt):
    if pkt.haslayer("IP"):
        entry = {
            "time": datetime.now().isoformat(),
            "src": pkt["IP"].src,
            "dst": pkt["IP"].dst,
            "proto": pkt["IP"].proto,
            "summary": pkt.summary()
        }
        with open("captured_packets.json", "a") as f:
            json.dump(entry, f)
            f.write("\n")
        
        output_text.insert(tk.END, pkt.summary() + "\n")
        output_text.see(tk.END)

def sniff_thread():
    conf.verb = 0
    try:
        sniff(iface="wlan0", prn=packet_callback, store=0, stop_filter=lambda x: stop_event.is_set())
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")

def toggle_sniff():
    global running, sniff_thread_var
    if not running:
        stop_event.clear()
        output_text.delete(1.0, tk.END)
        sniff_thread_var = threading.Thread(target=sniff_thread, daemon=True)
        sniff_thread_var.start()
        running = True
        btn.config(text="Stop Sniffing")
    else:
        stop_event.set()
        running = False
        btn.config(text="Start Sniffing")

def clear_logs():
    output_text.delete(1.0, tk.END)

# GUI
root = tk.Tk()
root.title("Packet Sniffer")
root.geometry("900x600")

btn = tk.Button(root, text="Start Sniffing", command=toggle_sniff, width=15)
btn.pack(pady=10)

clear_btn = tk.Button(root, text="Clear Logs", command=clear_logs)
clear_btn.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=30)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
