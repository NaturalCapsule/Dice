import json
import os

with open(f'/home/{os.getlogin()}/.config/bar/config/config.json', "r") as file:
    widgets = json.load(file)

for widget in widgets['bar']:
    widget_ = None

def bar_position():
    try:
        bar_pos = widget.get("position")
        return bar_pos
    except Exception as e:
        print(f"Error: {e}")

def bar_height():
    try:
        bar_height_ = widget.get("Bar Height")
        return bar_height_
    except Exception as e:
        print(f"Error: {e}")

def bar_gap():
    try:
        width_gap = widget.get("Width Gap")
        return width_gap
    except Exception as e:
        print(f"Error: {e}")

def bar_gap_():
    try:
        height_gap = widget.get('Height Gap')
        return height_gap
    except Exception as e:
        print(f"Error: {e}")