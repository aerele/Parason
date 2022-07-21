import frappe
import functools

@frappe.whitelist()
def custom_get_default_address(doctype, name, sort_key='is_primary_address'):
	print("custom")
	'''Returns default Address name for the given doctype, name'''
	if sort_key not in ['is_shipping_address', 'is_primary_address']:
		return None
	if doctype == "Company":
		return None

	out = frappe.db.sql(""" SELECT
			addr.name, addr.%s
		FROM
			`tabAddress` addr, `tabDynamic Link` dl
		WHERE
			dl.parent = addr.name and dl.link_doctype = %s and
			dl.link_name = %s and ifnull(addr.disabled, 0) = 0
		""" %(sort_key, '%s', '%s'), (doctype, name))

	if out:
		return sorted(out, key = functools.cmp_to_key(lambda x,y: cmp(y[1], x[1])))[0][0]
	else:
		return None