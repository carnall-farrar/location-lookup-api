variable "db_password" {
  type = string
}

# variable "tag" {
#   type = string
# }

variable "log_group_name" {
  type = string
}

variable "service_name" {
  type = string
}

variable "rds_subnet_name" {
  type = string
}

variable "rds_security_group_name" {
  type = string
}

variable "task_name" {
  type = string
}

variable "db_username" {
  type = string
}

variable "dns_name" {
  type = string
}

variable "lb_name" {
  type = string
}

variable "lb_target_name" {
  type = string
}

variable "docker_registry_name" {
  type = string
}

variable "dns_zone_id" {
  type = string
}

variable "bucket_raw_data_name" {
  type = string
}

variable "bucket_output_data_name" {
  type = string
}
