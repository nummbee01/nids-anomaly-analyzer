import tkinter as tk
from tkinter import ttk, messagebox
from scapy.all import *
import threading
import time
import collections
import statistics
import logging

class ArgusNIDS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Argus GUI")
        self.root.geometry("800x600")

        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Capture")
        menubar.add_cascade(label="Detection")
        menubar.add_cascade(label="View")
        menubar.add_cascade(label="Help")

        # Controls Frame
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        ttk.Label(controls_frame, text="CONTROLS").pack()

        self.running = False
        self.start_stop_btn = ttk.Button(controls_frame, text="Start", command=self.toggle_capture)
        self.start_stop_btn.pack()

        self.interface_var = tk.StringVar(value="eth0")
        ttk.Label(controls_frame, text="Interface").pack()
        ttk.Entry(controls_frame, textvariable=self.interface_var).pack()

        self.threshold_var = tk.IntVar(value=100)
        ttk.Label(controls_frame, text="Thresholds").pack()
        ttk.Entry(controls_frame, textvariable=self.threshold_var).pack()

        self.filter_var = tk.StringVar(value="ip")
        ttk.Label(controls_frame, text="Filters").pack()
        ttk.Entry(controls_frame, textvariable=self.filter_var).pack()

        self.logging_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Logging", variable=self.logging_var).pack()

        # Alerts Frame
        alerts_frame = ttk.Frame(self.root)
        alerts_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(alerts_frame, text="REAL-TIME ALERTS").pack()

        self.alerts_list = tk.Listbox(alerts_frame, height=10)
        self.alerts_list.pack(fill=tk.BOTH, expand=True)

        ttk.Button(alerts_frame, text="Clear", command=self.clear_alerts).pack(side=tk.LEFT)
        ttk.Button(alerts_frame, text="Export", command=self.export_alerts).pack(side=tk.LEFT)

        # Stats Frame
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        ttk.Label(stats_frame, text="STATS").pack()

        self.stats_text = tk.Text(stats_frame, height=10, width=20)
        self.stats_text.pack()

        # Viz Frame (placeholder)
        viz_frame = ttk.Frame(self.root)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(viz_frame, text="TRAFFIC VISUALIZATION").pack()
        ttk.Label(viz_frame, text="[Line Chart Placeholder]").pack(fill=tk.BOTH, expand=True)

        ttk.Button(viz_frame, text="Pause").pack(side=tk.LEFT)
        ttk.Button(viz_frame, text="Reset").pack(side=tk.LEFT)
        ttk.Button(viz_frame, text="Save").pack(side=tk.LEFT)

        # Data structures
        self.packet_count = 0
        self.protocol_counts = collections.Counter()
        self.src_counts = collections.Counter()
        self.syn_counts = collections.Counter()  # For SYN flood
        self.port_scans = collections.Counter()  # For port scans
        self.icmp_counts = []  # For anomaly stats
        self.alerts = []
        self.logger = logging.getLogger("Argus")
        logging.basicConfig(filename="argus.log", level=logging.INFO)

        self.root.mainloop()

    def toggle_capture(self):
        if self.running:
            self.running = False
            self.start_stop_btn.config(text="Start")
        else:
            self.running = True
            self.start_stop_btn.config(text="Stop")
            threading.Thread(target=self.sniff_packets, daemon=True).start()
            threading.Thread(target=self.update_stats, daemon=True).start()

    def sniff_packets(self):
        while self.running:
            packets = sniff(iface=self.interface_var.get(), filter=self.filter_var.get(), count=10, timeout=1)
            for pkt in packets:
                self.process_packet(pkt)

    def process_packet(self, pkt):
        self.packet_count += 1
        if IP in pkt:
            src = pkt[IP].src
            self.src_counts[src] += 1

            if TCP in pkt:
                self.protocol_counts['TCP'] += 1
                if pkt[TCP].flags == 'S':
                    self.syn_counts[src] += 1
                if pkt[TCP].dport in range(1, 1025):  # Simple port scan detect
                    self.port_scans[src] += 1

            elif UDP in pkt:
                self.protocol_counts['UDP'] += 1

            elif ICMP in pkt:
                self.protocol_counts['ICMP'] += 1
                self.icmp_counts.append(time.time())

        self.detect_rules()
        self.detect_anomalies()

    def detect_rules(self):
        threshold = self.threshold_var.get()
        for src, count in list(self.syn_counts.items()):
            if count > threshold:
                alert = f"[M] {time.strftime('%H:%M')} SYN Flood from {src}"
                self.add_alert(alert)
                del self.syn_counts[src]

        for src, count in list(self.port_scans.items()):
            if count > threshold / 10:
                alert = f"[H] {time.strftime('%H:%M')} Port Scan from {src}"
                self.add_alert(alert)
                del self.port_scans[src]

    def detect_anomalies(self):
        if len(self.icmp_counts) > 10:
            times = self.icmp_counts[-10:]
            diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
            if statistics.mean(diffs) < 0.1:  # High frequency ICMP
                alert = f"[L] {time.strftime('%H:%M')} ICMP Anomaly"
                self.add_alert(alert)
                self.icmp_counts = []

    def add_alert(self, alert):
        self.alerts.append(alert)
        self.alerts_list.insert(tk.END, alert)
        if self.logging_var.get():
            self.logger.info(alert)

    def clear_alerts(self):
        self.alerts_list.delete(0, tk.END)
        self.alerts = []

    def export_alerts(self):
        with open("alerts.txt", "w") as f:
            f.write("\n".join(self.alerts))
        messagebox.showinfo("Export", "Alerts exported to alerts.txt")

    def update_stats(self):
        while self.running:
            self.stats_text.delete(1.0, tk.END)
            total_protos = sum(self.protocol_counts.values())
            stats = (
                f"Pkts/sec: {self.packet_count / 60:.2f}\n"
                f"TCP: {self.protocol_counts['TCP']/total_protos*100 if total_protos else 0:.0f}%\n"
                f"UDP: {self.protocol_counts['UDP']/total_protos*100 if total_protos else 0:.0f}%\n"
                f"ICMP: {self.protocol_counts['ICMP']/total_protos*100 if total_protos else 0:.0f}%\n"
                f"Alerts: {len(self.alerts)}\n"
                f"Sources: {len(self.src_counts)}\n"
            )
            self.stats_text.insert(tk.END, stats)
            time.sleep(5)

if __name__ == "__main__":
    ArgusNIDS()
