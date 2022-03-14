from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import UserError

class PrintReport(models.TransientModel):
    _name = "vehicles.report.wizard"

    start_date = fields.Date("Start date", required=True, default=date.today())
    end_date = fields.Date("End date", required=True, default=date.today())

    def generateReport(self):
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return self.env.ref('vehicles.vehicles_report').report_action(self, data=data)

class PrintReportTemplate(models.AbstractModel):
    _name = 'report.vehicles.vehicles_report_template'

    @api.model
    def _get_report_values(self, docs, data=None):
        start_date = datetime.strptime(data["start_date"], '%Y-%m-%d')
        end_date = datetime.strptime(data["end_date"], '%Y-%m-%d')
        vehicles_records = self.env["vehicle"].search([("purchase_date",">=",start_date),("purchase_date","<=",end_date)])
        if len(vehicles_records) > 0:
            return {
                'model': self.env['report.vehicles.vehicles_report_template'],
                'data': vehicles_records,
            }
        else:
            raise UserError("There are not vehicles with purchase date in the date range selected")