# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import sys
import time
from datetime import datetime
from operator import itemgetter

from lxml import etree

from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools

class account_move_line(osv.osv):
    _inherit = "account.move.line"

    

    def get_periods_per_company(self, cr, uid, company_id, context=None):
        period_ids = self.pool.get('account.period').search(cr, uid, [('company_id', '=', int(company_id))])
        return self.pool.get('account.period').name_get(cr, uid, period_ids, context=context)
    def get_journals_per_company(self, cr, uid, company_id, context=None):
        journal_ids = self.pool.get('account.journal').search(cr, uid, [('company_id', '=', int(company_id))])
        return self.pool.get('account.journal').name_get(cr, uid, journal_ids, context=context)
    def list_periods(self, cr, uid, context=None):
        ids = self.pool.get('account.period').search(cr,uid,[])
        return self.pool.get('account.period').name_get(cr, uid, ids, context=context)

    def list_company(self, cr, uid, context=None):
        ids = self.pool.get('res.company').search(cr,uid,[])
        return self.pool.get('res.company').name_get(cr, uid, ids, context=context)

    def list_journals(self, cr, uid, context=None):
        ng = dict(self.pool.get('account.journal').name_search(cr,uid,'',[]))
        ids = ng.keys()
        result = []
        for journal in self.pool.get('account.journal').browse(cr, uid, ids, context=context):
            result.append((journal.id,ng[journal.id],journal.type,
                bool(journal.currency),bool(journal.analytic_journal_id)))
        return result

account_move_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: