### Step 1: Create ECR Repository
- **Start time:** 14:32  
- **End time:** 14:47  
- **Duration:** 15 minutes  
- **Actions taken:** 
  - Navigated to ECR console  
  - Created private repository named `task-manager-api`  
  - Enabled scan on push  
  - Noted repository URI  
  - Screenshots in `"C:\Users\yonat\OneDrive\Documents\Individual project\automated-cicd-pipeline\docs\screenshots\week-4-manual-deployment"`  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  
- **Notes:** Straightforward process, but had to look up what **"tag immutability"** means  

---

### Step 2: Push Docker Image to ECR
- **Start time:** 14:47  
- **End time:** 15:23  
- **Duration:** 36 minutes  
- **Actions taken:**
  - Built Docker image locally (5 mins)  
  - Retrieved ECR push commands from console (2 mins)  
  - Authenticated Docker to ECR (1 min)  
  - Tagged image (1 min)  
  - Pushed image to ECR (26 mins - large image)  
- **Screenshots:**
  - `ecr-push-commands.png`  
  - `docker-login-success.png`  
  - `docker-images-tagged.png`  
  - `docker-push-progress.png`  
  - `ecr-image-uploaded.png`  
- **Errors encountered:** 
  - Initial authentication failed (**wrong region specified**)  
  - Had to re-run login command with correct region  
- **Notes:** 
  - Push took longer than expected  
  - Image scanning started automatically  
  - Need to remember to specify region in all AWS CLI commands  

---

### Step 3: Create VPC
- **Start time:** 09:08  
- **End time:** 09:36  
- **Duration:** 28 minutes  
- **Actions taken:** 
  - Navigated to VPC console  
  - Created VPC with CIDR `10.0.0.0/16`  
  - Enabled DNS hostnames  
  - Enabled DNS resolution  
- **Screenshots:** `vpc-dashboard.png`, `vpc-created.png`, `vpc-dns-enabled.png`  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  
- **Notes:** Straightforward but had to look up what **DNS hostnames** means  

---

### Step 4: Create Subnets
- **Start time:** 09:36  
- **End time:** 10:19  
- **Duration:** 43 minutes  
- **Actions taken:**
  - Created **4 subnets** (**2 public**, **2 private**)  
  - Distributed across **2 availability zones**  
  - Enabled **auto-assign public IP** for public subnets  
- **Screenshots:** `subnets-form.png`, `subnets-created.png`, `auto-assign-ip.png`  
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Initially put both public subnets in the same AZ (**mistake**)  
  - Had to delete and recreate one subnet  
  - Forgot to enable auto-assign IP, had to go back  
- **Notes:** 
  - Most complex manual step so far  
  - Easy to make CIDR mistakes  
  - Need to carefully track which subnet goes in which AZ  
  - This would be much easier with **IaC**  

---

### Step 5: Create ALB Security Group
- **Start time:** 10:23  
- **End time:** 10:37  
- **Duration:** 14 minutes  
- **Actions taken:**
  - Navigated to EC2 Security Groups  
  - Created security group in `task-manager-vpc`  
  - Added inbound rule: **HTTP (80)** from `0.0.0.0/0`  
  - Left default outbound rule  
- **Screenshots:** 
  - `security-groups-page.png`  
  - `alb-sg-creation.png`  
  - `alb-sg-inbound-rule.png`  
  - `alb-sg-created.png`  
- **Difficulty (1-5):** 3  
- **Errors encountered:** 
  - Initially forgot to select correct VPC (used **default VPC**)  
  - Had to delete and recreate  
- **Notes:**
  - Must be careful to select correct VPC  
  - Easy to accidentally use default VPC  
  - Security group IDs need to be copied for later steps  

---

### Step 6: Create ECS Security Group
- **Start time:** 10:37  
- **End time:** 10:59  
- **Duration:** 22 minutes  
- **Actions taken:**
  - Created ECS tasks security group  
  - Critical: Set source as **ALB security group**, not `0.0.0.0/0`  
  - Port `5000` (Flask application port)  
- **Screenshots:**
  - `ecs-sg-creation.png`  
  - `ecs-sg-inbound-source-alb.png`  
  - `ecs-sg-created.png`  
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Initially set source as `0.0.0.0/0` (**security risk**)  
  - Realized mistake and edited to use ALB SG  
- **Notes:**
  - This is a common security mistake in manual deployments  
  - Must understand security group referencing  
  - Easy to expose application directly to internet by mistake  

---

### Step 7: Create ECS Task Execution Role
- **Start time:** 11:03  
- **End time:** 11:34  
- **Duration:** 31 minutes  
- **Actions taken:**
  - Navigated to IAM Roles  
  - Created role with **ECS Tasks** trusted entity  
  - Attached `AmazonECSTaskExecutionRolePolicy`  
  - Copied ARN for later use  
- **Screenshots:**
  - `iam-roles-page.png`  
  - `task-execution-role-trusted-entity.png`  
  - `task-execution-role-policy.png`  
  - `task-execution-role-created.png`  
  - `task-execution-role-arn.png`  
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Confusion between **"EC2 Container Service Task"** and **"Elastic Container Service Task"**  
  - Selected wrong option initially  
- **Notes:**
  - IAM role creation requires understanding trust policies  
  - Easy to confuse which service to select  
  - Must understand difference between execution role and task role  
  - ARN must be copied exactly (easy to make typos)  

---

### Step 8: Create ECS Task Role
- **Start time:** 11:34  
- **End time:** 11:49  
- **Duration:** 15 minutes  
- **Actions taken:**
  - Created task role with same trusted entity  
  - No policies attached (application doesn't need AWS permissions yet)  
  - Documented purpose for future reference  
- **Screenshots:**
  - `task-role-creation.png`  
  - `task-role-no-policies.png`  
  - `task-role-created.png`  
- **Difficulty (1-5):** 3  
- **Errors encountered:** None  
- **Notes:**
  - Simpler than execution role (no policies to attach)  
  - Important to understand why two separate roles needed  
  - This separation of concerns is a best practice  