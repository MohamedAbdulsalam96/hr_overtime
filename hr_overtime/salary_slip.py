import frappe
from frappe.utils.data import flt


# # @frappe.whitelist()
# def overtime(self,method):
#     over=frappe.db.get_all("Overtime Request",{"employee":self.employee,"status":"Approved","docstatus":1,"date": ["between", [self.start_date, self.end_date]]},["*"])
#     grade=frappe.get_doc("Employee Grade",self.grade)
#     standard_working_hours = frappe.get_doc("HR Settings")
#     assignment=frappe.get_doc("Salary Structure Assignment",{"employee":self.employee})
#     working_hourse= self.payment_days * (standard_working_hours.standard_working_hours)
#     print("working hourse",working_hourse)
#     employe_overtime=0.0
   
#     if over:
#         for v in over:
#             employe_overtime += v.overtime_hours
#         if grade.minimum_working_hours > 0:
#             if working_hourse <= grade.minimum_working_hours:
#                 if (working_hourse - grade.minimum_working_hours) + employe_overtime > 0:
#                     self.overtime=flt(working_hourse - grade.minimum_working_hours) + employe_overtime
#                     if grade.ot_multiplier_based_on=="Gross Pay":
#                         print("calculte al value",self.gross_pay,working_hourse,grade.ot_multiplier,self.overtime)
#                         self.overtime_amount=((self.gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                     elif grade.ot_multiplier_based_on=="Net Pay":
#                         self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                     elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
                       
#                         self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*self.overtime
#                 else:
#                     self.overtime = 0.0
#             else:
#                 self.overtime = employe_overtime
#                 if grade.ot_multiplier_based_on=="Gross Pay":
#                     print("calculte al value",self.gross_pay,working_hourse,grade.ot_multiplier,self.overtime)
#                     self.overtime_amount=((self.gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                 elif grade.ot_multiplier_based_on=="Net Pay":
#                     self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                 elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
#                     self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*self.overtime
#         else:
#                 self.overtime = employe_overtime
#                 if grade.ot_multiplier_based_on=="Gross Pay":
#                     print("calculte al value",self.gross_pay,working_hourse,grade.ot_multiplier,self.overtime)
#                     self.overtime_amount=((self.gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                 elif grade.ot_multiplier_based_on=="Net Pay":
#                     self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*self.overtime
#                 elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
#                     self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*self.overtime
            
        # self.db_set("overtime",employe_overtime)

#--------------------------------------------------------------------------------------------
#mt auto


# def overtime(self,method):
#     print('new ovetime')
#     over=frappe.db.get_all("Overtime Request",{"employee":self.employee,"status":"Approved","docstatus":1,"date": ["between", [self.start_date, self.end_date]]},["*"])
#     standard_working_hours = frappe.get_doc("HR Settings")
#     or_setting = frappe.get_doc('Overtime Setting')
#     ot=frappe.get_doc("Employee",{"name":self.employee,"custom_is_overtime_employee":1})
#     assignment=frappe.get_doc("Salary Structure Assignment",{"employee":self.employee})
#     working_hourse= self.payment_days * (standard_working_hours.standard_working_hours)
#     print("working hourse",working_hourse)
#     employe_overtime=0.0
#     if over and ot:
#         for v in over:
#             employe_overtime += v.overtime_hours
#         if working_hourse <= or_setting.minimum_overtime_hour:
#             print('if ')
#             self.overtime=flt(working_hourse - or_setting.minimum_working_hours) + employe_overtime
#             if or_setting.ot_multiplier_based_on=="Gross Pay":
#                 self.overtime_amount=((self.gross_pay/working_hourse))*self.overtime
#             elif or_setting.ot_multiplier_based_on=="Net Pay":
#                 self.overtime_amount=((self.net_pay/working_hourse))*self.overtime
#             elif or_setting.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
                
#                 self.overtime_amount=((assignment.base/working_hourse))*self.overtime
#         else:
#             print('else')
#             self.overtime = employe_overtime
#             if or_setting.ot_multiplier_based_on=="Gross Pay":
#                 self.overtime_amount=((self.gross_pay/working_hourse))*self.overtime
#             elif or_setting.ot_multiplier_based_on=="Net Pay":
#                 self.overtime_amount=((self.net_pay/working_hourse))*self.overtime
#             elif or_setting.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
#                 print('37',self.overtime)
#                 self.overtime_amount=((assignment.base/working_hourse))*self.overtime


#--------------------------------------------------

@frappe.whitelist()
def overtime(self,method):
    print('gross pat--------------======',self.gross_pay)
    # g = frappe.get_doc('')


    ot_settings = frappe.get_doc("Overtime Settings")
    over=frappe.db.get_all("Overtime Request",{"employee":self.employee,"status":"Approved","docstatus":1,"date": ["between", [self.start_date, self.end_date]]},["*"])
    grade=frappe.get_doc("Employee Grade",self.grade)
    standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours')
    assignment=frappe.get_doc("Salary Structure Assignment",{"employee":self.employee})
    gross_pay = assignment.base
    print('assignment.base-------',assignment.base)
    if not standard_working_hours:
        frappe.throw('Working hours not set in HR Settings')
    working_hourse= self.total_working_days * (standard_working_hours) 
    # print("working hourse",working_hourse)
    attendance_records = frappe.get_all("Attendance", 
    filters={
        "employee": self.employee,
        "status": ["in", ["Present", "Half Day"]],
        "attendance_date": ["between", [self.start_date, self.end_date]]
    },

    fields=["status", "shift"]
)
    # print("attendance--",attendance_records)
    night_shift_hours = 0

    for record in attendance_records:
        if record.shift:
            shift = frappe.get_doc("Shift Type", record.shift)
            if shift.custom_is_night_shift == 1:
                if record.status == "Present":
                    night_shift_hours += 1
                elif record.status == "Half Day":
                    night_shift_hours += 0.5

    # print(night_shift_hours)
    self.custom_night_shift = flt(night_shift_hours)
    employe_overtime=0.0
    incentive_hours = 0.0
    print('grade.is_overtime_paid',grade.is_overtime_paid)
    print('over----',over)
    if over and grade.is_overtime_paid:
        for v in over:
            print(v.name,v.overtime_hours)
            employe_overtime += v.overtime_hours
        print('employe_overtime',employe_overtime)
        print('ot_settings.actual_max_allowed_ot',ot_settings.actual_max_allowed_ot)
        print('ot_settings.max_allowed_ot',ot_settings.max_allowed_ot)
        if employe_overtime > ot_settings.actual_max_allowed_ot:
            incentive_hours = employe_overtime - ot_settings.actual_max_allowed_ot
            employe_overtime = ot_settings.actual_max_allowed_ot
            if employe_overtime >= ot_settings.max_allowed_ot:
                ot_hours = ot_settings.max_allowed_ot
                cal_ot_hours = ot_settings.actual_max_allowed_ot
            else:
                ot_hours = ot_settings.actual_max_allowed_ot
                cal_ot_hours = ot_settings.actual_max_allowed_ot
        else:
            if employe_overtime >= ot_settings.max_allowed_ot:
                ot_hours = ot_settings.max_allowed_ot
                cal_ot_hours = employe_overtime
            else:
                ot_hours = employe_overtime
                cal_ot_hours = employe_overtime
            self.custom_incentive_hours = 0.0
        print('total ot',employe_overtime)
        if grade.minimum_working_hours > 0:
            if working_hourse <= grade.minimum_working_hours:
                if (working_hourse - grade.minimum_working_hours) + employe_overtime > 0:
                    self.overtime=flt(working_hourse - grade.minimum_working_hours) + employe_overtime
                    print(self.overtime,flt(working_hourse),(grade.minimum_working_hours),employe_overtime)
                    self.custom_incentive_hours = incentive_hours
                    if grade.ot_multiplier_based_on=="Gross Pay":
                        print("calculte al value",gross_pay,working_hourse,grade.ot_multiplier,self.overtime)
                        """OT Formula: overtime_amount=(gross_pay / total_days_of_that_month / 8)*overtime_hour"""
                        # self.overtime_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
                        self.overtime_amount=((gross_pay/self.total_working_days) / standard_working_hours)*cal_ot_hours
                        # self.custom_incentive_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                        self.custom_incentive_amount=((gross_pay/self.total_working_days) / standard_working_hours)*incentive_hours
                    elif grade.ot_multiplier_based_on=="Net Pay":
                        self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*cal_ot_hours
                        self.custom_incentive_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                    elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
                    #    
                        self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*self.overtime
                        self.custom_incentive_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*incentive_hours
                else:
                    self.overtime = 0.0
                    self.custom_incentive_hours = 0.0
            else:
                self.overtime = ot_hours
                self.custom_incentive_hours = incentive_hours
                if grade.ot_multiplier_based_on=="Gross Pay":
                    print("calculte al value",gross_pay,working_hourse,grade.ot_multiplier,cal_ot_hours)
                    """OT Formula: overtime_amount=(gross_pay / total_days_of_that_month / 8)*overtime_hour"""
                    # self.overtime_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
                    self.overtime_amount=((gross_pay/self.total_working_days) / standard_working_hours)*cal_ot_hours
                    # self.custom_incentive_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                    self.custom_incentive_amount=((gross_pay/self.total_working_days) / standard_working_hours)*incentive_hours
                elif grade.ot_multiplier_based_on=="Net Pay":
                    self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*cal_ot_hours
                    self.custom_incentive_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
                    self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*cal_ot_hours
                    self.custom_incentive_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*incentive_hours
        else:
                self.overtime = ot_hours
                self.custom_incentive_hours = incentive_hours
                if grade.ot_multiplier_based_on=="Gross Pay":
                    print("calculte al value",gross_pay,working_hourse,grade.ot_multiplier,cal_ot_hours)
                    """OT Formula: overtime_amount=(gross_pay / total_days_of_that_month / 8)*overtime_hour"""
                    # self.overtime_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*self.overtime
                    self.overtime_amount=((gross_pay/self.total_working_days) / standard_working_hours)*cal_ot_hours
                    # self.custom_incentive_amount=((gross_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                    self.custom_incentive_amount=((gross_pay/self.total_working_days) / standard_working_hours)*incentive_hours
                elif grade.ot_multiplier_based_on=="Net Pay":
                    self.overtime_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*cal_ot_hours
                    self.custom_incentive_amount=((self.net_pay/working_hourse)*grade.ot_multiplier)*incentive_hours
                elif grade.ot_multiplier_based_on=="Base (Salary Structure Assignment)":
                    self.overtime_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*cal_ot_hours
                    self.custom_incentive_amount=((assignment.base/working_hourse)*grade.ot_multiplier)*incentive_hours
            # 
        self.db_set("overtime",ot_hours)

    else:
        self.overtime = 0
        self.overtime_amount = 0
        self.custom_incentive_hours = 0
        self.custom_incentive_amount = 0