from odoo import models, fields, api
from datetime import date

class Vehicle(models.Model):
    _name = 'vehicle'
    _rec_name = 'license_plate'

    license_plate = fields.Char("License plate", required=True)
    purchase_date = fields.Date("Purchase date", required=True)
    purchase_cost = fields.Float("Purchase cost")
    mileage = fields.Float("Mileage", required=True)
    qty_services = fields.Integer("Services Quantity", compute="_compute_qty_services", store=True, readonly=True)
    price = fields.Float("Price", readonly=True, compute="onchange_price", store=True,)
    year = fields.Integer("Year")
    brand = fields.Many2one("vehicle.brand", "Brand")
    model = fields.Many2one("vehicle.model", "Model")
    engine_model = fields.Char("Engine model")
    type = fields.Selection([("regular", "Regular"), ("industrial", "Industrial")], string="Vehicle type", required=True, default="regular")

    @api.onchange("mileage", "purchase_cost")
    @api.depends("mileage", "purchase_cost")
    def onchange_price(self):
        for record in self:
            record.price = record.purchase_cost * (100 - (record.mileage//10000 * 5)) / 100

    @api.depends("purchase_date")
    def _compute_qty_services(self):
        for record in self:
            if record.purchase_date:
                if date.today() >= record.purchase_date:
                    months = ((date.today().year - record.purchase_date.year) * 12 + date.today().month - record.purchase_date.month)//6
                    record.qty_services = months
                else:
                    record.qty_services = False
            else:
                record.qty_services = False


class VehicleBrand(models.Model):
    _name = 'vehicle.brand'
    name = fields.Char('Brand')

class VehicleModel(models.Model):
    _name = 'vehicle.model'
    name = fields.Char('Model')

