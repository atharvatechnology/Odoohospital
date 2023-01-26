from odoo import models,api,fields,_


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _rec_name = "doctor_name"

    doctor_name=fields.Char(string="Doctor Name", required=True)
    image = fields.Binary(string="Doctor Image")
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ],required=True,default='male')
    note=fields.Text(string="Description")
    phone_number = fields.Char(string="Phone Number")
    active = fields.Boolean(string="Active", default=True)
    doctorapp_id = fields.Many2one('hospital.opd', string="Opd")
    test_id = fields.One2many('hospital.test','doctor_id',string="Test")
    qualification=fields.Selection([
        # ('highschool', 'High School'),
        # ('bachelor', 'Bachelor'),
        ('master', 'Master'),
    ],string="Qualification",required=True,default='master')

    no_of_hospital = fields.Char(string="No of Hopistal Worked In")
    employment_type=fields.Selection([
        ('parttime', 'Part Time'),
        ('fulltime', 'Full Time'),
    ],required=True,default='male',string="Employment Type")
    arrivalat = fields.Datetime('Arrival At')
    leave_at = fields.Datetime('Leave At')

    def copy(self,default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)", self.doctor_name)
        default['note']= "Copied Record"
        return super(HospitalDoctor, self).copy(default)
