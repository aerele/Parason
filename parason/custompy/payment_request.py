import frappe
from erpnext.accounts.doctype.payment_request.payment_request import PaymentRequest
from erpnext.accounts.party import get_party_account, get_party_bank_account
from erpnext.accounts.utils import get_account_currency
from frappe.utils import nowdate
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	get_company_defaults,
	get_payment_entry,
)


class CustomPaymentRequest(PaymentRequest):
	def create_payment_entry(self, submit=True):
		payment_entry = super().create_payment_entry(submit=submit)
		if payment_entry.docstatus != 1 and self.payment_type:
			payment_entry.paid_to = frappe.db.get_value("Payment Type", self.payment_type, "account") or ""
		return payment_entry