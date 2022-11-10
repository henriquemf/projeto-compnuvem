variable "aws-region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI ID"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default = "t2.nano"
}

variable "access_key" {
  description = "AWS access key"
  type        = string
  sensitive = true
}

variable "secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive = true
}

variable "username" {
  description = "Username"
  type        = string
  sensitive = true
}

variable "password" {
  description = "Password"
  type        = string
  sensitive = true
}

variable "instance_name" {
  description = "Name"
  type        = string
  default = "padrao"
}

variable "instance_variables" {
  description = "Instance variables"
  type        = map(object({
    instance_name = string
    instance_type = string
  }))
}