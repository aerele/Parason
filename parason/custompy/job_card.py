import frappe
from datetime import datetime


def before_save(self, method):
    if not self.operation_id:
        return
    doc = frappe.get_doc("Work Order Operation", self.operation_id)
    log = {
        "from_time": doc.planned_start_time,
        "to_time": doc.planned_end_time,
        "time_in_mins": doc.time_in_mins,
        "completed_qty": doc.completed_qty,
    }
    print(log)
    self.append("time_logs", log)
