from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _order = "id desc"
    
    name=fields.Char(string="Name", required=True)
    reference = fields.Char(string="Order Reference", required="True",copy=False,
                                    default=lambda self: _('New'))
    age=fields.Integer(string='Age',tracking=True)
    image = fields.Binary(string="Patient Image")
    email = fields.Char(string="Email Address")
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ],required=True,default='male')
    patient_type=fields.Selection([
        ('in_patient', 'In Patient'),
        ('out_patient', 'Out Patient'),
        ('emergency_patient', 'Emergency Patient'),
    ],string="Patient Type",required=True,default='out_patient')
    occupation=fields.Text(string="Occupation")
    address=fields.Text(string="Address")
    followup = fields.Datetime(string="Follow up")
    responsible_id = fields.Many2one('res.partner', string="Partner")
    phone = fields.Char(string="Phone Number")
    website = fields.Char(string="Website")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")
    department_id = fields.Many2one('hospital.opd', string="Department")
    test_id = fields.One2many('hospital.test','patient_id',string="Test")
    problem = fields.Text(string="Problem")
    admit_date = fields.Date(string="Admit Date")
    release_date = fields.Date(string="Release Date")
    medicines = fields.One2many('hospital.medicine','patient',string="Medicine")
    move_id = fields.Many2one('account.move', string="Invoice")
    symptoms=fields.Char(string="Symptoms")
    complains=fields.Char(string="Complains")
    bp = fields.Char(string="BP")
    temperature=fields.Char(string='Temperature')
    weight = fields.Char(string="Weight")
    spo2 = fields.Char(string="SPO2")
    gcs = fields.Char(string="Gcs")
    pain_condition = fields.Char(string="Pain Conditions")    
    physical_appearances = fields.Char(string="Physical Appearances")
    deformation = fields.Char(string="Deformation")
    appetite = fields.Char(string="Appetite")
    bladder_habits = fields.Char(string="Bladder Habits")
    sleep_conditions = fields.Char(string="Sleep Conditions")

    company_id = fields.Many2one('res.company',
        string='Company',
        required=True,
        index=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        related='company_id.currency_id',
        depends=["company_id"],
        store=True
    )

    user_id = fields.Many2one('res.users',
        string='Assigned To',
        default = lambda self: self.env.user.id,
    )
    task_complete_percent = fields.Float(string="Treatment Completed(%)",
    required=True,digits=(16,2),
    compute='_compute_testComplete_percent'
    )
  
    total_amount = fields.Monetary(
        string='Total Amount',
        compute = '_compute_total',
        store = True,
    )

    @api.depends('test_id.amount')
    def _compute_total(self):
        print('hey')
        c=0
        for rec in self:
            for j in rec.test_id:
                c+=j.amount
            for k in rec.medicines:
                c+= k.amount  
            rec.total_amount=c  
            print('monkey',rec.total_amount)
        


    def _compute_testComplete_percent(self):
        for rec in self:
            total_tasks=len(rec.test_id)
            complete_tasks=sum([1 for t in rec.test_id if t.test_complete])
            if  total_tasks:
                complete_percent = (complete_tasks / total_tasks)*100
            else:
                complete_percent=0
            rec.task_complete_percent=complete_percent
    
    def _compute_appointment_count(self):
        # for lop ma rakhnu ko karan chai singleton error aucha vanera
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count
    
    @api.model
    def test_cron_job(self):
        patient_id = self.env['hospital.patient'].search([])
        for rec in patient_id:
            template_id = self.env.ref('projects.patient_card_email_template').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(rec.id, force_send=True)


    @api.model
    def create(self,vals):
        if not vals.get('occupation'):
            vals['occupation']="New occupation"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        res=super(HospitalPatient, self).default_get(fields)
        res['gender']='female'
        res['age']=50
        return res

    @api.constrains('name')
    def chec_name(self):
        for rec  in self:
            patients = self.env['hospital.patient'].search([('name','=',rec.name),('id','!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def chec_age(self):
        for rec  in self:
            if rec.age==0:
                raise ValidationError(_("Age Cannot Be Zero....!"))

    def name_get(self):
        result = []
        for rec in self:
            name ='['+rec.reference+']'+rec.name+' '+rec.gender
            result.append((rec.id, name))
        return result
    
    def action_open_appointments(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Appointment',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
    
    def action_send_card(self):
        template_id = self.env.ref('projects.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def _prepare_invoice_values(self):
        params = self.env['ir.config_parameter'].sudo() #NOTE: Important
        income_product_id = params.get_param('projects.task_income_product', default = 0)

        if not self.responsible_id:
            raise ValidationError('Partner is not set')

        invoice_vals = {
            'ref': self.name,
            'move_type': 'out_invoice',
            'invoice_origin': self.name,
            'invoice_user_id': self.user_id.id,
            'narration': '',
            'partner_id': self.responsible_id.id,
            'currency_id': self.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.name,
                'price_unit': self.total_amount,
                'quantity': 1.0,
                'product_id': int(income_product_id),
            })]
        }
        return invoice_vals

    def create_invoice(self):
        invoice_vals = self._prepare_invoice_values()
        print(self.company_id)
        invoice = self.env['account.move'].with_company(self.company_id)\
            .sudo().create(invoice_vals).with_user(self.env.uid)
        print(invoice.id)
        self.write({'move_id': invoice.id})

        return invoice


    def action_view_invoices(self):
        self.ensure_one()

        return {
            'name': _('Invoices'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [self.move_id.id])],
        }


class PatientScreening(models.Model):
    _name = "patient.screening"
    _description = "Patient Screening"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _rec_name = "symptoms"

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    symptoms=fields.Char(string="Symptoms")
    complains=fields.Char(string="Complains")
    bp = fields.Char(string="BP")
    temperature=fields.Char(string='Temperature')
    weight = fields.Char(string="Weight")
    spo2 = fields.Char(string="SPO2")
    gcs = fields.Char(string="Gcs")
    pain_condition = fields.Char(string="Pain Conditions")    
    physical_appearances = fields.Char(string="Physical Appearances")
    deformation = fields.Char(string="Deformation")
    appetite = fields.Char(string="Appetite")
    bladder_habits = fields.Char(string="Bladder Habits")
    sleep_conditions = fields.Char(string="Sleep Conditions")
