# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "samples"
app_title = "Frappe Ai Doc Scanner"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Ai Doc Scanner - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/samples/css/samples.bundle.css"
app_include_js = "/assets/samples/js/samples.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Ai Doc Scanner Entry": {
        "validate": "samples.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "samples.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "samples.tasks.hourly_sync"
    ],
    "daily": [
        "samples.tasks.daily_reconciliation"
    ],
    "weekly": [
        "samples.tasks.weekly_digest"
    ]
}
