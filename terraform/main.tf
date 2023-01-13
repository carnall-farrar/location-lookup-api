# Data required
data "aws_vpc" "selected" {
  id = "vpc-04159dd325ae32063"
}

data "aws_subnet_ids" "private_subnets" {
  vpc_id = data.aws_vpc.selected.id

  tags = {
    Tier = "Private"
  }
}

data "aws_subnet_ids" "public_subnets" {
  vpc_id = data.aws_vpc.selected.id

  tags = {
    Tier = "Public"
  }
}

data "aws_iam_role" "ecsTaskExecutionRole" {
  name = "ecsTaskExecutionRole"
}

resource "aws_iam_role_policy_attachment" "secretManagerReads" {
  role       = data.aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::037892153371:policy/cf-secret-manager-reads"
}

resource "aws_iam_role_policy_attachment" "ecs_policy_attachment2" {
  role       = data.aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

data "aws_secretsmanager_secret_version" "secrets" {
  # Fill in the name you gave to your secret
  secret_id = var.secret_name
}

data "aws_acm_certificate" "cfdata_issued" {
  domain   = "*.cfdata.io"
  statuses = ["ISSUED"]
}

data "aws_route53_zone" "cfdata_zone" {
  zone_id = var.dns_zone_id
}

# Resources required for provisioning a Task and a Service on ECS Cluster
resource "aws_ecr_repository" "docker_container_registry" {
  name = var.docker_registry_name
}

# ${aws_ecr_repository.docker_container_registry.repository_url}:${var.tag}
resource "aws_ecs_task_definition" "compute_task" {
  family                   = var.task_name
  container_definitions    = <<DEFINITION
  [
    {
      "name": "${var.task_name}",
      "image": "${aws_ecr_repository.docker_container_registry.repository_url}:${var.tag}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "secrets": [
        {
          "name": "POSTGRES_USER",
          "valueFrom" : "${data.aws_secretsmanager_secret_version.secrets.arn}:AWS_ACCESS_KEY::"
        },
        {
          "name": "POSTGRES_PASSWORD",
          "valueFrom" : "${data.aws_secretsmanager_secret_version.secrets.arn}:AWS_ACCESS_KEY::"
        },
        {
          "name": "POSTGRES_HOST",
          "valueFrom" : "${data.aws_secretsmanager_secret_version.secrets.arn}:AWS_ACCESS_KEY::"
        },
        {
          "name": "FLASK_ENV",
          "valueFrom" : "${data.aws_secretsmanager_secret_version.secrets.arn}:AWS_ACCESS_KEY::"
        },
        {
          "name": "APP_SETTINGS",
          "valueFrom" : "${data.aws_secretsmanager_secret_version.secrets.arn}:AWS_ACCESS_KEY::"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${var.log_group_name}",
          "awslogs-region": "eu-west-2",
          "awslogs-stream-prefix": "${var.log_group_name}-"
        }
      },
      "memory": 1024,
      "cpu": 512
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 1024
  cpu                      = 512
  execution_role_arn       = data.aws_iam_role.ecsTaskExecutionRole.arn
  tags = {
    Environment = "production"
  }
}

resource "aws_cloudwatch_log_group" "compute_log_group" {
  name = var.log_group_name

  tags = {
    Environment = "production"
    Application = var.log_group_name
  }
}

resource "aws_cloudwatch_log_subscription_filter" "datadog_log_subscription_filter" {
  name            = "datadog_log_subscription_filter"
  log_group_name  = aws_cloudwatch_log_group.compute_log_group.name
  destination_arn = "arn:aws:lambda:eu-west-2:037892153371:function:datadog-forwarder-Forwarder-NoHls4EeiUIy"
  filter_pattern  = ""
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = data.aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_service" "compute_service" {
  name            = var.service_name
  cluster         = "cf-cluster"
  task_definition = aws_ecs_task_definition.compute_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  load_balancer {
    target_group_arn = aws_lb_target_group.lb_target_group.arn
    container_name   = aws_ecs_task_definition.compute_task.family
    container_port   = 5000
  }

  network_configuration {
    subnets          = slice(tolist(data.aws_subnet_ids.private_subnets.ids), 0, 3)
    assign_public_ip = true
    security_groups  = [aws_security_group.service_security_group.id]
  }
}

resource "aws_alb" "application_load_balancer" {
  name               = var.lb_name
  load_balancer_type = "application"
  subnets            = slice(tolist(data.aws_subnet_ids.public_subnets.ids), 0, 3)

  security_groups = [aws_security_group.load_balancer_security_group.id]
}

resource "aws_security_group" "load_balancer_security_group" {
  vpc_id = data.aws_vpc.selected.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic in from all sources
  }

  egress {
    from_port   = 0             # Allowing any incoming port
    to_port     = 0             # Allowing any outgoing port
    protocol    = "-1"          # Allowing any outgoing protocol 
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
  }
}

resource "aws_security_group" "service_security_group" {
  vpc_id = data.aws_vpc.selected.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.load_balancer_security_group.id]
  }

  egress {
    from_port   = 0             # Allowing any incoming port
    to_port     = 0             # Allowing any outgoing port
    protocol    = "-1"          # Allowing any outgoing protocol 
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
  }
}

resource "aws_lb_target_group" "lb_target_group" {
  name        = var.lb_target_name
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = data.aws_vpc.selected.id

  health_check {
    matcher             = "200,301,302"
    path                = "/ping"
    interval            = 300
    timeout             = 120
    unhealthy_threshold = 5
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_alb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_load_balancer.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.cfdata_issued.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lb_target_group.arn
  }
}

# AWS RDS Postgres provisioning

resource "aws_db_subnet_group" "rds_subnet" {
  name       = var.rds_subnet_name
  subnet_ids = slice(tolist(data.aws_subnet_ids.private_subnets.ids), 3, 6)

  tags = {
    Name = var.rds_subnet_name
  }
}

resource "aws_security_group" "rds" {
  name   = var.rds_security_group_name
  vpc_id = data.aws_vpc.selected.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.rds_security_group_name
  }
}

resource "aws_db_parameter_group" "db_parameter_group" {
  name   = var.db_username
  family = "postgres13"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "db" {
  identifier             = var.db_username
  instance_class         = "db.t3.small"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "13.7"
  username               = var.db_username
  name                   = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.db_parameter_group.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}

# DNS provisioning
resource "aws_route53_record" "api_dns" {
  zone_id = data.aws_route53_zone.cfdata_zone.zone_id
  name    = var.dns_name
  type    = "A"

  alias {
    name                   = aws_alb.application_load_balancer.dns_name
    zone_id                = aws_alb.application_load_balancer.zone_id
    evaluate_target_health = true
  }
}
