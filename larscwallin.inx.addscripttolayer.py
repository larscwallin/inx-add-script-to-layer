#!/usr/bin/env python

import sys

from lxml import etree

sys.path.append('./')
sys.path.append('./inkex')
sys.path.append('/usr/share/inkscape/extensions')

import inkex

class AddScriptToLayer(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('--open_after_created', action='store',
                                     type=inkex.Boolean, dest='open_after_created', default=True,
                                     help='Open script for editing?')
        self.layer_scripts = []
        self.script_element = None
        self.current_layer_id = None

    def effect(self):
        self.active_layer = self.svg.get_current_layer()
        self.active_layer_id = self.active_layer.get('id')
        self.active_layer_scripts = self.active_layer.xpath('/svg:script', namespaces=inkex.NSS)
        self.open_after_created = self.options.open_after_created

        if self.active_layer_scripts.__len__() < 1:
            self.addScriptTag()
            inkex.utils.debug('Script added for layer "' + self.active_layer_id + '". Open "Document properties/Scripting/Embedded scripts" to edit it.')

        else:
            inkex.utils.debug('Layer "' + self.active_layer_id + '" already has a script attached')

    def addScriptTag(self):
        self.script_element = etree.Element('script')
        self.script_element.set('id', 'script_' + self.active_layer_id)
        self.script_element.text = '// Add code :) '
        self.active_layer.append(self.script_element)


effect = AddScriptToLayer()

effect.run(output=False)