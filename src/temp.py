import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP, DNS, Raw
import threading
import queue
import time

# Page config
st.set_page_config(page_title="NIDS Dashboard - Scapy", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 8px; }
    .critical { color: #ff4444; font-weight: bold; }
    .high { color: #ff8800; font-weight: bold; }
    .medium { color: #ffaa00; font-weight: bold; }
    .low { color: #4caf50; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'packets' not in st.session_state:
    st.session_state.packets = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'total_packets' not in st.session_state:
    st.session_state.total_packets = 0
if 'threats_detected' not in st.session_state:
    st.session_state.threats_detected = 0
if 'blocked_ips' not in st.session_state:
    st.session_state.blocked_ips = 0
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = {'time': [], 'packets': []}
if 'packet_queue' not in st.session_state:
    st.session_state.packet_queue = queue.Queue()
if 'sniffer_thread' not in st.session_state:
    st.session_state.sniffer_thread = None
if 'packet_count_current' not in st.session_state:
    st.session_state.packet_count_current = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Suspicious ports and IPs
SUSPICIOUS_PORTS = [21, 23, 135, 139, 445, 3389, 5900, 1433, 3306]
BLACKLISTED_IPS = ['192.168.1.100', '10.0.0.50']  # Example blacklist
DOS_THRESHOLD = 100  # Packets per second from single IP

def analyze_threat(packet_info):
    """Analyze packet for threats"""
    threat_level = 'Low'
    reasons = []
    
    # Check port-based threats
    if packet_info['dport'] in SUSPICIOUS_PORTS:
        threat_level = 'Medium'
        reasons.append(f"Suspicious port {packet_info['dport']}")
    
    # Check blacklisted IPs
    if packet_info['src'] in BLACKLISTED_IPS or packet_info['dst'] in BLACKLISTED_IPS:
        threat_level = 'Critical'
        reasons.append("Blacklisted IP detected")
    
    # Check for port scanning (multiple different ports from same source)
    if packet_info['protocol'] == 'TCP' and packet_info['flags'] == 'S':
        threat_level = 'High'
        reasons.append("Possible port scan (SYN packet)")
    
    # Check packet size for potential attacks
    if packet_info['length'] > 1500:
        threat_level = 'Medium' if threat_level == 'Low' else threat_level
        reasons.append("Large packet detected")
    
    # DNS-based threats
    if packet_info['protocol'] == 'DNS' and packet_info['dport'] != 53:
        threat_level = 'High'
        reasons.append("DNS traffic on non-standard port")
    
    # ICMP flood detection
    if packet_info['protocol'] == 'ICMP':
        threat_level = 'Medium'
        reasons.append("ICMP traffic detected")
    
    return threat_level, reasons

def packet_callback(packet):
    """Callback function for scapy sniffing"""
    try:
        if IP in packet:
            # Extract packet information
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            length = len(packet)
            
            # Determine protocol name and ports
            proto_name = "IP"
            sport = 0
            dport = 0
            flags = ""
            
            if TCP in packet:
                proto_name = "TCP"
                sport = packet[TCP].sport
                dport = packet[TCP].dport
                flags = packet[TCP].flags
                
            elif UDP in packet:
                proto_name = "UDP"
                sport = packet[UDP].sport
                dport = packet[UDP].dport
                
            elif ICMP in packet:
                proto_name = "ICMP"
                
            elif DNS in packet:
                proto_name = "DNS"
                sport = packet[UDP].sport if UDP in packet else 0
                dport = packet[UDP].dport if UDP in packet else 0
            
            # Create packet info dict
            packet_info = {
                'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3],
                'src': src_ip,
                'dst': dst_ip,
                'protocol': proto_name,
                'sport': sport,
                'dport': dport,
                'length': length,
                'flags': str(flags)
            }
            
            # Analyze for threats
            threat_level, reasons = analyze_threat(packet_info)
            packet_info['threat'] = threat_level
            packet_info['reasons'] = ', '.join(reasons) if reasons else 'Normal traffic'
            packet_info['action'] = 'Blocked' if threat_level in ['Critical', 'High'] else 'Allowed'
            
            # Put in queue for main thread
            st.session_state.packet_queue.put(packet_info)
            
    except Exception as e:
        pass  # Silently ignore malformed packets

def start_sniffing(interface=None):
    """Start packet sniffing in background thread"""
    try:
        # Sniff packets - filter for IP traffic only
        sniff(
            prn=packet_callback,
            store=False,
            iface=interface,
            filter="ip",
            stop_filter=lambda x: not st.session_state.monitoring
        )
    except Exception as e:
        st.session_state.monitoring = False
        st.error(f"Sniffing error: {str(e)}")

def process_packet_queue():
    """Process packets from queue"""
    packets_this_second = 0
    
    while not st.session_state.packet_queue.empty():
        try:
            packet_info = st.session_state.packet_queue.get_nowait()
            
            # Format packet for display
            display_packet = {
                'Timestamp': packet_info['timestamp'],
                'Source IP': packet_info['src'],
                'Dest IP': packet_info['dst'],
                'Protocol': packet_info['protocol'],
                'Src Port': packet_info['sport'],
                'Dst Port': packet_info['dport'],
                'Length': packet_info['length'],
                'Threat Level': packet_info['threat'],
                'Reason': packet_info['reasons'],
                'Action': packet_info['action']
            }
            
            st.session_state.packets.insert(0, display_packet)
            st.session_state.total_packets += 1
            packets_this_second += 1
            
            # Handle threats
            if packet_info['threat'] in ['Critical', 'High']:
                st.session_state.threats_detected += 1
                st.session_state.blocked_ips += 1
                alert_msg = f"[{packet_info['timestamp']}] {packet_info['threat']} threat: {packet_info['src']}:{packet_info['dport']} → {packet_info['dst']} - {packet_info['reasons']}"
                st.session_state.alerts.insert(0, alert_msg)
            
            # Limit stored packets
            if len(st.session_state.packets) > 200:
                st.session_state.packets.pop()
            if len(st.session_state.alerts) > 100:
                st.session_state.alerts.pop()
                
        except queue.Empty:
            break
    
    # Update traffic chart
    current_time = time.time()
    if current_time - st.session_state.last_update >= 1.0:
        st.session_state.packet_count_current = packets_this_second
        st.session_state.last_update = current_time
        
        chart_time = len(st.session_state.traffic_data['time'])
        st.session_state.traffic_data['time'].append(chart_time)
        st.session_state.traffic_data['packets'].append(packets_this_second)
        
        if len(st.session_state.traffic_data['time']) > 60:
            st.session_state.traffic_data['time'].pop(0)
            st.session_state.traffic_data['packets'].pop(0)

# Header
st.title("🛡️ Advanced NIDS - Real-Time Network Monitoring (Scapy)")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Network interface selection
    interface = st.text_input("Network Interface", value="", 
                             help="Leave empty for default, or specify (e.g., eth0, wlan0, en0)")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", use_container_width=True):
            if not st.session_state.monitoring:
                st.session_state.monitoring = True
                # Start sniffer thread
                sniffer = threading.Thread(
                    target=start_sniffing, 
                    args=(interface if interface else None,),
                    daemon=True
                )
                sniffer.start()
                st.session_state.sniffer_thread = sniffer
                st.success("Started monitoring!")
                
    with col2:
        if st.button("⏸️ Stop", use_container_width=True):
            st.session_state.monitoring = False
            st.warning("Stopped monitoring")
    
    if st.button("🗑️ Clear Logs", use_container_width=True):
        st.session_state.packets = []
        st.session_state.alerts = []
        st.session_state.total_packets = 0
        st.session_state.threats_detected = 0
        st.session_state.blocked_ips = 0
        st.session_state.traffic_data = {'time': [], 'packets': []}
        st.rerun()
    
    st.divider()
    
    filter_option = st.selectbox("🔍 Filter Threats", 
                                 ['All', 'Critical', 'High', 'Medium', 'Low'])
    
    st.divider()
    
    status_color = "🟢" if st.session_state.monitoring else "🔴"
    status_text = "Active Monitoring" if st.session_state.monitoring else "Stopped"
    st.markdown(f"### {status_color} Status: {status_text}")
    
    if st.session_state.monitoring:
        st.info("⚠️ Requires root/admin privileges")
    
    st.divider()
    
    st.subheader("📊 Statistics")
    st.metric("Total Packets", st.session_state.total_packets)
    st.metric("Threats Detected", st.session_state.threats_detected)
    st.metric("Blocked IPs", st.session_state.blocked_ips)
    st.metric("Current Rate", f"{st.session_state.packet_count_current} pkt/s")

# Process packets from queue
if st.session_state.monitoring:
    process_packet_queue()

# Traffic Chart
st.subheader("📈 Network Traffic Monitor")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=st.session_state.traffic_data['time'],
    y=st.session_state.traffic_data['packets'],
    mode='lines',
    name='Packets/sec',
    line=dict(color='#00d4ff', width=2),
    fill='tozeroy',
    fillcolor='rgba(0, 212, 255, 0.2)'
))

fig.update_layout(
    template='plotly_dark',
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Time (s)",
    yaxis_title="Packets per Second",
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Tabs for data display
tab1, tab2, tab3 = st.tabs(["📦 Live Packets", "⚠️ Alert Log", "ℹ️ Help"])

with tab1:
    if st.session_state.packets:
        df = pd.DataFrame(st.session_state.packets)
        
        if filter_option != 'All':
            df = df[df['Threat Level'] == filter_option]
        
        def colorize_threat(val):
            colors = {
                'Critical': 'background-color: #ff4444; color: white',
                'High': 'background-color: #ff8800; color: white',
                'Medium': 'background-color: #ffaa00; color: black',
                'Low': 'background-color: #4caf50; color: white'
            }
            return colors.get(val, '')
        
        styled_df = df.style.applymap(colorize_threat, subset=['Threat Level'])
        st.dataframe(styled_df, use_container_width=True, height=400)
    else:
        st.info("No packets captured yet. Start monitoring to see live data.")

with tab2:
    if st.session_state.alerts:
        for alert in st.session_state.alerts[:50]:  # Show last 50 alerts
            if 'Critical' in alert:
                st.markdown(f"<div class='critical'>🚨 {alert}</div>", unsafe_allow_html=True)
            elif 'High' in alert:
                st.markdown(f"<div class='high'>⚠️ {alert}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='medium'>⚡ {alert}</div>", unsafe_allow_html=True)
    else:
        st.info("No alerts triggered yet.")

with tab3:
    st.markdown("""
    ### 🔧 Setup Instructions
    
    **Linux:**
```bash
    sudo python3 -m pip install scapy streamlit plotly pandas
    sudo streamlit run app.py
```
    
    **Windows (Admin PowerShell):**
```powershell
    pip install scapy streamlit plotly pandas
    # Install Npcap from https://npcap.com/
    streamlit run app.py
```
    
    **macOS:**
```bash
    sudo pip3 install scapy streamlit plotly pandas
    sudo streamlit run app.py
```
    
    ### 🎯 Threat Detection Rules
    - **Critical**: Blacklisted IPs
    - **High**: Port scanning, DNS on non-standard ports
    - **Medium**: Suspicious ports (21, 23, 135, 139, 445, 3389, etc.), large packets, ICMP
    - **Low**: Normal traffic
    
    ### 📝 Network Interfaces
    - **Linux**: `eth0`, `wlan0`, `enp0s3`
    - **Windows**: Leave empty or use interface name from `ipconfig`
    - **macOS**: `en0`, `en1`
    
    ### ⚠️ Important Notes
    - Requires **root/administrator** privileges
    - May need to disable firewall temporarily
    - Performance depends on network traffic volume
    """)

# Auto-refresh
if st.session_state.monitoring:
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    st.rerun()
