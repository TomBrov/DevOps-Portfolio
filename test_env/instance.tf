resource "aws_instance" "instance" {
  ami = var.ami_id
  instance_type = var.instance_type
  associate_public_ip_address = var.associate_public_ip_address
  subnet_id = aws_subnet.application-subnet.id
  key_name = var.key_name
  iam_instance_profile = aws_iam_instance_profile.ecr_profile.name
  user_data = "${file("init.sh")}"
  vpc_security_group_ids = [
    aws_security_group.tom-instance-sg.id
  ]
  tags = {
    Name = var.app_tag
    owner = var.owner
    created = timestamp()
  }
}



