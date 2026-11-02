variable "vpc_id" {
  description = "Existing AWS VPC ID"
  type        = string
  default     = "vpc-0ba17be26d0c1ea7a"
}

variable "subnet_id" {
  description = "Existing subnet in Mumbai"
  type        = string
  default     = "subnet-06c5d71f3091dfee4"
}

variable "ssh_allowed_cidr" {
  description = "Your public IPv4 address with /32"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "AWS EC2 key pair name"
  type        = string
  default     = "shopsphere-key"
}