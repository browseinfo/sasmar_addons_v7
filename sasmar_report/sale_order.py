import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    ship_via = fields.Many2one('ship.via', 'SHIP VIA')
    delivery_date = fields.Date('Delivery Date')
    po_number = fields.Char('Purchase Order')
    supplier_number = fields.Char('Supplier Number')

    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'sasmar_report.sale_order_report_template_id', context=context)
    
    
class ship_via(models.Model):
    _name = 'ship.via'
    
    name = fields.Char('Name')
