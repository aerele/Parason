import frappe
__version__ = '0.0.1'

def update_type():
	payment_type = frappe.db.get_value("DocField", {"parent":"Payment Entry", "fieldname":"payment_type"}, "options")
	payment_type = [i.strip() for i in payment_type.split('\n')]
	create_type("Payment Entry Type", "payment_entry_type", payment_type)

	jv_type = frappe.db.get_value("DocField", {"parent":"Journal Entry", "fieldname":"voucher_type"}, "options")
	jv_type = [i.strip() for i in jv_type.split('\n')]
	create_type("Journal Entry Type", "journal_entry_type", jv_type)

def create_type(doctype,fieldname,  types):
	for i in types:
		if frappe.db.get_value(doctype, i):
			continue
		doc = frappe.new_doc(doctype)
		setattr(doc, fieldname, i)
		doc.save()