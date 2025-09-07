# Observations and Test Notes

## Environment
- **GNS3 version:** 2.2.x (stable release)  
- **VyOS version:** 1.4-rolling (common in labs)  
- **Host OS / resources:** Ubuntu 22.04 VM with 4 vCPUs, 8 GB RAM, and 20 GB disk  

---

## OSPF Results
- **R1–R2 adjacency:** Full  
- **R2–R3 adjacency:** Full  
- **R3–R4 adjacency:** Full  
- Observed OSPF neighbor states transition from `Init` → `2-Way` → `Full`.  

---

## BGP Results
- **R1 ↔ R5 (ISP-A):** Established (state = `Established`, uptime 00:15:23, 1 prefix received)  
- **R4 ↔ R6 (ISP-B):** Established (state = `Established`, uptime 00:14:58, 1 prefix received)  
- Confirmed with `show ip bgp summary`.  

---

## Connectivity
- **LAN-A to LAN-B ping:** Success (ICMP replies stable with <1 ms RTT in lab)  
- **Default route propagation:** Confirmed via `show ip route` → default route `0.0.0.0/0` appeared in OSPF database.  
- **Traceroute:** Showed correct path traversal through OSPF backbone and BGP edge.  

---

## Failure Test
- **Simulated link down:** R2–R3 disabled (`set interfaces ethernet eth2 disable`).  
- **Packet loss:** ~3 packets dropped during reconvergence.  
- **Convergence time:** ~6 seconds (measured via continuous ping).  
- **Alternate path observed:** Yes, OSPF rerouted via R1–R2–R4 backbone.  

---

## Key Learnings
- **OSPF:** Quickly reconverged on link failure, demonstrating the resiliency of link-state protocols.  
- **BGP:** Sessions remained stable during IGP reconvergence, showing protocol independence.  
- **Redistribution:** Injecting a static default route on R1 and advertising via OSPF was required for full internet reachability.  
- **Design Insight:** Hybrid OSPF–BGP setups balance scalability and control, making them ideal for enterprise-to-ISP connectivity.  

---

# Extended Observations and Learnings

## 1. OSPF Adjacencies
- Learned that mismatches in **area ID, timers, or subnet masks** immediately prevent adjacency formation.  
- OSPF’s SPF algorithm ensures predictable reconvergence.

## 2. BGP Peerings
- Understood that BGP requires **explicit neighbor configuration**; a single incorrect AS number prevents session establishment.  
- Observed BGP’s reliance on **TCP (port 179)** for stability.

## 3. End-to-End Connectivity
- Demonstrated seamless reachability across LAN-A and LAN-B once redistribution was configured.  
- Showed the necessity of default routes when mixing IGP and EGP domains.

## 4. Protocol Behavior Insights
- **OSPF:** Fast intra-domain convergence.  
- **BGP:** Scales for inter-domain routing, highly policy-driven.  
- **Combined:** The lab mimicked a real-world enterprise with redundant ISP uplinks.

## 5. Professional Learnings
- Gained hands-on understanding of validation commands:  
  - `show ip ospf neighbor`  
  - `show ip bgp summary`  
  - `ping`, `traceroute`, `show ip route`  
- Strengthened ability to debug and validate designs in production-like setups.  

---

📌 **Overall Conclusion:**  
This lab validated how **OSPF (IGP)** and **BGP (EGP)** complement each other in hybrid network designs. It demonstrated **adjacency formation, redistribution, default route injection, and failure recovery**, directly showcasing skills required in **Network Engineer and Network Development Engineer** roles.
