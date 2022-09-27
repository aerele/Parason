from . import __version__ as app_version

app_name = "parason"
app_title = "Parason"
app_publisher = "Parason"
app_description = "Parason"
app_icon = "Parason"
app_color = "Parason"
app_email = "Parason"
app_license = "Parason"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/parason/css/parason.css"
# app_include_js = "/assets/parason/js/parason.js"

# include js, css files in header of web template
# web_include_css = "/assets/parason/css/parason.css"
# web_include_js = "/assets/parason/js/parason.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "parason/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

from erpnext.manufacturing.doctype.production_plan import (
    production_plan as _production_plan,
)
from parason.custompy.production_plan import (
    custom_get_sales_orders as _custom_get_sales_order
)

_production_plan.get_sales_orders = _custom_get_sales_order

from frappe.contacts.doctype.address import address as _address
from parason.custompy.address import custom_get_default_address as _custom_get_default_address
_address.get_default_address = _custom_get_default_address

# Installation
# ------------

# before_install = "parason.install.before_install"
# after_install = "parason.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "parason.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Production Plan": "parason.custompy.production_plan.CustomProductionPlan",
	"Payment Request": "parason.custompy.payment_request.CustomPaymentRequest"
# 	"ToDo": "custom_app.overrides.CustomToDo"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    # 	"*": {
    # 		"on_update": "method",
    # 		"on_cancel": "method",
    # 		"on_trash": "method"
    # 	}
    "Job Card": {"before_save": "parason.custompy.job_card.before_save"},
    "Sales Order":{
        "validate": "parason.custompy.sales_order.before_submit"
    },
    "Journal Entry":{
        "validate":"parason.custompy.journal_entry.validate"
    },
    "Purchase Order":{
        "before_submit": "parason.custompy.share_doc.share_doc"
    },
    "Delivery Note":{
        "before_submit": "parason.custompy.share_doc.share_doc"
    }
}

after_migrate = [
    "parason.update_type"
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"parason.tasks.all"
# 	],
# 	"daily": [
# 		"parason.tasks.daily"
# 	],
# 	"hourly": [
# 		"parason.tasks.hourly"
# 	],
# 	"weekly": [
# 		"parason.tasks.weekly"
# 	]
# 	"monthly": [
# 		"parason.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "parason.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    # "frappe.contacts.doctype.address.address.get_default_address":"parason.custompy.address.get_default_address",
    "erpnext.accounts.custom.address.get_shipping_address": "parason.custompy.address.get_shipping_address",
    "erpnext.setup.doctype.company.company.get_default_company_address": "parason.custompy.address.get_default_company_address"
# 	"frappe.desk.doctype.event.event.get_events": "parason.event.get_events"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "parason.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {"doctype": "{doctype_4}"},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"parason.auth.validate"
# ]
