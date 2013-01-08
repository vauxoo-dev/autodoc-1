{
    'name': 'Herrera Docs',
    'category': 'Customization/Herrera',
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
    'author': 'Herrera',
    'version': '0.1',
    'depends': ['base','web', "process"],
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
