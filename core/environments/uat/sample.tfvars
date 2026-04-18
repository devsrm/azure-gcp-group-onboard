# Sample Terraform variables for uat
# Copy and adjust values for your deployment.

environment        = "uat"
location           = "centralus"
resource_group     = "rg-uat-sample"
project_name       = "group-onboard"

# Identity/group settings
group_display_name = "grp-uat-sample"
group_description  = "Sample Entra group for uat"

# Feature toggles
enable_logging     = true
enable_monitoring  = true
