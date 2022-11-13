output "password" {
    value = { for user_test, profile in aws_iam_user_login_profile.profile : user_test => profile.password }
}