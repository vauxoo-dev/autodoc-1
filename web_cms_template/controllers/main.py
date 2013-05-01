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
    _logger.warning("Please install latest Jinja2 package: http://jinja.pocoo.org/docs/intro/#prerequisites")

class Blog(web.http.Controller):
    _cp_path ='/internal'
    _password = openerp.tools.config.get('anonymous_password',"anonymous")
    _user = openerp.tools.config.get('anonymous_name',"anonymous")
    _db = openerp.tools.config.get('db_name')
    _model = "document.page"
    _posts_page = 2
    _obj_model = None
    _base_query = [('type','=','content')]
    _logger = logging.getLogger(__name__)
    _env = None

    def read_template(self, name):
        '''
        Read the template,
        This is the module base to select if we use Mako, Jinja, etc...
        :name: name of the file on template folder.
        '''
        module_path = openerp.addons.web_cms_template.__path__[0]
        tmpl_path = os.path.join(module_path,'static','src','template')
        f = open(os.path.join(tmpl_path,name), "r")
        html = f.read()
        return html

    def get_template_env(self):
        module_path = os.path.join(openerp.addons.web_cms_template.__path__[0])
        try:
            ofile = eval(open(os.path.join(module_path,'__openerp__.py')).read())
            templateFolder = ofile.get('template','static/src/template')
            self._env = Environment(loader=PackageLoader('web_cms_template', templateFolder))
        except Exception, e:
            self._logger.warning("Some problem loading template folder from your __openerp__.py file with this error %s" % e)
        if os.path.isdir(os.path.join(module_path,templateFolder)):
            return templateFolder
        else:
            self._logger.warning("Try to set a correct value for your template folder, actually you have: %s" % templateFolder)
            return ""

    def get_template(self, template, *arg, **karg):
        return self._env.get_template(template, arg)

    def read_template_jinja(self, name):
        template = Template('Hello {{ name }}!')
        html = template.render(name='John Doe')
        return html
    
    def render_template(self, name, **karg):
        '''
        Allow excecute in one line from other module
        rendering of the template.
        :arg: Params to pass to Jinja template
        '''
        self.get_template_env()
        return self.get_template(name).render(karg)

    def _get_model(self, req):
        '''
        Instanciate the model.
        :req: http request object
        '''
        req.session.authenticate(self._db, self._user, self._password, False)
        self._obj_model = req.session.model(self._model)
        return self._obj_model
    
    @web.http.httprequest
    def index(self, req, s_action=None, **kw):
        config = {'page_title':'OpenERP Blog Test', 
                    'modules':['get_articles', 'get_categories'],
                    'js':['blog.js']}
        return self.render_template("index.html", config=config)

    @web.http.httprequest
    def get_posts(self, req, **kw):
        params = req.params.items()
        query = self._base_query[:]
        page = 1
        for p in params:
            if p[0] == 'page':
                page = int(p[1])
            if p[0] == 'categ' and p[1].isdigit() and p[1] != '0':
                query.append(('parent_id','=', int(p[1]))) 
            if p[0] == 'author' and p[1].isdigit() and p[1] != '0':
                query.append(('create_uid','=', int(p[1]))) 
        pages = self._get_model(req)
        articles = pages.search_read(query, 
                                    offset=(page-1)*self._posts_page, 
                                    limit=self._posts_page, 
                                    order='write_date')
        for a in articles:
            fecha = datetime.datetime.strptime(a.get('write_date'), '%Y-%m-%d %H:%M:%S')
            a.update({'date':fecha.strftime('%Y-%m-%d')})
            a.update({'time':fecha.strftime('%H:%M:%S')})
        total=self._get_pager(req, query, page)
        return self.render_template("posts.html", posts=articles, pager=(total,page))

    def _get_pager(self, req, query, active_page):
        pages = self._get_model(req)
        n_registers = pages.search(query, count=True)
        npages = int(n_registers/self._posts_page)
        if npages*self._posts_page != n_registers: 
            npages += 1
        return (npages)

    @web.http.httprequest
    def get_categories(self, req, **kw):
        categs = self._get_model(req)
        categs = categs.search_read([('type','=','category')], 
                                    order='name')
        return self.render_template("categories.html", categories=categs)

    @web.http.httprequest
    def get_products(self, req, **kw):
        req.session.authenticate(self._db, self._user, self._password, False)
        products = req.session.model('product.product')
        lastest = products.search_read([('active','=',True)], 
                                    limit=4, 
                                    order='write_date')
        html = "<h3 class=\"label\">Lasted Products</h3><ul class=\"tabs vertical\">"
        for p in lastest:
            p_html = """<li>
							<div class="alignleft thumb_shadow">
								<a href="blog_post.html" title=""><img src="data:image/png;base64,%s" alt="" class="border light_border neutral_outline" /></a>
							</div>
							<p>%s</p>
							<p class="post_meta">04/05/10 . By <a href="#" title="">Admin</a></p>
						</li>""" % (p.get('image'), p.get('name'), )
            html = "%s %s"%(html, p_html)
        return html
