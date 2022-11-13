# resource "aws_iam_user" "user_test" {
#   for_each = var.users
#   name     = each.value
# }

# resource "aws_iam_access_key" "iam_access_key" {
#   for_each = var.users
#   user     = aws_iam_user.user_test[each.username].name
# }

# data "aws_iam_policy_document" "ec2_policy" {
#   statement {
#     effect = "Allow"
#     sid = "VisualEditor0"
#     actions = [
#       "*"
#     ]
#     resources = [
#       "*"
#     ]
#   }
# }

# resource "aws_iam_user_login_profile" "profile" {
#   for_each                = var.users
#   user                    = aws_iam_user.user_test[each.username].name
#   #pgp_key                 = var.pgp_key
#   password_length         = 13
#   password_reset_required = true
# }