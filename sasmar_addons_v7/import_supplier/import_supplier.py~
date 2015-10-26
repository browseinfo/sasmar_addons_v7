# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
import logging
import csv
import base64
import cStringIO
from openerp.tools.translate import _
import sys
from urllib2 import urlopen
from xlwt import Workbook, easyxf, Formula
import StringIO


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'attachment_csv' : fields.binary('file'),
        }

    def import_csv(self, cr, uid, ids, context=None):
            partner_obj = self.pool.get('res.partner')
            aa = self.browse(cr,uid,ids)[0]
            if not aa.attachment_csv:
                raise osv.except_osv(_('Import Error!'), _('Please Select Valid File.'))  
            if aa.attachment_csv:
                file_data = base64.decodestring(aa.attachment_csv)
                input = cStringIO.StringIO(file_data)
                reader = csv.reader(input,delimiter='\t')
                data = []
                count = 1 
                row_len = 1
                for row in reader:
	            print "####################", row
                    if count == 1:
                    	count = 0
                    	continue
                    partner_id = partner_obj.search(cr, uid, [('name', '=', row[1])])
                    if partner_id:
                    	partner_obj.write(cr, uid, partner_id, {'customer': True})
                    	
                    else:
                        data_create = {'ref':row[0],'name':row[1],
        		                           'street' : row[2], 'zip' : row[3], 'city' : row[4], 'customer': True}
                        partner_obj.create(cr, uid,data_create,context=context)
