# Sample Terraform variables for prod
# Copy and adjust values for your deployment.

environment        = "prod"
location           = "eastus2"
resource_group     = "rg-prod-sample"
project_name       = "group-onboard"

# Identity/group settings
group_display_name = "grp-prod-sample"
group_description  = "Sample Entra group for prod"

# Feature toggles
enable_logging     = true
enable_monitoring  = true
