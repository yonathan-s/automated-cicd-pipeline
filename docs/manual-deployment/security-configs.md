# Security Configuration Verification

## ALB Security Group
- Name: task-manager-alb-sg
- VPC: task-manager-vpc
- Security Group ID: [Fill in: sg-xxx]
- Inbound: HTTP (80) from 0.0.0.0/0
- Outbound: All traffic to 0.0.0.0/0
- Screenshot: alb-sg-details.png

## ECS Security Group
- Name: task-manager-ecs-sg
- VPC: task-manager-vpc
- Security Group ID: [Fill in: sg-xxx]
- Inbound: TCP 5000 from ALB SG only
- Outbound: All traffic to 0.0.0.0/0
- Screenshot: ecs-sg-details.png

## Security Test Questions
- Can internet traffic reach port 80 on ALB? YES
- Can internet traffic reach port 5000 on ECS tasks? NO (blocked)
- Can ALB reach port 5000 on ECS tasks? YES
- Can ECS tasks pull from ECR? YES (outbound allowed)
- Can ECS tasks send logs to CloudWatch? YES (outbound allowed)

## Common Security Mistakes to Avoid
- Did NOT allow 0.0.0.0/0 to port 5000 on ECS tasks
- DID allow ALB SG to port 5000 on ECS tasks
- Did NOT restrict outbound from ECS tasks (needs ECR/CloudWatch access)
- DID use correct VPC for both security groups
