resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = merge(var.common_tags, {
    Name = "main-vpc"
  })
}

resource "aws_subnet" "subnet1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet1_cidr
  availability_zone = "us-east-1a"

  tags = merge(var.common_tags, {
    Name = "public-subnet-1"
  })
}

resource "aws_subnet" "subnet2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet2_cidr
  availability_zone = "us-east-1b"

  tags = merge(var.common_tags, {
    Name = "public-subnet-2"
  })
}