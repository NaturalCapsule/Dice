import json
import subprocess
import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from functools import partial

# def terminal(command, button):
#     subprocess.Popen(command, shell = True)
def terminal(command, button):
    if command:
        subprocess.Popen(command, shell=True)
    else:
        print("No command provided!")


def load_css():
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path('config/style.css')
    
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)

def load(file_path, left_layout, middle_layout, right_layout, buttons, labels, bar_image, workspaces):
    try:
        with open(file_path, "r") as file:
            widgets = json.load(file)
    
            for widget in widgets['widgets']:
                layout_target = widget.get("layout", "SELECT A LAYOUT")
                widget_item = None

                if "media" in widget:
                    if widget["media"] == "show media":
                        widget_item = buttons.media_button
                        if layout_target == "left":
                            left_layout.pack_start(bar_image, False, False, 0)
                            left_layout.pack_start(widget_item, False, False, 0)
                        elif layout_target == "right":
                            right_layout.pack_start(bar_image, False, False, 0)
                            right_layout.pack_start(widget_item, False, False, 0)
                        elif layout_target == "middle":
                            middle_layout.pack_start(bar_image, False, False, 0)
                            middle_layout.pack_start(widget_item, False, False, 0)
                        continue 
                
                elif "wifi" in widget:
                    if widget["wifi"] == "show wifi":
                            widget_item = labels.network_label
                            if widget.get("onlineIcon") and widget.get("offlineIcon"):
                                labels.offline_icon = widget["offlineIcon"]
                                labels.online_icon = widget["onlineIcon"]
                                wifi_con = labels.wifi_icon
                                widget_item = wifi_con



   
                elif "package" in widget:
                    if widget["package"] == "show package":
                        widget_item = buttons.package_button_
                
                elif "time" in widget:
                    if widget["time"] == "show time":
                        widget_item = buttons.time_button

                elif "power menu" in widget:
                    if widget["power menu"] == "show power menu":
                        widget_item = buttons.power_settings
                
                elif "volume" in widget:
                    if widget["volume"] == "show volume":
                        widget_item = buttons.volume_control

                elif widget.get('workspaces') == "show workspaces":
                    for workspace_button in workspaces:
                        layout_target = widget['layout']
                        if layout_target == 'left':
                            left_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'right':
                            right_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'middle':
                            middle_layout.pack_start(workspace_button, False, False, 0)

                elif "type" in widget:
                    if widget["type"] == "label":
                        widget_item = Gtk.Label(label = widget["text"])
                        widget_item.get_style_context().add_class(widget["name"])

                    elif widget["type"] == "button":
                        widget_item = Gtk.Button(label = widget['text'])
                        widget_item.get_style_context().add_class(widget["name"])
                        if widget["action"] != "":
                            widget_item.connect("clicked", partial(terminal, widget["action"]))

                if widget_item:
                    if layout_target == "left":
                        left_layout.pack_start(widget_item, False, False, 0)
                    elif layout_target == "right":
                        right_layout.pack_start(widget_item, False, False, 0)
                    elif layout_target == "middle":
                        middle_layout.pack_start(widget_item, False, False, 0)

        
        load_css()
    except Exception as e:
        print("Error Loading Widget", e)