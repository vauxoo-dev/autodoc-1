#-*- coding: utf-8 -*-
from openerp.osv import osv, fields

class act_window(osv.osv):
    
    '''Adding link to doc'''
    
    _inherit = 'ir.actions.act_window'

    def _get_linktome(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        res = {}
        for i in ids:
            res[i] = "hola.txt"
        return res

    _columns = {
    'doc': fields.many2one('document.page', 'Long Doc.',
        domain = [('type', '=', 'content')],
        help = '''Link to document page of this action.'''),
    'doc_body': fields.related('doc', 'content', type='text',
        string = 'Doc', relation = 'dojcument.page', store = True,
        help = '''Documentation related to the document page element'''),
    'linktome': fields.function(_get_linktome, 'Link to me',
        help = """Link to edit me"""),
    }


