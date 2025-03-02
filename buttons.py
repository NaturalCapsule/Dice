import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Layouts:
    def __init__(self):
        self.left_buttons = []
        self.right_buttons = []
        self.middle_buttons = []

class Buttons:
    def __init__(self, media_dropdown, workspace_1, workspace_2, workspace_3, workspace_4, workspace_5, pause_play_action, forward_action, backward_action, reset_action, power_dropdown, power_off, reset, hibernate, lock, date_dropdown, volume_dropdown, search_dropdown):
        self.layout__ = Layouts()
        
        self.buttons(media_dropdown, workspace_1, workspace_2, workspace_3, workspace_4, workspace_5, pause_play_action, forward_action, backward_action, reset_action, power_dropdown, power_off, reset, hibernate, lock, date_dropdown, volume_dropdown, search_dropdown)

    def buttons(self, media_dropdown, workspace_1, workspace_2, workspace_3, workspace_4, workspace_5, pause_play_action, forward_action, backward_action, reset_action, power_dropdown, power_off, reset, hibernate, lock, date_dropdown, volume_dropdown, search_dropdown):
        # self.left_buttons = []
        # self.layout__.right_button = []
        # self.middle_buttons = []
        self.media_buttons(media_dropdown, pause_play_action, forward_action, backward_action, reset_action)
        self.Volume_controlButton(volume_dropdown)
        self.powerSettingsButtons(power_dropdown, power_off, reset, hibernate, lock)
        self.workspace_buttons(workspace_1, workspace_2, workspace_3, workspace_4, workspace_5)
        self.timeButton(date_dropdown)
        self.searchButton(search_dropdown)



    def searchButton(self, search_dropdown):
        self.search_button = Gtk.Button(label = '󰜏')
        self.search_button.set_tooltip_text('Search from FireFox')
        self.search_button.get_style_context().add_class('SearchButton')
        self.search_button.connect('clicked', search_dropdown)
        self.layout__.left_buttons.append(self.search_button)
    
    
    def Volume_controlButton(self, volume_dropdown):
        self.volume_control = Gtk.Button(label = '󱄡')
        self.volume_control.get_style_context().add_class('VolumeControlButton')
        self.volume_control.connect('clicked', volume_dropdown)
        self.layout__.right_buttons.append(self.volume_control)
    
    def timeButton(self, date_dropdown):
        self.time_button = Gtk.Button()
        self.time_button.get_style_context().add_class('timeButton')
        self.time_button.connect('clicked', date_dropdown)
        self.layout__.right_buttons.append(self.time_button)
    
    def powerSettingsButtons(self, power_dropdown, power_off, reset, hibernate, lock):
        self.power_settings = Gtk.Button(label = '󰐦')
        self.power_settings.get_style_context().add_class('powerSettings')
        self.power_settings.connect('clicked', power_dropdown)
        self.layout__.right_buttons.append(self.power_settings)

# self.layout__.right_button

        self.power_off_button = Gtk.Button(label = '󰐥')
        self.power_off_button.get_style_context().add_class('powerOffButton')
        self.power_off_button.connect('clicked', power_off)
        
        self.reboot_button = Gtk.Button(label = '󰜉')
        self.reboot_button.get_style_context().add_class('RebootButton')
        self.reboot_button.connect('clicked', reset)
        
        self.hib_button = Gtk.Button(label = '󰤁')
        self.hib_button.get_style_context().add_class('hibButton')
        self.hib_button.connect('clicked', hibernate)
        
        self.lock_button = Gtk.Button(label = '󰌾')
        self.lock_button.get_style_context().add_class('LockButton')
        self.lock_button.connect('clicked', lock)
    
    def workspace_buttons(self, workspace_1, workspace_2, workspace_3, workspace_4, workspace_5):
        self.workspace1 = Gtk.Button(label = '󰤂')
        self.workspace1.get_style_context().add_class('workspace1')
        self.workspace1.connect('clicked', lambda button: workspace_1(self))
        
        
        self.workspace2 = Gtk.Button(label = '󰤂')
        self.workspace2.get_style_context().add_class('workspace2')
        self.workspace2.connect('clicked', lambda button: workspace_2(self))
        
        
        self.workspace3 = Gtk.Button(label = '󰤂')
        self.workspace3.get_style_context().add_class('workspace3')
        self.workspace3.connect('clicked', lambda button: workspace_3(self))
        
        
        self.workspace4 = Gtk.Button(label = '󰤂')
        self.workspace4.get_style_context().add_class('workspace4')
        self.workspace4.connect('clicked', lambda button: workspace_4(self))
        
        
        self.workspace5 = Gtk.Button(label = '󰤂')
        self.workspace5.get_style_context().add_class('workspace5')
        self.workspace5.connect('clicked', lambda button: workspace_5(self))
        
        
        self.layout__.left_buttons.append(self.workspace1)
        self.layout__.left_buttons.append(self.workspace2)
        self.layout__.left_buttons.append(self.workspace3)
        self.layout__.left_buttons.append(self.workspace4)
        self.layout__.left_buttons.append(self.workspace5)
    
    def media_buttons(self, media_dropdown, pause_play_action, forward_action, backward_action, reset_action):
        self.media_button = Gtk.Button()
        self.media_button.get_style_context().add_class('mediaButton')
        self.media_button.connect("clicked", media_dropdown)
        
        
        self.layout__.middle_buttons.append(self.media_button)
        
        self.play_pause_button = Gtk.Button()
        self.play_pause_button.get_style_context().add_class('playPauseButton')
        self.play_pause_button.connect('clicked', pause_play_action)

        self.forward_button = Gtk.Button(label = '')
        self.forward_button.get_style_context().add_class('forwardButton')
        self.forward_button.connect('clicked', forward_action)
        
        self.backward_button = Gtk.Button(label = '')
        self.backward_button.get_style_context().add_class('backwardButton')
        self.backward_button.connect('clicked', backward_action)
        
        
        self.reset_button = Gtk.Button(label = '󱞳')
        self.reset_button.get_style_context().add_class('resetDropdownButton')
        self.reset_button.connect('clicked', reset_action)
        
    def get_layout(self):
        return self.layout__