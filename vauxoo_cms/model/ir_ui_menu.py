# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class ir_ui_menu_cms(osv.osv):

    """
    Especial Menus to be used on CMS.
    """
    _inherit = 'ir.ui.menu'
    _columns = {
        'external_link': fields.char('External Link',
                        size=254, required=False, readonly=False),
        'for_cms': fields.boolean('For CMS', required=False),
    }

    def get_main_cms_menus(cr, uid, context=None):
        return self.search(cr, uid, [], context=context and context or {})

ir_ui_menu_cms()
