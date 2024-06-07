#GCP Provider

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = "europe-central2-a"
}
