import frappe
from erpnext.controllers.accounts_controller import update_child_qty_rate
import json

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
	update_child_qty_rate(parent_doctype="Purchase Order", trans_items=json.dumps([dict(
        docname = i.name,
        name = i.name,
        item_code = i.item_code,
        schedule_date = str(i.get("schedule_date")),
        conversion_factor = i.conversion_factor,
        qty = i.qty,
        rate = i.rate,
        uom = i.uom,
        __islocal = False,
        idx = i.idx
    ) for i in doc.items]), parent_doctype_name=name, child_docname="items")