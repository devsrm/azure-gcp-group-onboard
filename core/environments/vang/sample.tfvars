# Sample Terraform variables for vang
# Copy and adjust values for your deployment.

environment        = "vang"
location           = "westus2"
resource_group     = "rg-vang-sample"
project_name       = "group-onboard"

# Identity/group settings
group_display_name = "grp-vang-sample"
group_description  = "Sample Entra group for vang"

# Feature toggles
enable_logging     = true
enable_monitoring  = true
