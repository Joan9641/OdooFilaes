from odoo import http
from odoo.http import request, Response
import json

class GestionFilaesController(http.Controller):

    @http.route('/gestion_filaes/socis', type='json', auth='public', methods=['POST'])
    def get_socis_filtrats(self, **kwargs):
        """
        Controlador per obtindre la llista de socis filtrats per filà i condició.
        Exemple de JSON d'entrada:
        {
            "filada_id": 1,
            "condicio": "actiu"
        }
        """
        filada_id = kwargs.get('filada_id')
        condicio = kwargs.get('condicio')

        domain = []
        if filada_id:
            domain.append(('filada_ids', 'in', [filada_id]))
        if condicio:
            domain.append(('condicio', '=', condicio))

        socis = request.env['gestion_filaes.socios'].sudo().search(domain)
        result = [{'id': s.id, 'name': s.name, 'condicio': s.condicio} for s in socis]

        return json.dumps(result)

    @http.route('/gestion_filaes/montepios', type='http', auth='public', methods=['GET'])
    def get_montepios(self, soci_id, filada_id, any):
        """
        Controlador per obtindre els montepios d'un soci en una filà i un any determinat.
        Exemple de URL: /gestion_filaes/montepios?soci_id=5&filada_id=1&any=2024
        """
        soci = request.env['gestion_filaes.socios'].sudo().browse(int(soci_id))
        if not soci.exists():
            return Response(json.dumps({'error': 'Soci no trobat'}), 
                            status=404, content_type='application/json')

        montepios = request.env['gestion_filaes.montepios'].sudo().search([
            ('soci_id', '=', soci.id),
            ('filada_id', '=', int(filada_id)),
            ('fecha_aportacio', '>=', f'{any}-01-01'),
            ('fecha_aportacio', '<=', f'{any}-12-31')
        ])

        total_montepios = sum(m.aportacio for m in montepios)

        return Response(json.dumps({
            'soci': soci.name, 
            'total_montepios': total_montepios
        }), content_type='application/json')

