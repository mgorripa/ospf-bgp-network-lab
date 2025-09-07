# ospf-bgp-network-lab
OSPF + BGP simulation in GNS3 (VyOS) with redistribution, default routing, and failover validation.

This project demonstrates how OSPF (Interior Gateway Protocol) and BGP (Exterior Gateway Protocol) work together in a network.  
I built the lab in GNS3 using VyOS routers, designed a 4-router OSPF backbone, and configured eBGP sessions with external ISP routers.  
The project covers route redistribution, default route propagation, and failover testing.

## Project Overview
- Goal: Understand and implement OSPF + BGP routing in a simulated environment.
- Tools: GNS3, VyOS (community router), Linux.
- Key Features:
  - OSPF Area 0 backbone with 4 routers (R1–R4)
  - eBGP sessions with external ISPs (R5, R6)
  - Route redistribution between OSPF and BGP
  - Default route advertisement
  - Failover and convergence testing

## Topology

![Network Topology](diagrams/topology.png)

## IP Addressing Plan

| Link / Interface        | IP / Mask      | AS Number | Notes              |
|-------------------------|----------------|-----------|--------------------|
| R1–LAN-A                | 10.10.10.1/24  | 65000     | Customer LAN-A     |
| R4–LAN-B                | 10.20.20.1/24  | 65000     | Customer LAN-B     |
| R1–R2                   | 192.0.2.0/30   | 65000     | OSPF Backbone      |
| R2–R3                   | 192.0.2.4/30   | 65000     | OSPF Backbone      |
| R3–R4                   | 192.0.2.8/30   | 65000     | OSPF Backbone      |
| R1–R5 (ISP-A)           | 203.0.113.0/30 | 65100     | eBGP to ISP-A      |
| R4–R6 (ISP-B, optional) | 203.0.113.4/30 | 65200     | eBGP to ISP-B      |

## Configuration Steps

Each router was configured using VyOS CLI. Full configs are saved in the `/configs` folder.  
Below are highlights:

### R1 (Customer Edge)
```bash
set system host-name R1
set interfaces ethernet eth0 address 192.0.2.1/30     # to R2
set interfaces ethernet eth2 address 10.10.10.1/24    # LAN-A
set interfaces ethernet eth3 address 203.0.113.1/30   # to ISP-A

# OSPF
set protocols ospf area 0 network 192.0.2.0/30
set protocols ospf area 0 network 10.10.10.0/24

# BGP
set protocols bgp 65000 neighbor 203.0.113.2 remote-as 65100
set protocols bgp 65000 network 10.10.10.0/24
set protocols static route 0.0.0.0/0 next-hop 203.0.113.2
set protocols ospf redistribute static

Similar configurations were applied to R2, R3, R4, R5, and R6. Full versions are available in the `/configs` folder.

## Validation and Testing

To confirm that the OSPF and BGP configuration worked as intended, I performed the following checks:

### OSPF Neighbors
I used the `show ip ospf neighbor` command. The output confirmed that R1–R2, R2–R3, and R3–R4 formed **full OSPF adjacencies**, ensuring all internal routers were properly connected.

### BGP Summary
I ran `show ip bgp summary`. The output showed that R1 successfully established an **eBGP session with R5 (ISP-A)**, and R4 established a session with **R6 (ISP-B)**.

### End-to-End Connectivity
I ran `ping 10.20.20.1` to verify connectivity. This test confirmed that a host in **LAN-A (10.10.10.0/24)** could successfully reach **LAN-B (10.20.20.0/24)** through the OSPF backbone and BGP edges.

### Failure Test
I simulated a failure by shutting down the **R2–R3 link**. Packet loss occurred briefly, and then OSPF quickly **rerouted traffic through the alternate path**. This demonstrated the **resiliency and convergence** of the design. Screenshots of the test results are available in the `/screenshots` folder.


## Results and Learnings

* **Connected LAN-A (10.10.10.0/24) to LAN-B (10.20.20.0/24)** through the OSPF backbone and eBGP edge connections.
* Observed how **OSPF builds adjacencies and reconverges** when links fail, showcasing its high availability features.
* Successfully **advertised customer prefixes into BGP** and validated external reachability through ISP peers.
* **Propagated a default route into OSPF** for full network reachability.
* Gained practical experience in how routing protocols contribute to **high availability and resilience** in production networks.

## Repository Structure

ospf-bgp-network-lab/
├── README.md # Project documentation, including an overview, validation steps, and key learnings.
├── diagrams/ # Network topology diagrams.
│ └── topology.png # A visual representation of the network setup.
├── configs/ # Router configurations (R1–R6) in plain text format.
├── screenshots/ # Evidence of the validation tests, including CLI outputs of show commands and ping results.
└── notes/ # Additional notes and observations made during the project.

## Prerequisites

- [GNS3](https://www.gns3.com/software/download) installed on your system  
- [VyOS ISO](https://vyos.io/) added as a router VM in GNS3  
- Basic understanding of routing protocols (OSPF, BGP)  


## How to Reproduce

1.  **Install GNS3.**
2.  **Download the VyOS ISO** and add it as a router VM in GNS3.
3.  **Build the topology** as shown in `diagrams/topology.png`.
4.  **Apply the configurations** from the `/configs` folder to each router.
5.  **Run validation tests** (`ping`, `traceroute`, `show ip ospf`, `show ip bgp`) to confirm connectivity and network behavior.

## Future Improvements

- Add BFD (Bidirectional Forwarding Detection) for faster OSPF/BGP failure detection  
- Implement route summarization to reduce routing table size  
- Secure OSPF and BGP sessions with authentication (MD5)  
- Automate configuration deployment using Python (Netmiko) or Ansible  

## License

This project is released under the MIT License.  


