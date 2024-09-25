terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}

resource "aws_s3_bucket" "bronze" {
  bucket = "nlca-bronze"
}

resource "aws_s3_bucket" "silver" {
  bucket = "nlca-silver"
}

resource "aws_ecr_repository" "nlca-pipelines" {
  name = "nlca/nlca-pipelines"
  image_tag_mutability = "MUTABLE"
}

resource "aws_athena_database" "silver" {
  name   = "silver"
  bucket = aws_s3_bucket.silver.id
}

module "aws-athena" {
  source  = "Adaptavist/aws-athena/module"
  version = "1.3.3"
  create_database = false
  bucket_name = "nlca-silver"
  database_force_destroy = true
  queries = {
    "create-table": "queries/create-table.sql"
    "top-5-oil-wells": "queries/top-5-oil-wells.sql",
    "sum-prod-by-basin": "queries/sum-prod-by-basin.sql"
  }
  namespace = ""
  name = "athena"
  stage = ""
  tags = {}
}
