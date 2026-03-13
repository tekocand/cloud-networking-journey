# Day 2: Security Groups & NACLs

**Date:** March 11, 2026  
**Time Spent:** ~2 hours  
**Status:** ✅ Complete

---

## What I Learned

### Security Groups vs NACLs

| Feature | Security Group | NACL |
|---------|---------------|------|
| **Level** | Instance (ENI) | Subnet |
| **Stateful** | ✅ Yes (return traffic auto-allowed) | ❌ No (need rules both ways) |
| **Default Behavior** | Deny all inbound, allow all outbound | Allow all |
| **Rule Types** | Allow only | Allow and Deny |
| **Evaluation** | All rules checked | Rules processed in number order |

### Key Concepts

**Stateful vs Stateless:**
- **Security Groups are stateful**: If I allow inbound SSH (port 22), the return traffic is automatically allowed. I don't need an outbound rule for the SSH response.
- **NACLs are stateless**: Even if I allow inbound traffic on port 80, I need a separate outbound rule allowing ephemeral ports (1024-65535) for the return traffic.

**Best Practices:**
- Principle of least privilege: Only open ports that are needed
- Restrict SSH (22) to specific IP addresses, not 0.0.0.0/0
- Use NACLs for broad subnet-level protection, Security Groups for instance-level fine-tuning
- Document all rules — future you will thank you

---

## Security Configuration

### Security Group Rules (Public Instance)

| Type | Protocol | Port | Source | Purpose |
|------|----------|------|--------|---------|
| SSH | TCP | 22 | My IP/32 | Admin access only from my PC |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web traffic |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Secure web (ready for SSL) |

**Outbound:** All traffic allowed (default)

### NACL Rules (Public Subnet)

**Inbound:**
| Rule # | Type | Protocol | Port | Source | Action |
|--------|------|----------|------|--------|--------|
| 100 | SSH | TCP | 22 | My IP/32 | Allow |
| 110 | HTTP | TCP | 80 | 0.0.0.0/0 | Allow |
| 120 | HTTPS | TCP | 443 | 0.0.0.0/0 | Allow |
| 130 | Ephemeral | TCP | 1024-65535 | 0.0.0.0/0 | Allow (return traffic) |
| * | All | All | All | 0.0.0.0/0 | Deny |

**Outbound:**
| Rule # | Type | Protocol | Port | Destination | Action |
|--------|------|----------|------|-------------|--------|
| 100 | All | All | All | 0.0.0.0/0 | Allow |

---

## Verification Tests

| Test | Command | Expected | Result |
|------|---------|----------|--------|
| SSH access | `ssh -i key.pem ec2-user@3.106.239.62` | Connect successfully | ✅ Pass |
| HTTP access | `curl http://3.106.239.62` | HTTP 200 response | ✅ Pass |
| HTTPS port open | `telnet 3.106.239.62 443` | Connection refused (no SSL service) | ⚠️ Rules configured, service not running |
| Ping blocked | `ping 3.106.239.62` | Request timed out | ✅ Pass |
| SSH from other IP | (tested from different network) | Connection timeout | ✅ Pass |

---

## Key Observations

### What Worked
- Security Group correctly restricted SSH to my IP only
- HTTP (80) accessible from anywhere as intended
- NACL rule ordering worked (rules 100-120 evaluated before deny)
- Ping correctly blocked — proving ICMP is not allowed by default

### What I Learned the Hard Way
- **NACLs need ephemeral port rules**: Initially forgot to allow 1024-65535 outbound, which broke return traffic. Fixed by adding outbound "All" rule.
- **Key file permissions on Windows**: SSH refused to use the .pem file until permissions were restricted. Used PuTTY as workaround.
- **Port 443 without SSL**: Configured the security rules correctly, but no service listening on 443 because httpd only serves HTTP by default. Would need mod_ssl for HTTPS.

### Stateful vs Stateless in Practice
When I SSH into the instance:
1. **Security Group**: Allows inbound 22 from my IP → SSH response automatically allowed (stateful)
2. **NACL**: Allows inbound 22 (rule 100) AND needs outbound rule for return traffic (stateless)

If NACL didn't have outbound allow, the SSH session would hang after connection — packets could get in but responses couldn't get out.

---

## Architecture After Hardening

![Security Groups and NACL Configuration](day-02/images/photo_2026-03-11_17-19-15.jpg)

```
Internet
    │
    ▼
┌─────────────────────────────────────────┐
│              VPC: 10.0.0.0/16           │
│  ┌─────────────────────────────────┐    │
│  │    Public Subnet: 10.0.1.0/24   │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Public Web Server      │    │    │
│  │  │  - SSH: My IP only      │    │    │
│  │  │  - HTTP/HTTPS: All      │    │    │
│  │  │  - ICMP: Blocked        │    │    │
│  │  └─────────────────────────┘    │    │
│  │           ↓                     │    │
│  │    Internet Gateway             │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │    Private Subnet: 10.0.2.0/24  │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │  Private Server         │    │    │
│  │  │  (no direct internet)   │    │    │
│  │  └─────────────────────────┘    │    │
│  │           ↓                     │    │
│  │    NAT Gateway (outbound only)  │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Questions for Tomorrow

- How do VPC Endpoints work for private S3/DynamoDB access?
- When should I use Network Firewall vs Security Groups vs NACLs?
- How do I monitor and log VPC traffic with Flow Logs?

---

## Resources Used

- AWS Security Groups: https://docs.aws.amazon.com/vpc/latest/userguide/security-groups.html
- AWS NACLs: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html
- Stateful vs Stateless firewalls: AWS documentation

---

## Tomorrow's Plan

**Day 3: VPC Components**
- VPC Endpoints (Gateway and Interface)
- VPC Flow Logs
- AWS Network Manager
- Service endpoints for S3 and DynamoDB

