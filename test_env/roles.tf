resource "aws_iam_policy" "iam_policy" {
  name = "${var.app_tag}_ecr"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
          Action = ["ecr:*"],
          Effect = "Allow",
          Resource = "*"
        }
    ]
    })
}

resource "aws_iam_role" "ecr_role" {
  name = "${var.app_tag}_ecr"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    "Statement": [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Sid = ""
          Principal = {
            Service = "ec2.amazonaws.com"
          }
        },
    ]
  })
  tags = {
    Name = var.app_tag
    owner = var.owner
    created = timestamp()
  }
}

resource "aws_iam_policy_attachment" "iam_attachment" {
  name   = var.app_tag
  roles = [aws_iam_role.ecr_role.name]
  policy_arn = aws_iam_policy.iam_policy.arn
}

resource "aws_iam_instance_profile" "ecr_profile" {
  name = "tom-ecr-ted_search"
  role = aws_iam_role.ecr_role.name
}