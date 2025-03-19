import gi
import os
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from configparser import ConfigParser

config = ConfigParser()
config.read(f'/home/{os.getlogin()}/.config/gtk-3.0/settings.ini')


def gtk_mouse():
    mouse_cursor = config.get('Settings', 'gtk-cursor-theme-name')
    mouse_size = config.getint('Settings', 'gtk-cursor-theme-size')
    Gtk.Settings.get_default().set_property("gtk-cursor-theme-name", mouse_cursor)
    Gtk.Settings.get_default().set_property("gtk-cursor-theme-size", mouse_size)
