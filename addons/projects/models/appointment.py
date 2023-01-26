from odoo import models,api,fields,_
from odoo.exceptions import ValidationError
# from .patient import HospitalPatient

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit=["mail.thread", "mail.activity.mixin"]


    name=fields.Char(string="Name", required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", help="This will allow you to create patient")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    age=fields.Integer(string='Age',tracking=True,related="patient_id.age")
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ],required=True,default='male')
    note=fields.Text(string="Description")
    state=fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ],required=True,default='cancel',string="Status")
    date_appointment = fields.Datetime(string="Appointment Time",default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date",default=fields.Date.context_today)
    date_checkup = fields.Datetime(string="Check Up Time")
    prescription=fields.Html(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.lines','appointment_id',string="Prescription Lines")
    is_appointment = fields.Boolean(string="Is Appointment Submitted?",default=False)
    problem = fields.Text(string="Patient Problem",related="patient_id.problem")
    priority = fields.Selection([
        ('0','Normal'),
        ('1','Low'),
        ('2','High'),
        ('3','Very High')],string="Priority")
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    userid = fields.Char("Patient",default=lambda self: self.env.user.name)
    # @api.depends('patient_id')
    # def _get_current_user(self):
    #     print(self.env.uid)
        # print('user',self.patient_id)


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == "draft":
                progress = 25
            elif rec.state == "in_consultation":
                progress = 50
            elif rec.state == "done":
                progress = 100
            else:
                progress = 0
            rec.progress = progress
        # context = self._context
        # # print('userid',userid)
        # current_uid = context.get('uid')


        # user = self.env['res.users'].browse(current_uid)
        # print('user',current_uid)

    def action_consultation(self):
        for rec in self:
           rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
           rec.state = "done"

    def action_draft(self):
        for rec in self:
           rec.state = "draft"

    def action_cancel(self):
        for rec in self:
           rec.state = "cancel"

    @api.model
    def create(self,vals):
        if not vals.get('note'):
            vals['note']="New Patient"
        res = super(HospitalAppointment, self).create(vals)
        res.state="draft"
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender


    def unlink(self):
        if self.state == "done":
            raise ValidationError(_("You Cannot Delete %s as it is in Done State" % self.name))
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.youtube.com/watch?v=7jbaJSZLL8A&list=PLqRRLx0cl0homY1elJbSoWfeQbRKJ-oPO&index=54',
        }

class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name=fields.Char(string="Medicine")
    qty=fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
