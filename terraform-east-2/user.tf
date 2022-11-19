resource "aws_iam_user" "user_test" {
    for_each = { for user in var.users : user.username => user }
    name     = each.value.username
}

resource "aws_iam_access_key" "iam_access_key" {
    for_each = { for user in var.users : user.username => user }
    user = aws_iam_user.user_test[each.value.username].name
}

data "aws_iam_policy_document" "ec2_policy" {
    for_each = {for user in var.users : user.username => user}
    policy_id = each.value.username
    statement {
        effect = "Allow"
        sid = "VisualEditor0"
        actions = each.value.restrictions.actions
        resources = each.value.restrictions.resources
    }
}

resource "aws_iam_policy" "ec2_policy" {
    for_each = { for user in var.users : user.username => user }
    name        = each.value.restrictions.restriction_name
    policy      = data.aws_iam_policy_document.ec2_policy[each.value.username].json
}

resource "aws_iam_user_policy_attachment" "user_policy_attachment" {
    for_each = { for user in var.users : user.username => user }
    user       = aws_iam_user.user_test[each.value.username].name
    policy_arn = aws_iam_policy.ec2_policy[each.value.username].arn
}

resource "aws_iam_user_login_profile" "profile" {
    for_each                = { for user in var.users : user.username => user }
    user                    = aws_iam_user.user_test[each.value.username].name
    password_length         = 18
    password_reset_required = true
}