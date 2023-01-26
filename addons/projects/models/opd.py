from odoo import models,api,fields,_

class HospitalOpd(models.Model):
    _name = "hospital.opd"
    _description = "Hospital Opd"
    _inherit=["mail.thread", "mail.activity.mixin"]
    # patient_ids = fields.One2many('hospital.patient', 'patientapp_id',string="Patient")
    # doctor_ids = fields.One2many('hospital.doctor', 'doctorapp_id',string="Doctor")
    name=fields.Char(string="Name", required=True)
    location=fields.Char(string="Location", required=True)
    patient_count = fields.Integer(string="Patient Count", compute="_compute_patient_count")

    number = fields.Integer(string="Number")
    phone_number = fields.Char(string="Phone Number")

    def _compute_patient_count(self):
        # for lop ma rakhnu ko karan chai singleton error aucha vanera
        for rec in self:
            patient_count = self.env['hospital.patient'].search_count([('department_id', '=', rec.id)])
            print(patient_count)
            rec.patient_count = patient_count
    
    def action_open_patient(self):
        print('hvhgvhj')