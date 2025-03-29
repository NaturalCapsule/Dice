import gi
import os
import json
import sys
import shutil
import time

username = os.getlogin()
current_dir = os.path.dirname(os.path.abspath(__file__))

folder_name = 'config'

folder_path = os.path.join(current_dir, folder_name)

if os.path.isdir(folder_path) and not os.path.exists(f'/home/{username}/.config/bar'):
    print("checking......")
    os.makedirs(f'/home/{username}/.config/bar')
    dst = f'/home/{username}/.config/bar/'
    src = 'config'
    print("moving.....")
    shutil.move(src, dst)
    print(f"'config' folder moved to /home/{username}/bar/, successfully!")


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk
from media import MediaPlayerMonitor
from buttons import Buttons
from layouts import LayOuts
from labels import Labels
from scales import Scales
from images import Images

from updates import *
from actions import *
from bar_config import *

from load_gtk_mouse import gtk_mouse
from widgets import load
from hypr_workspaces import poll_active_workspace
from timers import timers




class FluxBar(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bar")
        self.load_bar()
        self.initUI()
        self.load_css()
        load(f'/home/{os.getlogin()}/.config/bar/config/config.json', self.layouts.left_box, self.layouts.middle_box, self.layouts.right_box, self.buttons_, self.labels, self.images.bar_image, self.workspaces, self.custom_workspaces)
        self.show_all()


    def initUI(self):
        with open(f'/home/{os.getlogin()}/.config/bar/config/config.json', "r") as file:
            widgets = json.load(file)
            
            for self.widget_ in widgets['bar']:
                widget_ = None
                
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        self.get_style_context().add_class('window')

        display = Gdk.Display.get_default()
        if display:
            monitor = display.get_monitor(0)
            if monitor:
                geometry = monitor.get_geometry()
                screen_width = geometry.width
                screen_height = geometry.height
            else:
                print('no monitor detected!')
        else:
            print('no monitor detected!')


        gtk_mouse()

        self.media = MediaPlayerMonitor()
        self.images = Images()
        self.labels = Labels()
        self.scales = Scales()


        button_actions = [lambda button=None: self.media_dropdown(button), lambda button: workspace_1(button),
                lambda button=None: workspace_2(button), lambda button=None: workspace_3(button),
                lambda button=None: workspace_4(button), lambda button=None: workspace_5(button),
                lambda button=None: pause_play_action_(button), lambda button=None: forward_action(button),
                lambda button=None: backward_action(button), lambda button=None: reset_action(button),
                lambda button=None: self.power_dropdown(button), lambda button=None: power_off(button),
                lambda button=None: reset(button), lambda button=None: hibernate(button),
                lambda button=None: lock(button), lambda button=None: self.date_dropdown(button),
                lambda button=None: self.volume_dropdown(button), lambda button=None: update_action(button)]
        
        self.buttons_ = Buttons(button_actions[0], button_actions[1], button_actions[2], button_actions[3], button_actions[4], button_actions[5], button_actions[6], button_actions[7], button_actions[8], button_actions[9], button_actions[10], button_actions[11], button_actions[12], button_actions[13], button_actions[14], button_actions[15], button_actions[16], button_actions[17])
        poll_active_workspace(set_active_workspace, self.buttons_)

        self.play_pause_button = Gtk.Button(label="Play")
        self.play_pause_button.get_style_context().add_class('playPauseButton')

        self.layouts = LayOuts(parent = self)

        self._workspaces()

        
        if self.pos == 'top':
            self.set_default_size(screen_width - (2 * self.width_gap), self.bar_height)
            self.layouts.top_position(parent=self, width_gap=self.width_gap, height_gap=self.height_gap)

        elif self.pos == 'bottom':
            self.set_default_size(screen_width - (2 * self.width_gap), self.bar_height)
            self.layouts.bottom_position(parent=self, width_gap=self.width_gap, height_gap=self.height_gap)

        elif self.pos == 'left':
            self.set_default_size(self.bar_height, screen_height - (2 * self.height_gap))  # Adjusted width and height
            self.layouts.left_position(parent=self, width_gap=self.width_gap, desired_width=self.bar_height, height_gap=self.height_gap)

        elif self.pos == 'right':
            self.set_default_size(self.bar_height, screen_height - (2 * self.height_gap))  # Adjusted width and height
            self.layouts.right_position(parent=self, width_gap=self.width_gap, desired_width=self.bar_height, height_gap=self.height_gap)

        
        else:
            print("Invalid layout, the program will exit!")
            exit(0)


        timers(update_volume, update_date, update_time, update_image, update_pauseplay, update_network, update_title, fetch_updates_async, self.scales, self.labels, self.buttons_, self.images, self.play_pause_button)


    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f'/home/{os.getlogin()}/.config/bar/config/style.css')
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    def load_bar(self):
        self.pos = bar_position()
        self.bar_height = bar_height()
        self.width_gap = bar_gap()
        self.height_gap = bar_gap_()

    def _workspaces(self):
        total = self.widget_['workspaces']
        if total > 5:
            print("More than 5 workspaces detected.\nExiting...")
            exit(0)

        self.workspaces = []
        self.custom_workspaces = []

        for i in range(1, total + 1):
            btn = getattr(self.buttons_, f'workspace{i}')
            self.workspaces.append(btn)

            custom_btn = getattr(self.buttons_, f'custom_workspace{i}')
            self.custom_workspaces.append(custom_btn)

        
    def media_dropdown(self, button):
        if hasattr(self, "media_window") and self.media_window:
            self.media_window.destroy()
            self.media_window = None
            return

        self.media_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.media_window.get_style_context().add_class('MediaWindow')
        self.media_window.set_decorated(False)
        self.media_window.set_resizable(False)
        self.media_window.set_border_width(10)

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        fixed = Gtk.Fixed()

        pixbuf = self.images.dropdown_image.get_pixbuf()
        new_image = Gtk.Image.new_from_pixbuf(pixbuf.copy() if pixbuf else None)
        hig_box.pack_start(new_image, True, True, 0)

        ver_box.pack_start(self.labels.dropdown_artist, False, False, 10)
        ver_box.pack_start(self.labels.dropdown_title_label, False, False, 0)

        self.play_pause_button.connect("clicked", pause_play_action_)


        reset_button = Gtk.Button(label="󱞳")
        reset_button.connect("clicked", reset_action)
        reset_button.get_style_context().add_class('resetDropdownButton')

        forward_button = Gtk.Button(label="")
        forward_button.connect("clicked", forward_action)
        forward_button.get_style_context().add_class('forwardButton')

        backward_button = Gtk.Button(label="")
        backward_button.connect("clicked", backward_action)
        backward_button.get_style_context().add_class('backwardButton')


        fixed.put(reset_button, 70, 40)
        fixed.put(forward_button, 100, 10)
        fixed.put(self.play_pause_button, 70, 10)
        fixed.put(backward_button, 40, 10)
        ver_box.pack_start(fixed, True, True, 0)

        hig_box.pack_start(ver_box, False, False, 0)

        self.media_window.add(hig_box)
        self.media_window.connect("destroy", lambda w: setattr(self, "media_window", None))
        self.media_window.show_all()


    def date_dropdown(self, button):
        if hasattr(self, "date_window") and self.date_window:
            self.date_window.destroy()
            self.date_window = None
            return
        
        self.date_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.date_window.get_style_context().add_class('DateWindow')
        
        self.date_window.set_hexpand(False)
        self.date_window.set_vexpand(False)
        
        self.date_window.set_decorated(False)
        self.date_window.set_resizable(False)
        self.date_window.set_border_width(10)
        

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        hig_box.pack_start(self.labels.date_label, False, False, 0)

        self.date_window.add(hig_box)
        self.date_window.show_all()


    def power_dropdown(self, button):
        if hasattr(self, "power_window") and self.power_window:
            self.power_window.destroy()
            self.power_window = None
            return
        
        self.buttons_.powerSettingsButtons(self.power_dropdown, power_off, reset, hibernate, lock)

        self.power_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.power_window.get_style_context().add_class('PowerWindow')
        
        self.power_window.set_hexpand(False)
        self.power_window.set_vexpand(False)
        
        self.power_window.set_decorated(False)
        self.power_window.set_resizable(False)
        self.power_window.set_border_width(10)

        grid = Gtk.Grid()

        grid.attach(self.buttons_.power_off_button, 1, 0, 2, 1)
        grid.attach(self.labels.power_off_label, 0, 0, 1, 1)

        grid.attach(self.buttons_.reboot_button, 1, 1, 2, 1)
        grid.attach(self.labels.reset_label, 0, 1, 1, 1)
        
        grid.attach(self.buttons_.lock_button, 1, 2, 2, 1)
        grid.attach(self.labels.lock_label, 0, 2, 1, 1)
        
        grid.attach(self.buttons_.hib_button, 1, 3, 2, 1)
        grid.attach(self.labels.hibernate_label, 0, 3, 1, 1)

        self.power_window.add(grid)
        
        self.power_window.show_all()


    def volume_dropdown(self, button):
        if hasattr(self, "volume_window") and self.volume_window:
            if self.scales.volume_scale_ and self.scales.mic_scale_:
                self.scales.mic_scale_.destroy()
                self.scales.volume_scale_.destroy()
                self.scales.volume_scale_ = None
                self.scales.mic_scale_ = None
                
            self.volume_window.destroy()
            self.volume_window = None

            return


        self.scales.volume_scale()
        self.scales.mic_scale()


        self.volume_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.volume_window.get_style_context().add_class('VolumeWindow')
        
        
        self.volume_window.set_decorated(False)
        self.volume_window.set_resizable(False)
        self.volume_window.set_border_width(10)

        ver_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)


        hig_box.pack_start(ver_box, False, False, 0)
        ver_box.pack_start(self.scales.volume_scale_, False, True, 0)

        ver_box.pack_start(self.labels.volume_label, False, False, 0)
        ver_box.pack_start(self.scales.mic_scale_, False, False, 0)
        
        ver_box.pack_start(self.labels.mic_label, False, False, 0)
        

        self.volume_window.add(hig_box)
        self.volume_window.set_size_request(250, 50)
        self.volume_window.show_all()

win = FluxBar()
win.connect("destroy", Gtk.main_quit)
Gtk.main()