# -*- encoding: utf-8 -*-
##############################################################################
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Vauxoo CMS, CMS over OpenObject
##############################################################################
#    Collaborators of this module:
#    Coded by: nhomar@vauxoo.com
#              tulio@vauxoo.com
#    Planifyied by: nhomar@vauxoo.com
#    This project is mantained by Vauxoo Team:
#    https://launchpad.net/vauxoo-cms
#
##############################################################################
#    It is a collaborative effort between several companies that want to join
#    efforts in have a proposal solid and strong in the Health Care enviroment
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
###############################################################################
{
    "name": "Vauxoo ECM",
    "version": "0.2",
    "author": "Vauxoo",
    "category": "CMS",
    "description": """
Vauxoo ECM System.
==================

With this module you will be able to create several content to our CMS located
on:

http://launchpad.net/vauxoo_cms

After you install this module the document_base will have all information
necesary to manipulate your data content, mark your content with tags and
make public throught out CMS system.

You are able to manage your own openerp Instance locally, and buy our CMS
system and services.

Roadmap:
--------

* Portal.
* Tags.
* Store.

And so much more.

How Testing:
------------

Go to users and set CMS / Administrator group to your user.

See new menus installed and enjoy it!

http://launchpad.net/vauxoo-cms

    """,
    "website": "http://www.vauxoo.com",
    "license": "",
    "depends": [
        "base",
        "document_page",
        "portal_anonymous",
        "mail",
        "portal"
    ],
    "demo": [
        "demo/demo_data.xml"
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizard/create_menu_wizard.xml",
        "view/vauxoo_cms_view.xml",
        "view/vauxoo_menu_cms_view.xml",
        "process/new_content_process.xml",
        "data/doc_data.xml",
        "data/ir_config_data.xml"
    ],
    "test": [],
    "js": [],
    "css": [
        "static/src/css/vauxoo_page.css"
    ],
    "qweb": [],
    "installable": True,
    "auto_install": False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
