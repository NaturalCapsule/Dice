import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import subprocess
import os
import threading
import cairo
import queue

class CavaVisualizer(Gtk.DrawingArea):
    def __init__(self, r, g, b, r_, g_, b_, alpha, spacing):
        super().__init__()
        # self.r = r
        # self.g = g
        # self.b = b
        
        # self.r_ = r_
        # self.g_ = g_
        # self.b_ = b_
        # self.alpha = alpha
        
        self.r = r / 255.0
        self.g = g / 255.0
        self.b = b / 255.0

        self.r_ = r_ / 255.0
        self.g_ = g_ / 255.0
        self.b_ = b_ / 255.0
        self.alpha = alpha
        self.spacing = spacing
        
        # print(self.r, self.r_)

        
        self.set_size_request(150, 30)
        self.connect("draw", self.on_draw)
        
        self.num_bars = 12
        self.bar_values = [0] * self.num_bars
        
        self.data_queue = queue.Queue(maxsize=5)
        
        self.running = True
        self.reader_thread = threading.Thread(target=self.read_cava_data)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        GLib.timeout_add(33, self.update_from_queue)
        
        self.set_double_buffered(True)
    
    def create_cava_config(self):
        config_dir = os.path.expanduser("~/.config/cava")
        config_file = os.path.join(config_dir, "raw_config")
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        if not os.path.exists(config_file):
            with open(config_file, "w") as f:
                f.write("""[general]
bars = 12
framerate = 60

[input]
method = pulse
source = auto

[output]
method = raw
raw_target = /dev/stdout
data_format = binary
bit_format = 8bit

[smoothing]
integral = 77
monstercat = 0
gravity = 100
""")
        return config_file
    
    def read_cava_data(self):
        config_file = self.create_cava_config()
        
        try:
            process = subprocess.Popen(
                ["cava", "-p", config_file],
                stdout=subprocess.PIPE,
                bufsize=0
            )
            
            while self.running:
                try:
                    raw_data = process.stdout.read(self.num_bars)
                    if raw_data and len(raw_data) == self.num_bars:
                        if not self.data_queue.full():
                            self.data_queue.put(list(raw_data), block=False)
                except (BrokenPipeError, IOError):
                    break
                    
        except Exception as e:
            print(f"Error in cava reader thread: {e}")
        finally:
            if 'process' in locals():
                process.terminate()
    
    def update_from_queue(self):
        if not self.running:
            return False
            
        try:
            values = self.data_queue.get_nowait()
            self.bar_values = values
            self.queue_draw()
            self.data_queue.task_done()
        except queue.Empty:
            pass
            
        return True
    
    def on_draw(self, widget, cr):
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        
        spacing = self.spacing
        bar_width = (width - (spacing * (self.num_bars - 1))) / self.num_bars
        
        cr.set_source_rgba(self.r_, self.g_, self.b_, self.alpha)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        
        x_positions = [i * (bar_width + spacing) for i in range(self.num_bars)]
        
        for i, value in enumerate(self.bar_values):
            bar_height = (value / 255.0) * height
            
            x = x_positions[i]
            y = height - bar_height

            # cr.set_source_rgb(233, 233, 233)
            cr.set_source_rgb(self.r, self.g, self.b)
            
            cr.rectangle(x, y, bar_width, bar_height)
            cr.fill()
        
        return False

    def cleanup(self):
        self.running = False
        if hasattr(self, 'reader_thread'):
            self.reader_thread.join(1.0)