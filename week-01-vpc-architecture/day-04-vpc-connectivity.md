# Day 4: VPC Connectivity Options

**Date:** March 25, 2026  
**Time Spent:** ~4 hours (Theory + Labs)  
**Status:** 🟢 Completed (Multi-VPC & TGW Route Isolation Verified)

---

## What I Learned: AWS Transit Gateway (TGW) Master Synthesis

### Core Summary & Most Important Points
- **The Hub-and-Spoke Paradigm:** TGW replaces complex, unscalable full-mesh VPC peering. It acts as a central regional router (like an international airport hub) connecting thousands of VPCs, VPNs, and Direct Connects.
- **Route Table Segmentation:** A single TGW can hold multiple isolated route tables (e.g., Production vs. Sandbox). Attachments must be explicitly associated, and routes must be propagated for any communication to occur.
- **Appliance Mode for Stateful Firewalls:** TGWs naturally route traffic across different Availability Zones (AZs). This asymmetric routing breaks stateful firewalls because return traffic takes a different path. Enabling Appliance Mode forces return traffic through the same AZ, maintaining flow symmetry.
- **Bypassing IPsec Limits (TGW Connect):** Standard IPsec VPNs are capped at 1.25 Gbps. TGW Connect uses Generic Routing Encapsulation (GRE) to natively integrate third-party SD-WAN appliances at significantly higher bandwidths.
- **The Evolution to Cloud WAN:** Legacy global routing required manual, static TGW inter-region peering. The modern approach federates regional TGWs into AWS Cloud WAN, using BGP for automated, dynamic global route propagation.

### Real-World Implementation Patterns
1. **Centralized Inspection (The Security VPC)**
   - **Scenario:** An enterprise needs to audit all internet-bound and east-west (inter-VPC) traffic.
   - **Implementation:** Route all traffic (0.0.0.0/0) from spoke VPCs to a dedicated Inspection VPC attached to the TGW. Use Gateway Load Balancers (GWLB) and third-party firewalls inside this Inspection VPC.
   - **Crucial Step:** You must enable Appliance Mode on the Inspection VPC's TGW attachment to prevent dropped packets.
2. **Predictable Hybrid Failover (BGP Engineering)**
   - **Scenario:** A hospital requires highly available on-premises to cloud connectivity.
   - **Implementation:** Connect the data center to the TGW using AWS Direct Connect as the primary link and a Site-to-Site VPN as the backup.
   - **Crucial Step:** Configure Border Gateway Protocol (BGP) on both links. Apply AS-PATH Prepending (or Multi-Exit Discriminator/MED) to the VPN route to artificially lengthen it. This mathematically guarantees the TGW will only use the VPN if the Direct Connect circuit physically fails.
3. **Total Network Isolation on Shared Infrastructure**
   - **Scenario:** Development and Production environments share the same physical TGW hub but must never communicate.
   - **Implementation:** Create two separate TGW Route Tables. Attach the Dev VPCs to the Dev Table and Prod VPCs to the Prod Table. Explicitly manage route propagation so Dev routes are never advertised to the Prod table.
   - **💡 Key Lab Insight:** *Transit Gateway Association defines the SOURCE route table for a given attachment. Propagation defines the DESTINATION routes available within a given route table.*

### Architectural Challenges & Pitfalls
| Challenge | Impact | Architect's Solution |
|-----------|--------|----------------------|
| **IP Overlap** | TGW cannot route traffic between VPCs sharing the same CIDR blocks. | Strict IP Address Management (IPAM) and careful subnetting before deploying VPCs. |
| **BGP ASN Conflicts** | BGP peering fails when connecting a TGW to an AWS Cloud WAN core network. | Ensure the TGW and the Cloud WAN core network are configured with completely unique Autonomous System Numbers (ASNs). |
| **Routing Overhead** | Inter-region TGW peering creates a massive operational burden as environments scale. | Inter-region TGW peering relies on static routes. Migrate to AWS Cloud WAN for dynamic BGP routing. |
| **False Positives** | VPC Reachability Analyzer incorrectly reports routing failures through complex firewall meshes. | Understand the limits of AWS simulation tools when traffic passes through third-party stateful appliances via TGW. |

---

## Learning Goal

Today I want to understand **how different AWS networking options connect VPCs, on-prem networks, and large-scale architectures**.

By the end of this session, I should be able to answer:
- When should I use **VPC Peering**?
- When does **Transit Gateway** make more sense?
- Where do **Site-to-Site VPN** and **Direct Connect** fit in?
- What breaks when CIDR blocks overlap?
- Why doesn't VPC Peering scale well for bigger environments?

---

## What I Expect to Learn

### 1) VPC Peering
- One-to-one private connection between two VPCs
- Traffic stays within AWS backbone
- No transitive routing
- CIDR blocks must not overlap
- Good for simple architectures and a small number of VPCs

### 2) Transit Gateway
- Hub-and-spoke connectivity model
- Connect multiple VPCs and on-prem networks through one central gateway
- Supports route propagation and centralized network management
- Better for scaling than many peering connections

### 3) Site-to-Site VPN
- Encrypted tunnel between AWS and on-premises network
- Uses the public internet
- Faster to set up than Direct Connect
- Good for hybrid connectivity or backup connection

### 4) Direct Connect
- Dedicated private connection from on-prem to AWS
- More stable and predictable than internet-based VPN
- Better for enterprise workloads, higher throughput, and lower latency
- More expensive and slower to provision

---

## Connectivity Comparison

| Option | Best For | Pros | Limitations |
|--------|----------|------|-------------|
| **VPC Peering** | Small number of VPCs | Simple, private, low overhead | No transitive routing, poor scalability |
| **Transit Gateway** | Multi-VPC architecture | Centralized, scalable, cleaner routing | More cost, more moving parts |
| **Site-to-Site VPN** | Hybrid connectivity / fast setup | Encrypted, quick to deploy | Runs over public internet |
| **Direct Connect** | Enterprise hybrid connectivity | Private, stable, consistent performance | Higher cost, setup complexity |

---

## Hands-On Plan

### Lab 1: VPC Peering Concepts
- [ ] Review how peering works between two VPCs
- [ ] Verify that peered VPCs need non-overlapping CIDR blocks
- [ ] Understand route table updates required on both sides
- [ ] Test why peering is **not transitive**

### Lab 2: Transit Gateway Concepts
- [x] Learn hub-and-spoke design
- [x] Compare Transit Gateway against many peering links
- [x] Understand route propagation and route tables
- [x] Identify when Transit Gateway becomes worth the cost

### Lab 3: Hybrid Connectivity
- [ ] Compare Site-to-Site VPN vs Direct Connect
- [ ] Understand public vs private transport path
- [ ] Learn common use cases for each option
- [ ] Identify where VPN is enough and where Direct Connect is justified

---

## Verification Checklist

| Check | What I Should Confirm | Result |
|------|------------------------|--------|
| Peering limitation | No transitive routing | ⬜ |
| CIDR rule | Overlapping CIDR blocks break peering | ⬜ |
| Routing | Route tables must be updated manually for peering | ⬜ |
| TGW scaling | Transit Gateway reduces mesh complexity | ⬜ |
| VPN path | Site-to-Site VPN uses public internet | ⬜ |
| DX path | Direct Connect is private dedicated link | ⬜ |

---

## What I Want to Pay Attention To

### What Might Click Today
- Why **VPC Peering is easy but doesn't scale**
- Why **Transit Gateway is basically a network hub**
- Why hybrid networking choices depend on **cost, latency, and reliability**

### What Might Be Confusing
- Route propagation vs static route updates
- Why non-transitive routing matters in real architecture
- When VPN is "good enough" versus when Direct Connect is actually needed

---

## Architecture Sketches to Understand

### VPC Peering (Simple)

```text
VPC A  <------ peering ------>  VPC B
```

### Mesh Problem (Doesn't Scale Well)

```text
VPC A <--> VPC B
  |  \      /  |
  |   \    /   |
  |    \  /    |
  |     \/     |
  |     /\     |
  |    /  \    |
  |   /    \   |
VPC C <-------> VPC D
```

### Transit Gateway (Scalable Hub-and-Spoke)

```text
          VPC A
            |
            |
VPC B ---- Transit Gateway ---- VPC C
            |
            |
        On-Prem / VPN
```

---

## Key Questions to Answer by the End

- If I have only **2 VPCs**, should I use Peering or TGW?
- If I have **10 VPCs**, what becomes painful with Peering?
- If I need to connect office network to AWS quickly, is VPN enough?
- If I need reliable enterprise-grade connectivity, when is Direct Connect worth it?

---

## Resources to Use

- AWS VPC Peering: https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html
- AWS Transit Gateway: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html
- AWS Site-to-Site VPN: https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html
- AWS Direct Connect: https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html

---

## Study Plan

### Phase 1 — Core Understanding (30–45 min)
- Read VPC Peering basics
- Read Transit Gateway basics
- Compare both side by side
- Write down scaling differences in plain English

### Phase 2 — Hybrid Connectivity (30–45 min)
- Study Site-to-Site VPN
- Study Direct Connect
- Compare setup speed, reliability, and cost
- Note when each one is appropriate

### Phase 3 — Architecture Thinking (30–60 min)
- Sketch simple scenarios:
  - 2 VPCs
  - 5+ VPCs
  - AWS + office network
- Decide which connectivity option fits each case and why

### Phase 4 — Journal Writing (20–30 min)
- Fill in the “What I Learned” section with actual lessons
- Add at least one real confusion point
- Add one “what clicked” insight
- Add one practical architecture takeaway

---

## Lab Checklist

### Before Starting
- [ ] Open Day 1–3 notes for continuity
- [ ] Keep AWS documentation tabs ready
- [ ] Prepare one simple architecture diagram while studying

### During Study
- [ ] Write down differences between Peering and TGW immediately
- [ ] Note at least one real-world use case for each service
- [ ] Record one limitation for each option
- [ ] Capture screenshots/images worth reusing in the note

### Before Finishing
- [ ] Summarize what clicked
- [ ] Add one cost or scaling insight
- [ ] Add tomorrow’s follow-up topic
- [ ] Make sure the writing sounds like a learning journal, not textbook notes

---

## Verification Tests (Lab 2 & 3)

| Test | Source | Destination | Expected | Result |
|------|--------|-------------|----------|--------|
| App targets DB | App Server (`10.0.x.x`) | DB Server (`172.16.x.x`) | Successful ping (`0% loss`) | ✅ Pass |
| App targets SS | App Server (`10.0.x.x`) | SS Server (`192.168.x.x`) | Successful ping (`0% loss`) | ✅ Pass |
| DB targets SS | DB Server (`172.16.x.x`) | SS Server (`192.168.x.x`) | 100% Packet loss (Isolation) | ✅ Pass |
| Cross-TGW Security | DB Server (`172.16.x.x`) | App Server (`10.0.x.x`) | Successful ping (Return path works) | ✅ Pass |

---

## Key Observations

### What Worked
- Routing `10.x`, `172.16.x`, and `192.168.x` natively out of standard VPC Route Tables strictly into the Transit Gateway simplifies management infinitely over VPC peering.
- Placing App Attachments in their own TGW Route table to enable Hub-and-Spoke connectivity, while isolating DB and SS attachments into a separate table, perfectly solved the network segmentation issue without complex firewall rules.

### What I Learned the Hard Way
- **Association vs Propagation:** Transit Gateway Association defines the *source* route table for a given attachment. Propagation defines the *destination* routes available within a route table.
- **The Empty TGW Trap:** I accidentally created my custom route tables on a brand new TGW rather than the default `projectAlpha` TGW. Attachments are locked to their physical TGW; they cannot be associated with route tables belonging to a different TGW.
- **Unsaved Routes are Black Holes:** A route with a `-` status in the AWS Console is not active. The route MUST be saved explicitly, or the return pathway drops the ICMP response entirely, leading to a silent ping timeout.
- **TCP != ICMP in Security Groups:** If an instance allows "All TCP", SSH works perfectly but Ping completely fails because Ping relies on ICMP. Flow logs will show `REJECT OK`. The SG must explicitly allow ICMP or `All Traffic`.

---

## Adjusted Tomorrow's Plan (Day 5)

Because the multi-VPC environment required Transit Gateways immediately, yesterday's core topics (Peering and VPN) will be executed first.

**Day 5: Foundational Limits & Advanced Security**
- **VPC Peering Limits:** Spin up a manual Peering Link to physically observe the non-transitive routing failures compared to the TGW logic.
- **Site-to-Site VPN Mockup:** Simulate an external Customer Gateway to understand BGP dynamic propagation reaching into the TGW.
- **AWS Network Firewall & Route 53 Resolver:** Execute the original Day 5 targets to actively inspect the traffic and resolve private hostnames across the new hub-and-spoke.
