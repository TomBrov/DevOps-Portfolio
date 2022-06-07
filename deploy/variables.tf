variable "app_tag" {
  type = string
  default = "phonebook"
}

variable "region" {
  type = string
  default = "europe-central2"
}

variable "project" {
  type = string
  default = "testing-env-352509"
}

variable "sources" {
  type = string
  default = "0.0.0.0/0"
}

variable "cidr_block" {
  type = string
  default = "10.0.0.0/16"
}

variable "machine_type" {
  type = string
  default = "e2-medium"
}