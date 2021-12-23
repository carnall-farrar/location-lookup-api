terraform {
  backend "s3" {
    bucket = "carnallfarrar-terraform-state"
    key    = "location-lookup-api"
    region = "eu-west-2"
  }
}
