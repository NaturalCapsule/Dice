import json
import socket
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf

def get_hyprland_socket_path():
    socket_path = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    
    if not socket_path:
        print("Error: HYPRLAND_INSTANCE_SIGNATURE environment variable not found")
        print("Are you running this script in a Hyprland session?")
        return None
    
    # Get user ID for constructing path
    uid = os.getuid()
    
    # Check all possible socket locations
    possible_paths = [
        f"/tmp/hypr/{socket_path}/.socket2.sock",
        f"/run/user/{uid}/hypr/{socket_path}/.socket2.sock",
        os.path.expanduser(f"~/.hypr/{socket_path}/.socket2.sock"),
        f"/tmp/hypr/{socket_path}/.socket.sock",  # Alternative socket file
        f"/run/user/{uid}/hypr/{socket_path}/.socket.sock",
        # Add any other potential locations your system might use
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    print("Error: Couldn't locate Hyprland socket file.")
    print(f"Tried the following paths: {possible_paths}")
    return None

def get_active_window_class():
    # Get the Hyprland socket path
    hypr_socket = get_hyprland_socket_path()
    if not hypr_socket:
        return None
    
    # Create a socket connection
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        # Connect to the Hyprland socket
        sock.connect(hypr_socket)
        
        # Send the command to get active window
        sock.send(b"activewindow\n")
        
        # Receive the response
        response = sock.recv(1024).decode('utf-8')
        
        if not response or response.strip() == "":
            print("No response from Hyprland socket")
            return None
            
        # Check if the response is in JSON format
        if response.startswith('{') and response.endswith('}'):
            try:
                window_info = json.loads(response)
                app_class = window_info.get("class")
                return app_class
            except json.JSONDecodeError:
                print(f"Failed to parse response as JSON: {response}")
        
        # Handle non-JSON format (format: "activewindow>>app_class,window_title")
        if ">>" in response:
            parts = response.split(">>")
            if len(parts) >= 2:
                app_info = parts[1].split(',')
                if app_info:
                    return app_info[0]  # Return the first part which is the app class
        
        print(f"Unrecognized response format: {response}")
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    finally:
        sock.close()

def get_icon_path_from_class(app_class):
    if not app_class:
        return None

    if not Gtk.init_check():
        print("Warning: GTK failed to initialize")
        return None

    # Get the default icon theme
    icon_theme = Gtk.IconTheme.get_default()
    
    if icon_theme is None:
        # print("Error: Gtk.IconTheme.get_default() returned None")
        return None

    # print("Available Icon Themes:", icon_theme.get_search_path())

    # Check if the requested icon exists
    icon_info = icon_theme.lookup_icon(app_class.lower(), 48, 0)
    if icon_info:
        return icon_info.get_filename()
    else:
        print(f"Icon '{app_class.lower()}' not found in theme.")

    # Try with different case variations
    icon_info = icon_theme.lookup_icon(app_class, 48, 0)
    if icon_info:
        return icon_info.get_filename()
    else:
        print(f"Icon '{app_class}' not found in theme.")

    return None



def get_active_window_icon():
    # Get the class of the active window
    app_class = get_active_window_class()
    if not app_class:
        return None
    
    # Get the icon path from the class
    icon_path = get_icon_path_from_class(app_class)
    return icon_path
