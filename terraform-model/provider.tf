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
  region  = var.aws-region
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_vpc" "tcb_blog_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "vpc_test"
  }
}

resource "aws_subnet" "tcb_blog_public_subnet" {
  vpc_id     = aws_vpc.tcb_blog_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "subnet_test"
  }
}


resource "aws_instance" "app_server" {
  for_each = var.instance_variables
  ami           = var.ami
  instance_type = each.value.instance_type

  tags = {
    Name = "${each.value.instance_name}"
  }
}