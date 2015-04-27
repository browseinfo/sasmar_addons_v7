from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang', False)
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
        warning = False
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        partner = partner_obj.browse(cr, uid, partner_id)
        lang = partner.lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False

        fpos = False
        if not fiscal_position:
            fpos = partner.property_account_position or False
        else:
            fpos = self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position)
        if update_tax: #The quantity only have changed
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += '\n'+product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}
        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            pricelist_browse = self.pool.get('product.pricelist').browse(cr, uid, [pricelist])[0]
            pricelist_currency = pricelist_browse.currency_id.id
            pricelist_type = pricelist_browse.price_type
################TO ADD DIFFERENT PRICES FOR DIFF CURRENCY AND FOR DIFF PRICE TYPE ###############            
            prod_temp_id = product_obj.product_tmpl_id.id
            product_currency = self.pool.get('currency.extended').search(cr, uid, [('product_id','=',prod_temp_id),('currency_id', '=', pricelist_currency),('price_type', '=', pricelist_type)])
            if len(product_currency)==0:
                pricelist_currency_name = self.pool.get('product.pricelist').browse(cr, uid, [pricelist])[0].currency_id.name
                product_name = self.pool.get('product.product').browse(cr, uid, [product])[0].name
                raise osv.except_osv(
                    _('No price found!'),
                    _('"%s" has no "%s" price define for "%s" currency')%(product_name, pricelist_type,pricelist_currency_name,))
            else:
                price = self.pool.get('currency.extended').browse(cr, uid, product_currency)[0].amount
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
############################################################################################                
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error!'),
                       'message' : warning_msgs
                    }
        return {'value': result, 'domain': domain, 'warning': warning}
    
    
class product_template(osv.osv):
    _inherit = 'product.template'
    
    _columns = {
    
            'product_currency_ids' : fields.one2many('currency.extended', 'product_id', 'Product Currency'),
    }
    
    
class currency_extended(osv.osv):
    _name = 'currency.extended'
    
    _columns = {
        'currency_id':fields.many2one('res.currency','Currency', required=True),
        'amount':fields.float('Price',digits_compute=dp.get_precision('Account'), required=True),
        'product_id':fields.many2one('product.template','Product Name'),
        'price_type': fields.selection([('consumer', 'Consumer'), ('distributor', 'Distributor'),('wholesale', 'Wholesale')], 'Type', required=True),
    
    }
    _defaults = {
        'price_type': 'consumer',   
    }
    _sql_constraints = [
        ('name_currency_uniq', 'unique(currency_id, product_id, price_type)', 'You can\'t add multiple currency for the same product!'),
    ]
    
    
    
class product_pricelist(osv.osv):
    _inherit = 'product.pricelist'
    
    _columns = {
        'price_type': fields.selection([('consumer', 'Consumer'), ('distributor', 'Distributor'),('wholesale', 'Wholesale')], 'Type', required=True),
    }
    
    _defaults = {
            'price_type' : 'consumer',
    }
        
    def name_get(self, cr, uid, ids, context=None):
        result= []
        if not all(ids):
            return result
        for pl in self.browse(cr, uid, ids, context=context):
            name = pl.name + ' ('+ pl.currency_id.name + ')' + ' ('+ pl.price_type + ')'
            result.append((pl.id,name))
        return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
