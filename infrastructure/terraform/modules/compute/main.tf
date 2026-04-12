resource "aws_ecr_repository" "app" {
  name                 = "${var.environment}-task-manager-api"
  image_tag_mutability = "MUTABLE"
  force_delete         = true  

  image_scanning_configuration {
    scan_on_push = true  #
  }

  tags = {
    Name = "${var.environment}-task-manager-api"
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecs_cluster" "main" {
  name = "${var.environment}-task-manager-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"  # not needed for this project
  }

  tags = {
    Name = "${var.environment}-ecs-cluster"
  }
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.environment}-task-manager"
  retention_in_days = 7  # Short retention to avoid unnecessary storage costs

  tags = {
    Name = "${var.environment}-ecs-logs"
  }
}


resource "aws_ecs_task_definition" "app" {
  family                   = "${var.environment}-task-manager-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"  # Required for Fargate
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = var.ecs_task_execution_role_arn  # allows ECS to pull image from ECR and write logs
  task_role_arn            = var.ecs_task_role_arn  # permissions for the app itself at runtime

  container_definitions = jsonencode([
    {
      name      = "task-manager-container"
      image     = "${aws_ecr_repository.app.repository_url}:latest"
      essential = true  # says if the container stops so do does the task

      portMappings = [
        {
          containerPort = 5000 #default
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "FLASK_ENV"
          value = "production"  
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "task-manager"
        }
      }
    }
  ])

  tags = {
    Name = "${var.environment}-task-definition"
  }
}


resource "aws_lb" "main" {
  name               = "${var.environment}-task-manager-alb"
  internal           = false  #make public
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.public_subnet_ids  

  tags = {
    Name = "${var.environment}-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name        = "${var.environment}-task-manager-tg"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"  # Fargate tasks use IP targets and not instance id's

  health_check {
    enabled             = true
    healthy_threshold   = 2  #I need 2 passing checks to be considered healthy
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3  # removes task after 3 backto back failures
  }

  deregistration_delay = 30  # reduced from default 300s so failed tasks are removed faster

  tags = {
    Name = "${var.environment}-target-group"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

resource "aws_ecs_service" "app" {
  name            = "${var.environment}-task-manager-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids  #So tasks in private subnets are only reachable through ALB
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false  # no direct internet access, traffic goes through ALB only
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "task-manager-container"
    container_port   = 5000
  }

  health_check_grace_period_seconds = 60  #Added to give time to actually start health checks

  depends_on = [
    aws_lb_listener.http  
  ]

  tags = {
    Name = "${var.environment}-ecs-service"
  }
}