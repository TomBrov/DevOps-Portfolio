resource "google_compute_instance" "instance" {
  name         = "${var.app_tag}-instance"
  machine_type = var.machine_type
  zone         = "${var.region}-a"
  depends_on = [google_compute_router_nat.nat]
  tags = ["vm-instance"]
  metadata = {
    enable-oslogin = "FALSE"
  }
  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  metadata_startup_script = "${file("init.sh")}"

  network_interface {
    network = google_compute_network.network.id
    access_config {
    }
  }
}