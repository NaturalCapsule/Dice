from media import MediaPlayerMonitor
import subprocess
media = MediaPlayerMonitor()
import time



def forward_action(button):
    media.forward_10_seconds()

def reset_action(button):
    media.reset()

def backward_action(button):
    media.backward_10_seconds()

def pause_play_action_(button):
    media.pause_play_action()


def power_off(button):
    subprocess.run(['shutdown', 'now'])

def reset(button):
    subprocess.run(['reboot'])

def lock(button):
    subprocess.run(['hyprlock'])

def hibernate(button):
    subprocess.run(['systemctl', 'hibernate'])

def switch_workspace(workspace_num, buttons):
    subprocess.run(['hyprctl', 'dispatch', 'workspace', str(workspace_num)])
    
    set_active_workspace(workspace_num, buttons)

def workspace_1(button):
    switch_workspace(1, button)

def workspace_2(button):
    switch_workspace(2, button)

def workspace_3(button):
    switch_workspace(3, button)

def workspace_4(button):
    switch_workspace(4, button)

def workspace_5(button):
    switch_workspace(5, button)

def set_active_workspace(workspace_num, buttons):
    buttons.workspace1.get_style_context().remove_class('active')
    buttons.workspace2.get_style_context().remove_class('active')
    buttons.workspace3.get_style_context().remove_class('active')
    buttons.workspace4.get_style_context().remove_class('active')
    buttons.workspace5.get_style_context().remove_class('active')

    if workspace_num == 1:
        buttons.workspace1.get_style_context().add_class('active')
    elif workspace_num == 2:
        buttons.workspace2.get_style_context().add_class('active')
    elif workspace_num == 3:
        buttons.workspace3.get_style_context().add_class('active')
    elif workspace_num == 4:
        buttons.workspace4.get_style_context().add_class('active')
    elif workspace_num == 5:
        buttons.workspace5.get_style_context().add_class('active')
