#-*- coding: utf-8 -*-
from openerp.osv import osv


class document_page(osv.Model):
    _inherit = "document.page"

    def create(self, cr, uid, vals, context=None):
        '''
        Overwriting the create of page, to verify if it is comming from the
        "Create Help" link with this we will be sure that the new documentation
        Inmediatltly is saved will be related to the Action Windows

        @param context['action_doc_enviroment']: Integer - Action to be
        written after Create the Doc.
        '''
        if context is None:
            context = {}
        ctxaction = context.get('action_doc_enviroment')
        doc_created = super(document_page, self).create(cr, uid, vals, context)

        if isinstance(ctxaction, int):
            ao = self.pool.get('ir.actions.act_window')
            ao.write(cr, uid, ctxaction, {'doc': doc_created})

        return doc_created
