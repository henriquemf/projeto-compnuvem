output "password" {
    value = { for user_test, profile in aws_iam_user_login_profile.profile : user_test => profile.password }
}

output "lb_endpoint" {
  value = "http://${aws_lb.terramino.dns_name}"
}

output "asg_name" {
  value = aws_autoscaling_group.terramino.name
}