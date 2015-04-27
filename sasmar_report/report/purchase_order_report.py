from openerp.report import report_sxw
from openerp.osv import osv
from datetime import date,time,datetime

class purchase_order_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(purchase_order_report, self).__init__(cr, uid, name, context=context)
        self.total_qty = 0
        self.localcontext.update({
                                  'time' : time,
                                  'get_quantity' : self.get_quantity,
                                  'get_date' : self.get_date,
                                  'get_est_date' : self.get_est_date,
                                  })
                                  
    def get_quantity(self, obj):
        for line in obj.order_line:
            self.total_qty += line.product_qty
        return self.total_qty

    def get_date(self, obj):
        if obj.date_order:
            req_date = datetime.strptime(obj.date_order, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y')
            return req_date
        
    def get_est_date(self, obj):
        if obj.minimum_planned_date:
            req_date = datetime.strptime(obj.minimum_planned_date, '%Y-%m-%d').strftime('%d/%m/%y')
            return req_date
                                  
                                  
class purchase_order_report_template_id(osv.AbstractModel):
    _name='report.sasmar_report.purchase_order_report_template_id'
    _inherit='report.abstract_report'
    _template='sasmar_report.purchase_order_report_template_id'
    _wrapped_report_class=purchase_order_report
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
                       

    
