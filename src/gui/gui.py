#!/usr/bin/env python3
"""
Argus NIDS - Tkinter GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from datetime import datetime
from pathlib import Path


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def save_config_to_json(entry_widgets):
    """Save configuration values to JSON file"""
    config_data = {}
    
    for field_name, entry in entry_widgets.items():
        value = entry.get()
        try:
            if '.' in value:
                config_data[field_name] = float(value)
            elif value.lower() in ('true', 'false'):
                config_data[field_name] = value.lower() == 'true'
            else:
                config_data[field_name] = int(value)
        except ValueError:
            config_data[field_name] = value
    
    config_data['last_updated'] = datetime.now().isoformat()
    
    config_path = Path(__file__).parent.parent / 'config.json'
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        messagebox.showinfo("Success", f"Configuration saved to:\n{config_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")


def export_logs_to_json(logs_text, alerts_text):
    """Export logs and alerts to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"argus_logs_{timestamp}.json"
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialfile=default_filename
    )
    
    if not filepath:
        return
    
    logs_content = logs_text.get("1.0", "end-1c")
    alerts_content = alerts_text.get("1.0", "end-1c")
    
    logs_list = [line.strip() for line in logs_content.split('\n') if line.strip()]
    alerts_list = [line.strip() for line in alerts_content.split('\n') if line.strip()]
    
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "total_packets": len(logs_list),
        "total_alerts": len(alerts_list),
        "packet_logs": logs_list,
        "threat_alerts": alerts_list
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=4)
        messagebox.showinfo("Success", f"Logs exported to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export logs:\n{str(e)}")


# ============================================================================
# MAIN WINDOW SETUP
# ============================================================================

def create_gui():
    """Create and configure the main GUI window"""
    root = tk.Tk()
    root.title("Argus NIDS - Network Intrusion Detection System")
    root.geometry("1400x900")
    root.minsize(1200, 700)
    
    # Configure root grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    # Color scheme
    colors = {
        'bg_dark': '#1e1e1e',
        'bg_medium': '#2d2d2d',
        'bg_light': '#3d3d3d',
        'accent': '#007acc',
        'text': '#ffffff',
        'text_dim': '#cccccc',
        'success': '#4caf50',
        'warning': '#ff9800',
        'danger': '#f44336',
    }
    
    root.configure(bg=colors['bg_dark'])
    
    # ========================================================================
    # SIDEBAR / MENU
    # ========================================================================
    
    sidebar = tk.Frame(root, bg=colors['bg_medium'], width=200)
    sidebar.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
    sidebar.grid_propagate(False)
    
    # Argus Logo/Title
    logo_frame = tk.Frame(sidebar, bg=colors['bg_medium'])
    logo_frame.pack(fill='x', padx=20, pady=30)
    
    logo_label = tk.Label(
        logo_frame,
        text="ARGUS",
        font=('Arial', 28, 'bold'),
        fg=colors['accent'],
        bg=colors['bg_medium']
    )
    logo_label.pack()
    
    subtitle_label = tk.Label(
        logo_frame,
        text="Network IDS",
        font=('Arial', 10),
        fg=colors['text_dim'],
        bg=colors['bg_medium']
    )
    subtitle_label.pack()
    
    # Menu buttons
    menu_buttons = []
    current_view = {'view': 'dashboard'}  # Track current view
    
    def switch_view(view_name):
        """Switch between dashboard and configuration views"""
        current_view['view'] = view_name
        
        # Update button styles
        for btn, name in menu_buttons:
            if name == view_name:
                btn.configure(bg=colors['accent'], fg=colors['text'])
            else:
                btn.configure(bg=colors['bg_light'], fg=colors['text_dim'])
        
        # Show/hide frames
        if view_name == 'dashboard':
            dashboard_frame.pack(fill='both', expand=True)
            config_frame.pack_forget()
        elif view_name == 'configuration':
            dashboard_frame.pack_forget()
            config_frame.pack(fill='both', expand=True)
    
    # Dashboard button
    dashboard_btn = tk.Button(
        sidebar,
        text="📊 Dashboard",
        font=('Arial', 12),
        bg=colors['accent'],
        fg=colors['text'],
        activebackground=colors['accent'],
        activeforeground=colors['text'],
        relief='flat',
        cursor='hand2',
        command=lambda: switch_view('dashboard')
    )
    dashboard_btn.pack(fill='x', padx=10, pady=5)
    menu_buttons.append((dashboard_btn, 'dashboard'))
    
    # Configuration button
    config_btn = tk.Button(
        sidebar,
        text="⚙️ Configuration",
        font=('Arial', 12),
        bg=colors['bg_light'],
        fg=colors['text_dim'],
        activebackground=colors['accent'],
        activeforeground=colors['text'],
        relief='flat',
        cursor='hand2',
        command=lambda: switch_view('configuration')
    )
    config_btn.pack(fill='x', padx=10, pady=5)
    menu_buttons.append((config_btn, 'configuration'))
    
    # ========================================================================
    # MAIN CONTENT AREA
    # ========================================================================
    
    content_area = tk.Frame(root, bg=colors['bg_dark'])
    content_area.grid(row=0, column=1, sticky='nsew')
    content_area.grid_rowconfigure(0, weight=1)
    content_area.grid_columnconfigure(0, weight=1)
    
    # ========================================================================
    # DASHBOARD VIEW
    # ========================================================================
    
    dashboard_frame = tk.Frame(content_area, bg=colors['bg_dark'])
    dashboard_frame.pack(fill='both', expand=True)
    
    # Control buttons at top
    control_frame = tk.Frame(dashboard_frame, bg=colors['bg_dark'])
    control_frame.pack(fill='x', padx=20, pady=15)
    
    # Track running state
    is_running = {'state': False}
    
    def toggle_start_stop():
        """Toggle between Start and Stop states"""
        if is_running['state']:
            # Currently running, so stop it
            is_running['state'] = False
            start_stop_btn.config(
                text="▶ Start",
                bg=colors['success'],
                activebackground='#45a049'
            )
            status_label.config(text="● Stopped", fg=colors['text_dim'])
            messagebox.showinfo("Stopped", "Packet capture stopped")
        else:
            # Currently stopped, so start it
            is_running['state'] = True
            start_stop_btn.config(
                text="⏹ Stop",
                bg=colors['danger'],
                activebackground='#da190b'
            )
            status_label.config(text="● Running", fg=colors['success'])
            messagebox.showinfo("Started", "Packet capture started")
    
    def clear_logs():
        """Clear all logs and alerts"""
        logs_text.configure(state='normal')
        logs_text.delete('1.0', 'end')
        logs_text.configure(state='disabled')
        
        alerts_text.configure(state='normal')
        alerts_text.delete('1.0', 'end')
        alerts_text.configure(state='disabled')
        
        messagebox.showinfo("Cleared", "All logs and alerts cleared")
    
    # Dynamic Start/Stop button
    start_stop_btn = tk.Button(
        control_frame,
        text="▶ Start",
        font=('Arial', 11, 'bold'),
        bg=colors['success'],
        fg=colors['text'],
        activebackground='#45a049',
        relief='flat',
        cursor='hand2',
        padx=20,
        pady=8,
        command=toggle_start_stop
    )
    start_stop_btn.pack(side='left', padx=5)
    
    # Clear Logs button
    clear_btn = tk.Button(
        control_frame,
        text="🗑 Clear Logs",
        font=('Arial', 11),
        bg=colors['bg_light'],
        fg=colors['text'],
        activebackground=colors['bg_medium'],
        relief='flat',
        cursor='hand2',
        padx=20,
        pady=8,
        command=clear_logs
    )
    clear_btn.pack(side='left', padx=5)
    
    # Export Logs button
    export_btn = tk.Button(
        control_frame,
        text="💾 Export Logs",
        font=('Arial', 11),
        bg=colors['bg_light'],
        fg=colors['text'],
        activebackground=colors['bg_medium'],
        relief='flat',
        cursor='hand2',
        padx=20,
        pady=8,
        command=lambda: export_logs_to_json(logs_text, alerts_text)
    )
    export_btn.pack(side='left', padx=5)
    
    # Status indicator
    status_label = tk.Label(
        control_frame,
        text="● Stopped",
        font=('Arial', 11),
        fg=colors['text_dim'],
        bg=colors['bg_dark']
    )
    status_label.pack(side='right', padx=10)
    
    # Filter section
    filter_frame = tk.Frame(dashboard_frame, bg=colors['bg_dark'])
    filter_frame.pack(fill='x', padx=20, pady=(0, 10))
    
    filter_label = tk.Label(
        filter_frame,
        text="🔍 Filter:",
        font=('Arial', 10),
        fg=colors['text_dim'],
        bg=colors['bg_dark']
    )
    filter_label.pack(side='left', padx=(0, 10))
    
    filter_entry = tk.Entry(
        filter_frame,
        font=('Arial', 10),
        bg=colors['bg_light'],
        fg=colors['text'],
        insertbackground=colors['text'],
        relief='flat'
    )
    filter_entry.pack(side='left', fill='x', expand=True, ipady=5)
    
    # Add placeholder functionality
    placeholder_text = "e.g., ip.src == 192.168.1.1 or tcp.port == 80"
    filter_entry.insert(0, placeholder_text)
    filter_entry.config(fg=colors['text_dim'])
    
    def on_filter_focus_in(event):
        if filter_entry.get() == placeholder_text:
            filter_entry.delete(0, 'end')
            filter_entry.config(fg=colors['text'])
    
    def on_filter_focus_out(event):
        if filter_entry.get() == '':
            filter_entry.insert(0, placeholder_text)
            filter_entry.config(fg=colors['text_dim'])
    
    filter_entry.bind('<FocusIn>', on_filter_focus_in)
    filter_entry.bind('<FocusOut>', on_filter_focus_out)
    
    filter_apply_btn = tk.Button(
        filter_frame,
        text="Apply",
        font=('Arial', 10),
        bg=colors['accent'],
        fg=colors['text'],
        activebackground='#005a9e',
        relief='flat',
        cursor='hand2',
        padx=15
    )
    filter_apply_btn.pack(side='left', padx=(10, 0))
    
    # Two-column layout for logs and alerts
    columns_frame = tk.Frame(dashboard_frame, bg=colors['bg_dark'])
    columns_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
    columns_frame.grid_columnconfigure(0, weight=1)
    columns_frame.grid_columnconfigure(1, weight=1)
    columns_frame.grid_rowconfigure(0, weight=1)
    
    # Left column - Packet Logs
    logs_frame = tk.LabelFrame(
        columns_frame,
        text="📋 Packet Logs",
        font=('Arial', 11, 'bold'),
        fg=colors['text'],
        bg=colors['bg_dark'],
        relief='flat'
    )
    logs_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    logs_text = scrolledtext.ScrolledText(
        logs_frame,
        font=('Courier', 9),
        bg=colors['bg_medium'],
        fg=colors['text'],
        insertbackground=colors['text'],
        relief='flat',
        wrap='none'
    )
    logs_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Sample log entries
    sample_logs = [
        "[00:01:23] 192.168.1.100:54321 → 192.168.1.1:80 | TCP | SYN",
        "[00:01:24] 192.168.1.100:54322 → 192.168.1.1:443 | TCP | SYN",
        "[00:01:25] 10.0.0.5:12345 → 8.8.8.8:53 | UDP | DNS Query",
        "[00:01:26] 192.168.1.50 → 192.168.1.255 | ICMP | Echo Request",
        "[00:01:27] 172.16.0.10:22 → 172.16.0.1:54000 | TCP | ACK",
    ]
    
    for log in sample_logs:
        logs_text.insert('end', log + '\n')
    
    logs_text.configure(state='disabled')
    
    # Right column - Alerts
    alerts_frame = tk.LabelFrame(
        columns_frame,
        text="⚠️ Threat Alerts",
        font=('Arial', 11, 'bold'),
        fg=colors['danger'],
        bg=colors['bg_dark'],
        relief='flat'
    )
    alerts_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
    
    alerts_text = scrolledtext.ScrolledText(
        alerts_frame,
        font=('Courier', 9),
        bg=colors['bg_medium'],
        fg=colors['danger'],
        insertbackground=colors['text'],
        relief='flat',
        wrap='word'
    )
    alerts_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Sample alerts
    sample_alerts = [
        "[00:01:30] Port Scan: 192.168.1.100 tried 25 ports in 10s",
        "[00:01:45] SYN Flood: 10.0.0.50 sent 150 SYN packets in 5s",
        "[00:02:10] Brute Force: 172.16.0.99 made 22 attempts on port 22 in 60s",
    ]
    
    for alert in sample_alerts:
        alerts_text.insert('end', alert + '\n\n')
    
    alerts_text.configure(state='disabled')
    
    # Matplotlib graph section for threats over time
    graph_frame = tk.LabelFrame(
        dashboard_frame,
        text="📈 Threats Over Time",
        font=('Arial', 11, 'bold'),
        fg=colors['text'],
        bg=colors['bg_dark'],
        relief='flat'
    )
    graph_frame.pack(fill='x', padx=20, pady=(10, 10))
    
    # Placeholder for matplotlib graph
    graph_placeholder = tk.Label(
        graph_frame,
        text="[Matplotlib Graph Area]\nReal-time graph showing total threats detected over time will be displayed here",
        font=('Arial', 10),
        fg=colors['text_dim'],
        bg=colors['bg_medium'],
        height=8,
        relief='flat'
    )
    graph_placeholder.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Statistics section
    stats_frame = tk.LabelFrame(
        dashboard_frame,
        text="📊 Statistics",
        font=('Arial', 11, 'bold'),
        fg=colors['text'],
        bg=colors['bg_dark'],
        relief='flat'
    )
    stats_frame.pack(fill='x', padx=20, pady=(10, 10))
    
    # Statistics grid
    stats_grid = tk.Frame(stats_frame, bg=colors['bg_dark'])
    stats_grid.pack(fill='x', padx=10, pady=10)
    
    # Configure grid columns
    for i in range(6):
        stats_grid.grid_columnconfigure(i, weight=1)
    
    # Stat cards
    stats_data = [
        ("Total Packets", "1,234", colors['accent']),
        ("Total Alerts", "3", colors['danger']),
        ("Port Scans", "1", colors['warning']),
        ("SYN Floods", "1", colors['warning']),
        ("Brute Force", "1", colors['warning']),
        ("DDoS Attacks", "0", colors['success']),
    ]
    
    for idx, (label, value, color) in enumerate(stats_data):
        stat_card = tk.Frame(stats_grid, bg=colors['bg_medium'], relief='flat')
        stat_card.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')
        
        value_label = tk.Label(
            stat_card,
            text=value,
            font=('Arial', 20, 'bold'),
            fg=color,
            bg=colors['bg_medium']
        )
        value_label.pack(pady=(10, 0))
        
        name_label = tk.Label(
            stat_card,
            text=label,
            font=('Arial', 9),
            fg=colors['text_dim'],
            bg=colors['bg_medium']
        )
        name_label.pack(pady=(0, 10))
    
    # Additional statistics row
    stats_grid2 = tk.Frame(stats_frame, bg=colors['bg_dark'])
    stats_grid2.pack(fill='x', padx=10, pady=(0, 10))
    
    for i in range(6):
        stats_grid2.grid_columnconfigure(i, weight=1)
    
    stats_data2 = [
        ("IP Spoofing", "0", colors['success']),
        ("MAC Spoofing", "0", colors['success']),
        ("ARP Spoofing", "0", colors['success']),
        ("DNS Tunneling", "0", colors['success']),
        ("ICMP Floods", "0", colors['success']),
        ("Unusual Protocols", "0", colors['success']),
    ]
    
    for idx, (label, value, color) in enumerate(stats_data2):
        stat_card = tk.Frame(stats_grid2, bg=colors['bg_medium'], relief='flat')
        stat_card.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')
        
        value_label = tk.Label(
            stat_card,
            text=value,
            font=('Arial', 20, 'bold'),
            fg=color,
            bg=colors['bg_medium']
        )
        value_label.pack(pady=(10, 0))
        
        name_label = tk.Label(
            stat_card,
            text=label,
            font=('Arial', 9),
            fg=colors['text_dim'],
            bg=colors['bg_medium']
        )
        name_label.pack(pady=(0, 10))
    
    # ========================================================================
    # CONFIGURATION VIEW
    # ========================================================================
    
    config_frame = tk.Frame(content_area, bg=colors['bg_dark'])
    # Don't pack yet - will be shown when button clicked
    
    # Configuration title
    config_title = tk.Label(
        config_frame,
        text="⚙️ Detection Thresholds Configuration",
        font=('Arial', 16, 'bold'),
        fg=colors['text'],
        bg=colors['bg_dark']
    )
    config_title.pack(pady=20)
    
    # Scrollable configuration area
    config_canvas = tk.Canvas(config_frame, bg=colors['bg_dark'], highlightthickness=0)
    config_scrollbar = ttk.Scrollbar(config_frame, orient='vertical', command=config_canvas.yview)
    config_scrollable = tk.Frame(config_canvas, bg=colors['bg_dark'])
    
    config_scrollable.bind(
        '<Configure>',
        lambda e: config_canvas.configure(scrollregion=config_canvas.bbox('all'))
    )
    
    config_canvas.create_window((0, 0), window=config_scrollable, anchor='nw')
    config_canvas.configure(yscrollcommand=config_scrollbar.set)
    
    config_canvas.pack(side='left', fill='both', expand=True, padx=20)
    config_scrollbar.pack(side='right', fill='y')
    
    # Configuration fields
    config_fields = [
        ("Port Scan Detection", [
            ("PORT_SCAN_THRESHOLD", "20", "Number of unique ports to trigger alert"),
            ("PORT_SCAN_WINDOW", "10", "Time window in seconds"),
        ]),
        ("SYN Flood Detection", [
            ("SYN_FLOOD_THRESHOLD", "100", "Number of SYN packets to trigger alert"),
            ("SYN_FLOOD_WINDOW", "5", "Time window in seconds"),
        ]),
        ("DDoS Detection", [
            ("DDOS_THRESHOLD", "200", "Number of packets to single destination"),
            ("DDOS_WINDOW", "10", "Time window in seconds"),
        ]),
        ("Brute Force Detection", [
            ("BRUTE_FORCE_THRESHOLD", "20", "Number of attempts to trigger alert"),
            ("BRUTE_FORCE_WINDOW", "60", "Time window in seconds"),
        ]),
        ("ICMP Flood Detection", [
            ("ICMP_FLOOD_THRESHOLD", "100", "Number of ICMP packets to trigger alert"),
            ("ICMP_FLOOD_WINDOW", "5", "Time window in seconds"),
        ]),
        ("DNS Tunneling Detection", [
            ("DNS_TUNNELING_QUERY_THRESHOLD", "100", "Number of DNS queries to trigger alert"),
            ("DNS_TUNNELING_WINDOW", "60", "Time window in seconds"),
            ("DNS_TUNNELING_LONG_QUERY_LENGTH", "50", "Character length considered 'long'"),
            ("DNS_TUNNELING_LONG_QUERY_RATIO", "0.6", "Ratio of long queries to trigger alert"),
        ]),
        ("Abnormal Traffic Detection", [
            ("ABNORMAL_TRAFFIC_THRESHOLD", "2000", "Number of packets from single source"),
            ("ABNORMAL_TRAFFIC_WINDOW", "60", "Time window in seconds"),
        ]),
        ("IP/MAC Spoofing Detection", [
            ("SPOOFING_THRESHOLD", "3", "Number of different MACs/IPs before alerting"),
            ("SPOOFING_WINDOW", "300", "Time window to track changes (seconds)"),
        ]),
        ("Network Interface", [
            ("INTERFACE", "eth0", "Network interface to monitor (e.g., eth0, wlan0)"),
        ]),
        ("Capture Settings", [
            ("PACKET_COUNT", "0", "Number of packets to capture (0 = infinite)"),
            ("VERBOSE_MODE", "False", "Enable verbose logging (True/False)"),
        ]),
    ]
    
    entry_widgets = {}  # Store entry widgets for later access
    
    for section_name, fields in config_fields:
        # Section frame
        section_frame = tk.LabelFrame(
            config_scrollable,
            text=section_name,
            font=('Arial', 12, 'bold'),
            fg=colors['accent'],
            bg=colors['bg_dark'],
            relief='flat'
        )
        section_frame.pack(fill='x', padx=20, pady=10)
        
        # Fields in section
        for field_name, default_value, description in fields:
            field_frame = tk.Frame(section_frame, bg=colors['bg_dark'])
            field_frame.pack(fill='x', padx=15, pady=8)
            
            # Field name
            name_label = tk.Label(
                field_frame,
                text=field_name,
                font=('Arial', 10, 'bold'),
                fg=colors['text'],
                bg=colors['bg_dark'],
                anchor='w'
            )
            name_label.pack(fill='x')
            
            # Description
            desc_label = tk.Label(
                field_frame,
                text=description,
                font=('Arial', 9),
                fg=colors['text_dim'],
                bg=colors['bg_dark'],
                anchor='w'
            )
            desc_label.pack(fill='x')
            
            # Entry field
            entry = tk.Entry(
                field_frame,
                font=('Arial', 10),
                bg=colors['bg_light'],
                fg=colors['text'],
                insertbackground=colors['text'],
                relief='flat'
            )
            entry.pack(fill='x', pady=(5, 0), ipady=5)
            entry.insert(0, default_value)
            
            entry_widgets[field_name] = entry
    
    # Save button at bottom of config
    save_btn_frame = tk.Frame(config_scrollable, bg=colors['bg_dark'])
    save_btn_frame.pack(fill='x', padx=20, pady=20)
    
    save_config_btn = tk.Button(
        save_btn_frame,
        text="💾 Save",
        font=('Arial', 12, 'bold'),
        bg=colors['success'],
        fg=colors['text'],
        activebackground='#45a049',
        relief='flat',
        cursor='hand2',
        padx=30,
        pady=10,
        command=lambda: save_config_to_json(entry_widgets)
    )
    save_config_btn.pack()
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    footer = tk.Frame(root, bg=colors['bg_medium'], height=40)
    footer.grid(row=1, column=0, columnspan=2, sticky='ew')
    footer.grid_propagate(False)
    
    footer_label = tk.Label(
        footer,
        text="Made by Binam Adhikari 2026",
        font=('Arial', 10),
        fg=colors['text_dim'],
        bg=colors['bg_medium']
    )
    footer_label.pack(expand=True)
    
    return root


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the GUI"""
    root = create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
