#-*- encoding: utf-8 -*-

from openerp.osv import fields, osv


class set_help(osv.TransientModel):

    _name = "set.help"

    _columns = {
        "doc_id": fields.many2one("document.page", "Documents",
        help="Select the Document - Page that you want to attach to this action.",
        required=True),
    }

    def set_help(self, cr, uid, ids, context=None):
        '''
        Set the doc selected on wizard to the action Id enabled on View.
        '''
        if context is None:
            context = {}
        if context.get('action_doc_enviroment'):
            a_id = context.get('action_doc_enviroment')
            w = self.browse(cr, uid, ids, context=context)
            doc_id = w and w[0].doc_id and w[0].doc_id.id or False
            if doc_id:
                act_obj = self.pool.get('ir.actions.act_window')
                act_obj.write(cr, uid, a_id, {'doc': doc_id}, context=context)
        return True
