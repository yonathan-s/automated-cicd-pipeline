# Tgis file contains the manual deployment log that I will use as the baseline for my manual simulations

Screenshots for each step can be found in "C:\Users\yonat\OneDrive\Documents\Individual project\automated-cicd-pipeline\docs\screenshots\week-4-manual-deployment". These screenshots can act as proof that each step was actually completed and timed. 

### Step 1: Create ECR Repository
- **Start time:** 22:54 
- **End time:** 23:10  
- **Duration:** 15 minutes  
- **Actions:** 
  - Went to ECR console  
  - Created private repository `task-manager-api`  
  - Enabled scan on push  
  - Screenshots in `"C:\Users\yonat\OneDrive\Documents\Individual project\automated-cicd-pipeline\docs\screenshots\week-4-manual-deployment"`  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  
- **Notes:** pretty simple   


### Step 2: Push Docker Image to ECR
- **Start time:** 23:14  
- **End time:** 23:50  
- **Duration:** 36 minutes  
- **Actions:**
  - Built Docker image locally 
  - Retrieved push commands from ECR
  - Authenticated Dockr to ECR   
  - Tagged image  
  - Pushed image to ECR 

- **Errors encountered:** 
  - Initial authentication failed   
  - Had to rerun login command with correct region  
- **Notes:** 
  - Push took longer than expected  
  - Image scanning started automatically  
  - Need to remember to specify region in all AWS CLI commands  



### Step 3: Create VPC
- **Start time:** 09:08  
- **End time:** 09:36  
- **Duration:** 28 minutes  
- **Actions done:** 
  - Navigated to VPC console  
  - Created VPC with CIDR `10.0.0.0/16`  
  - Enabled DNS hostnames  
  - Enabled DNS resolution  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  
- **Notes:** Simple  



### Step 4: Create Subnets
- **Start time:** 09:36  
- **End time:** 10:19  
- **Duration:** 43 minutes  
- **Actions taken:**
  - Created 4 subnets (2 public, 2 private)  
  - Distributed across 2 availability zones  
  - Enabled auto-assign public IP for public subnets  
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Initially put both public subnets in the same zone
  - Forgot to enable auto-assign IP, had to go back  
- **Notes:** 
  - Most complex manual step so far  
  - Easy to make CIDR mistakes  
  - Need to carefully track which subnet goes in which AZ  


### Step 5: Create ALB Security Group
- **Start time:** 10:23  
- **End time:** 10:37  
- **Duration:** 14 minutes  
- **Actions taken:**
  - Navigated to EC2 Security Groups  
  - Created security group in `task-manager-vpc`  
  - Added inbound rule: HTTP (80) from `0.0.0.0/0`  
  - Left default outbound rule   
- **Difficulty (1-5):** 3  
- **Errors encountered:** 
  - Initially forgot to select correct VPC (useddefault VPC  )

- **Notes:**
  - Must be careful to select correct VPC  
  - Easy to accidentally use default VPC  
  - Security group IDs need to be copied for later steps  


### Step 6: Create ECS Security Group
- **Start time:** 10:37  
- **End time:** 10:59  
- **Duration:** 22 minutes  
- **Actions taken:**
  - Created ECS tasks security group  
  - Critical: Set source as **ALB security group**, not `0.0.0.0/0`  
  - Port `5000` (Flask application port)    
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Initially set source as `0.0.0.0/0` (apparently a security risk)  
  - Realized mistake and edited to use ALB security group  
- **Notes:**
  - Security concerns are likely 



### Step 7: Create ECS Task Execution Role
- **Start time:** 11:03  
- **End time:** 11:34  
- **Duration:** 31 minutes  
- **Actions taken:**
  - Navigated to IAM Roles  
  - Created role with ECS Tasks trusted entity  
  - Attached `AmazonECSTaskExecutionRolePolicy`  
  - Copied ARN for later use   
- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Confusion between "EC2 Container Service Task" and "Elastic Container Service Task"  
=- **Notes:**
  - Easy to confuse which service to select  
  - ARN must be copied exactly (easy to make typos)  



### Step 8: Create ECS Task Role
- **Start time:** 11:34  
- **End time:** 11:49  
- **Duration:** 15 minutes  
- **Actions taken:**
  - Created task role with same trusted entity  
  - No policies attached (application doesn't need AWS permissions yet)  
  - Documented purpose for future reference  
- **Difficulty (1-5):** 3  
- **Errors encountered:** None  
- **Notes:**
  - Simpler than execution role (no policies to attach)  
  - Important to understand why two separate roles needed  
  - This separation of concerns is a best practice  


### Step 9: Create ECS Cluster (ECS task definition and ecs cluster were configured simultaenously and hence have overlapping start times)
- **Start time:** 15:40  
- **End time:** 16:38  
- **Duration:** 11 minutes   
- **Actions taken:**
  - Navigated to ECS console  
  - Created Fargate cluster  
  - Named: `task-manager-cluster`  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  
- **Notes:** Simplest step so far. Just naming and selecting Fargate.  
  



### Step 10: Create ECS Task Definition
- **Start time:** 15:56  
- **End time:** 16:54  
- **Duration:** 47 minutes (58 - 11 (The duration of creating the ECS cluster))
- **Actions taken:**
  - Created task definition with Fargate  
  - Set CPU: 0.5 vCPU, Memory: 1GB  
  - Configured container with ECR image URI  
  - Set port mapping: 5000  
  - Added environment variable: `FLASK_ENV=production`  
  - Configured CloudWatch logging  
  - Added health check  
  - Referenced both IAM roles created earlier  
- **Difficulty (1-5):** 5  
- **Errors encountered:**
  - Initially forgot to add port mapping   
  - Put a typo in ECR image URI (had to edit task definition)  
  - forgot to select task execution role (error on create)  
- **Notes:**
  - Most complex configuration yet  
  - Many fields to fill correctly  
  - Easy to miss some fields  
  - Form's long 
  - Error messages aren't not always clear about what's wrong  


  ### Step 11: Create CloudWatch Log Group
- **Start time:** 17:00  
- **End time:** 17:12  
- **Duration:** 11 minutes  
- **Actions taken:**
  - Created log group for ECS tasks  
  - Name: `/ecs/task-manager`  
  - Set retention to 1 week  
`  
- **Difficulty (1-5):** 2  
- **Errors encountered:** None  


### Step 12: Create Target Group
- **Start time:** 17:21  
- **End time:** 17:38  
- **Duration:** 17 minutes  
- **Actions taken:**
  - I made target group with IP address type`task-manager-tg`  
  - Protocol HTTP, Port 5000  
  - Configured health check on `/health` endpoint  
- **Difficulty (1-5):** 3  
- **Errors encountered:**
  - I had to recreate IP addresses due to a misclick
- **Notes:**
  - Must use IP addresses for Fargate (not EC2 instances)  



### Step 13: Create Application Load Balancer
- **Start time:** 19:55  
- **End time:** 20:29 
- **Duration:** 34 minutes  
- **Actions taken:**
  - Created internet-facing ALB  
  - Selected `task-manager-vpc`  
  - Attached ALB security group  
  - Configured listener HTTP:80 → target group  
  - I had to waited for ALB to become active
  - Noted DNS name for application access   

- **Difficulty (1-5):** 4  
- **Errors encountered:**
  - Accidentally selected private subnets initially (ALB cannot be internet-facing in private subnets)  
  - Had to go back and select public subnets  
  - Forgot to remove default security group (multiple SGs attached)  
  - Had to reset desired tasks from 2 back to 1 because when I had 2 ECS tasks running with in-memory storage Each task had its own separate memory, so:
    -Request 1 went to Task A (creates task "X")
    -Request 2 went to Task B (doesn't have task "X")
    -Request 3 went to Task A (has task "X")
    -This alternated, making it look like data disappears
    (I can change desired tasks back to 2 once I've created a shared database that stores changes made from both tasks so it doesn't have this affect on the app)
- **Notes:**
  - ALB must be in public subnets for internet access  
  - Must carefully select correct subnets from dropdown  
 



### Step 14: Create ECS Service
- **Start time:** 20:32 
- **End time:** 21:20 
- **Duration:** 48 minutes  
- **Actions taken:**
  - Created ECS service in `task-manager-cluster`  
  - Selected task definition: `task-manager-task:1`  
  - Set desired count: 2 tasks  
  - Configured networking: private subnets, ECS security group  
  - Integrated with ALB and target group  
  - Waited for tasks to start and become healthy  
  - Verified 2 running tasks  
- **Difficulty (1-5):** 5  
- **Errors encountered:**
  - Initially selected public subnets (should be private for tasks)  
  - First task failed to start, type in imageuri  
  - I updated task definition to revision 2  
  - Re-deployed service with new revision  
- **Notes:**
  - Most complex creation so far  
  - Long wait time for service to stabilize  



### Step 15: Verify and Test Deployment
- **Start time:** 21:47  
- **End time:** 22:08 
- **Duration:** 21 minutes  
- **Actions taken:**
  - Checked target group health (2 healthy targets)  
  - Accessed application via ALB DNS  
  - Tested all CRUD operations  
  - Verified health endpoint  
  - Checked CloudWatch logs  
  - Documented successful deployment  
- **Difficulty (1-5):** 3  
- **Errors encountered:** None (after fixing service configuration)  
- **Notes:**
  - Application works correctly via ALB  
  - All functionality operational  
  - Logs flowing to CloudWatch  
  