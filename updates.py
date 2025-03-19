import time
import gi
import os
import threading
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from gi.repository import GdkPixbuf
from media import MediaPlayerMonitor
import hashlib
from date import get_calendar_html
from network import *
import urllib.request
import tempfile
import re
media = MediaPlayerMonitor()
# title_name = None


def update_volume(scales, labels):
    if not hasattr(scales, 'volume_scale_') or scales.volume_scale_ is None:
        return True
    
    value = int(scales.volume_scale_.get_value())
    
    if value == 0:
        labels.volume_label.set_text('󰕿')
    elif value <= 25:
        labels.volume_label.set_text('󰖀')
    elif value <= 50:
        labels.volume_label.set_text('󰕾')
    elif value <= 75:
        labels.volume_label.set_text('')  

    return True

def update_time(buttons):
    current_time = time.strftime('%H 󰇙 %M')
    buttons.time_button.set_label(current_time)
    return True

def update_date(labels):
    date = get_calendar_html()
    labels.date_label.set_markup(date)
    return True

media_tool_tip = 'No Active media is playing!'

title_name = ''
player_name = ''

def get_cached_filename(title):
    hashed = hashlib.md5(title.encode()).hexdigest()
    return f"/tmp/{hashed}.jpg"


def safe_set_label(label, text):
    GLib.idle_add(label.set_text, text)

def safe_set_image(image_widget, pixbuf):
    GLib.idle_add(image_widget.set_from_pixbuf, pixbuf)



def update_image(labels, images, buttons):
    global title_name, player_name
    media.monitor()
    thumbnail = None
    
    current_player = media.current_player or ''
    current_title = media.title_ or ''
    should_update = False

    if player_name != current_player:
        print(f"Player changed: {player_name} → {current_player}")
        player_name = current_player
        should_update = True

    # Detect title change
    if title_name != current_title:
        print(f"Title changed: {title_name} → {current_title}")
        title_name = current_title
        should_update = True

    if current_player:
        try:
            if should_update:
                print(f"title: {current_title}\nartist: {media.artist}")
                
                safe_set_label(labels.dropdown_title_label, current_title)
                safe_set_label(labels.dropdown_artist, media.artist)
                
                global media_tool_tip
                media_tool_tip = f'Now Playing: {current_title}\n          By\n{media.artist}'

                # Image part
                height, width = 50, 50
                if 'file:///' in media.art_url:
                    thumbnail = media.art_url.replace('file:///', '/')
                    height, width = 60, 60
                elif 'https://' in media.art_url or 'http://' in media.art_url:
                    thumbnail = get_cached_filename(current_title)
                    if not os.path.exists(thumbnail):
                        print(f"Downloading thumbnail to cache: {thumbnail}")
                        urllib.request.urlretrieve(media.art_url, thumbnail)
                    else:
                        print(f"Using cached thumbnail: {thumbnail}")
                    height, width = 35, 35

                if thumbnail and os.path.exists(thumbnail):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, height, width)
                    circular_pixbuf = images.create_circular_pixbuf(pixbuf)

                    pixbuf_large = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 400, 200)
                    radius_pixbuf = images.create_radius_pixbuf(pixbuf_large)

                    if circular_pixbuf and radius_pixbuf:
                        print("Setting images safely...")
                        safe_set_image(images.bar_image, circular_pixbuf)
                        safe_set_image(images.dropdown_image, radius_pixbuf)
                        images.bar_image.set_has_tooltip(True)
                        images.bar_image.connect("query-tooltip", media_tooltip)
                        images.bar_image.show()
                        images.dropdown_image.show()
                    else:
                        print("Error: Failed to create pixbufs.")



        except Exception as e:
            print(f"Exception in update_image: {e}")

    else:
        media_tool_tip = 'No Active media is playing!'
        safe_set_label(labels.dropdown_title_label, '')
        safe_set_label(labels.dropdown_artist, '')
        images.bar_image.hide()
        images.dropdown_image.hide()

    return True

def media_tooltip(widget, x, y, keyboard_mode, tooltip):
    global media_tool_tip
    tooltip.set_text(media_tool_tip)
    return True


def update_title(buttons):
    media.monitor()
    if media.current_player:
        if len(media.title_) >= 5:
            # print(type(media.title_))
            new_label = f"{media.title_[:5]}.."
            if buttons.media_button.get_label() != new_label:
                buttons.media_button.set_label(new_label)
        else:
            new_label = f"{media.title_}"
            if buttons.media_button.get_label() != new_label:
                buttons.media_button.set_label(new_label)
    else:
        buttons.media_button.set_label('')
    return True

# def update_title(buttons):
#     global title_name, player_name
#     media.monitor()
#     if media.current_player:
#         # Always check if player changed
#         if player_name != media.current_player or title_name != media.title_:
#             player_name = media.current_player
#             title_name = media.title_

#             if len(media.title_) >= 5:
#                 new_label = f"{media.title_[:5]}.."
#             else:
#                 new_label = media.title_

#             if buttons.media_button.get_label() != new_label:
#                 buttons.media_button.set_label(new_label)
#     else:
#         buttons.media_button.set_label('')
#     return True

def get_nvidia_gpu_usage():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                                stdout=subprocess.PIPE, text=True)
        usage = result.stdout.strip()
        return f"{usage}"
    except FileNotFoundError:
        return ''

def get_nvidia_total_vram():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        vram = result.stdout.strip()
        return f"{vram:.1}"
    except FileNotFoundError:
        return ''

def get_nvidia_used_vram():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        used_vram = result.stdout.strip()
        return f"{used_vram}"
    except FileNotFoundError:
        return ''

def get_nvidia_temp():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        temp = result.stdout.strip()
        return f"{temp}"
    except FileNotFoundError:
        return ''

def get_nvidia_powerdraw():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        power = result.stdout.strip()
        return f"{power}"
    except FileNotFoundError:
        return ''

def get_nvidia_name():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        name = result.stdout.strip()
        return f"{name}"
    except FileNotFoundError:
        return ''

def get_nvidia_fanspeed(): 
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=fan.speed', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        fan = result.stdout.strip()
        return f"{fan}"
    except FileNotFoundError:
        return ''


def get_total_ram():
    result = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], stdout=subprocess.PIPE)
    total_ram_kb = int(result.stdout.decode().split()[1])
    total_ram_gb = round(total_ram_kb / 1024 / 1024, 2)
    return f"{total_ram_gb}"

def get_free_ram():
    result = subprocess.run(['grep', 'MemFree', '/proc/meminfo'], stdout=subprocess.PIPE)
    free_ram_kb = int(result.stdout.decode().split()[1])
    free_ram_gb = round(free_ram_kb / 1024 / 1024, 2)
    return f"{free_ram_gb}"

def get_ram_usage():
    result = subprocess.run(
        ['awk', '/MemTotal/ {total=$2} /MemAvailable/ {avail=$2} END {print (total-avail)/1024/1024}', '/proc/meminfo'],
        capture_output=True,
        text=True
    )
    result = float(result.stdout.strip())  # Convert to float
    return f"{result:.3f}"

def get_used_ram():
    result = subprocess.run(
        ['awk', '/MemTotal/ {total=$2} /MemAvailable/ {avail=$2} END {print (total-avail)/1024/1024}', '/proc/meminfo'],
        capture_output=True,
        text=True
    )
    result = float(result.stdout.strip())  # Convert to float
    return f"{result:.3f}"


def get_cpu_temp():
    result = subprocess.run(['sensors'], capture_output=True, text=True)
    temps = []

    # Regex patterns for Intel & AMD
    patterns = [
        r'(Core \d+):\s+\+([\d\.]+)°C',        # Intel cores
        r'Package id \d+:\s+\+([\d\.]+)°C',    # Intel package
        r'Tctl:\s+\+([\d\.]+)°C',              # AMD Tctl
        r'Tdie:\s+\+([\d\.]+)°C',              # AMD Tdie
    ]

    for line in result.stdout.splitlines():
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                if 'Core' in pattern:
                    core = match.group(1)
                    temp = match.group(2)
                    temps.append(f"{core}: {temp}°C")
                else:
                    temp = match.group(1)
                    temps.append(f"{temp}")

    if temps:
        return temps[0]
    else:
        return ["CPU temperature not found"]

def get_cpu_usage():
    result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('%Cpu(s)'):
            parts = line.split(',')
            user = float(parts[0].split()[1])
            system = float(parts[1].split()[0])
            total_usage = user + system
            return f"{total_usage:.1f}"

def get_cpu_info():
    result = subprocess.run(['lscpu'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('Model name'):
            return line.split(":")[1].strip()


def update_pauseplay(button):
    if not media.current_player or media.playback_status == 'Paused':
        button.set_label('')
        
    elif media.playback_status == 'Playing':
        button.set_label('')


    return True

def fetch_updates_async(buttons):
    def run_checkupdates():
        try:
            process = subprocess.Popen(['pacman', '-Qqu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=5)

            if stderr:
                GLib.idle_add(buttons.package_button_.set_label, "󰏖 | Error")
                return

            
            updates = stdout.strip().split('\n')
            nums = str(len([pkg for pkg in updates if pkg]))  # Count non-empty lines

            glyph = "󰏖"
            text = f"{nums}"

            GLib.idle_add(buttons.package_button_.set_label, f'{glyph} {text}')
            # GLib.idle_add(buttons.package_button_.set_label, f'󰏖 | {nums}')

        except subprocess.TimeoutExpired:
            process.kill()
            GLib.idle_add(buttons.package_button_.set_label, "Timeout")

        except Exception as e:
            GLib.idle_add(buttons.package_button_.set_label, f"Crash")

    threading.Thread(target=run_checkupdates, daemon=True).start()

def update_network(labels):
    ssid_ = ssid()
    network = get_network()

    if network:
        labels.network_label.set_text("󰤨")
        labels.custom_wifi.set_text(labels.online_icon)
        labels.tooltip_text = ssid_
    else:
        # labels.network_label.set_text("󰤭")
        labels.network_label.set_text("󰤭")
        labels.custom_wifi.set_text(labels.offline_icon)
        
        
        labels.tooltip_text = "No Connection"
    
    return True
