#!/usr/bin/env python3
# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │        ▄▀█ █▀█ █▀▀ █░█ █▀ ░ █▄░█ █ █▀▄ █▀ ░ ─ ░ ▀█▀ █▄▀ █ █▄░█ ▀█▀ █▀▀ █▀█ ░ █▀▀ █░█ █           │
# │        █▀█ █▀▄ █▄█ █▄█ ▄█ ░ █░▀█ █ █▄▀ ▄█ ░ ─ ░ ░█░ █░█ █ █░▀█ ░█░ ██▄ █▀▄ ░ █▄█ █▄█ █           │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                                   █ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀ █▀                                     │
# │                                   █ █░▀░█ █▀▀ █▄█ █▀▄ ░█░ ▄█                                     │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
import json
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scapy.all import get_if_list
from core.packet_capture import select_interface, start_capture
from core.threat_detectors import create_state


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                  █░█ █▀▀ █░░ █▀█ █▀▀ █▀█ ░ █▀▀ █░█ █▄░█ █▀▀ ▀█▀ █ █▀█ █▄░█ █▀                    │
# │                  █▀█ ██▄ █▄▄ █▀▀ ██▄ █▀▄ ░ █▀░ █▄█ █░▀█ █▄▄ ░█░ █ █▄█ █░▀█ ▄█                    │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                         █▀ ▄▀█ █░█ █ █▄░█ █▀▀ ░ █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀                           │
# │                         ▄█ █▀█ ▀▄▀ █ █░▀█ █▄█ ░ █▄▄ █▄█ █░▀█ █▀░ █ █▄█                           │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def save_config_to_json(entry_widgets):
    config_data = {}

    for field_name, entry in entry_widgets.items():
        value = entry.get()
        try:
            if "." in value:
                config_data[field_name] = float(value)
            elif value.lower() in ("true", "false"):
                config_data[field_name] = value.lower() == "true"
            else:
                config_data[field_name] = int(value)
        except ValueError:
            config_data[field_name] = value

    config_data["last_updated"] = datetime.now().isoformat()

    config_path = Path(__file__).parent.parent / "config.json"

    try:
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        messagebox.showinfo("Success", f"Configuration saved to:\n{config_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")



# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                      █▀▀ ▀▄▀ █▀█ █▀█ █▀█ ▀█▀ █ █▄░█ █▀▀ ░ █░░ █▀█ █▀▀ █▀                         │
# │                      ██▄ █░█ █▀▀ █▄█ █▀▄ ░█░ █ █░▀█ █▄█ ░ █▄▄ █▄█ █▄█ ▄█                         │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def export_logs_to_json(logs_text, alerts_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"argus_logs_{timestamp}.json"

    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialfile=default_filename,
    )

    if not filepath:
        return

    logs_content = logs_text.get("1.0", "end-1c")
    alerts_content = alerts_text.get("1.0", "end-1c")

    logs_list = [line.strip() for line in logs_content.split("\n") if line.strip()]
    alerts_list = [line.strip() for line in alerts_content.split("\n") if line.strip()]

    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "total_packets": len(logs_list),
        "total_alerts": len(alerts_list),
        "packet_logs": logs_list,
        "threat_alerts": alerts_list,
    }

    try:
        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=4)
        messagebox.showinfo("Success", f"Logs exported to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export logs:\n{str(e)}")


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                           █▀▀ █░█ █ ░ █▀▀ █▀█ █▀▀ ▄▀█ ▀█▀ █ █▀█ █▄░█                             │
# │                           █▄█ █▄█ █ ░ █▄▄ █▀▄ ██▄ █▀█ ░█░ █ █▄█ █░▀█                             │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                 █▀▀ █▀█ █▀▀ ▄▀█ ▀█▀ █ █▄░█ █▀▀ ░ █▀▄▀█ ▄▀█ █ █▄░█ ░ █▀▀ █░█ █                    │
# │                 █▄▄ █▀▄ ██▄ █▀█ ░█░ █ █░▀█ █▄█ ░ █░▀░█ █▀█ █ █░▀█ ░ █▄█ █▄█ █                    │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def create_gui():
    root = tk.Tk()
    root.title("Argus NIDS - Network Intrusion Detection System")
    root.geometry("1400x900")
    root.minsize(1200, 700)

    # Configure root grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                       █▀▀ █▀█ █░░ █▀█ █▀█ ░ █▀█ ▄▀█ █░░ █▀▀ ▀█▀ ▀█▀ █▀▀                          │
# │                       █▄▄ █▄█ █▄▄ █▄█ █▀▄ ░ █▀▀ █▀█ █▄▄ ██▄ ░█░ ░█░ ██▄                          │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Color scheme
    colors = {
        "bg_dark": "#1e1e1e",
        "bg_medium": "#2d2d2d",
        "bg_light": "#3d3d3d",
        "accent": "#007acc",
        "text": "#ffffff",
        "text_dim": "#cccccc",
        "success": "#4caf50",
        "warning": "#ff9800",
        "danger": "#f44336",
    }

    root.configure(bg=colors["bg_dark"])


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                   █▀ ▀█▀ ▄▀█ ▀█▀ █▀▀ ░ & ░ █░█ ▄▀█ █▀█ █ ▄▀█ █▄▄ █░░ █▀▀ █▀                      │
# │                   ▄█ ░█░ █▀█ ░█░ ██▄ ░ & ░ ▀▄▀ █▀█ █▀▄ █ █▀█ █▄█ █▄▄ ██▄ ▄█                      │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Track running state and capture thread
    is_running = {"state": False}
    capture_thread = {"thread": None}
    capture_state = {"state": None}
    capture_sniffer = {"sniffer": None}

    # Statistics tracking
    stats = {
        "total_packets": 0,
        "total_alerts": 0,
        "port_scans": 0,
        "syn_floods": 0,
        "brute_force": 0,
        "ddos_attacks": 0,
        "ip_spoofing": 0,
        # 'mac_spoofing': 0,  # COMMENTED OUT: MAC Spoofing detection disabled
        "arp_spoofing": 0,
        "dns_tunneling": 0,
        "icmp_floods": 0,
        "unusual_protocols": 0,
    }

    # Dictionary to store references to stat label widgets
    stat_labels = {}
    
    # Track current view
    current_view = {"view": "dashboard"}
    
    # Store entry widgets for later access
    entry_widgets = {}

    # ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
    # │                                                                                              │
    # │                     █ █▄░█ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█ █░░    █░░ █▀█ █▀▀ █ █▀▀                     │
    # │                     █ █░▀█ ░█░ ██▄ █▀▄ █░▀█ █▀█ █▄▄    █▄▄ █▄█ █▄█ █ █▄▄                     │
    # │                                                                                              │
    # ╚──────────────────────────────────────────────────────────────────────────────────────────────╝


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │  █░█ █▀█ █▀▄ ▄▀█ ▀█▀ █ █▄░█ █▀▀ ░ █▀ ▀█▀ ▄▀█ ▀█▀ █ █▀ ▀█▀ █ █▀▀ █▀ ░ █▀▄ █ █▀ █▀█ █░░ ▄▀█ ▀▄▀    │
# │  █▄█ █▀▀ █▄▀ █▀█ ░█░ █ █░▀█ █▄█ ░ ▄█ ░█░ █▀█ ░█░ █ ▄█ ░█░ █ █▄▄ ▄█ ░ █▄▀ █ ▄█ █▀▀ █▄▄ █▀█ ░█░    │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def update_statistics_display():
        # Update all stat labels with current values
        for stat_key, label_widget in stat_labels.items():
            value = stats.get(stat_key, 0)
            # Format large numbers with commas
            if value >= 1000:
                formatted_value = f"{value:,}"
            else:
                formatted_value = str(value)
            label_widget.config(text=formatted_value)

            # Update color based on value
            if stat_key == "total_packets":
                label_widget.config(fg=colors["accent"])
            elif value > 0 and stat_key != "total_packets":
                if stat_key == "total_alerts":
                    label_widget.config(fg=colors["danger"])
                else:
                    label_widget.config(fg=colors["warning"])
            else:
                label_widget.config(fg=colors["success"])


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │             █▀▀ █░█ █ ░ █░█ █▀█ █▀▄ ▄▀█ ▀█▀ █▀▀ ░ █▀▀ ▄▀█ █░░ █░░ █▄▄ ▄▀█ █▀▀ █▄▀                │
# │             █▄█ █▄█ █ ░ █▄█ █▀▀ █▄▀ █▀█ ░█░ ██▄ ░ █▄▄ █▀█ █▄▄ █▄▄ █▄█ █▀█ █▄▄ █░█                │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def gui_callback(packet_info, alerts):

        # This is called from packet capture thread, so schedule GUI updates in main thread

# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                                  │
# │                           █░█ █▀█ █▀▄ ▄▀█ ▀█▀ █ █▄░█ █▀▀ ░ █▀▀ █░█ █                             │
# │                           █▄█ █▀▀ █▄▀ █▀█ ░█░ █ █░▀█ █▄█ ░ █▄█ █▄█ █                             │
# │                                                                                                  │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
        def update_gui():
            stats["total_packets"] = packet_info["packet_num"]

            # Format packet log entry
            timestamp = datetime.now().strftime("%H:%M:%S")
            ipv4 = packet_info["ipv4"]
            ipv6 = packet_info["ipv6"]
            tcp = packet_info["tcp"]
            udp = packet_info["udp"]
            icmp = packet_info["icmp"]

            # Only create log entry if there's actual packet data (IPv4 or IPv6)
            log_entry = None
            if ipv4:
                log_entry = f"[{timestamp}] {ipv4.src_ip} → {ipv4.dst_ip}"
                if tcp:
                    log_entry += f" | TCP {tcp.src_port}→{tcp.dst_port}"
                elif udp:
                    log_entry += f" | UDP {udp.src_port}→{udp.dst_port}"
                elif icmp:
                    log_entry += f" | ICMP type={icmp.type}"
            elif ipv6:
                log_entry = f"[{timestamp}] {ipv6.src_ip} → {ipv6.dst_ip}"

            # Update logs in GUI thread-safe way (only if we have a valid log entry)
            if log_entry:
                logs_text.configure(state="normal")
                logs_text.insert("end", log_entry + "\n")
                logs_text.see("end")
                logs_text.configure(state="disabled")

            # Handle alerts
            if alerts:
                stats["total_alerts"] += len(alerts)
                for alert in alerts:
                    # Update specific threat counters
                    if "Port Scan" in alert:
                        stats["port_scans"] += 1
                    elif "SYN Flood" in alert:
                        stats["syn_floods"] += 1
                    elif "Brute Force" in alert:
                        stats["brute_force"] += 1
                    elif "DDoS" in alert:
                        stats["ddos_attacks"] += 1
                    elif "IP Spoofing" in alert:
                        stats["ip_spoofing"] += 1
                    # COMMENTED OUT: MAC Spoofing detection disabled
                    # elif "MAC Spoofing" in alert:
                    #     stats['mac_spoofing'] += 1
                    elif "ARP Spoofing" in alert:
                        stats["arp_spoofing"] += 1
                    elif "DNS Tunneling" in alert:
                        stats["dns_tunneling"] += 1
                    elif "ICMP Flood" in alert:
                        stats["icmp_floods"] += 1
                    elif "Unusual Protocol" in alert:
                        stats["unusual_protocols"] += 1

                    # Add alert to alerts panel
                    alert_timestamp = datetime.now().strftime("%H:%M:%S")
                    alert_entry = f"[{alert_timestamp}] {alert}"
                    alerts_text.configure(state="normal")
                    alerts_text.insert("end", alert_entry + "\n\n")
                    alerts_text.see("end")
                    alerts_text.configure(state="disabled")

            # Update statistics display
            update_statistics_display()

        # Schedule update in main GUI thread
        root.after(0, update_gui)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                  █▀ ▀█▀ ▄▀█ █▀█ ▀█▀ █ █▄░█ █▀▀ ░ █▀▀ ▄▀█ █▀█ ▀█▀ █░█ █▀█ █▀▀                     │
# │                  ▄█ ░█░ █▀█ █▀▄ ░█░ █ █░▀█ █▄█ ░ █▄▄ █▀█ █▀▀ ░█░ █▄█ █▀▄ ██▄                     │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def start_packet_capture():
        try:
            # Get interface from configuration
            interface = entry_widgets.get("INTERFACE", None)
            if interface:
                interface = interface.get()
            else:
                # Try to auto-select interface
                interfaces = get_if_list()
                interface = interfaces[0] if interfaces else "eth0"

            # Create state for threat detection
            capture_state["state"] = create_state()

            # Start capture and store sniffer object
            sniffer = start_capture(
                interface=interface,
                state=capture_state["state"],
                callback=gui_callback,
                count=0,  # Infinite capture
            )
            capture_sniffer["sniffer"] = sniffer
        except Exception as e:
            # Handle errors in GUI thread
            root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Packet capture error: {str(e)}"
                ),
            )
            root.after(0, lambda: toggle_start_stop())  # Stop on error


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │   ▀█▀ █▀█ █▀▀ █▀▀ █░░ █ █▄░█ █▀▀ ░ █▀ ▀█▀ ▄▀█ █▀█ ▀█▀ / █▀ ▀█▀ █▀█ █▀█ ░ █▀ ▀█▀ ▄▀█ ▀█▀ █▀▀      │
# │   ░█░ █▄█ █▄█ █▄█ █▄▄ █ █░▀█ █▄█ ░ ▄█ ░█░ █▀█ █▀▄ ░█░ / ▄█ ░█░ █▄█ █▀▀ ░ ▄█ ░█░ █▀█ ░█░ ██▄      │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def toggle_start_stop():
        if is_running["state"]:
            # Currently running, so stop it
            is_running["state"] = False
            start_stop_btn.config(
                text="▶ Start", bg=colors["success"], activebackground="#45a049"
            )
            status_label.config(text="● Stopped", fg=colors["text_dim"])

            # Stop the AsyncSniffer
            if capture_sniffer["sniffer"]:
                try:
                    capture_sniffer["sniffer"].stop()
                    capture_sniffer["sniffer"] = None
                except Exception as e:
                    print(f"Error stopping sniffer: {e}")

        else:
            # Currently stopped, so start it
            is_running["state"] = True
            start_stop_btn.config(
                text="⏹ Stop", bg=colors["danger"], activebackground="#da190b"
            )
            status_label.config(text="● Running", fg=colors["success"])

            # Start capture in separate thread
            capture_thread["thread"] = threading.Thread(
                target=start_packet_capture, daemon=True
            )
            capture_thread["thread"].start()


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                        █▀▀ █░░ █▀▀ ▄▀█ █▀█ █ █▄░█ █▀▀ ░ █░░ █▀█ █▀▀ █▀                           │
# │                        █▄▄ █▄▄ ██▄ █▀█ █▀▄ █ █░▀█ █▄█ ░ █▄▄ █▄█ █▄█ ▄█                           │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def clear_logs():
        logs_text.configure(state="normal")
        logs_text.delete("1.0", "end")
        logs_text.configure(state="disabled")

        alerts_text.configure(state="normal")
        alerts_text.delete("1.0", "end")
        alerts_text.configure(state="disabled")

        # Reset statistics
        for key in stats:
            stats[key] = 0
        update_statistics_display()

        messagebox.showinfo("Cleared", "All logs and alerts cleared")


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                     █▀ █░█░█ █ ▀█▀ █▀▀ █░█ █ █▄░█ █▀▀ ░ █░█ █ █▀▀ █░█░█ █▀                       │
# │                     ▄█ ▀▄▀▄▀ █ ░█░ █▄▄ █▀█ █ █░▀█ █▄█ ░ ▀▄▀ █ ██▄ ▀▄▀▄▀ ▄█                       │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    def switch_view(view_name):
        current_view["view"] = view_name

        # Update button styles
        for btn, name in menu_buttons:
            if name == view_name:
                btn.configure(bg=colors["accent"], fg=colors["text"])
            else:
                btn.configure(bg=colors["bg_light"], fg=colors["text_dim"])

        # Show/hide frames
        if view_name == "dashboard":
            dashboard_frame.pack(fill="both", expand=True)
            config_frame.pack_forget()
        elif view_name == "configuration":
            dashboard_frame.pack_forget()
            config_frame.pack(fill="both", expand=True)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                                    █▀ █ █▀▄ █▀▀ █▄▄ ▄▀█ █▀█                                      │
# │                                    ▄█ █ █▄▀ ██▄ █▄█ █▀█ █▀▄                                      │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    sidebar = tk.Frame(root, bg=colors["bg_medium"], width=200)
    sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    sidebar.grid_propagate(False)

    # Argus Logo/Title
    logo_frame = tk.Frame(sidebar, bg=colors["bg_medium"])
    logo_frame.pack(fill="x", padx=20, pady=30)

    logo_label = tk.Label(
        logo_frame,
        text="ARGUS",
        font=("Arial", 28, "bold"),
        fg=colors["accent"],
        bg=colors["bg_medium"],
    )
    logo_label.pack()

    subtitle_label = tk.Label(
        logo_frame,
        text="Network IDS",
        font=("Arial", 10),
        fg=colors["text_dim"],
        bg=colors["bg_medium"],
    )
    subtitle_label.pack()

    # Menu buttons
    menu_buttons = []

    # Dashboard button
    dashboard_btn = tk.Button(
        sidebar,
        text="📊 Dashboard",
        font=("Arial", 12),
        bg=colors["accent"],
        fg=colors["text"],
        activebackground=colors["accent"],
        activeforeground=colors["text"],
        relief="flat",
        cursor="hand2",
        command=lambda: switch_view("dashboard"),
    )
    dashboard_btn.pack(fill="x", padx=10, pady=5)
    menu_buttons.append((dashboard_btn, "dashboard"))

    # Configuration button
    config_btn = tk.Button(
        sidebar,
        text="⚙️ Configuration",
        font=("Arial", 12),
        bg=colors["bg_light"],
        fg=colors["text_dim"],
        activebackground=colors["accent"],
        activeforeground=colors["text"],
        relief="flat",
        cursor="hand2",
        command=lambda: switch_view("configuration"),
    )
    config_btn.pack(fill="x", padx=10, pady=5)
    menu_buttons.append((config_btn, "configuration"))

    ############################################################################
    #                               CONTENT AREA                               #
    ############################################################################

    content_area = tk.Frame(root, bg=colors["bg_dark"])
    content_area.grid(row=0, column=1, sticky="nsew")
    content_area.grid_rowconfigure(0, weight=1)
    content_area.grid_columnconfigure(0, weight=1)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                               █▀▄ ▄▀█ █▀ █░█ █▄▄ █▀█ ▄▀█ █▀█ █▀▄                                 │
# │                               █▄▀ █▀█ ▄█ █▀█ █▄█ █▄█ █▀█ █▀▄ █▄▀                                 │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    dashboard_frame = tk.Frame(content_area, bg=colors["bg_dark"])
    dashboard_frame.pack(fill="both", expand=True)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                      █▀ ▀█▀ ▄▀█ █▀█ ▀█▀ ░ █▀▀ ▄▀█ █▀█ ▀█▀ █░█ █▀█ █▀▀                       │
# │                      ▄█ ░█░ █▀█ █▀▄ ░█░ ░ █▄▄ █▀█ █▀▀ ░█░ █▄█ █▀▄ ██▄                       │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Control buttons at top
    control_frame = tk.Frame(dashboard_frame, bg=colors["bg_dark"])
    control_frame.pack(fill="x", padx=20, pady=15)

    # Dynamic Start/Stop button
    start_stop_btn = tk.Button(
        control_frame,
        text="▶ Start",
        font=("Arial", 11, "bold"),
        bg=colors["success"],
        fg=colors["text"],
        activebackground="#45a049",
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=toggle_start_stop,
    )
    start_stop_btn.pack(side="left", padx=5)

    # Clear Logs button
    clear_btn = tk.Button(
        control_frame,
        text="🗑 Clear Logs",
        font=("Arial", 11),
        bg=colors["bg_light"],
        fg=colors["text"],
        activebackground=colors["bg_medium"],
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=clear_logs,
    )
    clear_btn.pack(side="left", padx=5)

    # Export Logs button
    export_btn = tk.Button(
        control_frame,
        text="💾 Export Logs",
        font=("Arial", 11),
        bg=colors["bg_light"],
        fg=colors["text"],
        activebackground=colors["bg_medium"],
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=lambda: export_logs_to_json(logs_text, alerts_text),
    )
    export_btn.pack(side="left", padx=5)

    # Status indicator
    status_label = tk.Label(
        control_frame,
        text="● Stopped",
        font=("Arial", 11),
        fg=colors["text_dim"],
        bg=colors["bg_dark"],
    )
    status_label.pack(side="right", padx=10)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                      █▀ ▀█▀ ▄▀█ █▀█ ▀█▀ ░ █▀▀ ▄▀█ █▀█ ▀█▀ █░█ █▀█ █▀▀                       │
# │                      ▄█ ░█░ █▀█ █▀▄ ░█░ ░ █▄▄ █▀█ █▀▀ ░█░ █▄█ █▀▄ ██▄                       │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Filter section
    filter_frame = tk.Frame(dashboard_frame, bg=colors["bg_dark"])
    filter_frame.pack(fill="x", padx=20, pady=(0, 10))

    filter_label = tk.Label(
        filter_frame,
        text="🔍 Filter:",
        font=("Arial", 10),
        fg=colors["text_dim"],
        bg=colors["bg_dark"],
    )
    filter_label.pack(side="left", padx=(0, 10))

    filter_entry = tk.Entry(
        filter_frame,
        font=("Arial", 10),
        bg=colors["bg_light"],
        fg=colors["text"],
        insertbackground=colors["text"],
        relief="flat",
    )
    filter_entry.pack(side="left", fill="x", expand=True, ipady=5)

    # Add placeholder functionality
    placeholder_text = "e.g., ip.src == 192.168.1.1 or tcp.port == 80"
    filter_entry.insert(0, placeholder_text)
    filter_entry.config(fg=colors["text_dim"])

    def on_filter_focus_in(event):
        if filter_entry.get() == placeholder_text:
            filter_entry.delete(0, "end")
            filter_entry.config(fg=colors["text"])

    def on_filter_focus_out(event):
        if filter_entry.get() == "":
            filter_entry.insert(0, placeholder_text)
            filter_entry.config(fg=colors["text_dim"])

    filter_entry.bind("<FocusIn>", on_filter_focus_in)
    filter_entry.bind("<FocusOut>", on_filter_focus_out)

    filter_apply_btn = tk.Button(
        filter_frame,
        text="Apply",
        font=("Arial", 10),
        bg=colors["accent"],
        fg=colors["text"],
        activebackground="#005a9e",
        relief="flat",
        cursor="hand2",
        padx=15,
    )
    filter_apply_btn.pack(side="left", padx=(10, 0))


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                        █▀ ▀█▀ █▀█ █▀█ ░ █▀▀ ▄▀█ █▀█ ▀█▀ █░█ █▀█ █▀▀                         │
# │                        ▄█ ░█░ █▄█ █▀▀ ░ █▄▄ █▀█ █▀▀ ░█░ █▄█ █▀▄ ██▄                         │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Two-column layout for logs and alerts
    columns_frame = tk.Frame(dashboard_frame, bg=colors["bg_dark"])
    columns_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    columns_frame.grid_columnconfigure(0, weight=1)
    columns_frame.grid_columnconfigure(1, weight=1)
    columns_frame.grid_rowconfigure(0, weight=1)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                            █░░ █▀█ █▀▀ █▀ ░ █▀█ ▄▀█ █▄░█ █▀▀ █░░                            │
# │                            █▄▄ █▄█ █▄█ ▄█ ░ █▀▀ █▀█ █░▀█ ██▄ █▄▄                            │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Left column - Packet Logs
    logs_frame = tk.LabelFrame(
        columns_frame,
        text="📋 Packet Logs",
        font=("Arial", 11, "bold"),
        fg=colors["text"],
        bg=colors["bg_dark"],
        relief="flat",
    )
    logs_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    logs_text = scrolledtext.ScrolledText(
        logs_frame,
        font=("Courier", 9),
        bg=colors["bg_medium"],
        fg=colors["text"],
        insertbackground=colors["text"],
        relief="flat",
        wrap="none",
    )
    logs_text.pack(fill="both", expand=True, padx=5, pady=5)
    logs_text.configure(state="disabled")


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                        ▄▀█ █░░ █▀▀ █▀█ ▀█▀ █▀ ░ █▀█ ▄▀█ █▄░█ █▀▀ █░░                        │
# │                        █▀█ █▄▄ ██▄ █▀▄ ░█░ ▄█ ░ █▀▀ █▀█ █░▀█ ██▄ █▄▄                        │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Right column - Alerts
    alerts_frame = tk.LabelFrame(
        columns_frame,
        text="⚠️ Threat Alerts",
        font=("Arial", 11, "bold"),
        fg=colors["danger"],
        bg=colors["bg_dark"],
        relief="flat",
    )
    alerts_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    alerts_text = scrolledtext.ScrolledText(
        alerts_frame,
        font=("Courier", 9),
        bg=colors["bg_medium"],
        fg=colors["danger"],
        insertbackground=colors["text"],
        relief="flat",
        wrap="word",
    )
    alerts_text.pack(fill="both", expand=True, padx=5, pady=5)
    alerts_text.configure(state="disabled")


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                       █▀ ▀█▀ ▄▀█ ▀█▀ █ █▀ ▀█▀ █ █▀▀ █▀                       │
# │                       ▄█ ░█░ █▀█ ░█░ █ ▄█ ░█░ █ █▄▄ ▄█                       │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Statistics section
    stats_section_frame = tk.LabelFrame(
        dashboard_frame,
        text="📊 Statistics",
        font=("Arial", 11, "bold"),
        fg=colors["text"],
        bg=colors["bg_dark"],
        relief="flat",
    )
    stats_section_frame.pack(fill="x", padx=20, pady=(10, 10))

    # Statistics grid
    stats_grid = tk.Frame(stats_section_frame, bg=colors["bg_dark"])
    stats_grid.pack(fill="x", padx=10, pady=10)

    # Configure grid columns
    for i in range(6):
        stats_grid.grid_columnconfigure(i, weight=1)

    # Stat cards - Store references to value labels for updates
    stats_data = [
        ("Total Packets", "total_packets", colors["accent"]),
        ("Total Alerts", "total_alerts", colors["danger"]),
        ("Port Scans", "port_scans", colors["warning"]),
        ("SYN Floods", "syn_floods", colors["warning"]),
        ("Brute Force", "brute_force", colors["warning"]),
        ("DDoS Attacks", "ddos_attacks", colors["success"]),
    ]

    for idx, (label, stat_key, color) in enumerate(stats_data):
        stat_card = tk.Frame(stats_grid, bg=colors["bg_medium"], relief="flat")
        stat_card.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

        value_label = tk.Label(
            stat_card,
            text="0",
            font=("Arial", 20, "bold"),
            fg=color,
            bg=colors["bg_medium"],
        )
        value_label.pack(pady=(10, 0))
        stat_labels[stat_key] = value_label

        name_label = tk.Label(
            stat_card,
            text=label,
            font=("Arial", 9),
            fg=colors["text_dim"],
            bg=colors["bg_medium"],
        )
        name_label.pack(pady=(0, 10))

    # Additional statistics row
    stats_grid2 = tk.Frame(stats_section_frame, bg=colors["bg_dark"])
    stats_grid2.pack(fill="x", padx=10, pady=(0, 10))

    for i in range(5):  # Changed from 6 to 5 (MAC Spoofing card removed)
        stats_grid2.grid_columnconfigure(i, weight=1)

    stats_data2 = [
        ("IP Spoofing", "ip_spoofing", colors["success"]),
        # ("MAC Spoofing", "mac_spoofing", colors['success']),  # COMMENTED OUT: MAC Spoofing detection disabled
        ("ARP Spoofing", "arp_spoofing", colors["success"]),
        ("DNS Tunneling", "dns_tunneling", colors["success"]),
        ("ICMP Floods", "icmp_floods", colors["success"]),
        ("Unusual Protocols", "unusual_protocols", colors["success"]),
    ]

    for idx, (label, stat_key, color) in enumerate(stats_data2):
        stat_card = tk.Frame(stats_grid2, bg=colors["bg_medium"], relief="flat")
        stat_card.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

        value_label = tk.Label(
            stat_card,
            text="0",
            font=("Arial", 20, "bold"),
            fg=color,
            bg=colors["bg_medium"],
        )
        value_label.pack(pady=(10, 0))
        stat_labels[stat_key] = value_label

        name_label = tk.Label(
            stat_card,
            text=label,
            font=("Arial", 9),
            fg=colors["text_dim"],
            bg=colors["bg_medium"],
        )
        name_label.pack(pady=(0, 10))


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                       █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█                          │
# │                       █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ ░█░ █ █▄█ █░▀█                          │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    config_frame = tk.Frame(content_area, bg=colors["bg_dark"])
    # Don't pack yet - will be shown when button clicked


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │  █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█ ░ ▀█▀ █ ▀█▀ █░░ █▀▀  │
# │  █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ ░█░ █ █▄█ █░▀█ ░ ░█░ █ ░█░ █▄▄ ██▄  │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Configuration title
    config_title = tk.Label(
        config_frame,
        text="⚙️ Detection Thresholds Configuration",
        font=("Arial", 16, "bold"),
        fg=colors["text"],
        bg=colors["bg_dark"],
    )
    config_title.pack(pady=20)


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                 █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ ░ █▀ █▀▀ █▀█ █▀█ █░░ █░░ █▄▄ ▄▀█ █▀█                 │
# │                 █▄▄ █▄█ █░▀█ █▀░ █ █▄█ ░ ▄█ █▄▄ █▀▄ █▄█ █▄▄ █▄▄ █▄█ █▀█ █▀▄                 │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Scrollable configuration area
    config_canvas = tk.Canvas(config_frame, bg=colors["bg_dark"], highlightthickness=0)
    config_scrollbar = ttk.Scrollbar(
        config_frame, orient="vertical", command=config_canvas.yview
    )
    config_scrollable = tk.Frame(config_canvas, bg=colors["bg_dark"])

    config_scrollable.bind(
        "<Configure>",
        lambda e: config_canvas.configure(scrollregion=config_canvas.bbox("all")),
    )

    config_canvas.create_window((0, 0), window=config_scrollable, anchor="nw")
    config_canvas.configure(yscrollcommand=config_scrollbar.set)

    config_canvas.pack(side="left", fill="both", expand=True, padx=20)
    config_scrollbar.pack(side="right", fill="y")

    # Configuration fields
    config_fields = [
        (
            "Port Scan Detection",
            [
                (
                    "PORT_SCAN_THRESHOLD",
                    "20",
                    "Number of unique ports to trigger alert",
                ),
                ("PORT_SCAN_WINDOW", "10", "Time window in seconds"),
            ],
        ),
        (
            "SYN Flood Detection",
            [
                (
                    "SYN_FLOOD_THRESHOLD",
                    "100",
                    "Number of SYN packets to trigger alert",
                ),
                ("SYN_FLOOD_WINDOW", "5", "Time window in seconds"),
            ],
        ),
        (
            "DDoS Detection",
            [
                ("DDOS_THRESHOLD", "200", "Number of packets to single destination"),
                ("DDOS_WINDOW", "10", "Time window in seconds"),
            ],
        ),
        (
            "Brute Force Detection",
            [
                ("BRUTE_FORCE_THRESHOLD", "20", "Number of attempts to trigger alert"),
                ("BRUTE_FORCE_WINDOW", "60", "Time window in seconds"),
            ],
        ),
        (
            "ICMP Flood Detection",
            [
                (
                    "ICMP_FLOOD_THRESHOLD",
                    "100",
                    "Number of ICMP packets to trigger alert",
                ),
                ("ICMP_FLOOD_WINDOW", "5", "Time window in seconds"),
            ],
        ),
        (
            "DNS Tunneling Detection",
            [
                (
                    "DNS_TUNNELING_QUERY_THRESHOLD",
                    "100",
                    "Number of DNS queries to trigger alert",
                ),
                ("DNS_TUNNELING_WINDOW", "60", "Time window in seconds"),
                (
                    "DNS_TUNNELING_LONG_QUERY_LENGTH",
                    "50",
                    "Character length considered 'long'",
                ),
                (
                    "DNS_TUNNELING_LONG_QUERY_RATIO",
                    "0.6",
                    "Ratio of long queries to trigger alert",
                ),
            ],
        ),
        (
            "Abnormal Traffic Detection",
            [
                (
                    "ABNORMAL_TRAFFIC_THRESHOLD",
                    "2000",
                    "Number of packets from single source",
                ),
                ("ABNORMAL_TRAFFIC_WINDOW", "60", "Time window in seconds"),
            ],
        ),
        (
            "IP/MAC Spoofing Detection",
            [
                (
                    "SPOOFING_THRESHOLD",
                    "3",
                    "Number of different MACs/IPs before alerting",
                ),
                ("SPOOFING_WINDOW", "300", "Time window to track changes (seconds)"),
            ],
        ),
        (
            "Capture Settings",
            [
                ("PACKET_COUNT", "0", "Number of packets to capture (0 = infinite)"),
                ("VERBOSE_MODE", "False", "Enable verbose logging (True/False)"),
            ],
        ),
    ]

    # Get available network interfaces
    available_interfaces = get_if_list()
    # Prefer wlp8s0 if available, otherwise use first available interface
    if "wlp8s0" in available_interfaces:
        default_interface = "wlp8s0"
    elif available_interfaces:
        default_interface = available_interfaces[0]
    else:
        default_interface = "eth0"


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │     █▄░█ █▀▀ ▀█▀ █░█░█ █▀█ █▀█ █▄▀ ░ █ █▄░█ ▀█▀ █▀▀ █▀█ █▀▀ ▄▀█ █▀▀ █▀▀     │
# │     █░▀█ ██▄ ░█░ ▀▄▀▄▀ █▄█ █▀▄ █░█ ░ █ █░▀█ ░█░ ██▄ █▀▄ █▀░ █▀█ █▄▄ ██▄     │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Create Network Interface section first (with dropdown)
    interface_section = tk.LabelFrame(
        config_scrollable,
        text="Network Interface",
        font=("Arial", 12, "bold"),
        fg=colors["accent"],
        bg=colors["bg_dark"],
        relief="flat",
    )
    interface_section.pack(fill="x", padx=20, pady=10)

    interface_field_frame = tk.Frame(interface_section, bg=colors["bg_dark"])
    interface_field_frame.pack(fill="x", padx=15, pady=8)

    # Field name
    interface_name_label = tk.Label(
        interface_field_frame,
        text="INTERFACE",
        font=("Arial", 10, "bold"),
        fg=colors["text"],
        bg=colors["bg_dark"],
        anchor="w",
    )
    interface_name_label.pack(fill="x")

    # Description
    interface_desc_label = tk.Label(
        interface_field_frame,
        text="Select network interface to monitor",
        font=("Arial", 9),
        fg=colors["text_dim"],
        bg=colors["bg_dark"],
        anchor="w",
    )
    interface_desc_label.pack(fill="x")

    # Dropdown (Combobox) for interface selection
    interface_combo = ttk.Combobox(
        interface_field_frame,
        values=available_interfaces,
        font=("Arial", 10),
        state="readonly",
    )
    interface_combo.pack(fill="x", pady=(5, 0), ipady=5)
    interface_combo.set(default_interface)

    # Store in entry_widgets for compatibility with save function
    entry_widgets["INTERFACE"] = interface_combo


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │  █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█ ░ █▀▀ █ █▀▀ █░░ █▀▄ █▀   │
# │  █▄▄ █▄█ █░▀█ █▀░ █ █▄█ █▄█ █▀▄ █▀█ ░█░ █ █▄█ █░▀█ ░ █▀░ █ ██▄ █▄▄ █▄▀ ▄█   │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Create other configuration sections
    for section_name, fields in config_fields:
        # Section frame
        section_frame = tk.LabelFrame(
            config_scrollable,
            text=section_name,
            font=("Arial", 12, "bold"),
            fg=colors["accent"],
            bg=colors["bg_dark"],
            relief="flat",
        )
        section_frame.pack(fill="x", padx=20, pady=10)

        # Fields in section
        for field_name, default_value, description in fields:
            field_frame = tk.Frame(section_frame, bg=colors["bg_dark"])
            field_frame.pack(fill="x", padx=15, pady=8)

            # Field name
            name_label = tk.Label(
                field_frame,
                text=field_name,
                font=("Arial", 10, "bold"),
                fg=colors["text"],
                bg=colors["bg_dark"],
                anchor="w",
            )
            name_label.pack(fill="x")

            # Description
            desc_label = tk.Label(
                field_frame,
                text=description,
                font=("Arial", 9),
                fg=colors["text_dim"],
                bg=colors["bg_dark"],
                anchor="w",
            )
            desc_label.pack(fill="x")

            # Entry field
            entry = tk.Entry(
                field_frame,
                font=("Arial", 10),
                bg=colors["bg_light"],
                fg=colors["text"],
                insertbackground=colors["text"],
                relief="flat",
            )
            entry.pack(fill="x", pady=(5, 0), ipady=5)
            entry.insert(0, default_value)

            entry_widgets[field_name] = entry


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                  █▀ ▄▀█ █░█ █▀▀ ░ █▄▄ █░█ ▀█▀ ▀█▀ █▀█ █▄░█                  │
# │                  ▄█ █▀█ ▀▄▀ ██▄ ░ █▄█ █▄█ ░█░ ░█░ █▄█ █░▀█                  │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    # Save button at bottom of config
    save_btn_frame = tk.Frame(config_scrollable, bg=colors["bg_dark"])
    save_btn_frame.pack(fill="x", padx=20, pady=20)

    save_config_btn = tk.Button(
        save_btn_frame,
        text="💾 Save",
        font=("Arial", 12, "bold"),
        bg=colors["success"],
        fg=colors["text"],
        activebackground="#45a049",
        relief="flat",
        cursor="hand2",
        padx=30,
        pady=10,
        command=lambda: save_config_to_json(entry_widgets),
    )
    save_config_btn.pack()


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                           █▀▀ █▄█ █▄█ ▀█▀ ██▄ █▀█                            │
# │                           █▀░ █▄█ █▄█ ░█░ ██▄ █▀▄                            │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
    footer = tk.Frame(root, bg=colors["bg_medium"], height=40)
    footer.grid(row=1, column=0, columnspan=2, sticky="ew")
    footer.grid_propagate(False)

    footer_label = tk.Label(
        footer,
        text="Made by Binam Adhikari 2026",
        font=("Arial", 10),
        fg=colors["text_dim"],
        bg=colors["bg_medium"],
    )
    footer_label.pack(expand=True)

    return root

# ╔──────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                               █▀▄▀█ ▄▀█ █ █▄░█                               │
# │                               █░▀░█ █▀█ █ █░▀█                               │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────╝


# ╔──────────────────────────────────────────────────────────────────────────────────────────────────╗
# │                                                                                              │
# │                            █▀▄▀█ ▄▀█ █ █▄░█ ░ █▀▀ █▄░█ ▀█▀ █▀█ ▀▄▀                               │
# │                            █░▀░█ █▀█ █ █░▀█ ░ ██▄ █░▀█ ░█░ █▀▄ ░█░                               │
# │                                                                                              │
# ╚──────────────────────────────────────────────────────────────────────────────────────────────────╝
def main():
    root = create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
