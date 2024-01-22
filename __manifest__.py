# -*- coding: utf-8 -*-
##############################################################################
#
#    Palmares Sucursal Matanzas
#    Departamento de Informática y Comunicaciones
#    Autor: Raúl Sánchez Pérez
#
##############################################################################
{
    'name': 'Equipos de Medicion',
    'version': '1.0',
    'summary': """Control de Equipos de medición""",
    'description': """Control de Equipos de medición como pesas, termómetros, manómetros y otros""",
    'category': 'Mantenimiento',
    'author': 'Dpto. Informática',
    'company': 'Sucursal Palmares Matanzas',
    'maintainer': 'Sucursal Palmares Matanzas',
    'website': "http://intranet.var.palmares.cu",
    'depends': ['base','xlsx_report_base', 'hr', 'ventas'],
    'data': [
        'security/gauge_security.xml',
        'security/ir.model.access.csv',
        'views/gauge.xml',
        'views/report.xml',
        'data/data.xml',
    ],
    # 'demo': ['data/data.xml'],
    # 'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
