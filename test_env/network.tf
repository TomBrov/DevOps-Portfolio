resource "google_compute_network" "network" {
  name = "${var.app_tag}-network"
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.app_tag}-subnet"
  network       = google_compute_network.network.id
  ip_cidr_range = var.cidr_block
  region        = var.region
  depends_on = [google_compute_network.network]
}

resource "google_compute_router" "router" {
  name    = "${var.app_tag}-router"
  region  = google_compute_subnetwork.subnet.region
  network = google_compute_network.network.id
  depends_on = [google_compute_network.network, google_compute_subnetwork.subnet]
  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = "${var.app_tag}-nat"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  depends_on = [google_compute_router.router]
  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

 resource "google_compute_firewall" "ssh" {
  name = "${var.app_tag}-firewall-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  network       = google_compute_network.network.name
  priority      = 1000
  source_ranges = [var.sources]
  target_tags   = ["vm-instance"]
  depends_on = [google_compute_network.network]
}

resource "google_compute_firewall" "application" {
  name = "${var.app_tag}-firewall-application"
  allow {
    ports    = ["${var.application}"]
    protocol = "tcp"
  }
  network       = google_compute_network.network.name
  priority      = 1000
  source_ranges = [var.sources]
  target_tags   = ["vm-instance"]
  depends_on = [google_compute_network.network]
}