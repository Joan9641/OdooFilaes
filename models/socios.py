from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Socios(models.Model):
    _name = 'gestion_filaes.socios'
    _inherits = {'res.partner': 'partner_id'}
    
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')

    fecha_nacimiento = fields.Date(string="Fecha de Naixement", required=True)
    historial = fields.Many2one('gestion_filaes.historial')
    filada_ids = fields.Many2many('gestion_filaes.filaes', string="Filàs")
    certificat_minusvalidesa = fields.Image(string="Certificat de Minusvalidesa")
    condicio = fields.Selection(
        [('jovenil', 'Jovenil'), ('actiu', 'Actiu'), ('baixa', 'Baixa'),
         ('honorari', 'Honorari'), ('social', 'Social')],
        string="Condició", compute="_compute_condicio", store=True)
    antiguitat = fields.Integer(string="Antiguitat en la Filà", compute="_compute_antiguitat", store=True)

    @api.depends('fecha_nacimiento', 'certificat_minusvalidesa', 'filada_ids')
    def _compute_condicio(self):
        today = date.today()
        for record in self:
            edat = (today - record.fecha_nacimiento).days // 365 if record.fecha_nacimiento else 0
            anys_filada = 0
            for filada in record.filada_ids:
                historial = self.env['gestion_filaes.historial'].search([
                    ('soci_id', '=', record.id),
                    ('filada_id', '=', filada.id),
                    ('accio', '=', 'alta')
                ])
                anys_filada += sum([(today - h.fecha_accion).days // 365 for h in historial])
            if record.certificat_minusvalidesa:
                record.condicio = 'social'
            elif anys_filada >= 30 and edat >= 70:
                record.condicio = 'honorari'
            elif edat < 18:
                record.condicio = 'jovenil'
            elif edat >= 18:
                record.condicio = 'actiu'
            else:
                record.condicio = 'baixa'

    @api.depends('filada_ids')
    def _compute_antiguitat(self):
        today = date.today()
        for record in self:
            total = 0
            for filada in record.filada_ids:
                historial = self.env['gestion_filaes.historial'].search([
                    ('soci_id', '=', record.id),
                    ('filada_id', '=', filada.id),
                    ('accio', '=', 'alta')
                ])
                total += sum([(today - h.fecha_accion).days // 365 for h in historial])
            record.antiguitat = total

    @api.model
    def create(self, vals):
        record = super(Socios, self).create(vals)
        if 'filada_ids' in vals and isinstance(vals['filada_ids'], list):
            for filada_id in vals['filada_ids']:
                self.env['gestion_filaes.historial'].create({
                    'soci_id': record.id,
                    'filada_id': filada_id,
                    'accio': 'alta',
                    'fecha_accion': fields.Date.today(),
                })
        return record

    def action_open_wizard_alta(self):
        return {
            'name': "Donar d'Alta en Filàs",
            'type': 'ir.actions.act_window',
            'res_model': 'gestion_filaes.soci_alta_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_soci_id': self.id},
        }

    def action_open_wizard_baixa(self):
        return {
            'name': "Donar de Baixa en Filàs",
            'type': 'ir.actions.act_window',
            'res_model': 'gestion_filaes.soci_baixa_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_soci_id': self.id},
        }
        
    def get_inscripcion_date(self, filada_id):
        historial = self.env['gestion_filaes.historial'].search([
            ('soci_id', '=', self.id),
            ('filada_id', '=', filada_id),
            ('accio', '=', 'alta')
        ], order='fecha_accion asc', limit=1)
        return historial.fecha_accion if historial else False
