terraform {
  required_providers {
    prefect = {
      source = "PrefectHQ/prefect"
      version = "0.1.2"
    }
    google = {
      source = "hashicorp/google"
      version = "5.24.0"
    }
  }
}

provider "prefect" {
  api_key    = var.prefect_api_key
  account_id = var.prefect_account_id
}

provider "google" {
    project     = var.google_project_id
    region      = "us-central1"
}
