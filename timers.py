import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib 

def timers(update_volume, update_date, update_time, update_image, update_pauseplay, update_network, fetch_updates_async, scales, labels, buttons, images):
    GLib.timeout_add(100, update_volume, scales, labels)
    GLib.timeout_add(1000, update_date, labels)
    GLib.timeout_add(1000, update_time, buttons)
    GLib.timeout_add(100, update_image, labels, images, buttons)
    GLib.timeout_add(100, update_pauseplay, buttons)
    GLib.timeout_add(100, update_network, labels)
    GLib.timeout_add(100, fetch_updates_async, buttons)