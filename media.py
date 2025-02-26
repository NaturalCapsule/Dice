import dbus
from time import sleep
import subprocess
import gi
gi.require_version('Gtk', '3.0')


class MediaPlayerMonitor:
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.players = {}
        self.current_player = None
        self.monitor() 

    def get_players(self):
        for service in self.session_bus.list_names():
            if service.startswith("org.mpris.MediaPlayer2."):
                if service not in self.players:
                    self.players[service] = self.session_bus.get_object(service, "/org/mpris/MediaPlayer2")
        return self.players

    def get_player_properties(self, player):
        try:
            # iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
            iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
            metadata = iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            playback_status = iface.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            position = iface.Get('org.mpris.MediaPlayer2.Player', 'Position')
            title = metadata.get('xesam:title', 'Unknown Title')
            artist = ', '.join(metadata.get('xesam:artist', []))
            album = metadata.get('xesam:album', 'Unknown Album')
            art_url = metadata.get('mpris:artUrl', '')

            return {
                'title': title,
                'artist': artist,
                'album': album,
                'art_url': art_url,
                'playback_status': playback_status,
                'position': position // 1_000_000
            }
        except dbus.exceptions.DBusException as e:
            print(f"Error retrieving properties: {e}")
            return None

    def update_current_player(self):
        for service, player in self.players.items():
            properties = self.get_player_properties(player)
            if properties and properties['playback_status'] != 'Stopped':
                self.current_player = player
                return

        self.current_player = None


                
    def monitor(self):
        self.get_players()
        self.update_current_player()

        if self.current_player:
            self.properties = self.get_player_properties(self.current_player)
            if self.properties:
                self.title_ = f"{self.properties['title']}"
                #  - {self.properties['artist']}
                self.artist = f"{self.properties['artist']}"
                self._album = f"{self.properties['album']}"
                self.psoition = f"{self.properties['position']}"
                self.playback_status = f"{self.properties['playback_status']}"
                self.art_url = f"{self.properties['art_url']}"
        else:
            # print("No active media player found.")
            return ''
        return True


    def pause_play_action(self):
        if self.current_player:
            subprocess.run(
    [
        "dbus-send",
        "--print-reply",
        f"--dest={self.current_player.bus_name}",
        "/org/mpris/MediaPlayer2",
        "org.mpris.MediaPlayer2.Player.PlayPause",
    ],
)

    def forward_10_seconds(self):
        session_bus = dbus.SessionBus()
    
        for service in session_bus.list_names():
            if service.startswith("org.mpris.MediaPlayer2."):
                player = session_bus.get_object(service, "/org/mpris/MediaPlayer2")
                iface = dbus.Interface(player, "org.mpris.MediaPlayer2.Player")

                iface.Seek(10 * 1_000_000)

                print("Skipped forward 10 seconds.")
                return

        # print("No active media player found.")

    def backward_10_seconds(self):
        session_bus = dbus.SessionBus()
    
        for service in session_bus.list_names():
            if service.startswith("org.mpris.MediaPlayer2."):
                player = session_bus.get_object(service, "/org/mpris/MediaPlayer2")
                iface = dbus.Interface(player, "org.mpris.MediaPlayer2.Player")

                iface.Seek(-10 * 1_000_000)

                print("Skipped forward 10 seconds.")
                return

        # print("No active media player found.")
        

    def reset(self):
        session_bus = dbus.SessionBus()
    
        for service in session_bus.list_names():
            if service.startswith("org.mpris.MediaPlayer2."):
                player = session_bus.get_object(service, "/org/mpris/MediaPlayer2")
                iface = dbus.Interface(player, "org.mpris.MediaPlayer2.Player")
    
                iface.SetPosition(dbus.ObjectPath("/org/mpris/MediaPlayer2"), 10)
    
                print("Video reset to the beginning.")
                return
    
        # print("No active media player found.")
