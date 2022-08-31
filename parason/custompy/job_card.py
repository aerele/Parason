import frappe
from datetime import datetime
from frappe.utils import get_datetime
from dateutil.relativedelta import relativedelta
from erpnext.manufacturing.doctype.manufacturing_settings.manufacturing_settings import get_mins_between_operations

def before_save(self, method):
	if not self.operation_id:
		return
	doc = frappe.get_doc("Work Order Operation", self.operation_id)
	self.time_logs = []
	if not (doc.planned_start_time and doc.planned_end_time):
		work_order = frappe.get_doc("Work Order", doc.parent)
		for i in work_order.operations:
			if i.idx==0:
				# first operation at planned_start date
				i.planned_start_time = work_order.planned_start_date
			else:
				i.planned_start_time = get_datetime(work_order.operations[i.idx-1].planned_end_time) + get_mins_between_operations()
				i.planned_end_time = get_datetime(i.planned_start_time) + relativedelta(minutes = i.time_in_mins)
			if i.idx == doc.idx:
				doc.planned_start_time = i.planned_start_time
				doc.planned_end_time = i.planned_end_time
	log = {
		"from_time": doc.planned_start_time,
		"to_time": doc.planned_end_time,
		"time_in_mins": doc.time_in_mins,
		"completed_qty": self.for_quantity,
	}
	self.append("time_logs", log)
