import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="NIDS Dashboard", layout="wide", initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.title("🛡️ Network Intrusion Detection System")

# Sidebar
with st.sidebar:
    st.header("⚙️ Control Panel")

    interface = st.text_input("Network Interface", placeholder="wlp8s0, eth0, en0")

    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("▶️ Start", use_container_width=True)
    with col2:
        stop_btn = st.button("⏹️ Stop", use_container_width=True)

    st.divider()

    capture_count = st.number_input(
        "Packets to Capture", min_value=10, max_value=10000, value=100
    )

    clear_btn = st.button("🗑️ Clear Data", use_container_width=True)

    st.divider()

    st.subheader("📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Packets", "0")
        st.metric("Threats", "0")
    with col2:
        st.metric("Blocked", "0")
        st.metric("Rate", "0 pkt/s")

    st.divider()

    status = st.empty()
    status.markdown("🔴 **Status:** Stopped")

# Main content
st.subheader("📈 Network Traffic Monitor")

# Placeholder chart
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=[0], y=[0], mode="lines", line=dict(color="#00d4ff", width=2), fill="tozeroy"
    )
)
fig.update_layout(
    template="plotly_dark",
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Time (s)",
    yaxis_title="Packets/sec",
)
st.plotly_chart(fig, use_container_width=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📦 Captured Packets", "⚠️ Threat Alerts", "📊 Analytics", "ℹ️ Help"]
)

with tab1:
    st.subheader("Live Packet Capture")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        protocol_filter = st.selectbox("Protocol", ["All", "TCP", "UDP", "ICMP", "DNS"])
    with filter_col2:
        threat_filter = st.selectbox(
            "Threat Level", ["All", "Critical", "High", "Medium", "Low"]
        )
    with filter_col3:
        export_btn = st.button("📥 Export CSV")

    # Sample empty dataframe
    sample_data = pd.DataFrame(
        {
            "Timestamp": [],
            "Source IP": [],
            "Dest IP": [],
            "Protocol": [],
            "Port": [],
            "Length": [],
            "Threat": [],
            "Action": [],
        }
    )

    st.dataframe(sample_data, use_container_width=True, height=400)

with tab2:
    st.subheader("Security Alerts")

    alert_filter = st.selectbox(
        "Filter Alerts", ["All Alerts", "Critical Only", "High & Critical", "Last Hour"]
    )

    st.info("No alerts detected yet. Start monitoring to see threats.")

with tab3:
    st.subheader("Traffic Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Protocol Distribution")
        # Placeholder pie chart
        fig_proto = go.Figure(
            data=[go.Pie(labels=["TCP", "UDP", "ICMP"], values=[0, 0, 0])]
        )
        fig_proto.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_proto, use_container_width=True)

    with col2:
        st.markdown("#### Top Source IPs")
        st.write("No data available")

    st.markdown("#### Threat Level Distribution")
    # Placeholder bar chart
    fig_threat = go.Figure(
        data=[
            go.Bar(
                x=["Low", "Medium", "High", "Critical"],
                y=[0, 0, 0, 0],
                marker_color=["#4caf50", "#ffaa00", "#ff8800", "#ff4444"],
            )
        ]
    )
    fig_threat.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_threat, use_container_width=True)

with tab4:
    st.markdown("""
    ### 🚀 Quick Start

    1. Enter your network interface (e.g., `wlp8s0`, `eth0`)
    2. Set number of packets to capture
    3. Click **Start** to begin monitoring
    4. View live packets and alerts in real-time

    ### 🎯 Features

    - **Real-time Packet Capture** - Monitor network traffic as it happens
    - **Threat Detection** - Automatic identification of suspicious activity
    - **Analytics Dashboard** - Visualize traffic patterns and threats
    - **Export Data** - Save captured packets to CSV/PCAP

    ### ⚠️ Requirements

    **Linux/macOS:**
    ```bash
    sudo pip install scapy streamlit plotly pandas
    sudo streamlit run app.py
    ```

    **Windows:**
    - Install Npcap from https://npcap.com/
    - Run as Administrator

    ### 📡 Finding Your Interface

    - **Linux:** `ip link` or `ifconfig`
    - **macOS:** `ifconfig`
    - **Windows:** `ipconfig`

    Common names: `eth0`, `wlp8s0`, `en0`, `Wi-Fi`
    """)

# Footer
st.divider()
st.caption("NIDS Dashboard v1.0 | Built with Scapy & Streamlit")
