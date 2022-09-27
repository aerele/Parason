import frappe

def share_doc(self, method):
    # if not self.for_plant:
    #     return
    # users = frappe.db.get_list("User Permission", {"allow": "Plant", "for_value": self.for_plant}, "user")
    users = frappe.db.get_list("User", "name as user")
    perms = []
    if self.doctype == "Purchase Order":
        perms = ["Purchase Manager", 'Purchase User', "Purchase Master Manager", "Purchase User Basic"]
    elif self.doctype == "Delivery Note":
        perms = ["Sales User", 'Sales Manager', "Sales Master Manager"]
    for i in users:
        if has_purchase_role(i.user, perms) and not frappe.db.get_value("DocShare", {"user": i.user,"share_doctype": self.doctype,"share_name": self.name}):
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



def has_purchase_role(user, perms):
	roles = frappe.db.sql(
		"""SELECT DISTINCT a.role FROM `tabHas Role` as a inner join `tabUser` as b on a.parent = b.name WHERE a.parent='{user}' and a.parent != 'Administrator'""".format(
			user=user
		),
		as_list=1,
	)
	return any(i[0] for i in roles if i[0] in perms)