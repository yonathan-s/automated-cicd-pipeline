# Network Configuration Verification

**Date:** [Current date]

## VPC
VPC created: task-manager-vpc

CIDR: 10.0.0.0/16

DNS hostnames: Enabled

DNS resolution: Enabled

VPC ID: Fill in

## Subnets
Public-1 10.0.1.0/24 in eu-west-2a - Auto-assign public IP: Yes

Public-2 10.0.2.0/24 in eu-west-2b - Auto-assign public IP: Yes

Private-1 10.0.3.0/24 in eu-west-2a

Private-2 10.0.4.0/24 in eu-west-2b

## Internet Gateway
IGW created: task-manager-igw

Attached to VPC

State: Attached

## NAT Gateway
Elastic IP allocated

NAT Gateway created: task-manager-nat

In public subnet: public-1

State: Available

## Route Tables
Public route table created

Public route: 0.0.0.0/0 → IGW

Public subnets associated public-1, public-2

Private route table created

Private route: 0.0.0.0/0 → NAT

Private subnets associated private-1, private-2
## Screenshots Collected
VPC dashboard

VPC details

All 4 subnets list

Public subnet auto-assign IP setting

Internet Gateway attached

NAT Gateway available

Public route table with routes

Public route table subnet associations

Private route table with routes

Private route table subnet associations

