from  lxml.html.clean import Cleaner
import re
import copy
from lxml import etree
from lxml.html import defs
from lxml.html import fromstring, tostring, XHTML_NAMESPACE 
from lxml.html import xhtml_to_html, _transform_result 
import lxml
try: 
    unichr 
except NameError: 
    # Python 3 
    unichr = chr 
try: 
    unicode 
except NameError: 
    # Python 3 
    unicode = str 
try: 
    bytes 
except NameError: 
    # Python < 2.6 
    bytes = str 
try: 
    basestring 
except NameError: 
    basestring = (str, bytes) 
try:
    from urlparse import urlsplit
except ImportError:
    # Python3
    from urllib.parse import urlsplit

class Cleaner(Cleaner):

    def __init__(self, **kw):
        super(Cleaner,self).__init__(**kw)

        
    def allow_embedded_url(self, el, url, allowed_scheme=None): 
        allowed_scheme = allowed_scheme or ('http', 'https')
        if (self.whitelist_tags is not None 
            and el.tag not in self.whitelist_tags): 
            return False 
        scheme, netloc, path, query, fragment = urlsplit(url) 
        netloc = netloc.lower().split(':', 1)[0] 
        if scheme not in allowed_scheme: 
            return False 
        if netloc in self.host_whitelist: 
            return True 
        return False 


    def clean_html(self, html): 
        result_type = type(html) 
        if isinstance(html, basestring): 
            doc = fromstring(html) 
        else: 
            doc = copy.deepcopy(html) 
        self(doc) 
        return _transform_result(result_type, doc)

lxml.html.clean.Cleaner = Cleaner

