resource "aws_ecr_repository" "nlca-pipelines" {
  name                 = "nlca/nlca-pipelines"
  image_tag_mutability = "MUTABLE"
}
