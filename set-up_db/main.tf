# Set up the overall cloud platform

provider "aws" {
    region = var.REGION
    access_key = var.AWS_ACCESS_KEY_ID
    secret_key = var.AWS_SECRET_ACCESS_KEY
}

# resource [type of resource] [name for it (within terraform)]

resource "aws_db_instance" "museum-db" {
    allocated_storage            = 10
    db_name                      = "postgres"
    identifier                   = var.DB_ID
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = data.aws_db_subnet_group.public_subnet_group.name
    vpc_security_group_ids       = [aws_security_group.rds_security_group.id]
    username                     = var.DB_USERNAME
    password                     = var.DB_PASSWORD
}

resource "aws_security_group" "rds_security_group" {
  # ... other configuration ...

    name = var.SG_NAME
    description = "Allows inbound Postgres access"
    vpc_id = var.VPC_ID

    ingress {
        cidr_blocks       = ["0.0.0.0/0"]
        from_port         = 5432
        protocol          = "tcp"
        to_port           = 5432
    }
}

# Things already created

data "aws_db_subnet_group" "public_subnet_group" {
    name = "public_subnet_group"
}

data "aws_vpc" var.VPC_NAME {
    id = var.ID
}