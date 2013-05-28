#-*- encoding: utf-8 -*-

from openerp.osv import fields, osv

class set_help(osv.TransientModel):

    _name="set.help"
    
    _columns = {
            "doc_id": fields.many2one("document.page", "Documents",
                help="Select the Document - Page that you want to attach to this action.")
    }
