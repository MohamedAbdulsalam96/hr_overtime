// Copyright (c) 2023, Dexciss Technology and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Overtime Request', {
// 	onload: function(frm) {
// 		frm.set_value("date",)

// 	}
// });

frappe.ui.form.on('Overtime Request', {
    // onload: function(frm) {
    //     var today = new Date();
    //     frm.set_value("date", frappe.datetime.get_datetime_as_string(today));
    // },
	// employee:function(frm){
	// 	frappe.call({
	// 		method:"get_approver",
	// 		doc:frm.doc,
	// 		callback:function(){
	// 			console.log("aprover sdkjfkdsjfsdjf",frm.doc.approver)
	// 			frm.refresh_field("approver")
	// 		}
	// 	})
		
	// },
	// setup: function(frm) {
	// 	frm.set_query("approver", function() {
	// 		return {
	// 			query: "hrms.hr.doctype.department_approver.department_approver.get_approvers",
	// 			filters: {
	// 				employee: frm.doc.employee,
	// 				doctype: frm.doc.doctype
	// 			}
	// 		};
	// 	});

	// 	frm.set_query("employee", erpnext.queries.employee);
	// },
});
