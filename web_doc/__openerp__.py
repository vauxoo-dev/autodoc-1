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
    'name': 'Docs',
    'category': 'Knowledge',
    'description':"""
Help and Documentation management.
==================================

This module is to manage all documentation available on a module.

Self Explain showing:

 * Action Help.
 * Fields descriptions and help.
 * Direct link to process.
 * Direct link to How To's. TODO: Platform to sopport it.
 * Direct link to videos. TODO: Platform to support it. (Youtube - Vimeo - Internal)?
 * Attached documents: It so common have help in .doc, .odt and so on.
 * Manage Attachments to process itself (Not so common to understand).
 
""",
    'author': 'Vauxoo',
    'version': '0.1',
    'depends': [
                        'base',
                        'web', 
                        'process',
                        'web_url2',
                        ],
    "data": [
        "view/web_doc_view.xml"
    ],
    "qweb": [
        "static/src/xml/doc.xml",
    ],
    "js": [
        "static/src/js/doc.js",
    ],
    "css": [
        "static/src/css/doc.css",
    ],
    'auto_install': False,
    'active': False,
}
