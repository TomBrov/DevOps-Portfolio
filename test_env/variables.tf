variable "ami_id" {
  type = string
  default = "ami-00e7df8df28dfa791"
}

variable "instance_type" {
  type = string
  default = "t2.micro"
}

variable "key_name" {
  type = string
  default = "tom_ireland"
}

variable "app_tag" {
  type = string
  default = "phonebook-testing"
}

variable "application_port" {
  type = number
  default = 80
}

variable "region" {
  type = string
  default = "eu-west-1"
}

variable "cidr_block" {
  type = string
  default = "0.0.0.0/0"
}

variable "ipv6_cidr_block" {
  type = string
  default = "::/0"
}

variable "owner" {
  type = string
  default = "Brov"
}

variable "associate_public_ip_address" {
  type = bool
  default = true
}