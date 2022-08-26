
import frappe
from erpnext.controllers.accounts_controller import update_child_qty_rate


def before_submit(self, method):
	self.update_items = []