resource "google_compute_network" "network" {
  name = var.app_tag
}

resource "google_compute_subnetwork" "subnet" {
  name          = var.app_tag
  network       = google_compute_network.network.id
  ip_cidr_range = var.cidr_block
  region        = var.region
}

resource "google_compute_router" "router" {
  name    = var.app_tag
  region  = google_compute_subnetwork.subnet.region
  network = google_compute_network.network.id

  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = var.app_tag
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

 resource "google_compute_firewall" "ssh" {
  name = var.app_tag
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.network.id
  priority      = 1000
  source_ranges = [var.sources]
  target_tags   = ["ssh"]
}

 resource "google_compute_firewall" "application" {
  name    = var.app_tag
  network = google_compute_network.network.id

  allow {
    protocol = "tcp"
    ports    = ["${var.application}"]
  }
  source_ranges = [var.sources]
}