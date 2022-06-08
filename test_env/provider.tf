provider "google" {
  project = var.project
  region  = var.region
  zone    = "${var.region}-a"
  version = "4.23.0"
}