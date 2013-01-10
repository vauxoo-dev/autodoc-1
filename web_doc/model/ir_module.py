# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import os
from openerp import pooler, tools
from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _

class ir_module(osv.Model):
    
    _inherit='ir.module.module'

    def action_compile_doc(self, cr, uid, ids, context = None):
        return True

    def _has_doc(self, cr, uid, ids, field_name, arg, context = None):
        """
        """
        if context is None:
            context = {}
        result = {}
        installed_ids = self.search(cr, uid, [('state', '=', 'installed')])
        for i in ids:
            if i in installed_ids:
#                print "Im installed"
                read_name = self.read(cr, uid, i, ['name'], context=context)
                name = read_name and read_name.get('name', '') or ''
                pathtodoclist = eval("addons."+name+".__path__")
                pathtodoc = pathtodoclist and pathtodoclist[0] or ''
                dirdoc = os.path.join(pathtodoc,'doc')
                if os.path.isdir(dirdoc):
                    result[i] = {'has_doc': True, 
                                 'link_doc': '/'+name+'/static/src/_build/html/index.html'}
                else:
                    result[i] = {'has_doc': False,
                                 'link_doc': 'http://localhost'}
                print result
        return result

    _columns = {
        'has_doc' : fields.function(_has_doc, 
                    string='Has doc to compile', 
                    type='boolean', 
                    help="Just to know if this module has doc to compile",
                    multi='has_doc'),
        'link_doc' : fields.function(_has_doc, 
                    string='See compiled doc', 
                    type='char', 
                    help="Link to embeded doc",
                    multi='has_doc')
    }
