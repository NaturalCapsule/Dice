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

# def update_image(labels, images, buttons):
#     global title_name
#     media.monitor()
#     if media.current_player:
#         try:
#             if 'file:///' in media.art_url:
                
#                 thumbnail = media.art_url.replace('file:///', '/')
#                 height, width = 60, 60
            
                
#             elif 'file:///' not in media.art_url:
                
#                 if title_name != media.title_:
                    
                    
#                     thumbnail = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
#                     thumbnail = thumbnail.name
#                     urllib.request.urlretrieve(media.art_url, thumbnail)
#                     title_name = media.title_
#                     height, width = 35, 35
            
#             if thumbnail and os.path.exists(thumbnail):
                
#                 labels.dropdown_title_label.set_label(media.title_)
#                 labels.dropdown_artist.set_text(media.artist)
#                 global media_tool_tip
#                 media_tool_tip = f'Now Playing: {media.title_}\n          By\n{media.artist}'

#                 pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, height, width)
#                 circular_pixbuf = images.create_circular_pixbuf(pixbuf)

#                 pixbuf_ = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 400, 200)
#                 radius_pixbuf = images.create_radius_pixbuf(pixbuf_)


#                 if circular_pixbuf and radius_pixbuf:
#                     images.bar_image.set_from_pixbuf(circular_pixbuf)
#                     images.bar_image.set_has_tooltip(True)
                        
#                     images.bar_image.connect("query-tooltip", media_tooltip)


#                     images.dropdown_image.set_from_pixbuf(radius_pixbuf)
                
#                 else:
#                     print("Error")
#         except Exception as e:
#             pass
#     return True


def safe_set_label(label, text):
    GLib.idle_add(label.set_text, text)

def safe_set_image(image_widget, pixbuf):
    GLib.idle_add(image_widget.set_from_pixbuf, pixbuf)

def update_image(labels, images, buttons):
    global title_name, player_name
    media.monitor()

    if media.current_player:
        try:
            should_update = False

            if title_name != media.title_:
                title_name = media.title_
                should_update = True

            if player_name != media.current_player:
                player_name = media.current_player
                should_update = True

            if should_update:
                print(f"Updating for title: {media.title_}, artist: {media.artist}")

                safe_set_label(labels.dropdown_title_label, media.title_)
                safe_set_label(labels.dropdown_artist, media.artist)
                global media_tool_tip
                media_tool_tip = f'Now Playing: {media.title_}\n          By\n{media.artist}'

                # Image part
                height, width = 50, 50

                if 'file:///' in media.art_url:
                    thumbnail = media.art_url.replace('file:///', '/')
                    height, width = 60, 60
                else:
                    thumbnail = get_cached_filename(media.title_)
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
                    else:
                        print("Error: Failed to create pixbufs.")
                else:
                    print("Thumbnail file missing, using default image.")

        except Exception as e:
            print(f"Exception in update_image: {e}")

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

            GLib.idle_add(buttons.package_button_.set_label, f'󰏖 | {nums}')

        except subprocess.TimeoutExpired:
            process.kill()
            GLib.idle_add(buttons.package_button_.set_label, "󰏖 | Timeout")

        except Exception as e:
            GLib.idle_add(buttons.package_button_.set_label, f"󰏖 | Crash")

    threading.Thread(target=run_checkupdates, daemon=True).start()

def update_network(labels):
    ssid_ = ssid()
    network = get_network()

    if network:
        labels.network_label.set_text("󰤨")
        labels.tooltip_text = ssid_
    else:
        labels.network_label.set_text("󰤭")
        labels.network_label.set_text("󰤭")
        
        labels.tooltip_text = "No Connection"
    
    return True
