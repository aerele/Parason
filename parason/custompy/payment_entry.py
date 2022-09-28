import frappe

@frappe.whitelist()
def get_customer_advance_account(customer, company):
    return frappe.db.get_value("Party Account", {'parent': customer, "company":company}, "account_for_advance") or None


