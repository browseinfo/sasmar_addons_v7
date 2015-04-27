from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class crm_assign2salesperson(osv.osv_memory):
    _name = 'crm.assign2salesperson'
    _description = 'CRM Assign to Salesperson'

    _columns = {
		'salesperson':fields.many2one('res.users',string='Salesperson', required=True),
}
    def assign2salesman(self, cr, uid, ids, context=None):
		lead_ids = context.get('active_ids')
		salesperson = self.browse(cr, uid, ids, context)[0].salesperson.id
		for lead_id in lead_ids:
			self.pool.get('crm.lead').write(cr, uid, [lead_id], {'user_id':salesperson},context)
		return
