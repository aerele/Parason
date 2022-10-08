import frappe

@frappe.whitelist()
def update_material_request(name):
	doc = frappe.get_doc("Purchase Order", name)
	mr_items = {}
	for i in doc.items:
		if i.item_code not in mr_items:
			mr_items[i.item_code] = None
		if not mr_items[i.item_code] and i.material_request:
			mr_items[i.item_code] = [i.material_request, i.material_request_item]
	for i in doc.items:
		if not i.material_request:
			frappe.db.set_value("Purchase Order Item", i.name, 'material_request', mr_items[i.item_code][0])
			frappe.db.set_value("Purchase Order Item", i.name, 'material_request_item', mr_items[i.item_code][1])
	doc.reload()
	doc.update_blanket_order()
	doc.update_billing_percentage()
	doc.set_status()