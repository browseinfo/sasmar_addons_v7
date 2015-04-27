import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    ship_via = fields.Many2one('ship.via', 'SHIP VIA')
    delivery_date = fields.Date('Delivery Date')
    po_number = fields.Char('Purchase Order')
    supplier_number = fields.Char('Supplier Number')
    incoterm = fields.Many2one('stock.incoterms', 'Incoterm')
    
    @api.multi
    def invoice_print(self):
        '''
        This function prints the Invoice order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'sasmar_report.invoice_report_template_id')
    
    
class ship_via(models.Model):
    _name = 'ship.via'
    
    name = fields.Char('Name')
