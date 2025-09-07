#!/usr/bin/env python3
"""
Simple validation script I wrote to test my OSPF + BGP lab.
This script checks basic reachability (ping) and, if SSH is enabled,
can run show commands on the routers.
"""

import subprocess

# Replace with management IPs or adapt if running inside GNS3 directly
ROUTERS = {
    "R1": "192.168.56.101",
    "R2": "192.168.56.102",
    "R3": "192.168.56.103",
    "R4": "192.168.56.104",
    "R5": "192.168.56.105",
    "R6": "192.168.56.106",
}

def run(cmd):
    print(f"$ {' '.join(cmd)}")
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=5)
        print(out.decode())
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("== Basic ping tests ==")
    for name, ip in ROUTERS.items():
        run(["ping", "-c", "2", ip])

    print("\n== End-to-end ping to LAN-B ==")
    run(["ping", "-c", "3", "10.20.20.1"])

if __name__ == "__main__":
    main()
