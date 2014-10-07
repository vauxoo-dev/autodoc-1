from lxml.html.clean import Cleaner
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

    '''
    Inherit Cleaner class to overwrite allow_embedded_url  method and add a new parameter with the
    schemes allowed for embedded url
    '''

    def __init__(self, **kw):
        super(Cleaner, self).__init__(**kw)

    def allow_embedded_url(self, el, url, allowed_scheme=None):
        '''
        Verifies that all urls follow the minimum requirements, like scheme(http, https) or that
        hosts are in allow list
        @param el: HtmlElement object with the url embedded
        @param url:  string with the url to inspect
        @allowed_scheme: iterable(list or tuple) with the allow schemes, if it's None the scheme
        allowed are http and https

        return True if the url follow the minimal requirements otherwise return False
        '''
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

lxml.html.clean.Cleaner = Cleaner
