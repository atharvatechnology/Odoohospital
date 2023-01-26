from odoo import models,api,fields,_


class Dashboard(models.Model):
    _name = "hospital.dashboard"
    _description = "Hospital Dashboard"
    _inherit=["mail.thread", "mail.activity.mixin"]

    # release_date = fields.Date(string="Release Date")
    patient_id = fields.Many2one('hospital.patient',string="Patient")
    test_name = fields.Many2one('hospital.test',string="Test")
    appointment = fields.Many2one('hospital.appointment',string="Appointment")
    medicine = fields.Many2one('hospital.medicine',string="Medicine")
  

