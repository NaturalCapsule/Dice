# import json
# import socket
# import os
# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, Gio, GdkPixbuf

# def get_hyprland_socket_path():
#     socket_path = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    
#     if not socket_path:
#         print("Error: HYPRLAND_INSTANCE_SIGNATURE environment variable not found")
#         print("Are you running this script in a Hyprland session?")
#         return None
    
#     uid = os.getuid()
    
#     possible_paths = [
#         f"/tmp/hypr/{socket_path}/.socket2.sock",
#         f"/run/user/{uid}/hypr/{socket_path}/.socket2.sock",
#         os.path.expanduser(f"~/.hypr/{socket_path}/.socket2.sock"),
#         f"/tmp/hypr/{socket_path}/.socket.sock",
#         f"/run/user/{uid}/hypr/{socket_path}/.socket.sock",
#     ]
    
#     for path in possible_paths:
#         if os.path.exists(path):
#             return path
    
#     print("Error: Couldn't locate Hyprland socket file.")
#     print(f"Tried the following paths: {possible_paths}")
#     return None

# def get_active_window_class():
#     hypr_socket = get_hyprland_socket_path()
#     if not hypr_socket:
#         return None
    
#     sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
#     try:
#         sock.connect(hypr_socket)
        
#         sock.send(b"activewindow\n")
        
#         response = sock.recv(1024).decode('utf-8')
        
#         if not response or response.strip() == "":
#             print("No response from Hyprland socket")
#             return None
            
#         if response.startswith('{') and response.endswith('}'):
#             try:
#                 window_info = json.loads(response)
#                 app_class = window_info.get("class")
#                 return app_class
#             except json.JSONDecodeError:
#                 print(f"Failed to parse response as JSON: {response}")
        
#         if ">>" in response:
#             parts = response.split(">>")
#             if len(parts) >= 2:
#                 app_info = parts[1].split(',')
#                 if app_info:
#                     return app_info[0]
        
#         print(f"Unrecognized response format: {response}")
#         return None
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
    
#     finally:
#         sock.close()

# def get_icon_path_from_class(app_class):
#     if not app_class:
#         return None

#     if not Gtk.init_check():
#         print("Warning: GTK failed to initialize")
#         return None

#     icon_theme = Gtk.IconTheme.get_default()
    
#     if icon_theme is None:
#         # print("Error: Gtk.IconTheme.get_default() returned None")
#         return None

#     icon_info = icon_theme.lookup_icon(app_class.lower(), 48, 0)
#     if icon_info:
#         return icon_info.get_filename()

#     else:
#         return None



# def get_active_window_icon():
#     app_class = get_active_window_class()
#     if not app_class:
#         return None
    
#     icon_path = get_icon_path_from_class(app_class)
#     return icon_path






import json
import socket
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


def get_hypr_socket():
    socket_path = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    
    if not socket_path:
        print("Error: HYPRLAND_INSTANCE_SIGNATURE environment variable not found")
        print("Are you running this script in a Hyprland session?")
        return None
    
    uid = os.getuid()
    
    possible_paths = [
        f"/tmp/hypr/{socket_path}/.socket2.sock",
        f"/run/user/{uid}/hypr/{socket_path}/.socket2.sock",
        os.path.expanduser(f"~/.hypr/{socket_path}/.socket2.sock"),
        f"/tmp/hypr/{socket_path}/.socket.sock",
        f"/run/user/{uid}/hypr/{socket_path}/.socket.sock",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    print("Error: Couldn't locate Hyprland socket file.")
    print(f"Tried the following paths: {possible_paths}")
    return None

def get_active_window_class():
    hypr_socket = get_hypr_socket()
    if not hypr_socket:
        return None

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        sock.connect(hypr_socket)
        
        sock.send(b"activewindow\n")
        
        # Receive the response
        response = sock.recv(1024).decode('utf-8')
        if not response or response.strip() == "":
            print("No response from Hyprland socket")
            return None
            
        if response.startswith('{') and response.endswith('}'):
            try:
                window_info = json.loads(response)
                app_class = window_info.get("class")
                return app_class
            except json.JSONDecodeError:
                print(f"Failed to parse response as JSON: {response}")
        
        if ">>" in response:
            parts = response.split(">>")
            if len(parts) >= 2:
                app_info = parts[1].split(',')
                if app_info:
                    return app_info[0]
        
        print(f"Unrecognized response format: {response}")
        return None

    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    finally:
        sock.close()

def get_icon_path_from_class(app_class):
    Gtk.init([])
    
    icon_theme = Gtk.IconTheme.get_default()
    
    icon_info = icon_theme.lookup_icon(app_class.lower(), 48, 0)
    if icon_info:
        return icon_info.get_filename()
    
    icon_info = icon_theme.lookup_icon(app_class, 48, 0)
    if icon_info:
        return icon_info.get_filename()
    
    app_info = Gio.DesktopAppInfo.new(f"{app_class.lower()}.desktop")
    if app_info:
        icon = app_info.get_icon()
        if icon:
            if isinstance(icon, Gio.ThemedIcon):
                icon_names = icon.get_names()
                if icon_names:
                    icon_info = icon_theme.lookup_icon(icon_names[0], 48, 0)
                    if icon_info:
                        return icon_info.get_filename()

    return None

def get_active_window_icon():
    app_class = get_active_window_class()
    if not app_class:
        return None
    
    icon_path = get_icon_path_from_class(app_class)
    return icon_path

