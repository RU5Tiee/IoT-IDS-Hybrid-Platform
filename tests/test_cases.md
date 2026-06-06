# IDS Test Cases

## Test Case 1: Normal IoT Traffic
- **Scenario**: Standard MQTT/HTTP traffic from an IoT device to a central server.
- **Expected Result**: ML model predicts `normal`.
- **Feature Profile**:
  - Ports: 1883, 80, 443
  - Packet count: Low (5-20)
  - Bytes: Moderate (500-2000)

## Test Case 2: Port Scanning (Anomaly)
- **Scenario**: An attacker scanning multiple ports on a target device.
- **Expected Result**: ML model predicts `anomaly`.
- **Feature Profile**:
  - Ports: Random/Low (1-1024)
  - Protocol: TCP
  - Alerts: High frequency

## Test Case 3: SYN Flood / DoS (Anomaly)
- **Scenario**: Large volume of packets sent in a short duration.
- **Expected Result**: ML model predicts `anomaly`.
- **Feature Profile**:
  - Packet count: Very High (>500)
  - Bytes: Very High (>50,000)

## Test Case 4: DNS Tunneling (Anomaly)
- **Scenario**: Unusual DNS query patterns.
- **Expected Result**: ML model predicts `anomaly`.
- **Feature Profile**:
  - Protocol: UDP (encoded as 17)
  - Port: 53
  - Bytes: Outlier size
