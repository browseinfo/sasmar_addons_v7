from openerp import tools, api
from openerp import models, fields, api, _
from openerp.osv import osv, fields


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
            'sequence' : fields.char('Sequence'),
    }

    def onchange_is_company(self, cr, uid, ids, is_company, c_type, parent_id, context=None):
        res = {}
        if isinstance(ids, (int)):
            ids = [ids]
        if is_company:
            if len(ids) > 0:
                sequence = {1: '0000', 2: '000', 3: '00', 4: '0'}
                seq = sequence.get(len(str(ids[0])), '') + str(ids[0])
                res.update({'sequence' : seq})
        else:
            if c_type == 'contact':
                if parent_id:
                    seq = self.pool.get('res.partner').browse(cr, uid, parent_id, context=context).sequence
                    res.update({'sequence' : seq})

        return {'value' : res}


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = {}
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        print"==============res", res
        partner_obj = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        res['value'].update({'client_order_ref': partner_obj.sequence or ''})
        print"========sale======res", res
        return res


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        res = {}
        res = super(account_invoice, self).onchange_partner_id(type, partner_id=partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id)
        partner_obj = self.env['res.partner'].browse(partner_id)
        res['value'].update({'name': partner_obj.sequence or ''})
        print"=========invoice=====res", res
        return res



