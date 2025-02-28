import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from labels import Labels
from actions import *
labels = Labels()

class DropDowns:
    def __init__(self, reset_button, forward_button, backward_button, play_pause_button, dropdown_image, lock_button, power_off_button, hib_button, reboot_button, mic_scale_, volume_scale_, volume_func, mic_func, media_buttons, powerSettingsButton, date_dropdown, search_dropdown, volume_dropdown):
        # self.buttons_ = Buttons.media_buttons()
        # self.media_buttons_ = Buttons.media_buttons()
        self.reset_button = reset_button
        self.forward_button = forward_button
        self.backward_button = backward_button
        self.play_pause_button = play_pause_button
        self.dropdown_image = dropdown_image
        self.lock_button = lock_button
        self.power_off_button = power_off_button
        self.hib_button = hib_button
        self.reboot_button = reboot_button
        self.mic_scale_ = mic_scale_
        self.volume_scale_ = volume_scale_
        self.mic_func = mic_func
        self.volume_func = volume_func
        self.media_buttons = media_buttons
        self.powerSettingsButton = powerSettingsButton
        self.date_dropdown_ = date_dropdown
        self.volume_dropdown_ = volume_dropdown
        self.search_dropdown_ = search_dropdown
        
    def media_dropdown(self, button):
        if hasattr(self, "media_window") and self.media_window:
            self.media_window.destroy()
            self.media_window = None
            return
        
        # self.media_buttons
        # self.media_buttons(self.media_dropdown, pause_play_action_, forward_action, backward_action, reset_action)
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

        labels.dropdown_title_label.set_halign(Gtk.Align.START)

        hig_box.pack_start(self.dropdown_image, True, True, 0)
        hig_box.pack_start(ver_box, False, False, 0)


        ver_box.pack_start(labels.dropdown_artist, False, False, 10)
        labels.dropdown_title_label.set_halign(Gtk.Align.CENTER) 
        ver_box.pack_start(labels.dropdown_title_label, False, False, 0)
        
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

        # self.entry()

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

        hig_box.pack_start(labels.date_label, False, False, 0)

        self.date_window.add(hig_box)
        self.date_window.show_all()

    def power_dropdown(self, button):
        if hasattr(self, "power_window") and self.power_window:
            self.power_window.destroy()
            self.power_window = None
            return
        
        # self.powerSettingsButtons
        # self.powerSettingsButtons(self.power_dropdown, self.power_off, self.reset, self.hibernate, self.lock)
        
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
        grid.attach(labels.power_off_label, 0, 0, 1, 1)

        grid.attach(self.reboot_button, 1, 1, 2, 1)
        grid.attach(labels.reset_label, 0, 1, 1, 1)
        
        grid.attach(self.lock_button, 1, 2, 2, 1)
        grid.attach(labels.lock_label, 0, 2, 1, 1)
        
        grid.attach(self.hib_button, 1, 3, 2, 1)
        grid.attach(labels.hibernate_label, 0, 3, 1, 1)

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


        # self.volume_scale()
        # self.mic_scale()
        # self.mic_func
        # self.volume_func


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

        ver_box.pack_start(labels.volume_label, False, False, 0)
        ver_box.pack_start(self.mic_scale_, False, False, 0)
        
        ver_box.pack_start(labels.mic_label, False, False, 0)
        

        self.volume_window.add(hig_box)
        self.volume_window.set_size_request(250, 50)
        self.volume_window.show_all()