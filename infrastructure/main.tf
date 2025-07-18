# Configuration du provider Google Cloud
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

# Configuration du provider
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Variables
variable "project_id" {
  description = "ID du projet Google Cloud"
  type        = string
}

variable "region" {
  description = "Région Google Cloud"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "Zone Google Cloud"
  type        = string
  default     = "europe-west1-b"
}

# Génération d'un ID aléatoire pour éviter les conflits de noms
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Bucket pour stocker les données RSS
resource "google_storage_bucket" "rss_data_bucket" {
  name     = "data-rss-storage-${random_id.bucket_suffix.hex}"
  location = "EU"
  
  # Configuration pour données
  force_destroy = true
  
  # Versioning pour historique
  versioning {
    enabled = true
  }
  
  # Lifecycle pour gérer les coûts
  lifecycle_rule {
    condition {
      age = 90  # 90 jours
    }
    action {
      type = "Delete"
    }
  }
  
  # Labels pour organisation
  labels = {
    environnement = "dev"
    projet        = "data-rss"
    type          = "storage"
  }
}

# Output pour l'application Python
output "rss_bucket_name" {
  value = google_storage_bucket.rss_data_bucket.name
  description = "Nom du bucket pour les données RSS"
}

output "rss_bucket_url" {
  value = google_storage_bucket.rss_data_bucket.url
  description = "URL du bucket pour les données RSS"
}