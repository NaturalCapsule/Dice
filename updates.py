import time
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf
from media import MediaPlayerMonitor
import os
from date import get_calendar_html
from network import *


media = MediaPlayerMonitor()

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


def update_image(labels, images):
    media.monitor()
    
    if media.current_player:
        thumbnail = media.art_url.replace('file:///', '/')
        if thumbnail and os.path.exists(thumbnail):
            
            labels.dropdown_title_label.set_label(media.title_)
            labels.dropdown_artist.set_text(media.artist)
            global media_tool_tip
            media_tool_tip = f'Now Playing: {media.title_}\n          By\n{media.artist}'

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 50, 50)
            circular_pixbuf = images.create_circular_pixbuf(pixbuf)

            pixbuf_ = GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail, 400, 200)
            radius_pixbuf = images.create_radius_pixbuf(pixbuf_)


            if circular_pixbuf and radius_pixbuf:
                images.bar_image.set_from_pixbuf(circular_pixbuf)
                images.bar_image.set_has_tooltip(True)
                    
                images.bar_image.connect("query-tooltip", media_tooltip)


                images.dropdown_image.set_from_pixbuf(radius_pixbuf)
            
            else:
                print("Error")
    return True



def media_tooltip(widget, x, y, keyboard_mode, tooltip):
    global media_tool_tip
    tooltip.set_text(media_tool_tip)
    return True



def update_title(buttons):
    media.monitor()
    if media.current_player:
        if len(media.title_) >= 5:
            text = f"{media.title_[:5]}.."
        else:
            text = media.title_
    else:
        text = ''
    buttons.media_button.set_label(str(text))
    
    return True


def update_pauseplay(buttons):
    if not media.current_player or media.playback_status == 'Paused':
        buttons.play_pause_button.set_label('')
    elif media.playback_status == 'Playing':
        buttons.play_pause_button.set_label('')

    return True


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