import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Labels:
    def __init__(self):
        self.labels()

    def labels(self):
        self.powerSettingsLabel()
        self.date_label_()
        self.dropdown_labels()
        self.volumeLabels()
        self.show_network()


    def powerSettingsLabel(self):
        self.power_off_label = Gtk.Label(label = 'Power Off  ')
        self.power_off_label.get_style_context().add_class('PowerOfflabel')
        
        self.reset_label = Gtk.Label(label = 'Reboot')
        self.reset_label.get_style_context().add_class('Resetlabel')
        
        self.lock_label = Gtk.Label(label = 'Lock')
        self.lock_label.get_style_context().add_class('LockLabel')
        
        self.hibernate_label = Gtk.Label(label = 'hibernate')
        self.hibernate_label.get_style_context().add_class('HibernateLabel')

    def dropdown_labels(self):
        self.dropdown_title_label = Gtk.Label()
        self.dropdown_title_label.get_style_context().add_class('DropdownTitle')
        self.dropdown_title_label.set_hexpand(False)
        self.dropdown_title_label.set_hexpand(False)
        
        self.dropdown_artist = Gtk.Label()
        self.dropdown_artist.get_style_context().add_class('DropdownArtist')
        
    def date_label_(self):
        self.date_label = Gtk.Label()
        self.date_label.get_style_context().add_class('Date')
    
    def volumeLabels(self):
        self.volume_label = Gtk.Label()
        self.volume_label.get_style_context().add_class('VolumeLabel')
        
        self.mic_label = Gtk.Label(label = "󰍬")
        self.mic_label.get_style_context().add_class('MicLabel')

    def show_network(self):
        self.network_label = Gtk.Label()
        self.network_label.get_style_context().add_class('Wifi')
        self.network_label.set_has_tooltip(True)
        self.network_label.connect("query-tooltip", self.on_query_tooltip)
        self.tooltip_text = "Checking..."

    def on_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text(self.tooltip_text)
        return True