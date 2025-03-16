# from threading import Timer
from gi.repository import GLib
import subprocess

def poll_active_workspace(set_active_workspace, buttons):
    try:
        result = subprocess.run(['hyprctl', 'activeworkspace'], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "workspace ID" in line:
                current_workspace = int(result.stdout.split()[2])
                # set_active_workspace(current_workspace, buttons)
                GLib.idle_add(set_active_workspace, current_workspace, buttons)
                break

    except (IndexError, ValueError) as e:
        print(e)

    # Timer(0.1, lambda: poll_active_workspace(set_active_workspace, buttons)).start()
    
    GLib.timeout_add(400, poll_active_workspace, set_active_workspace, buttons)
    return False