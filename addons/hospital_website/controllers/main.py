from odoo import http, _
from odoo.http import request

class TodoAppController(http.Controller):

    @http.route('/todos', type='http', auth='user', website=True)
    def list_todos(self, **kwargs):
        # if not request.session.uid:
        #     return request.redirect('/web/login', 303)

        context = {
            'todos': request.env['todo_app.todo'].search([])
        }


        return request.render("todo_app_website.todo_list_page", context)
