
provider "aws" {
  profile = "dev-setup-sample"
  region  = "ap-northeast-1"
}

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "771623671665-stg-test-terraform-state"
    key    = "terraform.tfstate"
    region = "ap-northeast-1"
  }
}

module "network" {
  source = "../modules/network"
}

module "ssm_parameters" {
  source = "../modules/ssm_parameters"
}
