resource "aws_instance" "default" {
  ami = var.ami
  instance_type = var.instance_type
}



