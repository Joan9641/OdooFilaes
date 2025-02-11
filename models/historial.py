from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Historial(models.Model):
    _name = 'gestion_filaes.historial'
    _description = 'Historial de Altes i Baixes en Filàs'

    soci_id = fields.Many2one('gestion_filaes.socios', string="Soci", required=True)
    filada_id = fields.Many2one('gestion_filaes.filaes', string="Filà", required=True)
    accio = fields.Selection([('alta', 'Alta'), ('baixa', 'Baixa')], string="Acció", required=True)
    fecha_accion = fields.Date(string="Data de l'Acció", required=True, default=fields.Date.today)




