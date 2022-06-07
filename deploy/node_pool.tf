resource "google_container_node_pool" "general" {
  name       = "${var.app_tag}-general"
  cluster    = google_container_cluster.primary.id
  node_count = 1

  node_config {
    machine_type = var.machine_type
    preemptible  = true

    labels = {
      role = "general"
    }

    tags = ["cluster"]

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
