import tkinter as tk
from tkinter import scrolledtext, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Main window
root = tk.Tk()
root.title("🛡️ Network Intrusion Detection System")
root.geometry("1200x800")
root.configure(bg="#0e1117")

# Main container
main_frame = tk.Frame(root, bg="#0e1117")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ===== LEFT SIDEBAR =====
sidebar = tk.Frame(main_frame, bg="#1e1e1e", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
sidebar.pack_propagate(False)

# Title
title = tk.Label(
    sidebar,
    text="⚙️ Control Panel",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="white",
)
title.pack(pady=10)

# Interface input
tk.Label(sidebar, text="Network Interface:", bg="#1e1e1e", fg="white").pack(
    pady=(10, 5)
)
interface_entry = tk.Entry(
    sidebar, width=20, bg="#2e2e2e", fg="white", insertbackground="white"
)
interface_entry.insert(0, "wlp8s0")
interface_entry.pack(pady=5)

# Start/Stop buttons
btn_frame = tk.Frame(sidebar, bg="#1e1e1e")
btn_frame.pack(pady=10)

start_btn = tk.Button(
    btn_frame, text="▶️ Start", bg="#4caf50", fg="white", width=10, relief=tk.FLAT
)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(
    btn_frame, text="⏹️ Stop", bg="#f44336", fg="white", width=10, relief=tk.FLAT
)
stop_btn.grid(row=0, column=1, padx=5)

# Separator
ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

# Packet count
tk.Label(sidebar, text="Packets to Capture:", bg="#1e1e1e", fg="white").pack(
    pady=(5, 5)
)
packet_count = tk.Spinbox(
    sidebar, from_=10, to=10000, width=18, bg="#2e2e2e", fg="white"
)
packet_count.delete(0, tk.END)
packet_count.insert(0, "100")
packet_count.pack(pady=5)

# Clear button
clear_btn = tk.Button(
    sidebar, text="🗑️ Clear Data", bg="#ff9800", fg="white", width=22, relief=tk.FLAT
)
clear_btn.pack(pady=10)

# Separator
ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

# Statistics
stats_label = tk.Label(
    sidebar, text="📊 Statistics", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white"
)
stats_label.pack(pady=5)

stats_frame = tk.Frame(sidebar, bg="#1e1e1e")
stats_frame.pack(pady=10, fill=tk.X, padx=10)


# Metric cards
def create_metric(parent, label, value, row):
    frame = tk.Frame(parent, bg="#2e2e2e", relief=tk.RAISED, bd=1)
    frame.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")

    tk.Label(frame, text=label, bg="#2e2e2e", fg="#888", font=("Arial", 8)).pack()
    tk.Label(
        frame, text=value, bg="#2e2e2e", fg="white", font=("Arial", 16, "bold")
    ).pack()


create_metric(stats_frame, "Total Packets", "0", 0)
create_metric(stats_frame, "Threats", "0", 1)
create_metric(stats_frame, "Blocked", "0", 2)
create_metric(stats_frame, "Rate", "0 pkt/s", 3)

# Separator
ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

# Status
status_frame = tk.Frame(sidebar, bg="#1e1e1e")
status_frame.pack(pady=10)
tk.Label(
    status_frame,
    text="🔴 Status: Stopped",
    bg="#1e1e1e",
    fg="#ff4444",
    font=("Arial", 10, "bold"),
).pack()

# ===== RIGHT CONTENT AREA =====
content = tk.Frame(main_frame, bg="#0e1117")
content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Header
header = tk.Label(
    content,
    text="📈 Network Traffic Monitor",
    font=("Arial", 16, "bold"),
    bg="#0e1117",
    fg="white",
)
header.pack(pady=10, anchor="w")

# Chart area
chart_frame = tk.Frame(content, bg="#1e1e1e", height=250)
chart_frame.pack(fill=tk.X, pady=10)
chart_frame.pack_propagate(False)

# Create matplotlib chart
fig = Figure(figsize=(10, 3), facecolor="#1e1e1e")
ax = fig.add_subplot(111)
ax.set_facecolor("#1e1e1e")
ax.plot([0], [0], color="#00d4ff", linewidth=2)
ax.fill_between([0], [0], alpha=0.3, color="#00d4ff")
ax.set_xlabel("Time (s)", color="white")
ax.set_ylabel("Packets/sec", color="white")
ax.tick_params(colors="white")
ax.spines["bottom"].set_color("white")
ax.spines["left"].set_color("white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

canvas = FigureCanvasTkAgg(fig, chart_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Tabs
notebook = ttk.Notebook(content)
notebook.pack(fill=tk.BOTH, expand=True, pady=10)

# Style for tabs
style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#0e1117", borderwidth=0)
style.configure(
    "TNotebook.Tab", background="#2e2e2e", foreground="white", padding=[20, 10]
)
style.map("TNotebook.Tab", background=[("selected", "#1e1e1e")])

# Tab 1: Captured Packets
tab1 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab1, text="📦 Captured Packets")

# Filters
filter_frame = tk.Frame(tab1, bg="#1e1e1e")
filter_frame.pack(fill=tk.X, pady=10, padx=10)

tk.Label(filter_frame, text="Protocol:", bg="#1e1e1e", fg="white").grid(
    row=0, column=0, padx=5
)
protocol_combo = ttk.Combobox(
    filter_frame,
    values=["All", "TCP", "UDP", "ICMP", "DNS"],
    width=15,
    state="readonly",
)
protocol_combo.set("All")
protocol_combo.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Threat Level:", bg="#1e1e1e", fg="white").grid(
    row=0, column=2, padx=5
)
threat_combo = ttk.Combobox(
    filter_frame,
    values=["All", "Critical", "High", "Medium", "Low"],
    width=15,
    state="readonly",
)
threat_combo.set("All")
threat_combo.grid(row=0, column=3, padx=5)

export_btn = tk.Button(
    filter_frame, text="📥 Export CSV", bg="#2196F3", fg="white", relief=tk.FLAT
)
export_btn.grid(row=0, column=4, padx=20)

# Packet table
table_frame = tk.Frame(tab1, bg="#1e1e1e")
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = (
    "Timestamp",
    "Source IP",
    "Dest IP",
    "Protocol",
    "Port",
    "Length",
    "Threat",
    "Action",
)
packet_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    packet_tree.heading(col, text=col)
    packet_tree.column(col, width=100)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=packet_tree.yview)
packet_tree.configure(yscrollcommand=scrollbar.set)

packet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Tab 2: Threat Alerts
tab2 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab2, text="⚠️ Threat Alerts")

alert_filter_frame = tk.Frame(tab2, bg="#1e1e1e")
alert_filter_frame.pack(fill=tk.X, pady=10, padx=10)

tk.Label(alert_filter_frame, text="Filter:", bg="#1e1e1e", fg="white").pack(
    side=tk.LEFT, padx=5
)
alert_filter_combo = ttk.Combobox(
    alert_filter_frame,
    values=["All Alerts", "Critical Only", "High & Critical", "Last Hour"],
    width=20,
    state="readonly",
)
alert_filter_combo.set("All Alerts")
alert_filter_combo.pack(side=tk.LEFT, padx=5)

alert_text = scrolledtext.ScrolledText(
    tab2, bg="#2e2e2e", fg="white", height=20, font=("Courier", 10)
)
alert_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
alert_text.insert(tk.END, "No alerts detected yet. Start monitoring to see threats.\n")
alert_text.config(state=tk.DISABLED)

# Tab 3: Analytics
tab3 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab3, text="📊 Analytics")

analytics_label = tk.Label(
    tab3,
    text="Traffic Analytics Dashboard",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="white",
)
analytics_label.pack(pady=20)

# Placeholder for charts
charts_container = tk.Frame(tab3, bg="#1e1e1e")
charts_container.pack(fill=tk.BOTH, expand=True, padx=20)

chart1 = tk.Frame(charts_container, bg="#2e2e2e", width=300, height=200)
chart1.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
tk.Label(
    chart1,
    text="Protocol Distribution\n(Pie Chart)",
    bg="#2e2e2e",
    fg="#888",
    font=("Arial", 12),
).pack(expand=True)

chart2 = tk.Frame(charts_container, bg="#2e2e2e", width=300, height=200)
chart2.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
tk.Label(
    chart2,
    text="Top Source IPs\n(Bar Chart)",
    bg="#2e2e2e",
    fg="#888",
    font=("Arial", 12),
).pack(expand=True)

# Tab 4: Help
tab4 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab4, text="ℹ️ Help")

help_text = scrolledtext.ScrolledText(
    tab4, bg="#2e2e2e", fg="white", height=20, font=("Arial", 10), wrap=tk.WORD
)
help_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

help_content = """
🚀 QUICK START

1. Enter your network interface (e.g., wlp8s0, eth0)
2. Set number of packets to capture
3. Click Start to begin monitoring
4. View live packets and alerts in real-time

🎯 FEATURES

• Real-time Packet Capture - Monitor network traffic as it happens
• Threat Detection - Automatic identification of suspicious activity
• Analytics Dashboard - Visualize traffic patterns and threats
• Export Data - Save captured packets to CSV/PCAP

⚠️ REQUIREMENTS

Linux/macOS:
    sudo pip install scapy matplotlib
    sudo python3 app.py

Windows:
    - Install Npcap from https://npcap.com/
    - Run as Administrator

📡 FINDING YOUR INTERFACE

• Linux: ip link or ifconfig
• macOS: ifconfig
• Windows: ipconfig

Common names: eth0, wlp8s0, en0, Wi-Fi

🔒 THREAT LEVELS

• Critical: Blacklisted IPs, known attacks
• High: Port scans, suspicious patterns
• Medium: Unusual ports, large packets
• Low: Normal traffic
"""

help_text.insert(tk.END, help_content)
help_text.config(state=tk.DISABLED)

# Footer
footer = tk.Label(
    content,
    text="NIDS Dashboard v1.0 | Built with Scapy & Tkinter",
    bg="#0e1117",
    fg="#666",
    font=("Arial", 8),
)
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
