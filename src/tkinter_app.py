import threading
import tkinter as tk
from tkinter import scrolledtext

from scapy.all import conf, sniff

running = False
stop_event = threading.Event()


def packet_callback(pkt):
    if pkt.haslayer("IP"):
        output_text.insert(tk.END, pkt.summary() + "\n")
        output_text.see(tk.END)


def sniff_thread():
    conf.verb = 0
    try:
        sniff(iface="wlan0", prn=packet_callback, store=0, stop_filter=stop_filter_func)
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")


def stop_filter_func(x):
    return stop_event.is_set()


def start_sniff():
    global running
    stop_event.clear()
    output_text.insert(tk.END, "Scan started\n")
    output_text.see(tk.END)
    threading.Thread(target=sniff_thread, daemon=True).start()
    running = True
    btn1.config(text="Stop")


def stop_sniff():
    global running
    stop_event.set()
    output_text.insert(tk.END, "Scan stopped\n")
    output_text.see(tk.END)
    running = False
    btn1.config(text="Start")


def toggle_sniff():
    if not running:
        start_sniff()
    else:
        stop_sniff()


def clear_logs():
    output_text.delete("1.0", tk.END)


root = tk.Tk()
root.title("App")

sidebar = tk.Frame(root, width=200)
sidebar.pack(side="left", fill="y")

main_area = tk.Frame(root)
main_area.pack(side="right", fill="both", expand=True)

output_text = scrolledtext.ScrolledText(main_area, wrap=tk.WORD)
output_text.pack(fill="both", expand=True)

btn1 = tk.Button(sidebar, text="Start", command=toggle_sniff)
btn1.pack(fill="x")

btn2 = tk.Button(sidebar, text="Clear logs", command=clear_logs)
btn2.pack(fill="x")

root.mainloop()
