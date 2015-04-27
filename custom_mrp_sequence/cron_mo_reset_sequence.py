# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################
import time
from openerp.osv import osv
import datetime
from datetime import date,timedelta

class cron_mo_reset_sequence(osv.osv):
    _name = 'mo.reset.sequence'

    def reset_sequence(self, cr, uid, context=None):
        models_data = self.pool.get("ir.model.data")
        form_view_id = models_data.get_object_reference(cr, uid, "mrp", "sequence_mrp_prod")
        self.pool.get("ir.sequence")._alter_sequence(cr, form_view_id and form_view_id[1], 1, 1)
        return True

cron_mo_reset_sequence()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
