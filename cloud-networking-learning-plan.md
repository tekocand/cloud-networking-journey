# Cloud Networking Learning Plan

## Overview
**Focus Areas:** VPC Architecture | Hybrid Connectivity | Cloud Segmentation
**Timeline:** 6-8 weeks (adjustable based on pace)
**Tools:** NotebookLLM + hands-on labs

---

## Phase 1: Foundation (Week 1-2)

### Topics
- Cloud networking fundamentals
- OSI model review (Layers 3-4 focus)
- IP addressing, CIDR, subnetting in cloud context
- Region vs Availability Zone concepts

### Resources
| Type | Resource | Notes |
|------|----------|-------|
| Course | **AWS VPC Fundamentals** (freecodecamp YouTube) | Good starting point |
| Course | **Google Cloud Networking** (Google Cloud Skills Boost) | Free tier available |
| Docs | AWS VPC Documentation | Reference material |
| Docs | Azure Virtual Network Docs | Compare approaches |

### NotebookLLM Workflow
1. Upload AWS VPC whitepaper PDF
2. Upload subnetting cheat sheets
3. Generate "explain like I'm technical but new to cloud" summary
4. Create audio briefing for commute/listening

---

## Phase 2: VPC Architecture Deep Dive (Week 3-4)

### Topics
- VPC design patterns (single vs multi-VPC)
- Public vs private subnets
- NAT Gateways, Internet Gateways
- Route tables and routing decisions
- VPC endpoints (Gateway vs Interface)
- Transit Gateway architecture

### Resources
| Type | Resource | Notes |
|------|----------|-------|
| Course | **A Cloud Guru - AWS Advanced Networking** | Paid but worth it |
| Course | **Adrian Cantrill's Networking Course** | Highly recommended |
| Whitepaper | AWS VPC Design Guide | Free, comprehensive |
| Lab | AWS Free Tier hands-on | Build your own VPC |

### Hands-On Labs
- [ ] Build a 3-tier VPC (web/app/db)
- [ ] Configure public + private subnets
- [ ] Set up NAT Gateway for outbound private traffic
- [ ] Create VPC endpoints for S3/DynamoDB

### NotebookLLM Workflow
1. Upload AWS VPC design whitepapers
2. Upload lab notes and architecture diagrams
3. Generate Q&A for self-testing
4. Create "common VPC design mistakes" analysis

---

## Phase 3: Hybrid Connectivity (Week 5-6)

### Topics
- Site-to-Site VPN
- Direct Connect / ExpressRoute / Cloud Interconnect
- VPN redundancy and failover
- Hybrid DNS resolution
- Cloud WAN concepts

### Resources
| Type | Resource | Notes |
|------|----------|-------|
| Whitepaper | AWS Hybrid Connectivity Guide | Must-read |
| Whitepaper | Azure Hybrid Networking | Compare with AWS |
| Video | **NetworkChuck Hybrid Cloud** (YouTube) | Engaging explanations |
| Lab | AWS Site-to-Site VPN setup | Free tier eligible |

### Hands-On Labs
- [ ] Configure Site-to-Site VPN (simulated on-prem)
- [ ] Set up VPC peering between regions
- [ ] Configure Transit Gateway with multiple VPCs

### NotebookLLM Workflow
1. Upload hybrid connectivity case studies
2. Upload comparison matrices (VPN vs Direct Connect)
3. Generate decision tree: "When to use what"
4. Create troubleshooting guide from docs

---

## Phase 4: Cloud Segmentation (Week 7-8)

### Topics
- Network ACLs vs Security Groups
- Micro-segmentation strategies
- Zero Trust architecture in cloud
- Service mesh concepts (Istio, AWS App Mesh)
- Network Firewall / Palo Alto / Fortinet in cloud

### Resources
| Type | Resource | Notes |
|------|----------|-------|
| Whitepaper | AWS Security Groups vs NACLs | Deep dive |
| Course | **SANS SEC540** (if available) | Cloud security focus |
| Docs | AWS Network Firewall | Managed firewall service |
| Article | **Zero Trust Architecture** (NIST) | Conceptual foundation |

### Hands-On Labs
- [ ] Implement defense-in-depth with SG + NACL
- [ ] Configure AWS Network Firewall rules
- [ ] Set up VPC Flow Logs and analyze traffic

### NotebookLLM Workflow
1. Upload security best practices guides
2. Upload compliance requirements (PCI-DSS, HIPAA networking)
3. Generate security checklist
4. Create "segmentation strategy for different use cases"

---

## Recommended Learning Path (Sequential)

```
Week 1-2: Foundation
    ↓
Week 3-4: VPC Architecture
    ↓
Week 5-6: Hybrid Connectivity
    ↓
Week 7-8: Cloud Segmentation
    ↓
Ongoing: Labs + Real-world scenarios
```

---

## NotebookLLM Best Practices for This Journey

### What to Feed It
1. **Whitepapers** - AWS/Azure/GCP official docs (PDF)
2. **Your lab notes** - Type up what you learned
3. **Architecture diagrams** - Screenshot and upload
4. **Error logs** - Paste troubleshooting scenarios

### How to Use It
| Activity | NotebookLLM Prompt |
|----------|-------------------|
| Pre-study | "Summarize this whitepaper in 5 key points" |
| During study | "Explain [concept] with a real-world example" |
| Review | "Generate 10 quiz questions on [topic]" |
| Troubleshooting | "I got this error [paste], what could be wrong?" |
| Commute learning | "Create an audio briefing on VPC design patterns" |

### Pro Tips
- Create separate notebooks per topic (VPC, Hybrid, Segmentation)
- Upload your own summaries - NotebookLLM learns YOUR understanding
- Use the audio feature for passive learning
- Ask it to compare AWS vs Azure vs GCP approaches

---

## Free Hands-On Platforms

| Platform | What You Get | Cost |
|----------|--------------|------|
| **AWS Free Tier** | 750 hrs EC2, VPC resources | Free for 12 months |
| **Google Cloud Free Tier** | $300 credit + always-free | $300 + limited free |
| **Azure Free Account** | $200 credit + 12 months | $200 + limited free |
| **CloudAcademy Labs** | Guided labs | Subscription |

---

## Certification Path (Optional)

If you want to validate:
1. **AWS Certified Advanced Networking - Specialty** (hardest, most respected)
2. **Azure Network Engineer Associate (AZ-700)**
3. **Google Cloud Professional Cloud Network Engineer**

My recommendation: Do AWS first (most market demand), then pick based on your work environment.

---

## Daily/Weekly Study Structure

### Suggested Daily Block (1-2 hours)
- **20 min** - Watch video/read docs
- **30 min** - Hands-on lab
- **10 min** - Document in NotebookLLM
- **10 min** - Review previous day's notes

### Weekly Review
- Revisit NotebookLLM summaries
- Do a "teach back" - explain what you learned to... me or your notes
- Identify gaps, adjust next week

---

## Quick Wins to Start Today

1. **Right now:** Create a NotebookLLM notebook called "Cloud Networking Mastery"
2. **Today:** Download AWS VPC whitepaper, upload to NotebookLLM, generate summary
3. **This week:** Set up AWS free tier, build your first VPC following a tutorial

Want me to expand on any section or adjust the timeline?
