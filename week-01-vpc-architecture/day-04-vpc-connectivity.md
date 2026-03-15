# Day 4: VPC Connectivity Options

**Date:** March 15, 2026  
**Time Spent:** ~2–4 hours (planned)  
**Status:** 🟡 Planned / In Progress

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
- [ ] Learn hub-and-spoke design
- [ ] Compare Transit Gateway against many peering links
- [ ] Understand route propagation and route tables
- [ ] Identify when Transit Gateway becomes worth the cost

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

## Draft Tomorrow's Plan

**Day 5: Hybrid & Advanced Network Security**
- AWS Network Firewall
- Route 53 Resolver
- Traffic inspection ideas
- Security architecture across VPCs

---

## Notes to Future Me

If Day 4 starts feeling too broad, narrow it down to this one question:

> **When should I choose VPC Peering, and when should I stop and move to Transit Gateway instead?**

That question alone is enough to make the whole topic practical.
