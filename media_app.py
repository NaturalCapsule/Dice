import gi
from media import MediaPlayerMonitor
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bar")
        
        self.initUI()
        self.show_all()


    def initUI(self):
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(False)
        self.media = MediaPlayerMonitor()

        self.image = Gtk.Image()


        self.set_default_size(640, 350)
        self.move(640, 350)

        self.set_size_request(640, 350)

        self.main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_layout)
        self.pause_playButton()
        self.forward_button()
        self.backward_button()
        self.reset_button()
        self.title_label = Gtk.Label(label = '')
        self.title_label.set_line_wrap(True)
        self.load_image()
        GLib.timeout_add(100, self.update_pauseplay)
        
        GLib.timeout_add(100, self.update_ui)


    def load_image(self):
        overlay = Gtk.Overlay()
        overlay.add(self.image)

        fixed = Gtk.Fixed()
        overlay.add_overlay(fixed)


        fixed.put(self.play_pause_button, 280, 200)
        fixed.put(self.title_label, 290, 25)
        fixed.put(self.forward_, 350, 200)
        fixed.put(self.backward_, 210, 200)
        fixed.put(self.reset_, 280, 250)
    
        self.main_layout.pack_start(overlay, True, True, 0)

        
    def pause_play_command(self, button):
        self.media.pause_play_action()
    
    def pause_playButton(self):
        self.play_pause_button = Gtk.Button(label = '')
        self.play_pause_button.connect("clicked", self.pause_play_command)

    def update_pauseplay(self):
        if self.media.playback_status == 'Paused':
            self.play_pause_button.set_label('')
        elif self.media.playback_status == 'Playing':
            self.play_pause_button.set_label('')
    
        return True

    def forward_action(self, button):
        self.media.forward_10_seconds()

    def forward_button(self):
        self.forward_ = Gtk.Button(label = '')
        self.forward_.connect('clicked', self.forward_action)        

    def backward_action(self, button):
        self.media.backward_10_seconds()
        
    def reset_action(self, button):
        self.media.reset()

    def reset_button(self):
        self.reset_ = Gtk.Button(label = '')
        self.reset_.connect('clicked', self.reset_action)

    def backward_button(self):
        self.backward_ = Gtk.Button(label = '')
        self.backward_.connect('clicked', self.backward_action)        


    def update_ui(self):
        self.media.monitor()

        if self.media.current_player:
            self.title_label.set_text(self.media.title_)

            thumbnail = self.media.art_url.replace('file:///', '/')
            
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumbnail)
                scaled_pixbuf = pixbuf.scale_simple(570, 320, GdkPixbuf.InterpType.BILINEAR)

                self.image.set_from_pixbuf(scaled_pixbuf)        
            except Exception as e:
                print(f"Failed to load image: {e}")
        else:
            self.title_label.set_text("No active player")
        
        return True


 

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
