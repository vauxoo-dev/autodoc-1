##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    planified and programmed by Nhomar Hernandez nhomar@vauxoo.com
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
{
    "name": "Docs", 
    "version": "0.1", 
    "author": "Vauxoo", 
    "category": "Knowledge", 
    "description": """
Help and Documentation management.
==================================

This module is to manage all documentation available on a module, and or in a
implementation.

The roadmap is allow in an unique smart windows in every single view show:

 * Action Help.
 * Fields descriptions and help.
 * Direct link to process.
 * Direct link to How To's.
  - Link in the bottom view of the module form.
  - TODO: Add link specific in actions.
 * Direct link to videos.
  - Link in the bottom view of the module form.
  - TODO: Add link specific in actions.
 * Attached documents: It so common have help in .doc, .odt and so on.
  - This files should be in Videostatic directory on module.
  - TODO: Add link specific in actions.
 * Manage Attachments to process itself (Not so common to understand).
 * Link to actions to a content, in this way we can call the "Help Extended"
 * Auto compile with sphinx if .rst files if they are presented. 

The following image show where icon will appear for access to the documentation:

.. image:: /web_doc/static/src/img/documentation_access_button.png
   :width: 600 px
   :align: center

You can find a mindmap with the explanation of the main idea here_.

TODO: With this module we will have a documentation index to manage all
relations in with the windows and actions.

.. _here: web_doc/static/src/doc/web_doc.xmind
""", 
    "website": "", 
    "license": "", 
    "depends": [
        "base", 
        "web", 
        "process", 
        "vauxoo_cms"
    ], 
    "demo": [], 
    "data": [
        "view/web_doc_view.xml", 
        "view/ir_actions_view.xml", 
        "wizard/set_help_view.xml"
    ], 
    "test": [], 
    "js": [
        "static/src/js/doc.js"
    ], 
    "css": [
        "static/src/css/doc.css"
    ], 
    "qweb": [
        "static/src/xml/doc.xml"
    ], 
    "installable": True, 
    "auto_install": False
}
#vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: