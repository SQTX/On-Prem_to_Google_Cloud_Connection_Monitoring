variable "email_address" {
  description = "The email address for notification channel"
  type        = string
}

variable "log_name" {
  description = "The log name for monitoring alert policies"
  type        = string
}

variable "credentials" {
  description = "Path to the GCP credentials JSON file"
  type        = string
}

variable "project" {
  description = "Project ID"
  type        = string
}