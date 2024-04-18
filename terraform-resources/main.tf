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