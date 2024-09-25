output "ecs_cluster_id" {
    value = aws_ecs_cluster.pipeline.id
}

output "ecs_service_name" {
    value = aws_ecs_service.pipeline.name
}
