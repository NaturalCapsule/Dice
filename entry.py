import gi
import subprocess
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class Entries:
    def __init__(self):
        pass
    
    def search_entry(self):
        self.entry_ = Gtk.Entry()
        self.entry_.get_style_context().add_class('SearchEntry')
        self.entry_.connect("activate", self.on_entry_activate)
        self.entry_.grab_focus()

    def on_entry_activate(self, widget):
        subprocess.run(['firefox', f'https://www.google.com/search?q={widget.get_text()}'])
        widget.set_text('')
        widget.set_text('')