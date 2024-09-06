# Import necessary modules
from frappe.utils.data import get_time
from hrms.hr.utils import validate_active_employee, validate_dates, validate_overlap
from frappe import _
import frappe
import datetime
from datetime import datetime, timedelta, time
from frappe.utils import getdate
from hrms.hr.doctype.compensatory_leave_request.compensatory_leave_request import CompensatoryLeaveRequest



# def new_generate_overtime_request():
#     print('Starting new_generate_overtime_request')
#     ot_settings = frappe.get_doc('Overtime Settings')

#     if not ot_settings.last_sync_date:
#         frappe.throw('Last Sync Date not set in Overtime Settings')

#     if ot_settings.enable and ot_settings.last_sync_date:
#         last_sync_date = ot_settings.last_sync_date

#         if isinstance(last_sync_date, datetime.date):
#             last_sync_date_str = last_sync_date.strftime('%Y-%m-%d')
#         else:
#             last_sync_date_str = last_sync_date
        
#         today = datetime.date.today()
#         today_str = today.strftime('%Y-%m-%d')

#         print(f"Date range: {last_sync_date_str} to {today_str}")

#         attendance_list = frappe.get_all(
#             "Attendance",
#             filters={
#                 'status': ['in', ['Present','Half Day']],
#                 'attendance_date': ['between', [last_sync_date_str, today_str]],
#                 "docstatus": 1
#             },
#             fields=["name", "employee", "attendance_date", "working_hours"]
#         )

#         print(f"Filtered Attendance List: {attendance_list}")

#         standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours')

#         for emp in attendance_list:
#             print(f"Processing Attendance: {emp['name']}, Date: {emp['attendance_date']}, Employee: {emp['employee']}")

#             attendance = frappe.get_doc("Attendance", emp.name)

#             existing_request = frappe.db.exists('Overtime Request', {
#                 'employee': attendance.employee,
#                 'date': attendance.attendance_date
#             })

#             if existing_request:
#                 print(f"Overtime Request already exists for employee {attendance.employee} on {attendance.attendance_date}")
#                 continue

#             leave_approver = frappe.get_doc("Employee", attendance.employee).leave_approver
            
#             day_working_hours = attendance.working_hours
            
#             employee = frappe.get_doc("Employee", attendance.employee)
#             grade = employee.grade
#             employee_grade = frappe.get_doc("Employee Grade", grade)
#             overtime_hour = day_working_hours - standard_working_hours
#             print(day_working_hours,standard_working_hours,overtime_hour)
#             if day_working_hours > standard_working_hours and overtime_hour > employee_grade.minimum_working_hours:
#                 doc = frappe.get_doc({
#                     'doctype': 'Overtime Request',
#                     'employee': attendance.employee,
#                     'date': attendance.attendance_date,
#                     'overtime_hours': overtime_hour,
#                     "approver": leave_approver,
#                     'select_status': 'Schedule',
#                     'notes': f"Auto created based on system policy {attendance.attendance_date}"
#                 })
#                 doc.save(ignore_permissions=True)
#                 if ot_settings.submit_auto_created_ot_request == 'Yes':
#                     doc.status = 'Approved'
#                     doc.submit()
#                 print(f"Created Overtime Request: {doc.name}")

#         ot_settings.last_sync_date = today
#         ot_settings.save(ignore_permissions=True)

#         print("Last Sync Date updated to today's date")
#     else:
#         frappe.throw('Last Sync Date not set in Overtime Settings')


import frappe
import datetime

# def new_generate_overtime_request():
#     print('Starting new_generate_overtime_request')
#     ot_settings = frappe.get_doc('Overtime Settings')

#     if not ot_settings.last_sync_date:
#         frappe.throw('Last Sync Date not set in Overtime Settings')

#     if ot_settings.enable and ot_settings.last_sync_date:
#         last_sync_date = ot_settings.last_sync_date

#         if isinstance(last_sync_date, datetime.date):
#             last_sync_date_str = last_sync_date.strftime('%Y-%m-%d')
#         else:
#             last_sync_date_str = last_sync_date
        
#         today = datetime.date.today()
#         today_str = today.strftime('%Y-%m-%d')

#         print(f"Date range: {last_sync_date_str} to {today_str}")

#         attendance_list = frappe.get_all(
#             "Attendance",
#             filters={
#                 'status': ['in', ['Present', 'Half Day']],
#                 'attendance_date': ['between', [last_sync_date_str, today_str]],
#                 "docstatus": 1
#             },
#             fields=["name", "employee", "attendance_date", "working_hours"]
#         )

#         print(f"Filtered Attendance List: {attendance_list}")

#         standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours')
#         missing_approvals = []

#         for emp in attendance_list:
#             try:
#                 print(f"Processing Attendance: {emp['name']}, Date: {emp['attendance_date']}, Employee: {emp['employee']}")

#                 attendance = frappe.get_doc("Attendance", emp.name)

#                 existing_request = frappe.db.exists('Overtime Request', {
#                     'employee': attendance.employee,
#                     'date': attendance.attendance_date
#                 })

#                 if existing_request:
#                     print(f"Overtime Request already exists for employee {attendance.employee} on {attendance.attendance_date}")
#                     continue

#                 # leave_approver = frappe.get_value("Employee", attendance.employee, "leave_approver")

#                 # if not leave_approver:
#                 #     missing_approvals.append(attendance.employee)
#                 #     print(f"Approver not found for employee {attendance.employee}")
#                 #     traceback = frappe.get_traceback()
#                 #     frappe.log_error(title=f"Approver not found for employee {attendance.employee}", message=traceback)
#                 #     continue

#                 day_working_hours = attendance.working_hours

#                 employee = frappe.get_doc("Employee", attendance.employee)
#                 grade = employee.grade
#                 employee_grade = frappe.get_doc("Employee Grade", grade)
#                 overtime_hour = day_working_hours - standard_working_hours
#                 print(day_working_hours, standard_working_hours, overtime_hour)



#                 in_time = attendance.in_time
#                 print("in_time:", in_time, "Type:", type(in_time))

#                 shift = frappe.get_doc('Shift Type', attendance.shift)
#                 print("shift.start_time:", shift.start_time, "Type:", type(shift.start_time))

#                 if employee.custom_is_early_ot_allowed:
#                     print('if--')
#                     if day_working_hours > standard_working_hours and overtime_hour > employee_grade.minimum_working_hours:
#                         doc = frappe.get_doc({
#                             'doctype': 'Overtime Request',
#                             'employee': attendance.employee,
#                             'date': attendance.attendance_date,
#                             'overtime_hours': overtime_hour,
#                             # "approver": leave_approver,
#                             'select_status': 'Schedule',
#                             'notes': f"Auto created based on system policy {attendance.attendance_date}"
#                         })
#                         doc.save(ignore_permissions=True)
                        
#                         if ot_settings.submit_auto_created_ot_request == 'Yes':
#                             doc.status = 'Approved'
#                             doc.submit()
                        
#                         print(f"Created Overtime Request: {doc.name}")


#                 elif get_time(in_time) >= get_time(shift.start_time):
#                     t = attendance.out_time.time()            # This is 21:00:57

#                     # Convert the time object to a timedelta object
#                     t_as_timedelta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
#                     print('elif---------')
#                     print('yes---------',(emp.name,shift.name,shift.start_time,attendance.out_time.time(), round(abs(shift.start_time-t_as_timedelta).total_seconds() /3600, 2)))


#                     if day_working_hours > standard_working_hours and overtime_hour > employee_grade.minimum_working_hours:
#                         doc = frappe.get_doc({
#                             'doctype': 'Overtime Request',
#                             'employee': attendance.employee,
#                             'date': attendance.attendance_date,
#                             'overtime_hours': overtime_hour,
#                             # "approver": leave_approver,
#                             'select_status': 'Schedule',
#                             'notes': f"Auto created based on system policy {attendance.attendance_date}"
#                         })
#                         doc.save(ignore_permissions=True)
                        
#                         if ot_settings.submit_auto_created_ot_request == 'Yes':
#                             doc.status = 'Approved'
#                             doc.submit()
                        
#                         print(f"Created Overtime Request: {doc.name}")

#                 else:

#                     t = attendance.out_time.time()            # This is 21:00:57

#                     # Convert the time object to a timedelta object
#                     t_as_timedelta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
#                     day_working_hours = round(abs(shift.start_time-t_as_timedelta).total_seconds() /3600, 2)
#                     print('else-----',day_working_hours)   
#                     overtime_hour = day_working_hours - standard_working_hours
#                     if day_working_hours > standard_working_hours and overtime_hour > employee_grade.minimum_working_hours:
#                         doc = frappe.get_doc({
#                             'doctype': 'Overtime Request',
#                             'employee': attendance.employee,
#                             'date': attendance.attendance_date,
#                             'overtime_hours': overtime_hour,
#                             # "approver": leave_approver,
#                             'select_status': 'Schedule',
#                             'notes': f"Auto created based on system policy {attendance.attendance_date}"
#                         })
#                         doc.save(ignore_permissions=True)
                        
#                         if ot_settings.submit_auto_created_ot_request == 'Yes':
#                             doc.status = 'Approved'
#                             doc.submit()
                        
#                         print(f"Created Overtime Request: {doc.name}")


                
#             except Exception as e:
#                 traceback = frappe.get_traceback()
#                 frappe.log_error(title='Overtime Request Creation Error', message=traceback)

#         ot_settings.last_sync_date = today
#         ot_settings.save(ignore_permissions=True)

#         print("Last Sync Date updated to today's date")
#     else:
#         frappe.throw('Last Sync Date not set in Overtime Settings')






#------------------running fast code below \/.




import datetime
from datetime import timedelta
from frappe.utils import getdate, today, get_datetime, time_diff_in_hours

def check_employee_checkins_and_calculate_hours(last_syn_date):
    print(last_syn_date)
    ot_settings = frappe.get_doc('Overtime Settings')
    try:
        doc = frappe.get_all('Employee',{'status':'Active'},pluck='name')
        # print(doc)
        for employee_id in doc:
            print(employee_id)
            emp = frappe.get_doc('Employee', employee_id)
            if emp.holiday_list:
                holidays_list = [x.holiday_date for x in frappe.get_doc('Holiday List', emp.holiday_list).holidays]
                # print(holidays_list)
                today_date = getdate(today())
                
                working_hours = {}
                for holiday in holidays_list:
                    # print('holiday----',holiday)
                    if getdate(last_syn_date) <= getdate(holiday) <= getdate(today_date):
                        checkins_on_holiday = frappe.get_all('Employee Checkin', 
                                                            filters={
                                                                'employee': employee_id,
                                                                'log_type': 'IN',
                                                                'time': ['between', [str(holiday) + ' 00:00:00', str(holiday) + ' 23:59:59']]
                                                            },
                                                            fields=['name', 'time'])
                        
                        checkouts_on_holiday = frappe.get_all('Employee Checkin', 
                                                            filters={
                                                                'employee': employee_id,
                                                                'log_type': 'OUT',
                                                                'time': ['between', [str(holiday) + ' 00:00:00', str(holiday) + ' 23:59:59']]
                                                            },
                                                            fields=['name', 'time'])

                        if checkins_on_holiday and checkouts_on_holiday:
                            for checkin in checkins_on_holiday:
                                checkin_time = get_datetime(checkin['time'])
                                checkout_time = None
                                for checkout in checkouts_on_holiday:
                                    if getdate(checkout['time']) == getdate(checkin_time):
                                        checkout_time = get_datetime(checkout['time'])
                                        break
                                if checkout_time:
                                    print(checkout_time,checkin_time)
                                    hours_worked = abs(time_diff_in_hours(checkout_time, checkin_time))
                                    working_hours[str(holiday)] = working_hours.get(str(holiday), 0) + hours_worked
                                    existing_request = frappe.db.exists('Overtime Request', {
                                        'employee': employee_id,
                                        'date': getdate(holiday)
                                    })

                                    if existing_request:
                                        print(f"Overtime Request already exists for employee {employee_id} on {holiday}")
                                        continue
                                    create_overtime_request_on_holiday(employee_id,getdate(holiday),hours_worked)
                                    print(f"Employee {employee_id} worked {hours_worked} hours on holiday {holiday}.")
                                else:
                                    print(f"Employee {employee_id} checked in on holiday {holiday} but did not check out.")
                        else:
                            print(f"Employee {employee_id} has no complete check-in/out records on holiday {holiday}.")
                ot_settings.last_sync_date = today_date

                ot_settings.save(ignore_permissions=True)
                print('working_hours- checkin out --',working_hours)
                # return working_hours

    except Exception as e:
        frappe.log_error(f"Error in check_employee_checkins_and_calculate_hours: {str(e)}", "Employee Checkin Error")
        print(f"An error occurred: {str(e)}")
        # return {}
    ot_settings.last_sync_date_holday = today_date

    ot_settings.save(ignore_permissions=True)




def new_generate_overtime_request():
    print('Starting new_generate_overtime_request')
    ot_settings = frappe.get_doc('Overtime Settings')

    if not ot_settings.last_sync_date:
        frappe.throw('Last Sync Date not set in Overtime Settings')

    if ot_settings.enable and ot_settings.last_sync_date:
        last_sync_date = ot_settings.last_sync_date

        if isinstance(last_sync_date, datetime.date):
            last_sync_date_str = last_sync_date.strftime('%Y-%m-%d')
        else:
            last_sync_date_str = last_sync_date
        
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')

        print(f"Date range: {last_sync_date_str} to {today_str}")

        standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours')

        query = """
            SELECT 
                att.name AS attendance_name, 
                att.employee, 
                att.attendance_date, 
                att.working_hours, 
                att.in_time, 
                att.out_time, 
                att.shift, 
                emp.grade, 
                emp.holiday_list,
                emp.custom_is_early_ot_allowed, 
                emp.custom_is_overtime_employee,
                grd.minimum_working_hours,
                shift.start_time AS shift_start_time
            FROM 
                `tabAttendance` AS att
            JOIN 
                `tabEmployee` AS emp ON att.employee = emp.name
            JOIN 
                `tabEmployee Grade` AS grd ON emp.grade = grd.name
            JOIN 
                `tabShift Type` AS shift ON att.shift = shift.name
            WHERE 
                att.status IN ('Present', 'Half Day')
                AND att.attendance_date BETWEEN %(last_sync_date)s AND %(today)s
                AND att.docstatus = 1
                AND emp.custom_is_overtime_employee = 1
                AND emp.status = 'Active'
        """
        
        attendance_list = frappe.db.sql(query, {'last_sync_date': last_sync_date_str, 'today': today_str}, as_dict=True)

        # print(f"Filtered Attendance List: {attendance_list}")
        for emp in attendance_list:
            try:
                print(f"Processing Attendance: {emp['attendance_name']}, Date: {emp['attendance_date']}, Employee: {emp['employee']}")

                existing_request = frappe.db.exists('Overtime Request', {
                    'employee': emp['employee'],
                    'date': emp['attendance_date']
                })

                if existing_request:
                    print(f"Overtime Request already exists for employee {emp['employee']} on {emp['attendance_date']}")
                    continue

                day_working_hours = emp['working_hours']
                overtime_hour = day_working_hours - standard_working_hours
                print(day_working_hours, standard_working_hours, overtime_hour)

                in_time = emp['in_time']
                print("in_time:", in_time, "Type:", type(in_time))

                shift_start_time = emp['shift_start_time']
                print("shift.start_time:", shift_start_time, "Type:", type(shift_start_time))
                if emp['in_time'] and emp['out_time']:
                    if emp['custom_is_early_ot_allowed']:
                        print('if--')
                        if day_working_hours > standard_working_hours and overtime_hour > emp['minimum_working_hours']:
                            create_overtime_request(emp, overtime_hour, ot_settings)
                    elif get_time(in_time) >= get_time(shift_start_time):
                        t = emp['out_time'].time()
                        t_as_timedelta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
                        print('elif---------')
                        print('yes---------', (emp['attendance_name'], shift_start_time, emp['out_time'].time(), round(abs(shift_start_time - t_as_timedelta).total_seconds() / 3600, 2)))
                        if day_working_hours > standard_working_hours and overtime_hour > emp['minimum_working_hours']:
                            create_overtime_request(emp, overtime_hour, ot_settings)
                    else:
                        t = emp['out_time'].time()
                        t_as_timedelta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
                        day_working_hours = round(abs(shift_start_time - t_as_timedelta).total_seconds() / 3600, 2)
                        print('else-----', day_working_hours)
                        overtime_hour = day_working_hours - standard_working_hours
                        if day_working_hours > standard_working_hours and overtime_hour > emp['minimum_working_hours']:
                            create_overtime_request(emp, overtime_hour, ot_settings)
            except Exception as e:
                traceback = frappe.get_traceback()
                frappe.log_error(title='Overtime Request Creation Error', message=traceback)

        ot_settings.last_sync_date = today
        ot_settings.save(ignore_permissions=True)

        print("Last Sync Date updated to today's date")
    else:
        frappe.throw('Last Sync Date not set in Overtime Settings')

def create_overtime_request(emp, overtime_hour, ot_settings):
    doc = frappe.get_doc({
        'doctype': 'Overtime Request',
        'employee': emp['employee'],
        'date': emp['attendance_date'],
        'overtime_hours': overtime_hour,
        'select_status': 'Schedule',
        'notes': f"Auto created based on system policy {emp['attendance_date']}"
    })
    doc.save(ignore_permissions=True)
    if ot_settings.submit_auto_created_ot_request == 'Yes':
        doc.status = 'Approved'
        doc.submit()
    print(f"Created Overtime Request: {doc.name}")

def create_overtime_request_on_holiday(employee,date,overtime_hour):
    ot_settings = frappe.get_doc('Overtime Settings')
    doc = frappe.get_doc({
        'doctype': 'Overtime Request',
        'employee': employee,
        'date': date,
        'overtime_hours': overtime_hour,
        'select_status': 'Schedule',
        'notes': f"Auto created based on system policy {date} (Holiday)"
    })
    doc.save(ignore_permissions=True)
    if ot_settings.submit_auto_created_ot_request_holiday == 'Yes':
        doc.status = 'Approved'
        doc.submit()
    print(f"Created Overtime Request: {doc.name}")



def overtime_request_on_holiday():

    ot_settings = frappe.get_doc('Overtime Settings')
    if ot_settings.apply_ot_on_holiday:
        check_employee_checkins_and_calculate_hours(getdate(ot_settings.last_sync_date_holday))