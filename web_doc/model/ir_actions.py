#-*- coding: utf-8 -*-
from openerp.osv import osv, fields

class act_window(osv.osv):
    
    '''Adding link to doc'''
    
    _inherit = 'ir.actions.act_window'

    def _get_linktome(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        res = {}
        page_obj = self.pool.get('document.page')
        for i in ids:
            my_brw = self.browse(cr, uid, [i], context = context)
            if my_brw[0] and my_brw[0].doc:
                l = "#id=" + str(my_brw[0].doc.id) + "&view_type=form&model=document.page"
            else:
                l = "#view_type=list&model=document.page"
            res[i] = l
        return res

    _columns = {
    'doc': fields.many2one('document.page', 'Long Doc.',
        domain = [('type', '=', 'content')],
        help = '''Link to document page of this action.'''),
    'doc_body': fields.related('doc', 'content', type='text',
        string = 'Doc', relation = 'document.page', store = True,
        help = '''Documentation related to the document page element'''),
    'doc_title': fields.related('doc', 'name', type='text',
        string = 'Title', relation = 'document.page', store = True,
        help = '''Documentation Title'''),
    'linktome': fields.function(_get_linktome, 'Link to me',
        help = """Link to edit me"""),
    }


