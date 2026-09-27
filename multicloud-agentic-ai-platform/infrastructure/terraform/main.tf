terraform { required_version = ">= 1.6.0" }
variable "environment" { type=string; default="dev" }
output "deployment_pattern" { value="Replace this demo module with Azure/AWS/GCP provider modules; keep agent app deployment separated from cloud credentials." }
