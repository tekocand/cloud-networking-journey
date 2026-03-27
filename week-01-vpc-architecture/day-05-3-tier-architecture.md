# Day 5: Building a Complete 3-Tier Architecture

**Date:** March 27, 2026  
**Time Spent:** ~5 hours  
**Mood:** Satisfying — hit a lot of real-world traps and each one taught something solid

---

## What I Learned

### 3-Tier Architecture Theory
- The 3-Tier model is not just about grouping servers — it's about creating **strict security boundaries**
- If one layer gets compromised, the attacker is trapped there and can't jump to the next tier
- The three tiers:
  - **Web Tier (Public):** Front door — only the ALB/proxy lives here, exposed to the internet
  - **App Tier (Private):** Business logic — private, can reach internet via NAT Gateway, not reachable from internet
  - **Database Tier (Isolated):** Vault — no internet route at all, not even a NAT Gateway route

### Security Group Chaining (Zero-Trust Core)
- Instead of using IP CIDR ranges, reference **Security Group IDs** as source/destination
- This locks access to the identity of the workload, not its IP address (IPs change, SG IDs don't)
- Chain:
  - Web SG: allows `0.0.0.0/0` on ports 80/443
  - App SG: allows **only** Web SG ID as source
  - DB SG: allows **only** App SG ID as source
- If a hacker hits the load balancer, they cannot jump to the database directly — they must traverse App layer rules first

### Network ACLs vs Security Groups (A lesson learned the hard way)
- Security Groups are **stateful** — allowed inbound automatically allows the return packet out
- Network ACLs are **stateless** — you must explicitly allow BOTH inbound AND outbound (including ephemeral ports 1024-65535 for return traffic)
- Every subnet is "captured" by one NACL — if you don't create a dedicated one, subnets inherit the default or wrong NACL

### EC2 Instance Connect Endpoint
- AWS allows only **1 EIC Endpoint per VPC** — it serves all subnets in that VPC
- The endpoint is anchored to one subnet, but can reach any instance in the VPC via the VPC's internal Local route
- Requires a two-sided SG "handshake":
  - Endpoint SG: **Outbound** port 22 → Target SG
  - Target SG: **Inbound** port 22 ← Endpoint SG

---

## What I Built

### Architecture

Three-tier VPC with strict isolation between layers:

1. **VPC:** 10.0.0.0/16 (ap-southeast-2)
2. **Web Tier (Public):** `10.0.1.0/24`, `10.0.2.0/24` across 2 AZs
   - Route: 0.0.0.0/0 → Internet Gateway
   - SG: Allow TCP 80/443 from `0.0.0.0/0`
3. **App Tier (Private):** `10.0.11.0/24`, `10.0.12.0/24` across 2 AZs
   - Route: 0.0.0.0/0 → NAT Gateway
   - SG: Allow All TCP from Web SG only
4. **DB Tier (Isolated):** `10.0.111.0/24`, `10.0.112.0/24` across 2 AZs
   - Route: Local only (no internet route)
   - SG: Allow All TCP from App SG only
   - Dedicated NACL (not shared with Web tier)

### Components Created
- [x] VPC with CIDR 10.0.0.0/16
- [x] 6 subnets across 3 tiers and 2 AZs
- [x] Internet Gateway + Public Route Table
- [x] NAT Gateway (in Public Subnet) + Private Route Table
- [x] Isolated Route Table (local only) for DB Tier
- [x] 3 Security Groups with strict SG ID chaining (Web → App → DB)
- [x] Dedicated NACL for DB subnets
- [x] EC2 Instance Connect Endpoint
- [x] 3 EC2 instances (one per tier) for validation testing

---

## Troubleshooting

### Problem 1: DB Security Group Not Showing in Dropdown

**Symptom:** When editing the DB SG inbound rule, the App SG didn't appear in the source search box.

**Root Cause:** The DB Security Group was created inside the **wrong VPC** (Default VPC from a previous lab) — not the 3-Tier Lab VPC.

**Solution:** Deleted the old DB SG and recreated it explicitly selecting the correct VPC.

**Key Takeaway:** AWS only shows SGs from the same VPC when setting source rules. If a SG doesn't appear, the VPC is wrong.

---

### Problem 2: Couldn't Connect to DB via EC2 Instance Connect

**Symptom:** Attempting to connect to the DB instance via EIC from the console timed out.

**Investigation:**
1. Checked EIC Endpoint SG outbound rules ✓
2. Checked DB SG inbound rules for port 22 from EIC SG ✓
3. Ran Reachability Analyzer: **SUBNET_ACL_RESTRICTION** on `PublicWeb-NACL`

**Root Cause:** The DB subnet was **associated with the PublicWeb-NACL** (leftover from initial setup). The Web NACL only permitted HTTP/HTTPS traffic and was blocking SSH entirely.

**Solution:** Created a dedicated `Private-DB-NACL` with permissive inbound/outbound rules and associated it with the DB subnets.

**Verification:**
```bash
# From App Server (10.0.11.186)
telnet 10.0.111.20 22
# Connected to 10.0.111.20 — SUCCESS
```

**Key Takeaway:** The VPC Reachability Analyzer put a red X exactly on `PublicWeb-NACL` and named the error `SUBNET_ACL_RESTRICTION`. This tool saved hours of guesswork.

---

## Verification Tests

| Test | Method | Result |
|------|--------|--------|
| App tier internet outbound | `ping google.com` from App EC2 | ✅ Success (NAT GW working) |
| IGW → DB direct access (should FAIL) | Reachability Analyzer (TCP any) | ✅ Not Reachable (DB isolated) |
| App → DB access (should PASS) | `telnet 10.0.111.20 22` | ✅ Connected |
| EIC → DB SSH | EC2 Console Connect | ✅ Connected after NACL fix |

---

## What Clicked

- The difference between **Timeout** and **Connection Refused** is critical:
  - **Timeout** = the network (SG or NACL) silently dropped the packet. AWS config problem.
  - **Connection Refused** = AWS delivered the packet, but nothing was listening. OS/app problem.
- NACLs act as a "subnet border patrol" — even if the SG says yes, the NACL can still kill it
- One EIC Endpoint handles the whole VPC — you don't need one per subnet
- Reachability Analyzer is the single most valuable debugging tool for AWS networking — use it first, not last

## What Was Confusing

- The Reachability Analyzer only shows the EIC Endpoint as a source if you select the correct resource type (Network Interface, not EC2 Instance)
- `Custom TCP` with port `0` in the SG UI does NOT mean "all ports" — it opens only TCP port 0
- Amazon Linux 2023 does not ship with `telnet` or `nc` (netcat) by default — install via `sudo dnf install telnet -y`

## Questions for Tomorrow

- How does Transit Gateway change the routing model when connecting multiple VPCs at scale?
- What's the best practice for NACL design in multi-tier architectures — one per tier or one shared private NACL?
- How would I implement VPC Flow Logs on just the DB subnet to audit access attempts?

---

## Resources Used

- AWS VPC Reachability Analyzer: https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html
- EC2 Instance Connect Endpoint: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-using-eice.html
- Network ACL documentation: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html

---

## Tomorrow's Plan

**Day 6: VPC Flow Logs & Network Observability**
- Enable VPC Flow Logs on the 3-Tier VPC built today
- Query logs in CloudWatch Logs Insights
- Identify rejected traffic patterns
- Lab: Prove the DB tier is isolated by analyzing real flow log data
