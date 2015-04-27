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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

class crm_phonecall2phonecall_partner(osv.osv_memory):
    _name = 'crm.phonecall2phonecall.partner'
    _description = 'Phonecall To Phonecall'

    _columns = {
        'name' : fields.char('Call summary', size=64, required=True, select=1),
        'user_id' : fields.many2one('res.users',"Assign To"),
        'contact_name':fields.char('Contact', size=64),
        'phone':fields.char('Phone', size=64),
        'categ_id': fields.many2one('crm.case.categ', 'Category', \
                domain="['|',('section_id','=',False),('section_id','=',section_id),\
                ('object_id.model', '=', 'crm.phonecall')]"), 
        'date': fields.datetime('Date'),
        'section_id':fields.many2one('crm.case.section','Sales Team'),
        'action': fields.selection([('schedule','Schedule a call'), ('log','Log a call')], 'Action', required=True),
        'partner_id' : fields.many2one('res.partner', "Partner"),
        'note':fields.text('Note')
    }


    def action_cancel(self, cr, uid, ids, context=None):
        """
        Closes Phonecall to Phonecall form
        """
        return {'type':'ir.actions.act_window_close'}

    def action_schedule(self, cr, uid, ids, context=None):
        value = {}
        if context is None:
            context = {}
        phonecall = self.pool.get('crm.phonecall')
        partner_id = context and context.get('active_ids') or []
        partner_browse = self.pool.get('res.partner').browse(cr, uid, partner_id)[0]
        for this in self.browse(cr, uid, ids, context=context):
            vals = {
                'name': this.name,
                'user_id': this.user_id and this.user_id.id or False,
                'categ_id': this.categ_id and this.categ_id.id or False,
                'description': this.note or '',
                'date': this.date or time.strftime('%Y-%m-%d %H:%M:%S'),
                'section_id': this.section_id and this.section_id.id or False,
                'partner_id': partner_id and partner_id[0],
                'partner_phone': partner_browse.phone or False,
                'partner_mobile': partner_browse.mobile or False,
            }
            new_id = phonecall.create(cr, uid, vals, context=context)
            #phonecall.case_open(cr, uid, [new_id], context=context)
            if this.action == 'log':
                phonecall.write(cr, uid, [new_id], {'state': 'done'}, context=context)

        return True
        
    
    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        
        """
        res = super(crm_phonecall2phonecall_partner, self).default_get(cr, uid, fields, context=context)
        record_id = context and context.get('active_id', False) or False
        res.update({'action': 'schedule', 'date': time.strftime('%Y-%m-%d %H:%M:%S')})
        if record_id:
            partner = self.pool.get('res.partner').browse(cr, uid, record_id, context=context)

            categ_id = False
            data_obj = self.pool.get('ir.model.data')
            try:
                res_id = data_obj._get_id(cr, uid, 'crm', 'categ_phone2')
                categ_id = data_obj.browse(cr, uid, res_id, context=context).res_id
            except ValueError:
                pass
            if 'name' in fields:
                res.update({'name': partner.name})
            if 'user_id' in fields:
                res.update({'user_id': partner.user_id and partner.user_id.id or False})
            if 'date' in fields:
                res.update({'date': False})
            if 'section_id' in fields:
                res.update({'section_id': partner.section_id and partner.section_id.id or False})
            if 'categ_id' in fields:
                res.update({'categ_id': categ_id})
            if 'partner_id' in fields:
                res.update({'partner_id': partner.id})
        return res
    
crm_phonecall2phonecall_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
