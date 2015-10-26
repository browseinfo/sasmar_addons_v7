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
from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_lead_stage(osv.osv_memory):
    """
    move multiple lead to one stage.
    """

    _name = 'crm.lead.stage'
    _description = 'Multiple lead to one stage'
    _columns = {
        'lead_ids': fields.many2many('crm.lead', rel='multi_lead_rel', id1='multi_id', id2='lead_id', string='Leads/Opportunities', domain="[('type', '=', 'lead')]"),
        'stage_id': fields.many2one('crm.case.stage', 'Stage', required=True),
    }

    def default_get(self, cr, uid, fields, context=None):
        """
        Use active_ids from the context to fetch the leads
        """
        if context is None:
            context = {}
        record_ids = context.get('active_ids', False)
        res = super(crm_lead_stage, self).default_get(cr, uid, fields, context=context)

        if record_ids:
            opp_ids = []
            opps = self.pool.get('crm.lead').browse(cr, uid, record_ids, context=context)
            for opp in opps:
                opp_ids.append(opp.id)
            if 'lead_ids' in fields:
                res.update({'lead_ids': opp_ids})

        return res

    def action_multi_lead_stage(self, cr, uid, ids, context=None):
        """
        Use lead_ids from the wizard and set to new stage
        """
        if context is None:
            context = {}

        wizard = self.browse(cr, uid, ids[0], context=context)
        lead_ids = wizard.lead_ids
        if lead_ids:
            for lead in lead_ids:
                self.pool.get('crm.lead').write(cr, uid, [lead.id], {'stage_id':wizard.stage_id.id},context)

        return {'type': 'ir.actions.act_window_close'}



crm_lead_stage()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
