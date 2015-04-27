from openerp.report import report_sxw
from openerp.osv import osv
from datetime import date,time,datetime

class invoice_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(invoice_report, self).__init__(cr, uid, name, context=context)
        self.index = 0
        self.total_qty = 0
        self.localcontext.update({
                                  'time' : time,
                                  'get_quantity' : self.get_quantity,
                                  'get_delivery_add' : self.get_delivery_add,
                                  'get_date_format' : self.get_date_format,
                                  })
    def get_delivery_add(self, o):
        order_id = self.pool.get('sale.order').search(self.cr, self.uid, [('name', '=', o.origin)])
        s_obj = self.pool.get('sale.order').browse(self.cr, self.uid, order_id)
        return s_obj
                                  
    def get_quantity(self, obj):
        for line in obj.invoice_line:
            self.total_qty += line.quantity
        return self.total_qty
        
    def get_date_format(self, date1):
        if date1:
            req_date = datetime.strptime(date1, '%Y-%m-%d').strftime('%d/%m/%y')
            return req_date
        
                                  
class invoice_report_template_id(osv.AbstractModel):
    _name='report.sasmar_report.invoice_report_template_id'
    _inherit='report.abstract_report'
    _template='sasmar_report.invoice_report_template_id'
    _wrapped_report_class=invoice_report
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
                       

    
