# IAM Roles for ECS

## Why Two Roles?

ECS uses two separate IAM roles with different purposes:

### 1. Task Execution Role (ecsTaskExecutionRole)
**Used by:** ECS service itself 
**Purpose:** Infrastructure operations
**Permissions:**
- Pull container images from ECR
- Create CloudWatch log groups
- Write logs to CloudWatch
- Retrieve secrets from Secrets Manager 

**When it's used:**
- Before container starts (pulling image)
- During container runtime (writing logs)

**ARN:** arn:aws:iam::222575804813:role/ecsTaskExecutionRole

### 2. Task Role (taskManagerTaskRole)
**Used by:** Your application code running in the container
**Purpose:** Application operations
**Permissions:**
- Currently: None
- Future examples: Access S3, DynamoDB, SNS, etc.

**When it's used:**
- When my application code makes AWS SDK calls

**ARN:** arn:aws:iam::222575804813:role/taskManagerTaskRole

## Analogy (I used from claude to help me understand)

Think of it like a delivery truck:

- **Task Execution Role:** The truck company's credentials to pick up packages (ECR images) and deliver them (start containers)
- **Task Role:** The driver's credentials to interact with customers (my app interacting with AWS services)

## Manual Setup Complexity

Manual IAM setup required:
1. Understanding the trust relationship (who can assume the role)
2. Knowing which managed policy to attach
3. Creating two separate roles
4. Copying ARNs for later use
5. Understanding the difference between the roles

