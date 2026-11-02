resource "aws_security_group" "shopsphere" {
  name        = "shopsphere-ec2-sg"
  description = "Security group for ShopSphere EC2"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from approved IP only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "shopsphere-ec2-sg"
    Project = "ShopSphere"
  }
}