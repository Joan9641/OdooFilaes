from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SociBaixaWizard(models.TransientModel):
    _name = 'gestion_filaes.soci_baixa_wizard'
    _description = 'Wizard per donar de baixa un soci d’una filà'

    soci_id = fields.Many2one('gestion_filaes.socios', string="Soci", required=True)
    filada_ids = fields.Many2many('gestion_filaes.filaes', string="Filàs del soci")

    @api.onchange('soci_id')
    def _onchange_soci_id(self):
        if self.soci_id:
            self.filada_ids = self.soci_id.filada_ids
        else:
            self.filada_ids = [(5, 0, 0)]

    def confirmar_baixa(self):
        for filada in self.filada_ids:
            if filada not in self.soci_id.filada_ids:
                raise ValidationError(f"El soci no està actiu en la filà {filada.name} o ja ha estat donat de baixa.")
            
            self.soci_id.filada_ids = [(3, filada.id)]
            filada.socis_ids = [(3, self.soci_id.id)]
            
            self.env['gestion_filaes.historial'].create({
                'soci_id': self.soci_id.id,
                'filada_id': filada.id,
                'accio': 'baixa',
                'fecha_accion': fields.Date.today(),
            })

