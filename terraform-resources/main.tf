# resource "prefect_work_pool" "gcp-workpool" {
#   name         = "my-work-pool"
#   type         = "cloud_run:push"
#   base_job_template = file("base_job_template.json") - Review this file and edit the "GCP Credentials ID" if using terraform to create a work pool. I found it more intuitive to use the Prefect Cloud UI to create the work pool.
#   paused       = false
#   workspace_id = var.prefect_workspace_id
# }

resource "prefect_account" "my-prefect-account" {
  name                    = var.prefect_acc_name
  handle                  = var.prefect_acc_handle
  allow_public_workspaces = true
}

resource "prefect_workspace" "uk-bike-analysis" {
    name   = var.prefect_workspace_name
    handle = var.prefect_workspace_handle
}

resource "google_storage_bucket" "uk-bike-analysis" {
  name          = var.bucket_name
  location      = var.default_location
  force_destroy = true
}

resource "google_bigquery_dataset" "uk-bike-analysis-dataset" {
  dataset_id                  = var.dataset_id
  location                    = var.default_location
  default_table_expiration_ms = 3600000
}