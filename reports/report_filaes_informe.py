from odoo import models

class ReportFilaesInforme(models.AbstractModel):
    _name = 'report.gestion_filaes.report_filaes_informe_document'
    _description = "Informe de Filàs"

    def _get_report_values(self, docids, data=None):
        docs = self.env['gestion_filaes.filaes'].browse(docids)
        return {
            'docs': docs,
        }

