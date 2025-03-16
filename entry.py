import gi
import subprocess
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

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

# def on_search_window_key_press(widget, event, search_window):
#     if event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter:
#         # Destroy the popup when Enter is pressed
#         search_window.destroy()
#         search_window = None
#         return True  # Stop event propagation

#     elif event.keyval == Gdk.KEY_Escape:
#         # Optionally close on Esc too
#         search_window.destroy()
#         search_window = None
#         return True

#     return False