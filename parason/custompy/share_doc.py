import frappe

def share_doc(self, method):
    if not self.for_plant:
        return
    users = frappe.db.get_list("User Permission", {"allow": "Plant", "for_value": self.for_plant}, "user")
    for i in users:
        if frappe.has_permission(self.doctype, 'read', user=i.user) and not frappe.db.get_value("DocShare", {"user": i.user,"share_doctype": self.doctype,"share_name": self.name}):
            doct = {
                "user": i.user,
                "share_doctype": self.doctype,
                "share_name": self.name,
                "read": 1,
                "write": 1,
                "share": 1,
                "submit": 0,
                "everyone": 0,
                "notify_by_email": 1,
                "doctype": "DocShare"
            }
            frappe.get_doc(doct).insert(ignore_permissions=True)