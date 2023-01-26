from odoo import models,api,fields,_


class HospitalBill(models.Model):
    _name = "hospital.bill"
    _description = "Hospital Bill"
    _inherit=["mail.thread", "mail.activity.mixin"]

    # release_date = fields.Date(string="Release Date")
    patient_id = fields.Many2one('hospital.patient',string="Patient")
    test_name = fields.One2many('hospital.test',string="Test",related="patient_id.test_id")
    bill_number = fields.Char(string="Bill Number")
    total_amount = fields.Float(string="Total Amount",compute="_compute_total")
    medicine = fields.One2many('hospital.medicine',string="Medicine",related="patient_id.medicines")
    @api.depends()
    def _compute_total(self):
        c=0
        for rec in self:
            for j in rec.test_name:
                print(j.price)
                c+=j.price
            for k in rec.medicine:
                print(k.price)
                c+=  k.price  
            rec.total_amount=c   


class Medicine(models.Model):
    _name = "hospital.medicine"
    _description = "Hospital Medicine"
    _inherit=["mail.thread", "mail.activity.mixin"]


    image = fields.Binary(string="Medicine Image")
    name = fields.Char(string="Medicine Name")
    price = fields.Float(string="Price")
    medicine_type=fields.Selection([
        ('tablet', 'Tablet'),
        ('liquid', 'Liquid'),
        ('capsules', 'Capsules'),
        ('drops', 'Drops'),
        ('injection', 'Injection'),
    ],string="Medicine Type",required=True,default='tablet')
    patient = fields.Many2one('hospital.patient', string="Patient")
    currency_id = fields.Many2one(
        related="patient.currency_id",
        depends = ["patient"],
        store=True,
    )
    amount = fields.Monetary(string='Amount')
