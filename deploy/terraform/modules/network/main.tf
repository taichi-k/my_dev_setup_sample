resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    "Name" = "test-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.this.id
  tags = {
    "Name" = "igw"
  }
}

resource "aws_subnet" "public1" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.0.0/20"
  tags = {
    "Name" = "subnet-public1-ap-northeast-1a"
  }
}

resource "aws_subnet" "public2" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.16.0/20"
  tags = {
    "Name" = "subnet-public2-ap-northeast-1c"
  }
}

resource "aws_subnet" "private1" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.128.0/20"
  tags = {
    "Name" = "subnet-private1-app-ap-northeast-1a"
  }
}

resource "aws_subnet" "private2" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.144.0/20"
  tags = {
    "Name" = "subnet-private2-app-ap-northeast-1c"
  }
}

resource "aws_subnet" "private3" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.160.0/20"
  tags = {
    "Name" = "subnet-private3-db-ap-northeast-1a"
  }
}

resource "aws_subnet" "private4" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.176.0/20"
  tags = {
    "Name" = "subnet-private4-db-ap-northeast-1c"
  }
}
