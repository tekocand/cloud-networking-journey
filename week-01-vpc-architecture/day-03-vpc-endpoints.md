# Day 03 — VPC Endpoints, Flow Logs & Network Manager

Short version (TL;DR)
- Want private, reliable access to AWS services from inside a VPC without traffic leaving the AWS network? Use VPC Endpoints.
- Interface endpoints = PrivateLink (ENIs + SGs). Gateway endpoints = free S3/DynamoDB routing.
- Flow Logs = your traffic CCTV (metadata only). Network Manager = the control room for big networks.

Why this mattered today
I kept thinking: do I need a NAT gateway or endpoints? Turns out it's a cost + security + scale tradeoff. Endpoints keep traffic inside AWS (more secure), but each interface endpoint costs money. NAT is cheaper when you need many external services but sends traffic via the internet gateway/NAT path.

What I actually learned (so you don't repeat my mistakes)

- Interface endpoints (AWS PrivateLink)
  - Picture: an invisible, private door (ENI) in your subnet that connects directly to the AWS service.
  - How it works: AWS creates an ENI in your subnet and Route53 resolves the service domain to that ENI IP. Traffic never sees a public IP.
  - Security: protected by Security Groups. Treat it like any other ENI — lock inbound/outbound to only what you need.
  - Cost: pay per endpoint + per-GB. If you need endpoints for many services (>~4), cost can exceed a NAT gateway — measure before you build.
  - Ops tip: create endpoints per AZ and prefer same‑AZ endpoints from your instances to reduce cross‑AZ traffic and latency.

- Gateway endpoints (S3 & DynamoDB only)
  - Free. Instead of DNS tricks, they add a prefix-list to your route table so S3/DynamoDB stays in the AWS network.
  - Control access with VPC endpoint policies (Allow/Deny). Useful to lock down which buckets or actions a subnet can access.

- Flow Logs
  - What it is: a stream of metadata about who talked to whom (ENI source/destination, ports, bytes). No payload.
  - When to enable: everywhere — VPC, subnet, or ENI level depending on how deep you want to inspect. Great for debugging, security hunting, and cost analysis.
  - Quick use case: enable flow logs, try accessing S3 from an instance, then watch logs to confirm traffic path and whether it hit a VPCE.

- Network Manager
  - Central dashboard to visualize topology across regions/accounts. Helpful when your network stops being a nice little island and becomes an archipelago.

Practical checklist (what I did / what you should do)
1. Decide cost vs security: list required services. If <=3 services and strict private access needed → endpoints. If lots of services or heavy egress traffic → NAT + IGW might be cheaper.
2. For Interface endpoints: create one per AZ, attach tight Security Groups, and document which instances should use which endpoint.
3. For S3/DynamoDB: create gateway endpoints and use endpoint policies to restrict access to specific buckets or prefixes.
4. Enable flow logs on the VPC or subnet, deliver to CloudWatch or S3, and verify traffic during tests.

Examples I tried
- Test: created a gateway endpoint for S3, uploaded a small test object, then curl from private EC2. Verified the route table and confirmed the source IP was the ENI via flow logs.
- Cost check: rough numbers — Interface endpoint ~ $8.9/mo + $0.01/GB; NAT gateway ~ $37/mo + data transfer. If you need 6 separate interface endpoints, NAT wins on cost.

Images
- nat-gateway.png — compare NAT vs endpoints
- igw.png — public vs private routing
- sg-inbound.png — example Security Group for an interface endpoint
- nacl-inbound.png — network-level context

Notes & next actions
- I’ll update the PR branch with this refinished note. Open the PR at: https://github.com/tekocand/cloud-networking-journey/pull/new/day-03-from-main to preview and merge.
- Want different tone? More anecdotes? Say the vibe you want: concise + punchy (default), or narrative + examples (longer). I can rewrite once more.
