import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib 

def timers(update_volume, update_date, update_time, update_image, update_pauseplay, update_network, update_title, fetch_updates_async, update_activeWindow, scales, labels, buttons, images , play_pause_button, poll_active_workspace, set_active_workspace, use_volume, use_wifi, use_workspace, use_active_icon, use_media, use_date):
    if use_volume == 'true':
        GLib.timeout_add(100, update_volume, scales, labels)
    if use_date == 'true':
        GLib.timeout_add(1000, update_date, labels)
        GLib.timeout_add(1000, update_time, buttons)
    if use_media == 'true':
        GLib.timeout_add(1000, update_title, buttons)
        GLib.timeout_add(500, update_image, labels, images, buttons)
        GLib.timeout_add(100, update_pauseplay, play_pause_button)
        GLib.timeout_add(100, fetch_updates_async, buttons)
    if use_wifi == 'true':
        GLib.timeout_add(1000, update_network, labels)
    if use_workspace == 'true':
        GLib.timeout_add(400, poll_active_workspace, set_active_workspace, buttons)
    if use_active_icon == 'true':
        GLib.timeout_add(250, update_activeWindow, images)
