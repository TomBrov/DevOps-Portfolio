resource "aws_vpc" "application-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = var.app_tag
    owner = var.owner
    created = timestamp()
  }
}

resource "aws_subnet" "application-subnet" {
  cidr_block = "10.0.0.0/28"
  vpc_id     = aws_vpc.application-vpc.id
  availability_zone = "${var.region}a"

  tags = {
    Name = var.app_tag
    owner = var.owner
    created = timestamp()
  }
}

resource "aws_internet_gateway" "application-igw" {
  vpc_id = aws_vpc.application-vpc.id

  tags = {
    Name = "${var.app_tag}-igw"
    owner = var.owner
    created = timestamp()
  }
}

resource "aws_route_table" "application-igw-route" {
  vpc_id = aws_vpc.application-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.application-igw.id
  }

  tags = {
    Name = "${var.app_tag}-igw-route"
    owner = var.owner
    created = timestamp()
  }
}

resource "aws_main_route_table_association" "application-igw-route" {
  route_table_id = aws_route_table.application-igw-route.id
  vpc_id         = aws_vpc.application-vpc.id
}