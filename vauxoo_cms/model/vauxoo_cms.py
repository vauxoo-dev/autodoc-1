# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class cms_text_format(osv.osv):

    """
    OpenERP Model : Ways to avoid unespected content type on files
    """

    _name = 'cms.text.format'
    _description = 'Same as Text Formats on Drupal'

    _columns = {
        'name': fields.char('Name', 32, required=False, readonly=False),
        'description': fields.text('Description'),
        'list_tags': fields.text('List of allowed tags',
                   help="A tag in every line"),
        'limit_allowed_html_tags': fields.boolean('Limit allowed HTML tags '),
        'display_any_html_as_pt': fields.boolean('Display any HTML as plain text'),
        'display_any_html_as_pt': fields.boolean('Display any HTML as plain text'),
        'convert_url': fields.boolean('Convert URLs into links'),
        'convert_line_breaks': fields.boolean('Convert line breaks into \
HTML (i.e. <br> and <p>)'),
        'url_shortener': fields.boolean('URL shortener ', required=False,
                    help="Replaces URLs with a shortened version."),
        'correct_chopped': fields.boolean('Correct faulty and chopped off HTML',
                      help="Replaces URLs with a shortened version."),
    }

    _defaults = {
        'name': lambda *a: None,
    }

cms_text_format()


class cms_type(osv.osv):

    """
    OpenERP Model : cms_type
    """

    _name = 'cms.type'
    _description = 'Same as Content Type on Drupal'

    _columns = {
        'name': fields.char('Name', 32, required=False, readonly=False),
        'description': fields.text('Description'),
        # TODO: automagically configure generic options.
    }
    _defaults = {
        'name': lambda *a: None,
    }

cms_type()


class document_page(osv.osv):

    """
    OpenERP Model : cms
    Contents to show on our website
    If you are familiarized with Drupal, some concepts are the same of content
    """

    _inherit = 'document.page'
    _description = "Base Content Type"

    def special_features(self, cr, uid, ids, context={}):
        '''
        Options that i want manage:
        come in a "Secure Html way"
        come in a "template way" [Mako, tornado, jinja,
        all of theme i want support with them own libraries]
        come in "RST Format"
        come in "Latex Format"
        come in "Plain Text Format"
        With this we will be able to manage several ways to write Docs.
        Think about the posibility: wiki?, odt?,
        word?, odp?, PowerPoint?, xmind?
        '''
        return context.get('content', False)

    def _get_display_content2(self, cr, uid, ids, name, args, context=None):
        '''
        Content display taking in account special fields alá drupal to mantain.
        Secured content edition trought frontend.
        '''
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            if page.type == "category":
                content = self._get_page_index(cr, uid, page, link=False)
            else:
                content = page.content
                context.update({'content': content})
                content = self.special_features(cr, uid, ids, context=context)
            res[page.id] = content
        return res

    _columns = {
        'name': fields.char('Title', 254, required=False, readonly=False),
        'body': fields.text('Body'),
        'type_id': fields.many2one('cms.type', 'Content Type', required=False, help='''
        Content Type (same as Drupal Content Type)
        '''),
        'publishing': fields.selection([
            ('published', 'Published'),
            ('promoted', 'Promoted to front page.'),
            ('sticky', 'Sticky at top of lists'),

        ], 'Publishing Options', select=True),
        'user_id': fields.many2one('res.users', 'Authoring Information',
                                  help='''Leave blank for Anonymous.'''),
        'text_id': fields.many2one('cms.text.format', 'Text Format',),
        'url': fields.char('Url Path Settings', 254,
                           help='''
        Optionally specify an alternative URL by which this content can be
        accessed.
        For example, type "about" when writing an about page. Use a relative
        path and don't add a trailing slash or the URL alias won't work.
        '''),
        'allow_comments': fields.boolean('Comment Settings', required=False,
                                        help='''
        True: Users with the "Post comments" permission can post comments.
        False: Users cannot post comments.
        '''),
        'sequence': fields.integer('Sequence'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('review', 'Review'),
            ('menucreated', 'Menu Created'),
            ('published', 'Published'),

        ], 'State', select=True,
            help="""draft: Content is just created,
        review: Element is ready to be reviewed for the manager,
        Menu Created: The menu to see this element on CMS is created,
        Published: All is ready, this element is available for be seen for
        everybody
        """),
        'display_content2': fields.function(_get_display_content2,
                            string='Displayed Content', type='text'),
        'type': fields.selection([('content', 'Content'),
                                 ('block', 'Block'),
                                 ('category', 'Category')], 'Type',
                                 help='''Page type, Content for Contents
                                 to show, block to be treated as a Drupal
                                 Block, category, to be used as category.'''),
        'cms_menu_ids': fields.many2many('ir.ui.menu', 'cms_menu_ids_rel',
                   "document_page_id", "cms_menu_id", "Menus",
                   help='Menu to show this content on your cms'),
    }

    _defaults = {
        'state': 'draft',
    }

    def public_search_read(self, cr, uid, ids, context=None):
        '''
        Method to return Just Public availables fields to show, the objective is
        avoid show udesired information or even filter as an API object per
        object.
        @return: Dict with fields values in document_page
        '''
        _fields = ['name',
        'allow_comments',
        'user_id',
        'display_content2',
        'url',
        'cms_menu_ids',
                   ]
        return self.read(cr, uid, ids, [_fields], context=context)

    def act_draft(self, cr, user, ids, context=None):
        """
        Set document page to published
        @return: id page setted
        """
        return self.write(cr, user, ids, {'state': 'draft'})

    def act_review(self, cr, user, ids, context=None):
        """
        Set document page to review
        @return:  id page setted
        """
        return self.write(cr, user, ids, {'state': 'review'},
                context=context and context or {})

    def act_published(self, cr, user, ids, context=None):
        """
        Set document page to published
        @return:  id page setted
        """
        return self.write(cr, user, ids, {'state': 'published'},
                context=context and context or {})

    def get_all_published_content(self, cr, uid, context=None):
        '''
        Return all published content.

        All published methods are the document.page elements that them "state"
        field is equal to Publihed.

        This method is used i.e: to build feeds.

        :return: List with all published content, ordered but sequence.
        '''
        return self.search_read(cr, uid, [('state', '=', 'published')],
                                context=context and context or {})

    def get_front_page_content(self, cr, uid, context=None):
        '''
        Return all content to the front page.

        All published pages in front page are the document.page elements that
        them "state" field is equal to Publihed and publishing field is equal
        to "promoted".

        This method is used i.e: to build Home.
        :return: List with all published content, ordered but sequence.
        '''
        return self.search_read(cr, uid, [('state', '=', 'published'),
                                          ('publishing', '=', 'promoted')],
                                context=context and context or {})

document_page()
