resource "google_compute_network" "main" {
  name                            = "${var.app_tag}-gke-network"
  routing_mode                    = "REGIONAL"
  auto_create_subnetworks         = false
  mtu                             = 1460
  delete_default_routes_on_create = false
}

resource "google_compute_subnetwork" "private" {
  name                     = "${var.app_tag}-gke-private"
  ip_cidr_range            = "10.0.0.0/18"
  region                   = var.region
  network                  = google_compute_network.main.id
  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "k8s-pod-range"
    ip_cidr_range = "10.48.0.0/14"
  }
  secondary_ip_range {
    range_name    = "k8s-service-range"
    ip_cidr_range = "10.52.0.0/20"
  }
  depends_on = [google_compute_network.main]
}

resource "google_compute_router" "router" {
  name    = "${var.app_tag}-gke-router"
  region  = google_compute_subnetwork.private.region
  network = google_compute_network.main.id
  depends_on = [google_compute_network.main, google_compute_subnetwork.private]
  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = "${var.app_tag}-gke-nat"
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

resource "google_compute_firewall" "allow-ssh" {
  name    = "${var.app_tag}-gke-allow-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  target_tags = ["cluster"]
  source_ranges = ["0.0.0.0/0"]
  depends_on = [google_compute_network.main, google_compute_subnetwork.private]
}

resource "google_compute_firewall" "allow-http" {
  name    = "${var.app_tag}-gke-allow-http"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  target_tags = ["cluster"]
  source_ranges = ["0.0.0.0/0"]
  depends_on = [google_compute_network.main, google_compute_subnetwork.private]
}