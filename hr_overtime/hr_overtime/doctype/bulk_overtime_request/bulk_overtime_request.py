# Copyright (c) 2024, Dexciss Technology and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
class BulkOvertimeRequest(Document):

    @frappe.whitelist(allow_guest=True)
    def create_overtime_requests(self, employees):
        created_requests = []
        missing_approvals = []

        for emp in employees:
            print('Processing employee:', emp)
            today = self.overtime_request_date
            employee_name = emp['employee_name']
            overtime_hours = emp['hours']

            existing_request = frappe.db.exists('Overtime Request', {
                'employee': employee_name,
                'date': today
            })

            if existing_request:
                print(f"Overtime Request already exists for employee {employee_name} on {today}")
                continue

            employee_details = frappe.get_doc('Employee', employee_name)
            # approver = employee_details.leave_approver

            # if not approver:
            #     missing_approvals.append(employee_name)
            #     print(f"Approver not found for employee {employee_name}")
            #     continue

            doc = frappe.get_doc({
                'doctype': 'Overtime Request',
                'employee': employee_name,
                'date': today,
                'overtime_hours': overtime_hours,
                'select_status': self.request_type,
                'notes': self.notes,
                # 'approver': approver
            })

            doc.save(ignore_permissions=True)
            
            if self.auto_submit_ot_requests:
                doc.status = 'Approved'
                doc.submit()

            created_requests.append(doc)
            print('Created Overtime Request:', doc)

        if created_requests:
            frappe.msgprint(f"Successfully created {len(created_requests)} overtime request(s).")

        if missing_approvals:
            missing_approvals_str = ', '.join(missing_approvals)
            frappe.msgprint(f"Approval is missing for the following employees: {missing_approvals_str}")

        return created_requests
