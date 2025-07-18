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

# Dataset BigQuery pour les données RSS
resource "google_bigquery_dataset" "rss_dataset" {
  dataset_id    = "rss"
  friendly_name = "RSS Data Dataset"
  description   = "Dataset pour stocker les données RSS collectées"
  location      = "EU"


  
  # Labels pour organisation
  labels = {
    environnement = "dev"
    projet        = "data-rss"
    type          = "bigquery"
  }
}

# Table BigQuery pour StackOverflow RSS
resource "google_bigquery_table" "stackoverflow_r_bronze" {
  dataset_id = google_bigquery_dataset.rss_dataset.dataset_id
  table_id   = "stackoverflow_r_bronze"
  
  # Suppression des données si on détruit la table
  deletion_protection = false
  
  # Schéma de la table
  schema = jsonencode([
    {
      name = "ID"
      type = "STRING"
      mode = "REQUIRED"
      description = "ID unique de l'article RSS"
    },
    {
      name = "TITLE"
      type = "STRING"
      mode = "NULLABLE"
      description = "Titre de l'article"
    },
    {
      name = "LINK"
      type = "STRING"
      mode = "NULLABLE"
      description = "URL de l'article"
    },
    {
      name = "Published"
      type = "STRING"
      mode = "NULLABLE"
      description = "Date de publication"
    },
    {
      name = "Updated"
      type = "STRING"
      mode = "NULLABLE"
      description = "Date de mise à jour de l'article"
    },
    {
      name = "AUTHOR"
      type = "STRING"
      mode = "NULLABLE"
      description = "Auteur de l'article"
    },
    {
      name = "TAGS_LIST"
      type = "STRING"
      mode = "NULLABLE"
      description = "Tags associés à l'article"
    },
    {
      name = "Author_link"
      type = "STRING"
      mode = "NULLABLE"
      description = "Lien vers le profil de l'auteur"
    },
    {
      name = "ingestion_timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
      description = "Timestamp d'ingestion des données"
    }
  ])
  
  # Labels pour organisation
  labels = {
    environnement = "dev"
    projet        = "data-rss"
    source        = "stackoverflow"
    layer         = "bronze"
  }
}

# Outputs pour l'application Python
output "rss_bucket_name" {
  value = google_storage_bucket.rss_data_bucket.name
  description = "Nom du bucket pour les données RSS"
}

output "rss_bucket_url" {
  value = google_storage_bucket.rss_data_bucket.url
  description = "URL du bucket pour les données RSS"
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.rss_dataset.dataset_id
  description = "ID du dataset BigQuery"
}

output "bigquery_table_id" {
  value = google_bigquery_table.stackoverflow_r_bronze.table_id
  description = "ID de la table BigQuery StackOverflow"
}

output "bigquery_table_full_id" {
  value = "${var.project_id}.${google_bigquery_dataset.rss_dataset.dataset_id}.${google_bigquery_table.stackoverflow_r_bronze.table_id}"
  description = "ID complet de la table BigQuery (pour les requêtes)"
}