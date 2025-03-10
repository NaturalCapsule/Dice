import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RotatedButton(Gtk.Widget):
    def __init__(self, button):
        super().__init__()
        self.button = button
        self.set_size_request(100, 100)

    def do_draw(self, cr):
        # Get the widget size
        width, height = self.get_allocated_width(), self.get_allocated_height()
        
        # Move the origin to the center of the widget for rotation
        cr.translate(width / 2, height / 2)
        
        # Rotate by 90 degrees (in radians)
        cr.rotate(90 * 3.14159 / 180)  # 90 degrees in radians
        
        # Move the button back to its original position
        cr.translate(-width / 2, -height / 2)
        
        # Draw the button (you can use any widget drawing code here)
        self.button.draw(cr)

        return True

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Rotated Button Example")
        self.set_default_size(400, 400)

        # Create the button
        self.button = Gtk.Button(label="Click Me")
        self.button.connect("clicked", self.on_button_clicked)

        # Create a custom widget to rotate the button
        rotated_button = RotatedButton(self.button)

        # Add the rotated button to the window
        self.add(rotated_button)

    def on_button_clicked(self, widget):
        print("Button clicked!")

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
