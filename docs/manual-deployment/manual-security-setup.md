# Manual Security Configuration

## Security Groups

### ALB Security Group
- **Name:** task-manager-alb-sg
- **VPC:** task-manager-vpc
- **Inbound Rules:**
  - HTTP (80) from 0.0.0.0/0 (allow internet traffic)
- **Outbound Rules:**
  - All traffic to 0.0.0.0/0 (default)

### ECS Tasks Security Group
- **Name:** task-manager-ecs-sg
- **VPC:** task-manager-vpc
- **Inbound Rules:**
  - TCP 5000 from ALB Security Group only
- **Outbound Rules:**
  - All traffic to 0.0.0.0/0 (for pulling images, sending logs)

## IAM Roles

### ECS Task Execution Role
- **Name:** ecsTaskExecutionRole
- **Trusted Entity:** ecs-tasks.amazonaws.com
- **Policies:**
  - AmazonECSTaskExecutionRolePolicy (AWS managed)
  - Allows: Pull from ECR, write to CloudWatch Logs

### ECS Task Role
- **Name:** taskManagerTaskRole
- **Trusted Entity:** ecs-tasks.amazonaws.com
- **Policies:**
  - None (application doesn't need AWS permissions yet)