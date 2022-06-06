resource "aws_security_group" "tom-instance-sg" {
  name = "${var.app_tag}-sg"
  description = "AWS sg for do it easy"
  vpc_id = aws_vpc.application-vpc.id

  ingress {
    description = "Allow port 80"
    from_port = var.application_port
    protocol  = "TCP"
    to_port   = var.application_port
    cidr_blocks = [var.cidr_block]
    ipv6_cidr_blocks = [var.ipv6_cidr_block]
  }

  ingress {
    description = "Allow SSH"
    from_port = 22
    protocol  = "TCP"
    to_port   = 22
    cidr_blocks = [var.cidr_block]
    ipv6_cidr_blocks = [var.ipv6_cidr_block]
  }

  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = [var.cidr_block]
    ipv6_cidr_blocks = [var.ipv6_cidr_block]
  }

  tags = {
    Name = var.app_tag
    owner = var.owner
    created = timestamp()
  }
}