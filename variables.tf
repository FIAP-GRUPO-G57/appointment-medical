variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  default = "appointment-lambda-function"
}

variable "dynamodb_table_name" {
  default = "AppointmentsMedical"
}