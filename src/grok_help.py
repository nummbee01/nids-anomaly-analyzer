import json
import queue
import threading
from datetime import datetime

import streamlit as st
from scapy.all import conf, sniff

q = queue.Queue()
stop_event = threading.Event()


def pkt_cb(pkt):
    if pkt.haslayer("IP"):
        s = pkt.summary()
        q.put(s + "\n")
        with open("packets.jsonl", "a") as f:
            json.dump({"time": datetime.now().isoformat(), "summary": s}, f)
            f.write("\n")


def sniffer():
    conf.verb = 0
    sniff(iface="lo", prn=pkt_cb, store=0, stop_filter=lambda _: stop_event.is_set())


st.title("CLI-style Packet Sniffer")

if "output" not in st.session_state:
    st.session_state.output = ""

if "running" not in st.session_state:
    st.session_state.running = False

with st.sidebar:
    if st.button("Start" if not st.session_state.running else "Stop"):
        if not st.session_state.running:
            stop_event.clear()
            st.session_state.output = ""
            threading.Thread(target=sniffer, daemon=True).start()
            st.session_state.running = True
        else:
            stop_event.set()
            st.session_state.running = False

    st.button("Clear", on_click=lambda: st.session_state.update(output=""))

placeholder = st.empty()

while not q.empty():
    st.session_state.output += q.get()

placeholder.code(st.session_state.output, language=None)

if st.session_state.running:
    st.rerun()
