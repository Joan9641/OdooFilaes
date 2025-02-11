from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SociAltaWizard(models.TransientModel):
    _name = 'gestion_filaes.soci_alta_wizard'
    _description = 'Wizard per donar d’alta un soci en una filà'

    soci_id = fields.Many2one('gestion_filaes.socios', string="Soci", required=True)
    filada_ids = fields.Many2many('gestion_filaes.filaes', string="Filàs disponibles")

    def confirmar_alta(self):
        """ Afegeix el soci a les filaes seleccionades i crea un historial. """
        for filada in self.filada_ids:
            if filada.socis_ids.ids in [self.soci_id.id]:
                raise ValidationError(f"El soci ja està donat d'alta en la filà {filada.name}.")

            self.soci_id.filada_ids = [(4, filada.id)]
            filada.socis_ids = [(4, self.soci_id.id)]

            self.env['gestion_filaes.historial'].create({
                'soci_id': self.soci_id.id,
                'filada_id': filada.id,
                'accio': 'alta',
                'fecha_accion': fields.Date.today(),
            })
