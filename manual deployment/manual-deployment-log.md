### Step 1: Create ECR Repository
- **Start time:** 14:30:00
- **End time:** 14:45:00
- **Duration:** 15 minutes
- **Actions taken:** 
  - Navigated to ECR console
  - Created private repository named task-manager-api
  - Enabled scan on push
  - Noted repository URI
  - Screenshots in "C:\Users\yonat\OneDrive\Documents\Individual project\automated-cicd-pipeline\docs\screenshots\week-4-manual-deployment"
  
- **Difficulty (1-5):** 2
- **Errors encountered:** None
- **Notes:** Straightforward process, but had to look up what "tag immutability" means

### Step 2: Push Docker Image to ECR
- **Start time:** 14:45:00
- **End time:** 15:20:00
- **Duration:** 35 minutes
- **Actions taken:**
  - Built Docker image locally (5 mins)
  - Retrieved ECR push commands from console (2 mins)
  - Authenticated Docker to ECR (1 min)
  - Tagged image (1 min)
  - Pushed image to ECR (26 mins - large image)
- **Screenshots:**
  - ecr-push-commands.png
  - docker-login-success.png
  - docker-images-tagged.png
  - docker-push-progress.png
  - ecr-image-uploaded.png
- **Errors encountered:** 
  - Initial authentication failed (wrong region specified)
  - Had to re-run login command with correct region
- **Notes:** 
  - Push took longer than expected
  - Image scanning started automatically
  - Need to remember to specify region in all AWS CLI commands

  ### Step 3: Create VPC
- **Start time:** 09:00:00
- **End time:** 09:30:00
- **Duration:** 30 minutes
- **Actions taken:** 
  - Navigated to VPC console
  - Created VPC with CIDR 10.0.0.0/16
  - Enabled DNS hostnames
  - Enabled DNS resolution
- **Screenshots:** vpc-dashboard.png, vpc-created.png, vpc-dns-enabled.png
- **Difficulty (1-5):** 2
- **Errors encountered:** None
- **Notes:** Straightforward but had to look up what DNS hostnames means

### Step 4: Create Subnets
- **Start time:** 09:30:00
- **End time:** 10:10:00
- **Duration:** 40 minutes
- **Actions taken:**
  - Created 4 subnets (2 public, 2 private)
  - Distributed across 2 availability zones
  - Enabled auto-assign public IP for public subnets
- **Screenshots:** subnets-form.png, subnets-created.png, auto-assign-ip.png
- **Difficulty (1-5):** 4
- **Errors encountered:**
  - Initially put both public subnets in same AZ (mistake)
  - Had to delete and recreate one subnet
  - Forgot to enable auto-assign IP, had to go back
- **Notes:** 
  - Most complex manual step so far
  - Easy to make CIDR mistakes
  - Need to carefully track which subnet goes in which AZ
  - This would be much easier with IaC

[Continue for all Day 2 steps]