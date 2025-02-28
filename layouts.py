import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from buttons import Layouts

class LayOuts:
    def __init__(self, parent, bar_image, network_label):
        self.layouts(parent, bar_image, network_label)

    def layouts(self, parent, bar_image, network_label):
        self.buttons_layout = parent.buttons_.get_layout()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        parent.add(main_box)

        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.middle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.left_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        main_box.pack_start(self.left_box, False, False, 0)
        main_box.pack_start(self.left_spacer, True, True, 0)
        main_box.pack_start(self.middle_box, False, False, 0)
        main_box.pack_start(self.right_spacer, True, True, 0)
        main_box.pack_start(self.right_box, False, False, 0)

        self.middle_box.set_halign(Gtk.Align.CENTER)

        self.middle_box.pack_start(bar_image, False, False, 0)

        for button in self.buttons_layout.left_buttons:
            self.left_box.pack_start(button, False, False, 0)

        for button in self.buttons_layout.middle_buttons:
            self.middle_box.pack_start(button, True, False, 0)
            
        self.right_box.pack_start(network_label, False, False, 0)

        for button in self.buttons_layout.right_buttons:
            self.right_box.pack_start(button, False, False, 0)