ARP-SPOOFER_V1 is a tool that automates the arpspoofing with scapy.

usage : python3 ARP-SPOOFER.PY "router_ip" "target_ip"

NOTE : IP forwaring has to be set otherwise this will DOS the devices.

To enable IP forwarding in linux, type : echo > 1 /proc/sys/net/ipv4/ip_forward

NOTE : Designed for Linux and Designed to be executed from terminal