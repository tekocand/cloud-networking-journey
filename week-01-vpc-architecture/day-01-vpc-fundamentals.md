# Day 1: VPC Fundamentals & First Architecture

**Date:** March 11, 2026  
**Time Spent:** ~4 hours  
**Mood:** Solid first day, went deeper than planned

---

## What I Learned

### VPC Basics
- VPC = Virtual Private Cloud, logically isolated network in AWS
- Default limit: 5 VPCs per region (can be increased)
- Each region has a default VPC with a subnet per AZ
- CIDR block must be between /16 and /28
- **Important:** First 4 and last IP in each subnet are reserved by AWS
- CIDR cannot be modified after creation — plan carefully
- CIDR blocks must not overlap (critical for VPC Peering)

### Subnet Design
- Public subnet: Has route to Internet Gateway (0.0.0.0/0 → IGW)
- Private subnet: No direct internet route, uses NAT Gateway for outbound
- Created:
  - VPC: 10.0.0.0/16
  - Public subnet: 10.0.1.0/24
  - Private subnet: 10.0.2.0/24

### Routing
- Route tables control traffic flow
- Public route table: 0.0.0.0/0 → Internet Gateway
- Private route table: 0.0.0.0/0 → NAT Gateway
- Subnets are associated with route tables

---

## What I Built

### Architecture

![VPC Architecture - Two-tier with Public and Private Subnets](day-01/images/photo_2026-03-11_15-06-21.jpg)

Two-tier VPC with public and private subnets:

1. **VPC:** 10.0.0.0/16
2. **Public Subnet:** 10.0.1.0/24
   - Internet Gateway attached
   - Public web server (t2.micro)
   - Elastic IP for static public IP
3. **Private Subnet:** 10.0.2.0/24
   - NAT Gateway for outbound internet
   - Private server (no public IP)

### Components Created
- [x] VPC with CIDR 10.0.0.0/16
- [x] 2 subnets (public 10.0.1.0/24, private 10.0.2.0/24)
- [x] Internet Gateway
- [x] NAT Gateway (with Elastic IP)
- [x] 2 route tables (public, private)
- [x] Security Groups
- [x] 2 EC2 instances (public web server, private server)

---

## Troubleshooting: NAT Gateway Blackhole

### Problem
After creating NAT Gateway, status showed "blackholed" and private subnet couldn't reach internet.

### Investigation
1. Checked NAT Gateway was in public subnet ✓
2. Verified Elastic IP was attached ✓
3. Checked private subnet route table...

### Root Cause
Route table association issue. The private subnet's route to NAT Gateway wasn't working correctly.

### Solution
Deleted the route and recreated it:
- Destination: 0.0.0.0/0
- Target: NAT Gateway ID (not the Elastic IP)

### Verification
```bash
# From private instance
ping 8.8.8.8 -c 4
# Success! Outbound internet working via NAT Gateway
```

### Key Takeaway
NAT Gateway requires three things:
1. Deployed in a public subnet (with route to IGW)
2. Elastic IP attached
3. Private subnet route table with 0.0.0.0/0 → NAT Gateway

---

## Verification Tests

| Test | Command | Result |
|------|---------|--------|
| Local to public instance | `ping <public-ip>` | ✅ Success |
| SSH to public instance | `ssh -i key.pem ec2-user@<public-ip>` | ✅ Success |
| Public to private SSH | `ssh -i key.pem ec2-user@<private-ip>` | ✅ Success |
| Private internet via NAT | `ping 8.8.8.8` from private instance | ✅ Success |

---

## What Clicked

- The difference between public and private subnets is just the route table
- NAT Gateway is one-way: outbound only, no inbound from internet
- Security Groups are stateful (return traffic allowed), NACLs are stateless
- CIDR planning matters — can't change later

## What Was Confusing

- Initially thought NAT Gateway needed to be in private subnet (wrong — it goes in public)
- Route table associations weren't immediately obvious in AWS console

## Questions for Tomorrow

- How do Security Groups differ from NACLs in practice?
- When would I use VPC Endpoints instead of NAT Gateway?
- How do I monitor VPC Flow Logs?

---

## Resources Used

- AWS VPC Documentation: https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html
- NAT Gateway troubleshooting: AWS Knowledge Center

---

## Tomorrow's Plan

**Day 2: Security Groups & NACLs**
- Deep dive on Security Groups (stateful)
- Network ACLs (stateless)
- Best practices for least privilege
- Lab: Lock down the VPC built today

