#!/usr/bin/env python

import sys
import tkinter as tk

from lxml import etree

sys.path.append('./')
sys.path.append('./inkex')
sys.path.append('/usr/share/inkscape/extensions')

import inkex

class Application(tk.Frame):
    def __init__(self, master=None, text_content='', on_save_handler=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.textbox_script.insert('1.0', text_content, 'end')
        self.on_save_handler = on_save_handler

    def create_widgets(self):

        self.textbox_script = tk.Text(self, undo=True)
        self.textbox_script.pack(side='top')

        self.button_save = tk.Button(self, text='Save script', command=self.button_save_on_click)
        self.button_save.pack(side="right")

        self.button_quit = tk.Button(self, text="close", command=self.master.destroy)
        self.button_quit.pack(side="left")

    def button_save_on_click(self):
        if self.on_save_handler is not None:
            self.on_save_handler(self.textbox_script.get('1.0','end'))


class AddScriptToLayer(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('--open_after_created', action='store',
                                     type=inkex.Boolean, dest='open_after_created', default=True,
                                     help='Open script for editing?')
        self.layer_scripts = []
        self.script_element = None
        self.current_layer_id = None
        self.tk_app_root = None

    def effect(self):
        self.active_layer = self.svg.get_current_layer()
        self.active_layer_id = self.active_layer.get('id')
        self.open_after_created = self.options.open_after_created
        active_layer_script = self.svg.getElement('//svg:g[@id="' + self.active_layer_id + '"]/svg:script')

        if active_layer_script is None:
            self.addScriptTag()

            if self.open_after_created:
                self.start_editor_app()

            inkex.utils.debug('Script added for layer "' + self.active_layer_id + '". Open "Document properties/Scripting/Embedded scripts" to edit it.')

        else:
            inkex.utils.debug('Layer "' + self.active_layer_id + '" already has a script attached')
            self.script_element = active_layer_script
            if self.open_after_created:
                self.start_editor_app()

    def addScriptTag(self):
        self.script_element = etree.Element('script')
        self.script_element.set('id', 'script_' + self.active_layer_id)
        self.script_element.text = '// Add code :) '
        self.active_layer.append(self.script_element)

    def start_editor_app(self):
        tk_app_root = tk.Tk()
        tk_app_root.title = "Script editor"
        app = Application(master=tk_app_root, text_content=self.script_element.text,
                          on_save_handler=self.on_editor_save)
        app.mainloop()

    def close_editor_app(self):
        if self.tk_app_root is not None:
            self.tk_app_root.destory()

    def on_editor_save(self, text_content):
        self.script_element.text = text_content

effect = AddScriptToLayer()
effect.run(output=False)

