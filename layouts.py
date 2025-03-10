import gi
import os
import sys
gi.require_version('Gtk', '3.0')
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import Gtk, GtkLayerShell
from configparser import ConfigParser


class LayOuts:
    def __init__(self, parent, bar_image, network_label):
        self.config = ConfigParser()
        self.config.read(f'/home/{os.getlogin()}/python/FlXBar/config/config.ini')
        if not GtkLayerShell.is_supported():
            print("Error: Layer Shell not supported. if you on Hyprland run this command: GDK_BACKEND=wayland python bar.py")
            # sys.exit()
            exit(1)
            
        
        
        self.layouts(parent, bar_image, network_label)

    def layouts(self, parent, bar_image, network_label):
        self.buttons_layout = parent.buttons_.get_layout()


        pos = self.config.get('Appearance', 'position')

        if pos == 'left' or  pos == 'right':
            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            parent.add(main_box)
            
            self.left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.middle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            self.left_spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.right_spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        elif pos == 'top' or pos == 'bottom':
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
    
    def left_position(self, parent, width_gap, desired_width):
        
        GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.LEFT, True)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.LEFT, width_gap)


        GtkLayerShell.set_exclusive_zone(parent, desired_width)

        parent.set_size_request(desired_width, -1)

        GtkLayerShell.auto_exclusive_zone_enable(parent)

    
    def right_position(self, parent, width_gap, desired_width):
        
        GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.RIGHT, True)

        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)

        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.RIGHT, width_gap)


        GtkLayerShell.set_exclusive_zone(parent, desired_width)

        parent.set_size_request(desired_width, -1)

        GtkLayerShell.auto_exclusive_zone_enable(parent)

    
    def top_position(self, parent, width_gap):
        GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.TOP)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.auto_exclusive_zone_enable(parent)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.TOP, width_gap)


    def bottom_position(self, parent, width_gap):
        GtkLayerShell.init_for_window(parent)
        GtkLayerShell.set_layer(parent, GtkLayerShell.Layer.BOTTOM)
        GtkLayerShell.set_anchor(parent, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.auto_exclusive_zone_enable(parent)
        GtkLayerShell.set_margin(parent, GtkLayerShell.Edge.BOTTOM, width_gap)
