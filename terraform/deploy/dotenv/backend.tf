terraform {
  cloud {
    organization = "exaf-epfl"
    workspaces {
      name = "african-cities-lab-org-dotenv"
    }
  }
}
