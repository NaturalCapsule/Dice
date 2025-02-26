import gi
gi.require_version("GtkLayerShell", "0.1")
gi.require_version("Gtk", "3.0")
import cairo
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, Pango, GtkLayerShell
import subprocess
import sys
from media import MediaPlayerMonitor
import os
import time
from network import ssid, get_network
from date import get_calendar_html



class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bar")
        self.initUI()
        self.load_css()
        self.show_all()

    def initUI(self):
        if not GtkLayerShell.is_supported():
            print("Error: Layer Shell not supported. Are you running Wayland?")
            exit(1)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.auto_exclusive_zone_enable(self)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 10)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        self.get_style_context().add_class('window')

        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        screen_hight = screen.get_height()
        
        taskbar_height = 20
        width_gap = 10

        self.set_default_size(screen_width - (2 * width_gap), taskbar_height)


        self.media = MediaPlayerMonitor()
        self.dropdown_image = Gtk.Image()
        
        self.dropdown_image.get_style_context().add_class('DropdownImage')
        self.bar_image = Gtk.Image()
        self.bar_image.get_style_context().add_class('BarImage')


        GLib.timeout_add(100, self.update_image)

        self.labels()
        self.buttons()
 
        self.show_network()
        self.layouts()
        self.update_title()

        GLib.timeout_add(100, self.update_volume)

        GLib.timeout_add(100, self.update_date)

        GLib.timeout_add(100, self.update_time)
        GLib.timeout_add(100, self.update_image)
        GLib.timeout_add(100, self.update_pauseplay)
        GLib.timeout_add(100, self.update_network)
        GLib.timeout_add(100, self.update_title)


    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('/home/naturalcapsule/python/FlXBar/config/style.css')
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    def layouts(self):
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_box)

        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.middle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.left_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.main_box.pack_start(self.left_box, False, False, 0)
        self.main_box.pack_start(self.left_spacer, True, True, 0)
        self.main_box.pack_start(self.middle_box, False, False, 0)
        self.main_box.pack_start(self.right_spacer, True, True, 20)
        self.main_box.pack_start(self.right_box, False, False, 0)

        self.middle_box.set_halign(Gtk.Align.CENTER)


        for button in self.left_buttons:
            self.left_box.pack_start(button, False, False, 0)

        for button in self.middle_buttons:
            self.middle_box.pack_start(button, True, False, 0)
            
        self.right_box.pack_start(self.network_label, False, False, 0)

        for button in self.right_buttons:
            self.right_box.pack_start(button, False, False, 0)
    
    def buttons(self):
        self.left_buttons = []
        self.right_buttons = []
        self.middle_buttons = []

        self.time_button = Gtk.Button()
        self.time_button.get_style_context().add_class('timeButton')
        self.time_button.connect('clicked', self.date_dropdown)
        self.right_buttons.append(self.time_button)
            
        self.middle_buttons.append(self.bar_image)
        
            
        self.media_button = Gtk.Button()
        self.media_button.get_style_context().add_class('mediaButton')
        self.media_button.connect("clicked", self.media_dropdown)
        
        self.middle_buttons.append(self.media_button)
        
        self.play_pause_button = Gtk.Button()
        self.play_pause_button.get_style_context().add_class('playPauseButton')
        self.play_pause_button.connect('clicked', self.pause_play_action_)

        self.forward_button = Gtk.Button(label = '')
        self.forward_button.get_style_context().add_class('forwardButton')
        self.forward_button.connect('clicked', self.forward_action)
        
        self.backward_button = Gtk.Button(label = '')
        self.backward_button.get_style_context().add_class('backwardButton')
        self.backward_button.connect('clicked', self.backward_action)
        
        
        self.reset_button = Gtk.Button(label = '󱞳')
        self.reset_button.get_style_context().add_class('resetDropdownButton')
        self.reset_button.connect('clicked', self.reset_action)
    
        self.volume_control = Gtk.Button(label = '󱄡')
        self.volume_control.get_style_context().add_class('VolumeControlButton')
        self.volume_control.connect('clicked', self.volume_dropdown)
        self.right_buttons.append(self.volume_control)
        
        
        self.workspace1 = Gtk.Button(label = '󰤂')
        self.workspace1.get_style_context().add_class('workspace1')
        self.workspace1.connect('clicked', self.workspace_1)
        
        
        self.workspace2 = Gtk.Button(label = '󰤂')
        self.workspace2.get_style_context().add_class('workspace2')
        self.workspace2.connect('clicked', self.workspace_2)
        
        
        self.workspace3 = Gtk.Button(label = '󰤂')
        self.workspace3.get_style_context().add_class('workspace3')
        self.workspace3.connect('clicked', self.workspace_3)
        
        
        self.workspace4 = Gtk.Button(label = '󰤂')
        self.workspace4.get_style_context().add_class('workspace4')
        self.workspace4.connect('clicked', self.workspace_4)
        
        
        self.workspace5 = Gtk.Button(label = '󰤂')
        self.workspace5.get_style_context().add_class('workspace5')
        self.workspace5.connect('clicked', self.workspace_5)
        
        
        self.left_buttons.append(self.workspace1)
        self.left_buttons.append(self.workspace2)
        self.left_buttons.append(self.workspace3)
        self.left_buttons.append(self.workspace4)
        self.left_buttons.append(self.workspace5)

        self.power_settings = Gtk.Button(label = '󰐦')
        self.power_settings.get_style_context().add_class('powerSettings')
        self.power_settings.connect('clicked', self.power_dropdown)
        self.right_buttons.append(self.power_settings)

        self.power_off_button = Gtk.Button(label = '󰐥')
        self.power_off_button.get_style_context().add_class('powerOffButton')
        self.power_off_button.connect('clicked', self.power_off)
        
        self.reboot_button = Gtk.Button(label = '󰜉')
        self.reboot_button.get_style_context().add_class('RebootButton')
        self.reboot_button.connect('clicked', self.reset)
        
        self.hib_button = Gtk.Button(label = '󰤁')
        self.hib_button.get_style_context().add_class('hibButton')
        self.hib_button.connect('clicked', self.hibernate)
        
        self.lock_button = Gtk.Button(label = '󰌾')
        self.lock_button.get_style_context().add_class('LockButton')
        self.lock_button.connect('clicked', self.lock)

        self.search_button = Gtk.Button(label = '󰜏')
        self.search_button.set_tooltip_text('Search from FireFox')
        self.search_button.get_style_context().add_class('SearchButton')
        self.search_button.connect('clicked', self.search_dropdown)
        self.left_buttons.append(self.search_button)

    def entry(self):
        self.entry_ = Gtk.Entry()
        self.entry_.get_style_context().add_class('SearchEntry')
        self.entry_.connect("activate", self.on_entry_activate)
        self.entry_.grab_focus()

    def on_entry_activate(self, widget):
        subprocess.run(['firefox', f'https://www.google.com/search?q={widget.get_text()}'])
        widget.set_text('')

    def power_off(self, button):
        subprocess.run(['shutdown', 'now'])
    
    def reset(self, button):
        subprocess.run(['reboot'])
    
    def lock(self, button):
        subprocess.run(['hyprlock'])
    
    def hibernate(self, button):
        subprocess.run(['systemctl', 'hibernate'])

    def switch_workspace(self, workspace_num):
        subprocess.run(['hyprctl', 'dispatch', 'workspace', str(workspace_num)])
        
        self.set_active_workspace(workspace_num)

    def workspace_1(self, button):
        self.switch_workspace(1)

    def workspace_2(self, button):
        self.switch_workspace(2)

    def workspace_3(self, button):
        self.switch_workspace(3)

    def workspace_4(self, button):
        self.switch_workspace(4)

    def workspace_5(self, button):
        self.switch_workspace(5)

    def set_active_workspace(self, workspace_num):
        self.workspace1.get_style_context().remove_class('active')
        self.workspace2.get_style_context().remove_class('active')
        self.workspace3.get_style_context().remove_class('active')
        self.workspace4.get_style_context().remove_class('active')
        self.workspace5.get_style_context().remove_class('active')

        if workspace_num == 1:
            self.workspace1.get_style_context().add_class('active')
        elif workspace_num == 2:
            self.workspace2.get_style_context().add_class('active')
        elif workspace_num == 3:
            self.workspace3.get_style_context().add_class('active')
        elif workspace_num == 4:
            self.workspace4.get_style_context().add_class('active')
        elif workspace_num == 5:
            self.workspace5.get_style_context().add_class('active')

    def volume_scale(self):
        self.volume_scale_ = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.volume_scale_.get_style_context().add_class('VolumeScale')
        self.volume_scale_.set_value(50)
        self.volume_scale_.set_vexpand(True)
        self.volume_scale_.set_hexpand(True)
        self.volume_scale_.set_size_request(200, 50)
        self.volume_scale_.set_digits(0)
        self.volume_scale_.set_draw_value(False)

        self.volume_scale_.connect("value-changed", self.on_volume_value_changed)

    def mic_scale(self):
        self.mic_scale_ = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.mic_scale_.get_style_context().add_class('MicScale')
        self.mic_scale_.set_value(50)
        self.mic_scale_.set_hexpand(False)
        self.mic_scale_.set_size_request(200, 50)
        self.mic_scale_.set_vexpand(True)
        self.mic_scale_.set_digits(0)
        self.mic_scale_.set_draw_value(False)

        self.mic_scale_.connect("value-changed", self.on_mic_value_changed)



    def on_volume_value_changed(self, widget):
        value = max(0, min(100, int(widget.get_value())))

        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{value}%'])
        
    def on_mic_value_changed(self, widget):
        value = max(0, min(100, int(widget.get_value())))

        subprocess.run(['pactl', 'set-source-volume', '@DEFAULT_SOURCE@', f'{value}%'])
        
        
    def media_dropdown(self, button):
        if hasattr(self, "media_window") and self.media_window:
            self.media_window.destroy()
            self.media_window = None
            return
        
        self.buttons()
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

        self.dropdown_title_label.set_halign(Gtk.Align.START)

        hig_box.pack_start(self.dropdown_image, True, True, 0)
        hig_box.pack_start(ver_box, False, False, 0)


        ver_box.pack_start(self.dropdown_artist, False, False, 10)
        self.dropdown_title_label.set_halign(Gtk.Align.CENTER) 
        ver_box.pack_start(self.dropdown_title_label, False, False, 0)
        
        fixed.put(self.reset_button, 70, 40)
        fixed.put(self.forward_button, 100, 10)
        fixed.put(self.play_pause_button, 70, 10)
        fixed.put(self.backward_button, 40, 10)
        
        
        ver_box.pack_start(fixed, True, True, 0)

        self.media_window.add(hig_box)
        self.media_window.show_all()

    def search_dropdown(self, button):
        if hasattr(self, "search_window") and self.search_window:
            self.search_window.destroy()
            self.search_window = None
            return

        self.entry()

        hig_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hig_box.pack_start(self.entry_, False, False, 0)

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

        hig_box.pack_start(self.date_label, False, False, 0)

        self.date_window.add(hig_box)
        self.date_window.show_all()

    def power_dropdown(self, button):
        if hasattr(self, "power_window") and self.power_window:
            self.power_window.destroy()
            self.power_window = None
            return
        
        self.buttons()
        
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


        grid.attach(self.power_off_button, 1, 0, 2, 1)
        grid.attach(self.power_off_label, 0, 0, 1, 1)

        grid.attach(self.reboot_button, 1, 1, 2, 1)
        grid.attach(self.reset_label, 0, 1, 1, 1)
        
        grid.attach(self.lock_button, 1, 2, 2, 1)
        grid.attach(self.lock_label, 0, 2, 1, 1)
        
        grid.attach(self.hib_button, 1, 3, 2, 1)
        grid.attach(self.hibernate_label, 0, 3, 1, 1)

        self.power_window.add(grid)
        
        self.power_window.show_all()

    def volume_dropdown(self, button):
        if hasattr(self, "volume_window") and self.volume_window:
            if self.volume_scale_ and self.mic_scale_:
                self.mic_scale_.destroy()
                self.volume_scale_.destroy()
                self.volume_scale_ = None
                self.mic_scale_ = None
                
            self.volume_window.destroy()
            self.volume_window = None

            return


        self.volume_scale()
        self.mic_scale()


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
        ver_box.pack_start(self.volume_scale_, False, True, 0)

        ver_box.pack_start(self.volume_label, False, False, 0)
        ver_box.pack_start(self.mic_scale_, False, False, 0)
        
        ver_box.pack_start(self.mic_label, False, False, 0)
        

        self.volume_window.add(hig_box)
        self.volume_window.set_size_request(250, 50)
        self.volume_window.show_all()

    def create_circular_pixbuf(self, pixbuf):
        width, height = pixbuf.get_width(), pixbuf.get_height()
        radius = min(width, height) // 2

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.set_operator(cairo.Operator.SOURCE)
        ctx.paint()

        ctx.set_operator(cairo.Operator.OVER)
        ctx.arc(width // 2, height // 2, radius, 0, 2 * 3.1416)
        ctx.clip()

        gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
        ctx.set_source_surface(gdk_cairo, 0, 0)
        ctx.paint()

        return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)


    def create_eaten_pixbuf(self, pixbuf):
        width, height = pixbuf.get_width(), pixbuf.get_height()

        corner_radius = 30

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.set_operator(cairo.Operator.SOURCE)
        ctx.paint()

        ctx.set_operator(cairo.Operator.OVER)
        ctx.move_to(corner_radius, 0)
        ctx.line_to(width - corner_radius, 0)
        ctx.arc(width - corner_radius, corner_radius, corner_radius, 3 * 3.1416 / 2, 2 * 3.1416)
        ctx.line_to(width, height - corner_radius)
        ctx.arc(width - corner_radius, height - corner_radius, corner_radius, 0, 3.1416 / 2)
        ctx.line_to(corner_radius, height)
        ctx.arc(corner_radius, height - corner_radius, corner_radius, 3.1416 / 2, 3.1416)
        ctx.line_to(0, corner_radius)
        ctx.arc(corner_radius, corner_radius, corner_radius, 3.1416, 3 * 3.1416 / 2)
        ctx.close_path()

        bite_radius = corner_radius // 2  
        bite_angle_start = 1.5 
        bite_angle_end = 2.0   

        ctx.arc(corner_radius, corner_radius, bite_radius, bite_angle_start * 3.1416, bite_angle_end * 3.1416)
        ctx.line_to(corner_radius, corner_radius)

        ctx.clip()

        gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
        ctx.set_source_surface(gdk_cairo, 0, 0)

        ctx.paint()

        return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)

    def update_volume(self):
        if not hasattr(self, 'volume_scale_') or self.volume_scale_ is None:
            return True
        
        value = int(self.volume_scale_.get_value())
        
        if value == 0:
            self.volume_label.set_text('󰕿')
        elif value <= 25:
            self.volume_label.set_text('󰖀')
        elif value <= 50:
            self.volume_label.set_text('󰕾')
        elif value <= 75:
            self.volume_label.set_text('')  

        return True

    def update_time(self):
        current_time = time.strftime('%H 󰇙 %M')
        self.time_button.set_label(current_time)

    def update_date(self):
        date = get_calendar_html()
        self.date_label.set_markup(date)


    def update_image(self):
        self.media.monitor()
        
        
        if self.media.current_player:
            thumbnail = self.media.art_url.replace('file:///', '/')
            if thumbnail and os.path.exists(thumbnail):
                
                self.dropdown_title_label.set_label(self.media.title_)
                self.dropdown_artist.set_text(self.media.artist)
                self.media_tool_tip = f'Now Playing: {self.media.title_}\n          By\n{self.media.artist}'
                

                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 50, 50)
                circular_pixbuf = self.create_circular_pixbuf(pixbuf)

                pixbuf_ = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 400, 200)
                eaten_pixbuf = self.create_eaten_pixbuf(pixbuf_)


                if circular_pixbuf and eaten_pixbuf:
                    self.bar_image.set_from_pixbuf(circular_pixbuf)
                    self.bar_image.set_has_tooltip(True)
                    self.bar_image.connect("query-tooltip", self.media_tooltip)

                    self.dropdown_image.set_from_pixbuf(eaten_pixbuf)
                
                else:
                    print("Error")
        return True

    def update_title(self):
        self.media.monitor()
        if self.media.current_player:
            if len(self.media.title_) >= 10:
                text = f"{self.media.title_[:10]}..."
            else:
                text = self.media.title_
        else:
            text = ''
        self.media_button.set_label(str(text))
        
        return True

    def forward_action(self, button):
        self.media.forward_10_seconds()

    def reset_action(self, button):
        self.media.reset()

    def backward_action(self, button):
        self.media.backward_10_seconds()

    def pause_play_action_(self, button):
        self.media.pause_play_action()

    def update_pauseplay(self):
        if self.media.playback_status == 'Paused':
            self.play_pause_button.set_label('')
        elif self.media.playback_status == 'Playing':
            self.play_pause_button.set_label('')
    
        return True


    def labels(self):
        self.dropdown_title_label = Gtk.Label()
        self.dropdown_title_label.get_style_context().add_class('DropdownTitle')
        self.dropdown_title_label.set_hexpand(False)
        self.dropdown_title_label.set_hexpand(False)
        
        self.dropdown_artist = Gtk.Label()
        self.dropdown_artist.get_style_context().add_class('DropdownArtist')
        
        self.date_label = Gtk.Label()
        self.date_label.get_style_context().add_class('Date')
        
        self.volume_label = Gtk.Label()
        self.volume_label.get_style_context().add_class('VolumeLabel')
        
        self.mic_label = Gtk.Label(label = "󰍬")
        self.mic_label.get_style_context().add_class('MicLabel')
        
        self.power_off_label = Gtk.Label(label = 'Power Off  ')
        self.power_off_label.get_style_context().add_class('PowerOfflabel')
        
        self.reset_label = Gtk.Label(label = 'Reboot')
        self.reset_label.get_style_context().add_class('Resetlabel')
        
        self.lock_label = Gtk.Label(label = 'Lock')
        self.lock_label.get_style_context().add_class('LockLabel')
        
        self.hibernate_label = Gtk.Label(label = 'hibernate')
        self.hibernate_label.get_style_context().add_class('HibernateLabel')
        

    
    def show_network(self):
        self.network_label = Gtk.Label()
        self.network_label.get_style_context().add_class('Wifi')
        self.network_label.set_has_tooltip(True)
        self.network_label.connect("query-tooltip", self.on_query_tooltip)
        self.tooltip_text = "Checking..."
    
    def update_network(self):
        ssid_ = ssid()
        network = get_network()

        if network:
            self.network_label.set_text("󰤨")
            self.tooltip_text = ssid_
        else:
            self.network_label.set_text("󰤭")
            self.network_label.set_text("󰤭")
            
            self.tooltip_text = "No Connection"

        return True

    def media_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text(self.media_tool_tip)
        return True

    def on_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text(self.tooltip_text)
        return True


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
