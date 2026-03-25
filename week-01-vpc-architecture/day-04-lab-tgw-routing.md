---
date: 2026-03-25
tags:
  - aws
  - networking
  - transit-gateway
  - lab
status: completed
---

# 🧪 Lab 2: Transit Gateway Hub-and-Spoke Setup & Lab 3: TGW Routing Isolation

*Parent Note:* [[day-04-vpc-connectivity]]

## Objective
Connect three separate isolated VPCs (`App`, `Database`, and `SharedServices`) using a centralized **AWS Transit Gateway (TGW)**, replacing full-mesh VPC peering. Then, use TGW Route Table Isolation to permit App->DB and App->SS, while completely blocking DB->SS.

---

## Lab Execution Steps

### Phase 1: Deploy the Transit Gateway (The Hub)
*Narrative:* This acts as the central router for your entire AWS network. If we wanted strict segregation from the start, we'd disable the defaults. But for a connected Hub-and-Spoke, keep them on so it automatically meshes everything.
1. In the VPC Console, scroll down to **Transit Gateways** and click **Create Transit Gateway**.
2. **Name tag:** `projectAlpha-TGW`
3. **Description:** Hub for App, DB, and Shared Services routing.
4. **Options:** 
   - Default route table association: **Enable**
   - Default route table propagation: **Enable**
5. Click **Create** (Takes 2–4 minutes to become "Available").

### Phase 2: Create TGW Attachments (The Spokes)
*Narrative:* We need to physically plug your three VPCs into the new Hub. TGWs need an Elastic Network Interface (ENI) in at least one private subnet per AZ to physically route the traffic in and out of the VPC.
1. Go to **Transit Gateway Attachments** > **Create Transit Gateway Attachment**.
2. **Attach the App VPC:**
   - Name: `TGW-Attach-App`
   - Transit Gateway ID: Select `projectAlpha-TGW`
   - VPC ID: Select `projectAlpha-AppVPC`
   - Subnets: Select `APP-private1-ap-southeast-2a` and `APP-private2-ap-southeast-2b` (Always attach private subnets to TGWs, not public!).
3. **Attach the Database VPC:**
   - Name: `TGW-Attach-DB`
   - VPC ID: Select `projectAlpha-DatabaseVPC`
   - Subnets: Select `DB-private1` and `DB-private2`.
4. **Attach Shared Services:**
   - Name: `TGW-Attach-SharedServices`
   - VPC ID: Select `projectAlpha-SharedServicesVPC`
   - Subnets: Select `SS-private1` and `SS-private2`.
   *(Note: If you turn this Shared Services VPC into a Centralized Inspection VPC with a firewall later, you must enable **Appliance Mode** via CLI or console on this specific attachment to prevent stateful asymmetric routing drops!)*

### Phase 3: Configure VPC Route Tables (The Traffic Director)
*Narrative:* Right now, the VPCs are plugged into the Hub, but the VPC's local networks don't know to send traffic to it. We have to tell the local route tables to forward traffic to the TGW.
1. Go to **Route Tables**.
2. Select the Route Table for the **APP-private** subnets.
   - Go to **Routes** > **Edit routes** > **Add route**.
   - **Destination:** `10.0.0.0/8` (or explicit `172.16.0.0/16` and `192.168.0.0/16`).
   - **Target:** Transit Gateway -> Select `projectAlpha-TGW`.
   - **Save changes**. *(Critical: don't leave it unsaved!)*
3. Repeat step 2 on the **DB-private** route table (send `10.0.0.0/16` traffic to the TGW).
4. Repeat step 2 on the **SS-private** route table.

### Phase 4: Route Table Isolation (Lab 3)
*Narrative:* Because you used the Default Route Table in Lab 2, all three of your VPCs were automatically associated and propagated into one giant mesh, allowing everyone to talk to everyone. To segment them, we have to rip out the defaults and build two custom tables: one for the App (which talks to everything) and one for DB/SS (which only talk to the App).

**Step 1: Create the Custom TGW Route Tables**
1. Go to **Transit Gateway Route Tables** and click **Create**.
2. Create: `tgw-rt-app` (Select your `projectAlpha-TGW` ID).
3. Create: `tgw-rt-isolated` (Select your `projectAlpha-TGW` ID).

**Step 2: Break the Defaults & Reassign "Associations"**
*(Association means: "When traffic leaves an attachment, which Route Table does it look at first?")*
1. Click on the original Default TGW Route Table from Lab 2.
2. Go to the **Associations** tab. Select all three of your VPC attachments and hit **Delete association**. 
3. Click the new `tgw-rt-app` table. Go to Associations -> **Create association**, and add the **App VPC**.
4. Click the new `tgw-rt-isolated` table. Go to Associations -> **Create association**, and add both the **Database VPC** AND the **Shared Services VPC**.

**Step 3: Configure "Propagations" (The Magic Step)**
*(Propagation means: "Broadcast this attachment's IP route into this route table.")*
1. Select `tgw-rt-app`. Go to the **Propagations** tab -> **Create propagation**. Select your DB Attachment, and then do it again for your Shared Services Attachment. *(When you check the "Routes" tab, you should see routes for all of them so App can reach everywhere).*
2. Select `tgw-rt-isolated`. Go to the **Propagations** tab -> **Create propagation**. **ONLY select the App VPC Attachment.** Do absolutely nothing else. 
*(Because you didn't propagate the DB to this table, the Shared Services VPC doesn't know the DB exists. If DB pings SS, the TGW simply drops the packet.)*

**Step 4: The Verification**
1. Ping from App -> DB **(Success)**
2. Ping from App -> Shared Services **(Success)**
3. Ping from DB -> Shared Services **(100% Packet Loss / Timeout)**

---

## 🛠️ Key Lessons & Troubleshooting Challenges Today

### 💡 Core Insight: Association vs Propagation
> **"Transit Gateway Association is creating a group of source. Propagation is the destination for which it can connect."**
If a VPC is *associated* to Table A, it looks at Table A when sending packets. If a VPC is *propagated* into Table A, it simply allows Table A to know how to reach it. 

### 🚨 Trap 1: The Phantom Transit Gateway (UI Confusion)
When creating the custom Route Tables in Lab 3, I accidentally had a different Transit Gateway ID selected from the creation dropdown. 
- **Symptom:** When trying to associate my attachments, the dropdown said "No transit gateway attachments found."
![Phantom TGW Error](images/screenshot-tgw-attachment-bug.png)
- **Lesson:** Attachments belong explicitly to the physical TGW. Double-check the exact TGW ID when creating secondary route tables so you don't build them on an empty hub!

### 🚨 Trap 2: The Unsaved DB Return Route
- **Symptom:** Ping timed out. The VPC Route Table editor showed a hyphen (`-`) under the route status.
![Unsaved Return Route](images/screenshot-unsaved-route.png)
- **Lesson:** Pings are two-way. You can edit a route, but if you don't explicitly click "Save changes" to make the route `Active`, the return ping (`pong`) will drop dead in the Database VPC because it doesn't know how to route back to the App. 

### 🚨 Trap 3: The TCP vs ICMP Security Group Trap
- **Symptom:** VPC Flow Logs explicitly showed `REJECT OK` targeting the destination server.
![VPC Flow Log REJECT OK](images/screenshot-flow-logs-reject.png)
- **Lesson:** My Database inbound Security Group was set to its default, which only allows its own SG ID, dropping traffic from the App's SG. Also, setting it to `All TCP` allows SSH but silently drops ping. Ping runs strictly on `ICMP`. I added a rule for `0.0.0.0/0 All Traffic` (or explicitly `All ICMP IPv4`) to allow the ping fully.
![Security Group Inbound Rules Update](images/screenshot-sg-inbound.png)

### 🚨 Trap 4: Flow Logs Ghost Traffic
- **Symptom:** CloudWatch Logs Insights returned `0 records` when querying `srcAddr="<YOUR_APP_PRIVATE_IP>"`.
- **Lesson:** Literal copy-paste trap. I also pinged the local sub-network IP (`10.0.11.194` TGW ENI) instead of the actual Database (`172.16.1.126`), which proved I copied the wrong private IP from the EC2 instance console. Look closely at exactly where the packets are being sent!

![Successful Cross-VPC Ping Tests](images/screenshot-successful-ping.png)
