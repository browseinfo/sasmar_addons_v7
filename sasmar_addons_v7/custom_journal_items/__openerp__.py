# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses Broseinfo, Open Source Management Solution Framework.
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
    "name" : "Custom Journal Item",
    "version" : "1.0",
    "depends" : [
                 'sale',
                 'account_accountant',
                 'account_analytic_analysis',
                 ],
    "author" : "Browseinfo",

    "description": """
    This module is use to Add Custom view in journal item and help to filter company wise Period and journals.
    """,

    "website" : "www.browseinfo.in",

    "data" : [
              #'menuitem_journal.xml',
              'views/custom_journal_items.xml',
              ],

    'qweb' : [
        "static/src/xml/account_move_line_quickadd.xml",
    ],
    'css':[
        'static/src/css/account_move_line_quickadd.css'
    ],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
