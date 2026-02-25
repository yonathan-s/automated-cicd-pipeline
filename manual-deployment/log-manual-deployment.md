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
- **Notes:** Straightforward process, but had to look up what "tag immutability" means  

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


### Step 9: Create ECS Cluster
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Navigated to ECS console
  - Created Fargate cluster
  - Named: task-manager-cluster
- **Screenshots:** ecs-console.png, cluster-creation.png, cluster-created.png
- **Difficulty (1-5):** 2
- **Errors encountered:** None
- **Notes:** Simplest step so far. Just naming and selecting Fargate.

### Step 10: Create CloudWatch Log Group
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Created log group for ECS tasks
  - Name: /ecs/task-manager
  - Set retention to 1 week
- **Screenshots:** cloudwatch-logs.png, log-group-created.png
- **Difficulty (1-5):** 2
- **Errors encountered:** None
- **Notes:** Need to remember exact log group name for task definition

### Step 11: Create ECS Task Definition
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Created task definition with Fargate
  - Set CPU: 0.5 vCPU, Memory: 1GB
  - Configured container with ECR image URI
  - Set port mapping: 5000
  - Added environment variable: FLASK_ENV=production
  - Configured CloudWatch logging
  - Added health check
  - Referenced both IAM roles created on Day 3
- **Screenshots:**
  - task-def-infrastructure.png
  - task-def-container-image.png
  - task-def-port-mapping.png
  - task-def-env-vars.png
  - task-def-logging.png
  - task-def-created.png
  - task-def-details.png
- **Difficulty (1-5):** 5
- **Errors encountered:**
  - Initially forgot to add port mapping (error on create)
  - Typo in ECR image URI (had to edit task definition)
  - Forgot to select task execution role (error on create)
- **Notes:**
  - Most complex configuration yet
  - Many fields to fill correctly
  - Must have exact ECR URI, role ARNs, log group name
  - Easy to miss required fields
  - Form is long and requires scrolling
  - Error messages not always clear about what's wrong
  - This complexity highlights benefit of IaC


### Step 12: Create Target Group
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Created target group with IP address type (for Fargate)
  - Named: task-manager-tg
  - Protocol HTTP, Port 5000
  - Configured health check on /health endpoint
  - Left targets empty (ECS will register)
- **Screenshots:** target-group-creation.png, health-check-config.png, target-group-created.png
- **Difficulty (1-5):** 3
- **Errors encountered:**
  - Initially selected "Instances" type instead of "IP addresses" (had to recreate)
- **Notes:**
  - Must use IP addresses for Fargate (not EC2 instances)
  - Health check configuration critical for proper operation
  - Empty targets normal at this stage

### Step 13: Create Application Load Balancer
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Created internet-facing ALB
  - Selected task-manager-vpc
  - Placed in both public subnets (eu-west-2a, eu-west-2b)
  - Attached ALB security group
  - Configured listener HTTP:80 → target group
  - Waited for ALB to become active (5 minutes)
  - Noted DNS name for application access
- **Screenshots:**
  - alb-type-selection.png
  - alb-basic-config.png
  - alb-network-mapping.png
  - alb-security-groups.png
  - alb-listener-config.png
  - alb-creating.png
  - alb-active.png
  - alb-dns-name.png
- **Difficulty (1-5):** 4
- **Errors encountered:**
  - Accidentally selected private subnets initially (error - ALB can't be internet-facing in private subnets)
  - Had to go back and select public subnets
  - Forgot to remove default security group (had multiple SGs attached)
- **Notes:**
  - ALB must be in public subnets for internet access
  - Must carefully select correct subnets from dropdown
  - Provisioning takes several minutes
  - DNS name is long and complex - easy to make typos
  - This is a critical component - if misconfigured, application won't be accessible


  ### Step 14: Create ECS Service
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Created ECS service in task-manager-cluster
  - Selected task definition: task-manager-task:1
  - Set desired count: 2 tasks
  - Configured networking: private subnets, ECS security group
  - Integrated with ALB and target group
  - Waited for tasks to start and become healthy
  - Verified 2 running tasks
- **Screenshots:**
  - service-creation-compute.png
  - service-creation-deployment.png
  - service-creation-networking.png
  - service-creation-load-balancing.png
  - service-creating.png
  - service-active.png
  - tasks-running.png
- **Difficulty (1-5):** 5
- **Errors encountered:**
  - Initially selected public subnets (should be private for tasks)
  - Corrected before creating service
  - First task failed to start (checked logs - typo in image URI in task definition)
  - Updated task definition to revision 2
  - Re-deployed service with new revision
- **Notes:**
  - Most complex creation yet - brings together all previous components
  - Many configuration options and dependencies
  - Easy to select wrong subnets (public vs private)
  - Task failures require checking CloudWatch logs
  - Long wait time for service to stabilize
  - Must understand entire architecture to configure correctly

### Step 15: Verify and Test Deployment
- **Start time:** [Your time]
- **End time:** [Your time]
- **Duration:** [Minutes]
- **Actions taken:**
  - Checked target group health (2 healthy targets)
  - Accessed application via ALB DNS
  - Tested all CRUD operations
  - Verified health endpoint
  - Checked CloudWatch logs
  - Documented successful deployment
- **Screenshots:**
  - target-group-healthy.png
  - app-via-alb.png
  - app-create-task.png
  - app-task-complete.png
  - app-task-delete.png
  - health-endpoint-response.png
  - cloudwatch-logs.png
- **Difficulty (1-5):** 3
- **Errors encountered:** None (after fixing service configuration)
- **Notes:**
  - Application works correctly via ALB
  - All functionality operational
  - Logs flowing to CloudWatch
  - DNS name is long and hard to remember
  - No custom domain configured (manual DNS setup is complex)