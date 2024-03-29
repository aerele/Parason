import frappe
from erpnext.manufacturing.doctype.production_plan.production_plan import ProductionPlan

def custom_get_sales_orders(self):
    so_filter = item_filter = ""
    bom_item = "bom.item = so_item.item_code"
    if self.for_plant:
        so_filter += " and so.set_warehouse='{0}'".format(self.for_plant)
    date_field_mapper = {
        "from_date": (">=", "so.transaction_date"),
        "to_date": ("<=", "so.transaction_date"),
        "from_delivery_date": (">=", "so_item.delivery_date"),
        "to_delivery_date": ("<=", "so_item.delivery_date"),
    }

    for field, value in date_field_mapper.items():
        if self.get(field):
            so_filter += f" and {value[1]} {value[0]} %({field})s"

    for field in ["customer", "project", "sales_order_status"]:
        if self.get(field):
            so_field = "status" if field == "sales_order_status" else field
            so_filter += f" and so.{so_field} = %({field})s"

    if self.item_code and frappe.db.exists("Item", self.item_code):
        bom_item = self.get_bom_item() or bom_item
        item_filter += " and so_item.item_code = %(item_code)s"

    open_so = frappe.db.sql(
        f"""
        select distinct so.name, so.transaction_date, so.customer, so.base_grand_total
        from `tabSales Order` so, `tabSales Order Item` so_item
        where so_item.parent = so.name
            and so.docstatus = 1 and so.status not in ("Stopped", "Closed")
            and so.company = %(company)s
            and so_item.qty > so_item.work_order_qty {so_filter} {item_filter}
            and (exists (select name from `tabBOM` bom where {bom_item}
                    and bom.is_active = 1)
                or exists (select name from `tabPacked Item` pi
                    where pi.parent = so.name and pi.parent_item = so_item.item_code
                        and exists (select name from `tabBOM` bom where bom.item=pi.item_code
                            and bom.is_active = 1)))
        """,
        self.as_dict(),
        as_dict=1,
    )

    return open_so

class CustomProductionPlan(ProductionPlan):
    def set_sub_assembly_items_based_on_level(self, row, bom_data, manufacturing_type=None):
        bom_data = sorted(bom_data, key=lambda i: i.bom_level)
        for data in bom_data:
            data.qty = data.stock_qty
            data.production_plan_item = row.name
            data.schedule_date = row.planned_start_date
            data.type_of_manufacturing = manufacturing_type or (
                "Subcontract" if data.is_sub_contracted_item else "In House"
            )
            plant = frappe.db.get_value("Warehouse", row.warehouse, "plant")
            wip_warehouse = frappe.db.get_value("Warehouse", { 'plant': plant, 'stage': 'Work in Progress'})
            data.fg_warehouse = wip_warehouse if data.type_of_manufacturing=="In House" else row.warehouse

            #self.append("sub_assembly_items", data)
