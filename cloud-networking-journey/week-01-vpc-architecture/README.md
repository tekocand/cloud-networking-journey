# Week 1: VPC Architecture Deep Dive

**Dates:** March 11-16, 2026  
**Goal:** Master AWS VPC fundamentals and build production-ready network topology

---

## Week Goals

- [x] Create first working VPC with public/private subnets
- [x] Understand CIDR blocks and subnetting
- [x] Configure Internet Gateway and NAT Gateway
- [x] Master Security Groups and NACLs
- [ ] Build 3-tier VPC architecture
- [ ] Document everything

---

## Daily Log

| Day | Date | Topic | Status |
|-----|------|-------|--------|
| 1 | Mar 11 | VPC Fundamentals + Subnet Design + Routing | ✅ Complete |
| 2 | Mar 11 | Security Groups & NACLs | ✅ Complete |
| 3 | Mar 12 | VPC Components (Endpoints, Flow Logs) | ⏳ Planned |
| 4 | Mar 14 | VPC Peering & Transit Gateway Intro | ⏳ Planned |
| 5 | Mar 15 | Build 3-Tier Architecture | ⏳ Planned |
| 6 | Mar 16 | Weekly Review & Documentation | ⏳ Planned |

---

## Key Learnings This Week

### Day 1: VPC Fundamentals
- VPC is logically isolated network inside AWS
- Default limit: 5 VPCs per region
- CIDR range: /16 to /28 (commonly /16 for main VPC)
- First 4 and last IP in each subnet are reserved
- Cannot modify CIDR after creation
- Default VPC exists in each region with subnet per AZ

### Architecture Built
```
┌─────────────────────────────────────────┐
│              VPC: 10.0.0.0/16           │
│  ┌─────────────────────────────────┐    │
│  │    Public Subnet: 10.0.1.0/24   │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Public Web Server      │    │    │
│  │  │  (t2.micro, Elastic IP) │    │    │
│  │  └─────────────────────────┘    │    │
│  │           ↓                     │    │
│  │    Internet Gateway             │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │    Private Subnet: 10.0.2.0/24  │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Private Server         │    │    │
│  │  │  (no public IP)         │    │    │
│  │  └─────────────────────────┘    │    │
│  │           ↓                     │    │
│  │    NAT Gateway (in public)      │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Troubleshooting Log

### Issue: NAT Gateway Blackholed
**Symptom:** NAT Gateway status showed "blackholed", private subnet couldn't reach internet

**Root Cause:** Route table association issue

**Fix:** Deleted and recreated route to NAT Gateway in private subnet route table

**Lesson:** NAT Gateway requires:
1. Deployment in a public subnet (with IGW route)
2. Elastic IP attached
3. Private subnet route table pointing to NAT Gateway (0.0.0.0/0 → nat-gateway-id)

---

## Verification Tests Passed

- [x] Ping from local PC to public instance
- [x] SSH from public instance to private instance
- [x] Internet connectivity from private subnet via NAT Gateway

---

## Time Invested

- Day 1: ~4 hours
- Day 2: ~2 hours

