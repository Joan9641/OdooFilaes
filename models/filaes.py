from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Filaes(models.Model):
    _name = 'gestion_filaes.filaes'
    _description = 'Filàs'

    name = fields.Char(string="Nom de la Filà", required=True)
    cif = fields.Char(string="CIF")
    any_fundacio = fields.Date(string="Any de Fundació")

    historial_ids = fields.One2many('gestion_filaes.historial', 'filada_id', string="Historial de Socis")
    socis_ids = fields.Many2many(
        'gestion_filaes.socios',
        'gestion_filaes_socios_filaes_rel',
        'filada_id',
        'soci_id',
        string="Socis"
    )

    nombre_components = fields.Integer(string="Nombre de Components", compute="_compute_nombre_components", store=True)
    total_montepios = fields.Float(string="Total Montepíos", compute="_compute_total_montepios", store=True)

    @api.depends('socis_ids')
    def _compute_nombre_components(self):
        for record in self:
            record.nombre_components = len(record.socis_ids)

    @api.depends('historial_ids')
    def _compute_total_montepios(self):
        for record in self:
            montepios = self.env['gestion_filaes.montepios'].search([
                ('filada_id', '=', record.id)
            ])
            record.total_montepios = sum(montepio.aportacio for montepio in montepios)

    def get_sorted_socis(self):
        """
        Retorna els socis associats a la filà ordenats primer per la data d'inscripció (alta)
        i després per la data de naixement (ascendent). S'assumeix que el model 'gestion_filaes.socios'
        té implementat el mètode 'get_inscripcion_date(filada_id)' i el camp 'fecha_nacimiento'.
        """
        return self.socis_ids.sorted(
            key=lambda s: (s.get_inscripcion_date(self.id) or '', s.fecha_nacimiento or '')
        )

    @api.onchange('socis_ids')
    def _onchange_socis_ids(self):
        for record in self:

            if not record._origin:
                continue

            socis_antics = set(record._origin.socis_ids.ids)
            socis_actuals = set(record.socis_ids.ids)

            for soci_id in socis_actuals - socis_antics:
                self.env['gestion_filaes.historial'].create({
                    'soci_id': soci_id,
                    'filada_id': record.id,
                    'accio': 'alta',
                    'fecha_accion': fields.Date.today(),
                })
            for soci_id in socis_antics - socis_actuals:
                self.env['gestion_filaes.historial'].create({
                    'soci_id': soci_id,
                    'filada_id': record.id,
                    'accio': 'baixa',
                    'fecha_accion': fields.Date.today(),
                })

