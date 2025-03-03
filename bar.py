import gi
import subprocess
import os
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, GLib
from configparser import ConfigParser
from media import MediaPlayerMonitor
from threading import Timer 
from buttons import Buttons
from entry import Entries
from layouts import LayOuts
from labels import Labels
# from dropdowns import DropDowns
from scales import Scales
from images import Images
from updates import *
from actions import *



class FluxBar(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bar")
        self.config = ConfigParser()
        self.config.read(f'/home/{os.getlogin()}/python/FlXBar/config/config.ini')
    
        self.load_config()
        self.initUI()
        self.load_css()
        self.texts()
        self.show_all()

    def initUI(self):

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
            else:
                print('no monitor detected!')
        else:
            print('no monitor detected!')
        

        self.set_default_size(screen_width - (2 * self.width_gap), self.bar_height)


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
                lambda button=None: self.volume_dropdown(button), lambda button=None: self.search_dropdown(button)]
        
        self.buttons_ = Buttons(button_actions[0], button_actions[1], button_actions[2], button_actions[3], button_actions[4], button_actions[5], button_actions[6], button_actions[7], button_actions[8], button_actions[9], button_actions[10], button_actions[11], button_actions[12], button_actions[13], button_actions[14], button_actions[15], button_actions[16], button_actions[17])

        self.poll_active_workspace()
        
        self.layouts = LayOuts(parent = self, network_label = self.labels.network_label, bar_image = self.images.bar_image)
    
        self.entries = Entries()

        
        if self.pos == 'top':
            self.layouts.top_position(parent = self, width_gap = self.width_gap)
        elif self.pos == 'bottom':
            self.layouts.bottom_position(parent = self, width_gap = self.width_gap)
        elif self.pos == 'left':
            self.layouts.left_position(parent = self, width_gap = self.width_gap, desired_width = bar_height)
        elif self.pos == 'right':
            self.layouts.right_position(parent = self, width_gap = self.width_gap, desired_width = bar_height)

        GLib.timeout_add(100, update_volume, self.scales, self.labels)
        GLib.timeout_add(100, update_date, self.labels)
        GLib.timeout_add(100, update_title, self.buttons_)
        GLib.timeout_add(100, update_time, self.buttons_)
        GLib.timeout_add(100, update_image, self.labels, self.images)
        GLib.timeout_add(100, update_pauseplay, self.buttons_)
        GLib.timeout_add(100, update_network, self.labels)
        GLib.timeout_add(100, update_title, self.buttons_)

    def load_config(self):
        self.pos = self.config.get('Appearance', 'position')
        self.bar_height = self.config.getint('Appearance', 'BarHeight')
        self.width_gap = self.config.getint('Appearance', 'widthGap')


    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('/home/naturalcapsule/python/FlXBar/config/style.css')
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    def texts(self):
        text_pos = f"[{time.strftime(r'%d %b %Y | %H:%M:%S')}] [Info!] Using: ({self.pos}) as the bar position!"
        print(text_pos)


    def poll_active_workspace(self):
        try:
            result = subprocess.run(['hyprctl', 'activeworkspace'], capture_output=True, text=True)
            current_workspace = int(result.stdout.split()[1])
            set_active_workspace(current_workspace, self.buttons_)
        except (IndexError, ValueError):
            pass

        Timer(1, self.poll_active_workspace).start()

    def media_dropdown(self, button):
        if hasattr(self, "media_window") and self.media_window:
            self.media_window.destroy()
            self.media_window = None
            return
        
        self.buttons_.media_buttons(self.media_dropdown, pause_play_action_, forward_action, backward_action, reset_action)
        self.media_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.media_window.get_style_context().add_class('MediaWindow')
        
        self.media_window.set_hexpand(False)
        self.media_window.set_vexpand(False)
        
        self.media_window.set_decorated(False)
        self.media_window.set_resizable(False)
        self.media_window.set_border_width(10)


        x, y = self.get_position()
        bx, by = button.translate_coordinates(self, 0, 0)
        self.media_window.move(x + bx - 100, y + by - 120)

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        ver_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)

        fixed = Gtk.Fixed()

        self.labels.dropdown_title_label.set_halign(Gtk.Align.START)

        hig_box.pack_start(self.images.dropdown_image, True, True, 0)
        hig_box.pack_start(ver_box, False, False, 0)


        ver_box.pack_start(self.labels.dropdown_artist, False, False, 10)
        self.labels.dropdown_title_label.set_halign(Gtk.Align.CENTER) 
        ver_box.pack_start(self.labels.dropdown_title_label, False, False, 0)
        
        fixed.put(self.buttons_.reset_button, 70, 40)
        fixed.put(self.buttons_.forward_button, 100, 10)
        fixed.put(self.buttons_.play_pause_button, 70, 10)
        fixed.put(self.buttons_.backward_button, 40, 10)
        
        
        ver_box.pack_start(fixed, True, True, 0)

        self.media_window.add(hig_box)
        self.media_window.show_all()

    def search_dropdown(self, button):
        if hasattr(self, "search_window") and self.search_window:
            self.search_window.destroy()
            self.search_window = None
            return

        self.entries.search_entry()

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hig_box.pack_start(self.entries.entry_, False, False, 0)

        self.search_window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.search_window.set_decorated(False)
        self.search_window.set_resizable(False)
        self.search_window.set_border_width(10)
        
        
        self.search_window.add(hig_box)
        self.search_window.show_all()
        
        self.search_window.get_style_context().add_class('SearchWindow')


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
        
        x, y = self.get_position()
        bx, by = button.translate_coordinates(self, 0, 0)
        self.date_window.move(x + bx - 100, y + by - 120)

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
        
        x, y = self.get_position()
        bx, by = button.translate_coordinates(self, 0, 0)
        self.power_window.move(x + bx - 100, y + by - 120)

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

        x, y = self.get_position()
        bx, by = button.translate_coordinates(self, 0, 0)
        self.volume_window.move(x + bx - 50, y + by - 120)


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