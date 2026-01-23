import json
import sys
import threading
from datetime import datetime

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget
from scapy.all import conf, sniff

running = False
stop_event = threading.Event()


class Emitter(QObject):
    log = Signal(str)


emitter = Emitter()


def packet_callback(pkt):
    if pkt.haslayer("IP"):
        summary = pkt.summary()
        entry = {
            "time": datetime.now().isoformat(),
            "src": pkt["IP"].src,
            "dst": pkt["IP"].dst,
            "proto": pkt["IP"].proto,
            "summary": summary,
        }
        with open("captured_packets.json", "a") as f:
            json.dump(entry, f)
            f.write("\n")

        emitter.log.emit(summary)


def sniff_thread():
    conf.verb = 0
    sniff(
        iface="wlan0",
        prn=packet_callback,
        store=0,
        stop_filter=lambda x: stop_event.is_set(),
    )


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packet Sniffer")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.btn = QPushButton("Start Sniffing")
        self.btn.clicked.connect(self.toggle_sniff)

        self.clear_btn = QPushButton("Clear Logs")
        self.clear_btn.clicked.connect(self.clear_logs)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.output)
        self.setLayout(layout)

        emitter.log.connect(self.output.append)

    def toggle_sniff(self):
        global running
        if not running:
            stop_event.clear()
            self.output.clear()
            threading.Thread(target=sniff_thread, daemon=True).start()
            self.btn.setText("Stop Sniffing")
            running = True
        else:
            stop_event.set()
            self.btn.setText("Start Sniffing")
            running = False

    def clear_logs(self):
        self.output.clear()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
