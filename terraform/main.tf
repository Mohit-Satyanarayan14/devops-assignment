terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = var.aws_region

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  skip_region_validation      = true

  s3_use_path_style           = true

  endpoints {
    ec2 = "http://host.docker.internal:4566"
    s3  = "http://host.docker.internal:4566"
  }
}
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}
module "network" {
  source = "./modules/network"

  vpc_cidr     = "10.20.0.0/16"
  subnet1_cidr = "10.20.1.0/24"
  subnet2_cidr = "10.20.2.0/24"

  common_tags = local.common_tags
}
resource "aws_security_group" "web_sg" {
  name   = "web-sg"
  vpc_id = module.network.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}
resource "aws_instance" "web1" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  subnet_id     = module.network.subnet_ids[0]

  tags = merge(local.common_tags, {
    Name = "web-1"
    Tier = "web"
  })
}

resource "aws_instance" "web2" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  subnet_id     = module.network.subnet_ids[1]

  tags = merge(local.common_tags, {
    Name = "web-2"
    Tier = "web"
  })
}
resource "aws_s3_bucket" "logs" {
  bucket = "nimbuskart-logs"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_ebs_volume" "orphan_volume" {
  availability_zone = "us-east-1a"
  size              = 10

  tags = merge(local.common_tags, {
    Name = "orphan-volume"
  })
}