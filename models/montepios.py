from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Montepios(models.Model):
    _name = 'gestion_filaes.montepios'
    _description = 'Aportacions a Montepios'

    soci_id = fields.Many2one('gestion_filaes.socios', string="Soci", required=True)
    filada_id = fields.Many2one('gestion_filaes.filaes', string="Filà", required=True)
    aportacio = fields.Float(string="Aportació", required=True)
    fecha_aportacio = fields.Date(string="Data d'Aportació", required=True, default=fields.Date.today)

    @api.constrains('soci_id')
    def _check_soci_actiu(self):
        for record in self:
            historial = self.env['gestion_filaes.historial'].search([
                ('soci_id', '=', record.soci_id.id),
                ('filada_id', '=', record.filada_id.id),
                ('accio', '=', 'alta')
            ], limit=1)
            if not historial:
                raise ValidationError("El soci no està actiu en aquesta filà i no pot fer aportacions.")

