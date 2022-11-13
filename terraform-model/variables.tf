variable "aws-region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI ID"
  type        = string
  default = "ami-0ee23bfc74a881de5"
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

variable "instance_variables" {
  description = "Instance variables"
  type        = map(object({
    instance_name = string
    instance_type = string
    security_group = object({
      security_name = string
      security_description = string
      security_ingress = string
      security_from_port = number
      security_to_port = number
      security_protocol = string
      security_cidr_blocks = list(string)
    })
  }))
  default = {
    "instance_variables" = {
      instance_name = "padraozao"
      instance_type = "t2.micro"
      security_group = {
        usable_var = true
        security_cidr_blocks = [ "0.0.0.0/24" ]
        security_description = "nossa, que padraozinho"
        security_from_port = 1
        security_ingress = "ingress default"
        security_name = "defaultzera"
        security_protocol = "tcp"
        security_to_port = 1
      }
    }
  }
}