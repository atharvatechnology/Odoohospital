from odoo import api,fields,models,_


class CreateAppointmentWizard(models.TransientModel):
    _name="create.appointment.wizard"
    _description="Create Appointment wizard"
    name = fields.Char(string="Name")
    date_appointment=fields.Date(string="Date Appointment")
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)

    def action_create_appointment(self):
        vals = {
            'name':self.name,
            'patient_id':self.patient_id.id,
            'date_appointment':self.date_appointment
        }
        self.env['hospital.appointment'].create(vals)
        # return {
        #     'name':_('Appointment'),
        #     'type':'ir.actions.act_window',
        #     'view_mode':'form',
        #     'res_model':'hospital.appointment',
        #     'res_id':appointment_rec.id,
        #     'target':'new',
        # }

    def action_view_appointment(self):
        #method 1
        # action = self.env.ref('projects.appointment_action').read()[0]
        # action['domain']=[('patient_id', '=', self.patient_id.id)]
        # return action
        # method 2
        return {
            'name':'Appointment',
            'type':'ir.actions.act_window',
            'res_model':'hospital.appointment',
            'view_type':'form',
            'domain':[('patient_id', '=', self.patient_id.id)],
            'view_mode':'tree,form',
            'target':'current',
        }
