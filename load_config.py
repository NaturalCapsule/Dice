import json
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from functools import partial

def terminal(command):
    subprocess.Popen(command, shell = True)

def load(file_path, left_layout, middle_layout, right_layout, buttons, labels):
    try:
        with open(file_path, "r") as file:
            widgets = json.load(file)
    
            for widget in widgets['widgets']:
                layout_target = widget.get("layout", "SELECT A LAYOUT")
                widget_item = None
                
                if "media" in widget:
                    widget_item = labels.wifi_label
                    if widget.get("onlineIcon") and widget.get("offlineIcon"):
                        labels.offline_icon = widget["offlineIcon"]
                        labels.online_icon = widget["onlineIcon"]
                        wifi_con = labels.wifi_icon
                        widget_item = wifi_con
                        
                        
                elif "time" in widget:
                    widget_item = labels.time_label

                elif "type" in widget:
                    if widget["type"] == "label":
                        widget_item = Gtk.Label(widget["text"])
                        widget_item.get_style_context().add_class(widget["name"])

                elif widget["type"] == "button":
                    widget_item = Gtk.Button(widget["text"])
                    widget_item.get_style_context().add_class(widget["name"])
                    if "action" in widget:
                        widget_item.clicked.connect(partial(terminal, widget["action"]))
                
            if widget_item:
                if layout_target == "left":
                    left_layout.pack_start(widget_item, False, False, 0)
                elif layout_target == "right":
                    right_layout.pack_start(widget_item, False, False, 0)
                elif layout_target == "middle":
                    middle_layout.pack_start(widget_item, False, False, 0)


        # for widget in widgets['widgets']:
        #     if widget.get('workspaces') == "show workspaces":
        #         for dock_button in docks:
        #             layout_target = widget['layout']
        #             if layout_target == 'left':
        #                 left_layout.addWidget(dock_button)
        #             elif layout_target == 'right':
        #                 right_layout.addWidget(dock_button)
        #             elif layout_target == 'middle':
        #                 middle_layout.addSpacing(20)
        #                 middle_layout.addWidget(dock_button)
    except Exception as e:
        print("Error Loading Widget", e)