
{
    'name': 'Crm Assign to Salesperson',
    'version': '7.0',
    'category': 'CRM',
    'description': """
                    The purpose of the module is to assign the sales person via wizard in lead's list view.
""",
    'author': 'Browseinfo',
    'website': 'http://www.browseinfo.in',
    'images': [],
    'depends': ['crm','project','sale'],
    'data': [
             'wizard/crm_assign_wizard.xml',
             'crm_customize_view.xml',
             'wizard/crm_lead_stage_view.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
