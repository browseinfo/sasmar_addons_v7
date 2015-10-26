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

from openerp import SUPERUSER_ID, workflow
from openerp.osv import fields, osv


class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    _columns = {
    
                'user_id': fields.many2one('res.users','Responsible Person'),
                'qoute_no': fields.char('Your Quotation #'),
                'ship_via': fields.many2one('ship.via', 'SHIP VIA'),
    }
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the request for quotation and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'send_rfq')
        return self.pool['report'].get_action(cr, uid, ids, 'sasmar_report.purchase_order_report_template_id', context=context)

	def wkf_send_rfq(self, cr, uid, ids, context=None):
		res = super(purchase_order, self).wkf_send_rfq(cr, uid, ids, context=context)
		company =self.browse(cr, uid, ids)[0].company_id.name
		mail_temp = self.pool.get('email.template')
		# 1 - SASMAR SPRL
		# 5 - SASMAR LIMITED
		temp_id = res.get('context').get('default_template_id')
		if company == 'SASMAR SPRL':
			temp_id = mail_temp.search(cr, uid, [('name','=','Purchase Order Sasmar-SASMAR SPRL')])
		if company == 'SASMAR LIMITED':
			temp_id = mail_temp.search(cr, uid, [('name','=','Purchase Order Sasmar-SASMAR LIMITED')])
		res.get('context').update({'default_template_id':temp_id})
		return res    
