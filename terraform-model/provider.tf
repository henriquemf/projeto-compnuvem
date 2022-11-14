terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws-region
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_vpc" "vpc_test" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "vpc_test"
  }
}

resource "aws_subnet" "vpc_test_subnet" {
  vpc_id     = aws_vpc.vpc_test.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "subnet_test"
  }
}

resource "aws_security_group" "security_group" {
  for_each    = var.security_groups
  name        = each.value.security_name
  description = each.value.security_description
  vpc_id      = aws_vpc.vpc_test.id

  ingress {
    description = each.value.security_ingress
    from_port   = each.value.security_from_port
    to_port     = each.value.security_to_port
    protocol    = each.value.security_protocol
    cidr_blocks = each.value.security_cidr_blocks
  }
}

resource "aws_instance" "app_server" {
  for_each      = var.instances
  ami           = var.ami
  instance_type = each.value.instance_type
  vpc_security_group_ids = [aws_security_group.security_group[each.value.security_name].id]
  subnet_id     = aws_subnet.vpc_test_subnet.id

  tags = {
    Name = "${each.value.instance_name}"
  }
}

module "user" {
  source    = "./user"
  users = var.users
}

output "user" {
  value = module.user
}


