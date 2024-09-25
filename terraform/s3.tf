resource "aws_s3_bucket" "bronze" {
  bucket = "nlca-bronze"
}

resource "aws_s3_bucket" "silver" {
  bucket = "nlca-silver"
}
