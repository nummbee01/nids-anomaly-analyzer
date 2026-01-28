System Architecture

Module Structure

```
src/
├── core/
│   ├── packet_capture.py    # Scapy-based packet capture
│   ├── packet_parser.py     # Packet field extraction
│   ├── flow_tracker.py      # Session/flow management
│   ├── rule_engine.py       # Signature-based detection
│   ├── anomaly_detector.py  # Statistical anomaly detection
│   └── alert_system.py      # Alert generation and storage
├── gui/
│   ├── main_window.py       # Primary Tkinter interface
│   ├── packet_display.py    # Real-time packet visualization
│   ├── alert_panel.py       # Alert management interface
│   └── config_panel.py      # Configuration forms
├── utils/
│   ├── data_structures.py   # Custom data structures
│   ├── statistics.py        # Statistical calculations
│   └── file_handlers.py     # Configuration and log I/O
└── tests/
    ├── unit_tests.py        # Comprehensive unit tests
    └── integration_tests.py # End-to-end testing
```

Data Flow Architecture

1. Packet Capture Layer → Scapy captures packets from wlan0
2. Processing Pipeline → Functional transformation chain
3. Detection Engines → Parallel rule-based and statistical analysis
4. Alert Management → Priority-based alert storage
5. GUI Interface → Real-time updates and user interaction

Core Detection Approaches

Rule-Based Detection
- Port Scan Detection: Track connection attempts per source IP
- Suspicious Payload: Regex patterns for common attack signatures
- Protocol Violations: Invalid packet structures and sequences

Statistical Anomaly Detection
- Connection Rate Analysis: Z-score on packets per minute per IP
- Packet Size Distribution: Detect unusual payload sizes
- Flow Duration Anomalies: Identify abnormally long/short connections
- Protocol Distribution: Shifts in normal protocol mix

Recommended Data Structures

Functional Data Structures
- Immutable Flow Records: Tuples for flow data (src_ip, dst_ip, protocol, etc.)
- Efficient Counting: collections.Counter for frequency analysis
- Sliding Windows: Circular buffers for time-series data
- Hash Tables: Fast IP address lookups with O(1) complexity

Key Algorithms
- Flow Tracking: Hash-based aggregation with time-based expiration
- Statistical Analysis: Moving averages with configurable windows
- Anomaly Scoring: Weighted combination of multiple statistical features

Tkinter UI Layout

Main Window Structure
┌─────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools  Help                           │
├─────────────────────────────────────────────────────────┤
│ [Start] [Stop] [Clear] [Export] [Settings]             │
├─────────────────────────────────────────────────────────┤
│ Packet Display                │ Alert Panel             │
│ ┌────────────────────────────┐ │ ┌─────────────────────┐ │
│ │ Timestamp | Src | Dst │... │ │ │ Time | Severity | Msg│ │
│ │ 12:34:56 |192.168|... │... │ │ │ 12:34 | HIGH    │...│ │
│ │ 12:34:57 |10.0.0 |... │... │ │ │ 12:35 | MED     │...│ │
│ └────────────────────────────┘ │ └─────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Statistics Panel                                        │
│ Packets: 1234 | Flows: 45 | Alerts: 2 | CPU: 15%       │
└─────────────────────────────────────────────────────────┘

7-Day Execution Plan

Day 1: Foundation Setup ✅ COMPLETED
- [x] Set up project structure and Git branching
- [x] Create requirements.txt with exact versions
- [x] Implement basic packet capture with Scapy
- [x] Create immutable data structures for packet info
- [x] Write unit tests for packet capture functions

Day 2: Core Processing Pipeline ⏭️ SKIPPED
- [x] Build packet parser with functional transformations
- [x] Skip flow tracking (not needed for simple NIDS)
- [x] Skip sliding window buffers (not needed for threat detection)
- [x] Skip complex statistics (use simple counters)
- [x] Skip over-engineering (focus on threat detection)

Day 3: THREAT DETECTION ENGINES 🔄 IN PROGRESS
- [ ] Port scan detection (same IP, multiple ports, short time)
- [ ] SYN flood detection (massive SYN packets)
- [ ] IP spoofing detection (invalid/fake IP headers)
- [ ] ARP spoofing detection (local network impersonation)
- [ ] DDoS attack detection (high-volume traffic patterns)
- [ ] Malicious payload detection (known attack signatures)
- [ ] Brute force detection (repeated login attempts)
- [ ] ICMP flood detection (high ICMP packet volume)
- [ ] DNS tunneling detection (suspicious DNS patterns)
- [ ] Unusual protocol usage (rare/invalid protocols)
- [ ] Abnormal traffic patterns (statistical anomalies)
- [ ] MAC spoofing detection (invalid MAC addresses)
- [ ] Alert system implementation
- [ ] Detection engine unit tests

Day 4: GUI & Integration (Moved from Day 5)
- [ ] Create basic GUI framework for real-time alerts
- [ ] Implement packet display with threat indicators
- [ ] Build alert panel with filtering capabilities
- [ ] Add basic control buttons (Start/Stop/Clear/Export)
- [ ] Integrate threat detection with GUI
- [ ] Test GUI responsiveness with real threats

Day 5: Advanced Features & Performance
- [ ] Add configuration panel for detection thresholds
- [ ] Implement statistics dashboard for threats
- [ ] Create alert export functionality (JSON/CSV)
- [ ] Add packet drill-down views with context
- [ ] Performance optimization for high-traffic environments

Day 6: Integration & Testing
- [ ] Full end-to-end system testing with real attacks
- [ ] Performance benchmarking and profiling
- [ ] Complete documentation and README with threat examples
- [ ] Fix remaining bugs and edge cases
- [ ] Final code review and cleanup

Day 7: DEPLOYMENT & VALIDATION
- [ ] Test against real-world attack scenarios
- [ ] Create installation scripts and setup guide
- [ ] User manual with threat detection examples
- [ ] Final validation and deployment preparation

Technical Implementation Details

Functional Programming Approach
- Pure functions with no side effects
- Immutable data structures using tuples and frozensets
- Map/filter/reduce for data transformations
- Higher-order functions for detection logic composition

Performance Optimizations
- O(1) lookups with hash tables for IP tracking
- Efficient circular buffers for sliding windows
- Lazy evaluation for packet processing pipeline
- Memory-mapped files for large alert logs

Testing Strategy
- 95%+ code coverage with pytest
- Property-based testing with hypothesis
- Mock network traffic for reproducible tests
- Integration tests with real packet captures

---
Project Progress Tracking

Overall Completion: Day 1/7 ✅ COMPLETED

**Day 1 Achievements (100%):**
- ✅ Project structure established with proper module organization
- ✅ Requirements.txt with exact dependency versions
- ✅ Basic Scapy packet capture functionality
- ✅ Immutable NamedTuple data structures for packets
- ✅ Comprehensive test suite (10/10 tests passing)
- ✅ Command-line interface (main.py) with multiple options
- ✅ Core packet parsing pipeline functional

**Day 2 Current Status:**
- ✅ Packet parser refactored for functional approach
- 🔄 Flow tracker implementation (next step)
- 🔄 Sliding window buffers implementation
- 🔄 Comprehensive test coverage for new modules
- 🔄 Algorithm documentation

**Day 2 Focus Areas:**
1. **Flow Tracking**: Hash-based O(1) flow aggregation with time-based expiration
2. **Statistical Analysis**: Circular buffers for moving averages and anomaly detection  
3. **Performance Optimization**: Thread-safe operations for real-time processing
4. **Integration**: Connect new components with existing packet pipeline

**Key Architecture Decisions Made:**
- NamedTuple for immutable packet structures
- Functional programming approach for packet parsing
- Command-line interface design with argparse
- Modular architecture enabling easy testing and extension

**Next Major Milestones:**
- Day 3: Detection Engines (rule-based + statistical)
- Day 4: Alert System & Storage
- Day 5-6: GUI Development (Tkinter-based)
- Day 7: Integration & Performance Optimization
