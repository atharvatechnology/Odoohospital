from odoo import models,api,fields,_

class HospitalUser(models.Model):
    _name = "hospital.user"
    _description = "Hospital User"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _rec_name = "first_name"


    first_name=fields.Char(string="First Name", required=True)
    last_name=fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email Address")
    age=fields.Integer(string='Age',tracking=True)
    image = fields.Binary(string="Profile Picture")
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ],required=True,default='male')
    user_type=fields.Selection([
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('pharmacy', 'Pharmacy'),
        ('receiptionist', 'Receiptionist'),

    ],required=True,default='admin')
    phone_number = fields.Char(string="Phone Number")