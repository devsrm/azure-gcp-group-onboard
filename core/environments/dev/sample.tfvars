# Sample Terraform variables for dev
# Copy and adjust values for your deployment.

environment        = "dev"
location           = "eastus"
resource_group     = "rg-dev-sample"
project_name       = "group-onboard"

# Identity/group settings
group_display_name = "grp-dev-sample"
group_description  = "Sample Entra group for dev"

# Feature toggles
enable_logging     = true
enable_monitoring  = true
