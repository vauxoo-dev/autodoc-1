#-*- coding: utf-8 -*-
from openerp.osv import osv, fields

class act_window(osv.osv):
    
    '''Adding link to doc'''
    
    _inherit = 'ir.actions.act_window'
    _columns = {
    'doc': fields.many2one('document.page', 'Long Doc.',
        domain = [('type', '=', 'content')],
        help = '''Link to document page of this action.'''),
    'doc_body': fields.related('doc', 'body', type='text', string='Doc'),
    }


