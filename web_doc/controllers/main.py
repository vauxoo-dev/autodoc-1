# -*- coding: utf-8 -*-
import os
import openerp
from openerp.addons.web import http
openerpweb = http


def read_base_doc(name):
    '''
    Method that will be sure to convert path of index in absolute path.
    :return: Absolute path for template system
    '''
    m = openerp.addons.web_doc.__path__
    base = m and m[0] or ''
    templates = os.path.join(base, 'static', 'src', 'templates')
    if os.path.isdir(templates):
        return templates
    else:
        raise ValueError("Template folder dont exist in this module")


class HerreraDoc(openerpweb.Controller):

    '''
    With this controller we will manage all documentation.
    The important thing here is the admin part.
    We will auto compile.
    Using Sphinx
    TODO: controller for Menu Help.
    TODO: controller for Process Help.
    TODO: controller for index Help.
    '''
    _cp_path = '/doc'

    @openerpweb.httprequest
    def index(self, req, s_action=None, **kw):
        #        basepath = read_base_doc("index.html")
        basepath = "////"
        return str(basepath)


class JsonInfoDoc(openerpweb.Controller):

    _cp_path = '/doc/generic'

    @openerpweb.jsonrequest
    def doc_info(self, req):
        return {
            "doc": "Hello"
        }
