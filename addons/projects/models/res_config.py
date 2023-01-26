# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2022-Present Lekhnath Rijal <lekhnath@greatbear.tech>
#
##########################################################################

from odoo import models, api, fields

class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    #NOTE: default_ prefix has special meaning in Odoo so not using that here
    projects_product_id = fields.Many2one('product.product',
        config_parameter = 'projects.task_income_product',
        string = 'Task Income Product',
        domain = [('type', '=', 'service')]
    )
