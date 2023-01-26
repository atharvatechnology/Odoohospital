from odoo import models,api,fields,_


# class HospitalTest(models.Model):
#     _name = "hospital.test"
#     _description = "Hospital Test"
#     _inherit=["mail.thread", "mail.activity.mixin"]
#     name = fields.Char(string="Name")
#     price = fields.Integer(string="Price")
#     patient_id = fields.Many2one('hospital.patient',string="Patient")
#     doctor_id = fields.Many2one('hospital.doctor',string="Doctor")
#     files = fields.Binary(string="Image")
#     test_complete = fields.Boolean(string="Is Test Done?",default=False)
# from odoo import models,api,fields,_


class HospitalTest(models.Model):
    _name = "hospital.test"
    _description = "Hospital Test"
    _inherit=["mail.thread", "mail.activity.mixin"]
    name = fields.Char(string="Name")
    # price = fields.Integer(string="Price")
    patient_id = fields.Many2one('hospital.patient',string="Patient")
    doctor_id = fields.Many2one('hospital.doctor',string="Doctor")
    files = fields.Binary(string="Image")
    test_complete = fields.Boolean(string="Is Test Done?",default=False)
    currency_id = fields.Many2one(
        related="patient_id.currency_id",
        depends = ["patient_id"],
        store=True,
    )
    amount = fields.Monetary(string='Amount')
