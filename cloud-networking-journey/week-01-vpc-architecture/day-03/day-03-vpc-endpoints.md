# Day 03 — VPC Endpoints, Flow Logs, Network Manager

## What I learned

- VPC Endpoints
  - Purpose: let resources in a VPC access supported AWS services or VPC endpoint services without sending traffic over the public internet.
  - Types:
    - Interface endpoints (AWS PrivateLink): create ENIs in private subnets and route traffic to the service privately. They rely on security groups and DNS (Route53) to resolve the service to the ENI.
    - Gateway endpoints: supported for Amazon S3 and DynamoDB. They add a prefix list to route tables so traffic stays within the AWS network.
  - Costs & design notes:
    - Interface endpoints are subscription-based (example: $8.9/month + $0.01/GB). For many services (>~4) evaluate cost vs using a NAT gateway (~$37/month).
    - For HA, create endpoints in each AZ. Configure instances to prefer same-AZ endpoint for lower latency and fall back to others for redundancy.
  - Security:
    - Interface endpoints: control access with Security Groups.
    - Gateway endpoints: control with VPC endpoint policies (Allow/Deny).
  - Practical: after creating an endpoint, route tables are updated (target = vpce) and DNS resolves to the private ENI. EC2 IAM roles are still required to access S3/DynamoDB — use instance roles with appropriate policies.

- Flow Logs
  - Purpose: capture metadata about IP traffic to/from network interfaces (not packet payload).
  - Scope: can enable at VPC, subnet, or ENI level (useful for ELB, RDS, etc.).
  - Uses: auditing, troubleshooting, security monitoring.

- Network Manager
  - Provides a dashboard and visualization for network topology and status across accounts/regions.

## Notes / next steps
- I picked images that match the content and placed them in day-03/images/ so they can be referenced by the markdown.
- If you want filenames cleaned (no spaces, hyphens), tell me and I’ll rename them.
