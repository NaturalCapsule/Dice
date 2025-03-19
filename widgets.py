import json
import subprocess
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from functools import partial
from updates import *

def terminal(command, button):
    if command:
        subprocess.Popen(command, shell=True)
    else:
        print("No command provided!")


def load_css():
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(f'/home/{os.getlogin()}/.config/bar/config/style.css')
    
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
)

# def load(file_path, left_layout, middle_layout, right_layout, buttons, labels, bar_image, workspaces: list, custom_workspace: list):
#     try:
#         with open(file_path, "r") as file:
#             widgets = json.load(file)
    
#             for widget in widgets['widgets']:
#                 layout_target = widget.get("layout", "SELECT A LAYOUT")
#                 widget_item = None

#                 if "media" in widget:
#                     if widget["media"] == "show media":
#                         widget_item = buttons.media_button
#                         if layout_target == "left":
#                             left_layout.pack_start(bar_image, False, False, 0)
#                             left_layout.pack_start(widget_item, False, False, 0)
#                         elif layout_target == "right":
#                             right_layout.pack_start(bar_image, False, False, 0)
#                             right_layout.pack_start(widget_item, False, False, 0)
#                         elif layout_target == "middle":
#                             middle_layout.pack_start(bar_image, False, False, 0)
#                             middle_layout.pack_start(widget_item, False, False, 0)
#                         continue 
                
#                 elif "wifi" in widget:
#                     if widget["wifi"] == "show wifi":
#                             widget_item = labels.network_label
#                             if widget.get("onlineIcon") != "" and widget.get("offlineIcon") !="":
#                                 labels.offline_icon = widget["offlineIcon"]
#                                 labels.online_icon = widget["onlineIcon"]
#                                 wifi_con = labels.custom_wifi
#                                 widget_item = wifi_con

#                 elif "package" in widget:
#                     if widget["package"] == "show package":
#                         widget_item = buttons.package_button_

#                 elif "time" in widget:
#                     if widget["time"] == "show time":
#                         widget_item = buttons.time_button

#                 elif "power menu" in widget:
#                     if widget["power menu"] == "show power menu":
#                         widget_item = buttons.power_settings
#                         if widget['icon'] != "":
#                             buttons.power_settings.set_label(widget['icon'])
                
                
#                 elif "volume" in widget:
#                     if widget["volume"] == "show volume":
#                         widget_item = buttons.volume_control
#                         if widget['icon'] != "":
#                             buttons.volume_control.set_label(widget['icon'])


#                 elif widget.get('workspaces') == "show workspaces":
#                     if widget_item['active icon'] != "" and widget_item['default icon'] != "":
#                         for workspace_button in custom_workspace:
#                             buttons.acitve_icon = widget['active icon']
#                             buttons.default_icon = widget['default icon']
                            
#                             layout_target = widget['layout']
#                             if layout_target == 'left':
#                                 left_layout.pack_start(workspace_button, False, False, 0)
#                             elif layout_target == 'right':
#                                 right_layout.pack_start(workspace_button, False, False, 0)
#                             elif layout_target == 'middle':
#                                 middle_layout.pack_start(workspace_button, False, False, 0)


#                     else:
#                         for workspace_button in workspaces:
#                             layout_target = widget['layout']
#                             if layout_target == 'left':
#                                 left_layout.pack_start(workspace_button, False, False, 0)
#                             elif layout_target == 'right':
#                                 right_layout.pack_start(workspace_button, False, False, 0)
#                             elif layout_target == 'middle':
#                                 middle_layout.pack_start(workspace_button, False, False, 0)

#                 elif "type" in widget:
#                     if widget["type"] == "label":
#                         widget_item = Gtk.Label(label = widget["text"])
#                         widget_item.get_style_context().add_class(widget["name"])

#                     elif widget["type"] == "button":
#                         widget_item = Gtk.Button(label = widget['text'])
#                         widget_item.get_style_context().add_class(widget["name"])
#                         if widget["action"] != "":
#                             widget_item.connect("clicked", partial(terminal, widget["action"]))

#                 if widget_item:
#                     if layout_target == "left":
#                         left_layout.pack_start(widget_item, False, False, 0)
#                     elif layout_target == "right":
#                         right_layout.pack_start(widget_item, False, False, 0)
#                     elif layout_target == "middle":
#                         middle_layout.pack_start(widget_item, False, False, 0)

        
#         load_css()
#     except Exception as e:
#         print("Error Loading Widget", e)


def load(file_path, left_layout, middle_layout, right_layout, buttons, labels, bar_image, workspaces: list, custom_workspace: list):
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
                        if widget.get("onlineIcon") != "" and widget.get("offlineIcon") !="":
                            labels.offline_icon = widget["offlineIcon"]
                            labels.online_icon = widget["onlineIcon"]
                            wifi_con = labels.custom_wifi
                            widget_item = wifi_con

            elif "package" in widget:
                if widget["package"] == "show package":
                    widget_item = buttons.package_button_
                    if widget['icon'] != "":
                        package_icon = widget['icon']
                        buttons.custom_package.set_label(package_icon)
                        widget_item = buttons.custom_package

            elif "time" in widget:
                if widget["time"] == "show time":
                    widget_item = buttons.time_button

            elif "power menu" in widget:
                if widget["power menu"] == "show power menu":
                    widget_item = buttons.power_settings
                    if widget['icon'] != "":
                        buttons.power_settings.set_label(widget['icon'])
            
            
            elif "volume" in widget:
                if widget["volume"] == "show volume":
                    widget_item = buttons.volume_control
                    if widget['icon'] != "":
                        buttons.volume_control.set_label(widget['icon'])


            elif widget.get('workspaces') == "show workspaces":
                if widget['active icon'] != "" and widget['default icon'] != "":
                    for workspace_button in custom_workspace:
                        buttons.active_icon = widget['active icon']
                        buttons.default_icon = widget['default icon']
                        
                        layout_target = widget['layout']
                        if layout_target == 'left':
                            left_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'right':
                            right_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'middle':
                            middle_layout.pack_start(workspace_button, False, False, 0)


                else:
                    for workspace_button in workspaces:
                        layout_target = widget['layout']
                        if layout_target == 'left':
                            left_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'right':
                            right_layout.pack_start(workspace_button, False, False, 0)
                        elif layout_target == 'middle':
                            middle_layout.pack_start(workspace_button, False, False, 0)

            # elif "type" in widget:
            #     if widget["type"] == "label":
            #         if "{gpuUsage}" in widget['text']:
            #             result = widget['text'].replace("{gpuUsage}", get_nvidia_gpu_usage())
            #         widget_item = Gtk.Label(label = result)
            #         widget_item.get_style_context().add_class(widget["name"])

            elif "type" in widget:
                if widget["type"] == "label":
                    if "{gpuUsage}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuUsage}", get_nvidia_total_vram())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                        def update_gpu_usage(label=widget_item, template_text=widget['text']):
                            usage = get_nvidia_gpu_usage()
                            new_text = template_text.replace("{gpuUsage}", usage)
                            label.set_text(new_text)
                            return True

                        GLib.timeout_add(1000, update_gpu_usage)

                    elif "{gpuVram}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuVram}", get_nvidia_total_vram())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])


                    elif "{gpuTemp}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuTemp}", get_nvidia_temp())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                        def update_gpu_tmp(label=widget_item, template_text=widget['text']):
                            temp = get_nvidia_temp()
                            new_text = template_text.replace("{gpuTemp}", temp)
                            label.set_text(new_text)
                            return True

                        GLib.timeout_add(1000, update_gpu_tmp)


                    elif "{gpuPower}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuPower}", get_nvidia_powerdraw())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                        def update_gpu_power(label=widget_item, template_text=widget['text']):
                            temp = get_nvidia_powerdraw()
                            new_text = template_text.replace("{gpuPower}", temp)
                            label.set_text(new_text)
                            return True

                        GLib.timeout_add(1000, update_gpu_power)


                    elif "{gpuUsed}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuUsed}", get_nvidia_used_vram())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                        def update_gpu_used_vram(label=widget_item, template_text=widget['text']):
                            used_vram = get_nvidia_used_vram()
                            new_text = template_text.replace("{gpuUsed}", used_vram)
                            label.set_text(new_text)
                            return True

                        GLib.timeout_add(1000, update_gpu_used_vram)

                    elif "{gpuName}" in widget['text']:
                        print("True")

                        initial_text = widget['text'].replace("{gpuName}", get_nvidia_name())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                    elif "{gpuFan}" in widget['text']:
                        initial_text = widget['text'].replace("{gpuFan}", get_nvidia_used_vram())
                        widget_item = Gtk.Label(label=initial_text)
                        widget_item.get_style_context().add_class(widget["name"])

                        def update_gpu_fan(label=widget_item, template_text=widget['text']):
                            fan = get_nvidia_fanspeed()
                            new_text = template_text.replace("{gpuFan}", fan)
                            label.set_text(new_text)
                            return True

                        GLib.timeout_add(1000, update_gpu_fan)

                    else:
                        widget_item = Gtk.Label(label=widget['text'])
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
    # except Exception as e:
        # print("Error Loading Widget", e)