# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
{
    "name" : "Sasmar Report",
    "version" : "1.0",
    "depends" : ['account', 'stock', 'base_vat', 'purchase', 'sale'],
    "description": """
        This module is use to make Sale Order, Invoice, Purchase Order report.
    """,
    "website" : "www.browseinfo.in",
    "data" :[
		'report/sale_order_report_menu.xml',
		'report/sale_order_layout.xml',
		'views/sale_order_report_view.xml',
        'views/sale_order_view.xml',
		'report/invoice_layout.xml',
		'report/invoice_report_menu.xml',
		'views/invoice_report_view.xml',
		'views/tax_invoice_view.xml',
		'report/purchase_order_layout.xml',
		'report/purchase_order_report_menu.xml',
		'views/purchase_order_report_view.xml',
		'views/purchase_order_view.xml',
    ],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
