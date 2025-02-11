{
    'name': "Gestió de Filaes",
    'version': "1.0",
    'summary': "Mòdul per gestionar la informació que respecta les filaes de Muro",
    'description': """
Amb aquest mòdul podem gestionar les dades d'una filà, com puguen ser els socis, les filaes a les que pertanyen, el historial d'altes i baixes, i els montepios realitzats per els socis.

Compta amb:
- Model Socis --> Camps com Data de Naixement, Filaes assignades, etc.
- Model Filaes --> Camps com CIF, Nom, Any de Fundació, etc.
- Model Historial --> Registra altes i baixes.
- Model Montepios --> per a la gestió d'aportacions.
    """,
    'author': "Joan Company Richart",
    'website': "https://github.com/Joan9641",
    'category': "Management",
    'depends': ['base'],
    'data': [
         'security/ir.model.access.csv',
         'views/socios_views.xml',
         'views/filaes_views.xml',
         'views/historial_views.xml',
         'views/montepios_views.xml',
         'reports/report_filaes_informe_templates.xml',
         'reports/report.xml',
         'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}

