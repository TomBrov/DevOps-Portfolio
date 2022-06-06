resource "google_compute_instance" "instance" {
  name         = var.app_tag
  machine_type = var.machine_type
  zone         = "${var.region}-a"
  tags         = [var.owner]

  metadata = {
    enable-oslogin = "TRUE"
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