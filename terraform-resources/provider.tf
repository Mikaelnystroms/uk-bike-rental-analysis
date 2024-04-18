terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.24.0"
    }
  }
}
provider "google" {
    project     = var.google_project_id
    region      = "us-central1"
    credentials = "YOUR_SERVICE_ACCOUNT_FILE"
}
