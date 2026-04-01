# Day 7: VPC Flow Logs & Network Monitoring

**Date:** April 01, 2026  
**Time Spent:** ~2.5 hours  
**Mood:** Great — seeing actual packets get dropped and accepted in native AWS logging was a lightbulb moment.

---

## What I Learned

### VPC Flow Logs Concept
- Captures IP traffic metadata going to and from network interfaces in a VPC. It doesn't capture the packet payload, just the network flow details (source, dest, port, protocol, action).

### Storage Destinations
- **CloudWatch Logs:** Great for real-time troubleshooting using Insights, but can get expensive for long-term storage or high-volume environments.
- **Amazon S3:** Cheaper long-term storage, but requires a query engine like Athena to parse and analyze the raw `.log.gz` files.

### Log Formats & Analysis
- The default format outputs 14 space-separated fields.
- Analyzing these logs is the definitive way to distinguish between a "routing blackhole" (packet never arrives) and a "Security Group reject" (packet arrives but is blocked, logging a `REJECT`).

---

## What I Built

### Part 1: Enable VPC Flow Logs
- [x] Create an IAM Role for CloudWatch Logs (`vpc-flow-logs-role`)
- [x] Create a CloudWatch Log Group (`/vpc/app-vpc-flow-logs`)
- [x] Enable Flow Logs on `App-VPC` with a 1-minute aggregation interval
- [x] Generate traffic by pinging an external IP (e.g., 8.8.8.8) and an unreachable internal IP

![IAM Role](images/day7IAMrole.jpg)
![VPC Flow Logs](images/day7VPCflowlogs.jpg)
![Ping Traffic](images/day7ping.jpg)

### Part 2: CloudWatch Logs Insights
- [x] Filter logs for `REJECT` actions to find blocked traffic
- [x] Filter logs for `ACCEPT` actions and group by `bytes` to find top talkers
- [x] Identify the exact ICMP flow for the ping test

![CloudWatch Log Analysis](images/day7cloudwatchlog.jpg)
![Ping Logs](images/day7pinglogs.jpg)

### Part 3: S3 & Athena 
- [x] Create an S3 Bucket and direct a second Flow Log to it
- [x] Configure Athena's query results location in S3 (`/athena-results/`)
- [x] Execute a `CREATE EXTERNAL TABLE` statement to map the raw VPC flow logs
- [x] Run SQL queries in Athena to hunt down `REJECT` packets natively

![Athena Setup](images/day7athenaquery1.jpg)
![Athena Table Creation](images/day7athenaquery2.jpg)
![Athena Query Results](images/day7athenaquery3.jpg)

---

## Troubleshooting

### Problem 1: CloudWatch Insights Not Detecting Fields
**Symptom:** Querying `filter action="REJECT"` returned empty results or errors because Insights didn't auto-detect the `action` column.
**Root Cause:** The default AWS flow log format is space-separated. Sometimes Insights fails to auto-discover the fields unless explicitly parsed.
**Solution:** Added `parse @message "* * * * * * * * * * * * * *" as version, accountId, interfaceId, srcAddr, dstAddr, srcPort, dstPort, protocol, packets, bytes, start, end, action, logStatus` to manually force-map the raw string before filtering.

---

## Verification Tests

| Test | Method | Expected | Result |
|------|--------|----------|--------|
| CloudWatch logging | Check log group stream | Log streams populate after 10 mins | ✅ Success |
| `REJECT` traffic detection | CW Insights filter `action="REJECT"` | Blocked IPs are aggregated | ✅ Success |
| Athena SQL tracking | Athena query `WHERE action = 'REJECT'` | Returns tabular results | ✅ Success |

---

## What Clicked

- **Ingestion Delay:** Traffic is NOT real-time. Even with a "1-minute" interval, it can take 5 to 10 minutes for AWS to batch, compress, and deliver the logs to CloudWatch or S3.
- **Athena is Powerful but Strict:** You must absolutely define a distinct query results output folder in S3 before it will let you run a single SQL command.

## Questions for Tomorrow
- Which flow log analysis approach is more common in enterprises: shipping everything to a SIEM (like Splunk), or querying locally via Athena?
- Can Flow Logs be used to trigger automated lambda functions to block malicious IPs automatically?

---

## Resources Used

- AWS VPC Flow Logs: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
- Querying Flow Logs in Athena: https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html
- CloudWatch Logs Insights syntax: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html

---

## Tomorrow's Plan

**Day 8: Transit Gateway & Network Segmentation**
- Understand Hub-and-Spoke architectures vs Peering
- Deploy AWS Transit Gateway (TGW)
- Attach multiple VPCs to the TGW
- Update route tables and analyze TGW cost implications
