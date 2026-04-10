terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "task-manager"
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}

#Data sources
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
}

module "networking" {
  source = "./modules/networking"

  vpc_cidr             = var.vpc_cidr
  environment          = var.environment
  availability_zones   = slice(data.aws_availability_zones.available.names, 0, 2)
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}


module "security" {
  source = "./modules/security"

  vpc_id      = module.networking.vpc_id
  environment = var.environment
}

module "compute" {
  source = "./modules/compute"

  environment                 = var.environment
  vpc_id                      = module.networking.vpc_id
  private_subnet_ids          = module.networking.private_subnet_ids
  public_subnet_ids           = module.networking.public_subnet_ids
  ecs_security_group_id       = module.security.ecs_security_group_id
  alb_security_group_id       = module.security.alb_security_group_id
  ecs_task_execution_role_arn = module.security.ecs_task_execution_role_arn
  ecs_task_role_arn           = module.security.ecs_task_role_arn
  aws_region                  = var.aws_region
  task_cpu                    = var.ecs_task_cpu
  task_memory                 = var.ecs_task_memory
  desired_count               = var.desired_count
}