# -*- coding: utf-8 -*-
{
    'name': "Matriculas",

    'summary': "Módulo para controle de matrículas",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': "Uncategorized",
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [],
    'installable': True,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/grade_schedules_line.xml',
        'views/grade.xml',
        'views/students.xml',
        'views/professors.xml',
        'views/menu.xml'
    ]
}

