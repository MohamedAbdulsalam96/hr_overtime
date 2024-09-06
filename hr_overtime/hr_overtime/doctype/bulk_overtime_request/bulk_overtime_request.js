// Copyright (c) 2024, Dexciss Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Overtime Request", {
	refresh(frm) {
		frm.set_df_property("filters_section", "hidden", 1);
		frm.trigger('set_options');
		frm.trigger('render_filters_table');
        frm.add_custom_button(__('Create Overtime Request'), () => {
            frm.trigger('create_overtime_request');
        });
        frm.custom_buttons = true;

		frm.disable_save();

	},

    set_options: function(frm) {
		let aggregate_based_on_fields = [];
		const doctype = 'Employee';

		if (doctype) {
			frappe.model.with_doctype(doctype, () => {
				frappe.get_meta(doctype).fields.map(df => {
					if (frappe.model.numeric_fieldtypes.includes(df.fieldtype)) {
						if (df.fieldtype == 'Currency') {
							if (!df.options || df.options !== 'Company:company:default_currency') {
								return;
							}
						}
						aggregate_based_on_fields.push({label: df.label, value: df.fieldname});
					}
				});

				frm.set_df_property('aggregate_function_based_on', 'options', aggregate_based_on_fields);
			});
		}
	},

	render_filters_table: function(frm) {
		frm.set_df_property("filters_section", "hidden", 0);

		let wrapper = $(frm.get_field('filter_contact').wrapper).empty();
		frm.filter_table = $(`<table class="table table-bordered" style="cursor:pointer; margin:0px;">
			<thead>
				<tr>
					<th style="width: 33%">${__('Filter')}</th>
					<th style="width: 33%">${__('Condition')}</th>
					<th>${__('Value')}</th>
				</tr>
			</thead>
			<tbody></tbody>
		</table>`).appendTo(wrapper);
		$(`<p class="text-muted small">${__("Click table to edit")}</p>`).appendTo(wrapper);


		frm.filters = JSON.parse(frm.doc.filter_contact || '[]');

		frm.trigger('set_filters_in_table');

		frm.filter_table.on('click', () => {
			let dialog = new frappe.ui.Dialog({
				title: __('Set Filters'),
				fields: [{
					fieldtype: 'HTML',
					fieldname: 'filter_area',
				}],
				primary_action: function() {
					let values = this.get_values();
					if (values) {
						this.hide();
						frm.filters = frm.filter_group.get_filters();
						frm.set_value('filter_contact', JSON.stringify(frm.filters));
						frm.trigger('set_filters_in_table');
					}
				},
				primary_action_label: "Set"
			});

			frappe.dashboards.filters_dialog = dialog;

			frm.filter_group = new frappe.ui.FilterGroup({
				parent: dialog.get_field('filter_area').$wrapper,
				doctype: 'Employee',
				on_change: () => {},
			});

			frm.filter_group.add_filters_to_filter_group(frm.filters);

			dialog.show();
			dialog.set_values(frm.filters);
		});

	},

	set_filters_in_table: function(frm) {

        console.log("Current Filters: ", frm.filters);
		if (!frm.filters.length) {
			const filter_row = $(`<tr><td colspan="3" class="text-muted text-center">
				${__("Click to Set Filters")}</td></tr>`);
			frm.filter_table.find('tbody').html(filter_row);
		} else {
			let filter_rows = '';
			frm.filters.forEach(filter => {
				filter_rows +=
					`<tr>
						<td>${filter[1]}</td>
						<td>${filter[2] || ""}</td>
						<td>${filter[3]}</td>
					</tr>`;

			});
			frm.filter_table.find('tbody').html(filter_rows);
		}
	},

    fetch: async function(frm) {
        // for (let i=0 ;i<10;i++){
        //     console.log("loop running",i)
        //     frm.add_child("employee_ovetime_hours",{
               
        //     })
        // }
        // frm.refresh_field("employee_ovetime_hours")
        // return
        let data 
        if (frm.filters.length) {
            await frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Employee',
                    filters: frm.filters,
                    fields: ['*']
                },
                freeze:true,
                callback: function(r) {
                    if (r.message) {
                        console.log("Fetched Records: ", r.message[0].name);
                        frm.clear_table('employee_overtime_hours');
                        r.message.forEach(employee => {
                            console.log("for each",employee)
                            frm.add_child('employee_overtime_hours',{
                                'employee':employee.name,
                                'employee_name':employee.employee_name
                            });
                        });
                        
                    } else {
                        console.log("No records found");
                    }
                }
            });
            frm.refresh_field('employee_overtime_hours')
        } else {
            console.log("No filters set");
        }
    },


	create_overtime_request: function(frm) {
		let employees = frm.doc.employee_overtime_hours
			.filter(row => row.hours > 0)
			.map(row => ({
				employee_name: row.employee,
				hours: row.hours,
			}));
	
		console.log("Filtered Employees and hours: ", employees);
	
		if (employees.length > 0) {
			frappe.call({
				method: 'create_overtime_requests',
				doc:frm.doc,
				args: {
					employees: employees
				},
				callback: function(response) {
					console.log("API Response: ", response);
					if (response){
						console.log('response')
						// frappe.msgprint({
						// 	title: ('Notification'),
						// 	indicator: 'green',
						// 	message:('Overtime Request Created for the Employees')
						// });
					}
				}
			});
		} else {
			console.log("No valid employee hours to submit.");
			frappe.msgprint(__('Please ensure that there are employee entries with hours greater than 0.'));
		}
	}
	

});



