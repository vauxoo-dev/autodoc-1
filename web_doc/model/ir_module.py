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
import subprocess
import re

from openerp import pooler, tools
from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
import httplib
import urlparse


def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None


def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes


class ir_module(osv.Model):

    _inherit = 'ir.module.module'

    def action_compile_doc(self, cr, uid, ids, context=None):
        '''
        This method will be used to autocompile docs per module.
        For now it is braking with Popen command and it will need
        deeper research, i will mark as TODO: For now posposed.
        '''
        read_names = self.read(cr, uid, ids, ['name'], context=context)
        for r in read_names:
            name = r and r.get('name', '') or ''
            pathtodoclist = eval("addons." + name + ".__path__")
            pathtodoc = pathtodoclist and pathtodoclist[0] or ''
            dirdoc = os.path.join(pathtodoc, 'doc')
            if os.path.isdir(dirdoc):
                print "dirdoc     ....    %s" % dirdoc
                a = subprocess.call(['cd', dirdoc, '&&', 'make', 'html'])
                print "AND IT RETURN ....       ", a
#                a = subprocess.call(['cd', dirdoc])
        return True

    def _has_doc(self, cr, uid, ids, field_name, arg, context=None):
        """
        """
        if context is None:
            context = {}
        result = {}
        installed_ids = self.search(cr, uid, [('state', '=', 'installed')])
        for i in ids:
            if i in installed_ids:
                read_name = self.read(cr, uid, i, ['name'], context=context)
                name = read_name and read_name.get('name', '') or ''
                pathtodoclist = eval("addons."+name+".__path__")
                pathtodoc = pathtodoclist and pathtodoclist[0] or ''
                dirdoc = os.path.join(pathtodoc, 'doc')
                if os.path.isdir(dirdoc):
                    result[i] = {'has_doc': True,
                                 'link_doc': '/'+name+'/static/src/_build/html/index.html'}
                else:
                    result[i] = {'has_doc': False,
                                 'link_doc': "http://doc.openerp.com"}
            else:
                read_name = self.read(cr, uid, i, ['name'], context=context)
                name = read_name and read_name.get('name', '') or ''
                result[i] = {'has_doc': False,
                             'link_doc': '/web_doc/'+name+'/doc/index.html'}
                # test if computed url exist, it is to avoid cross reference in
                # js side.
            link = result[i].get('link_doc')
            if link and re.match('^(http|https|ftp|sftp)', link):
                print "If it is or not   "+str(check_url(link))

        return result

    _columns = {
        'has_doc': fields.function(_has_doc,
                                   string='Has doc to compile',
                                   type='boolean',
                                   help="Just to know if this module has doc to compile, True if all the module comply with doc structure, if not, 2 options, go and compile documentation with sphinx or verify you cam make it comply",
                                   multi='has_doc'),
        'link_doc': fields.function(_has_doc,
                                    string='See compiled doc',
                                    type='char',
                                    help="Link to embeded doc",
                                    multi='has_doc')
    }
