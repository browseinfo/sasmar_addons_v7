# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Browseinfo (http://browseinfo.in)
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
from openerp.osv import fields, osv

#class account_invoice(osv.osv):
#    _inherit = 'account.invoice'
#    _columns = {
#                }
#    def create(self, cr, uid, vals, context=None):
#        res = super(account_invoice,self).create(cr, uid, vals, context=context)
#        if self.browse(cr, uid,res,context=context).type == 'out_invoice':
#            self.send_mail_sasmar(cr, uid, res, context=context)
#        return res
#    def send_mail_sasmar(self, cr, uid,ids, context=None):
#        email_temp = self.pool.get('email.template')
#        template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'send_email_finance', 'email_template_sasmar_invoice')[1]
#        if isinstance(ids, (int,float,long)):
#           ids = [ids]
#        email_temp.send_mail(cr, uid, template_id, ids[0], force_send=False, context=context)
#        return True
#    def confirm_paid(self, cr, uid, ids, context=None):
#        res = super(account_invoice,self).confirm_paid(cr, uid, ids, context=context)
#        if isinstance(ids, (int)):
#            ids = [ids]
#        if self.browse(cr, uid,ids[0],context=context).type == 'out_invoice':
#            self.send_mail_sasmar(cr, uid, ids, context=context)
#        return res
#    def invoice_validate(self, cr, uid, ids, context=None):
#        res = super(account_invoice,self).invoice_validate(cr, uid, ids, context=context)
#        if isinstance(ids, (int)):
#            ids = [ids]
#        if self.browse(cr, uid,ids[0],context=context).type == 'out_invoice':
#            self.send_mail_sasmar(cr, uid, ids, context=context)
#        return res
#
#    def set_to_proforma(self, cr, uid, ids, context=None):
#        self.write(cr, uid, ids, {'state':'proforma2'}, context=context)
#        if isinstance(ids, (int)):
#            ids = [ids]
#        if self.browse(cr, uid,ids[0],context=context).type == 'out_invoice':
#            self.send_mail_sasmar(cr, uid, ids, context=context)
#        return True
#
#account_invoice()
class sale_order(osv.osv):
    _inherit = 'sale.order'
    _columns = {
                }
    def create(self, cr, uid, vals, context=None):
        res = super(sale_order,self).create(cr, uid, vals, context=context)
        self.send_mail_sasmar(cr, uid, res, context=context)
        return res
    def send_mail_sasmar(self, cr, uid,ids, context=None):
        email_temp = self.pool.get('email.template')
        template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'send_email_finance', 'email_template_sasmar_invoice')[1]
        if isinstance(ids, (int,float,long)):
           ids = [ids]
        email_temp.send_mail(cr, uid, template_id, ids[0], force_send=False, context=context)
        return True