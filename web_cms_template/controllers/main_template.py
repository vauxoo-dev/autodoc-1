# -*- coding: utf-8 -*-
import ast
import base64
import csv
import glob
import itertools
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import time
import urllib2
import xmlrpclib
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO
import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
import openerp
from openerp.addons import web
import logging
try:
    from jinja2 import Template
    from jinja2 import Environment, PackageLoader
except ImportError:
    _logger = logging.getLogger(__name__)
    _logger.warning("""Please install latest Jinja2 package:
                     http://jinja.pocoo.org/docs/intro/#prerequisites""")

class Main(web.http.Controller):
    _cp_path ='/main'
    _password = openerp.tools.config.get('anonymous_password',"anonymous")
    _user = openerp.tools.config.get('anonymous_name',"anonymous")
    _db = openerp.tools.config.get('db_name')
    _posts_page = 2
    _obj_model = None
    _base_query = [('type','=','content')]
    _logger = logging.getLogger(__name__)
    _env = None

    def get_template_env(self):
        """
        This method instaciate an enviroment with the template folder due to 
        JinJa needs.
        :return: Jinja Enviroment
        """
        module_path = os.path.join(openerp.addons.web_cms_template.__path__[0])
        try:
            filepath = os.path.join(module_path,'__openerp__.py')
            ofile = eval(open(filepath).read())
            templateFolder = ofile.get('template','static/src/template')
            self._env = Environment(loader=PackageLoader('web_cms_template', 
                                                         templateFolder))
        except Exception, e:
            self._logger.warning("""Some problem loading template folder from 
                            your __openerp__.py file with this error %s""" % e)
        if os.path.isdir(os.path.join(module_path,templateFolder)):
            return templateFolder
        else:
            self._logger.warning("""Try to set a correct value for your 
                              template folder, actually you have: 
                              %s""" % templateFolder)
            return ""

    def get_template(self, template, *arg):
        """
        Little method to be able to ask for template with just one line.
        :template: Template name in templates folder.
        :arg: Parameters spected in the template Just if it apply.
        """
        return self._env.get_template(template, arg)
    
    def render_template(self, template, *arg):
        '''
        Allow excecute in one line from other module
        rendering of the template.
        :arg: Params to pass to Jinja template
        '''
        self.get_template_env()
        return self.get_template(template).render(title = "Hola Mundo")

    def _get_model(self, model, req):
        '''
        Instanciate the model.
        :req: http request object
        '''
        req.session.authenticate(self._db, self._user, self._password, False)
        self._obj_model = req.session.model(model)
        return self._obj_model

    def get_menus(self, req):
        menus_model = self._get_model('ir.ui.menu', req)
        menus = menus_model.search_read([], 
                                    order='name')
        return menus

    @web.http.httprequest
    def index(self, req, s_action=None, **kw):
        self.get_menus(req)
        return self.render_template("main.html")
