import frappe


def validate(self, method):
	if not self.voucher_type == "Cash Entry":
		return
	
	has_cash = False
	for i in self.accounts:
		if i.account and frappe.db.get_value("Account", i.account, 'account_type') == "Cash":
			has_cash = True

	if not has_cash:
		frappe.throw("Debit or Credit account type must be Cash")