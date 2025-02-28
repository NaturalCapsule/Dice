import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess

class Scales:
    def __init__(self):
        self.volume_scale()
        self.mic_scale()
    
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
        