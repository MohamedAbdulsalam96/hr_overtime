# Copyright (c) 2023, Dexciss Technology and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hrms.hr.utils import get_holiday_dates_for_employee
from hrms.hr.doctype.leave_application.leave_application import get_leave_approver
class OvertimeRequest(Document):

	def before_submit(self):
		if self.status not in ['Approved', 'Rejected']:
			frappe.throw(("Only OT Requests with status 'Approved' or 'Rejected' can be submitted."))
	


	# def before_submit(self):
	# 	absent=frappe.get_doc("Attendance",{"attendance_date":self.date})
	# 	if absent:
	# 		if absent.status == "On Leave" or absent.status == "Absent":
	# 			frappe.throw(f"'{self.employee}' is not present date:'{self.date}'")

	# 	if self.approver != frappe.session.user:
	# 		frappe.throw(f"Could not find Approver: {self.employee}")


	# @frappe.whitelist()
	# def get_approver(self):
	# 	if self.employee:
	# 		print("======employee",self.employee)
	# 		self.approver=get_leave_approver(employee=self.employee)
	# 		# return approver
	# 		# self.db_get("approver",app)
	# 		print("======employee2222222222222",self.employee,frappe.session.user)
			
	

