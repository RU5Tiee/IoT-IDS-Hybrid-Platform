# Suricata Configuration Reference (eve.json)

To enable the ML integration, ensure `suricata.yaml` is configured to output `eve.json` with the following settings:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert:
            payload: yes             # enable for deep inspection if needed
            payload-buffer-size: 4kb
            payload-printable: yes
            packet: yes
            http: yes
        - http:
            extended: yes
        - dns:
            query: yes
            answer: yes
        - tls:
            extended: yes
        - flow:
            enabled: yes
        - netflow:
            enabled: yes
```

## Key Fields for ML Extraction:
- `timestamp`: Time of event.
- `src_ip`, `dest_ip`: Source and destination IP addresses.
- `src_port`, `dest_port`: Port numbers.
- `proto`: Protocol (TCP/UDP/ICMP).
- `flow_id`: Unique flow identifier.
- `app_proto`: Application layer protocol (HTTP, DNS, etc.).
- `event_type`: Category of the event.
