from media import MediaPlayerMonitor
import subprocess
media = MediaPlayerMonitor()


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

def update_action(button):
    command = 'sudo pacman -Syu'
    subprocess.Popen(["kitty", "-e", "sh", "-c", command])

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
    buttons.custom_workspace1.get_style_context().remove_class('active')
    buttons.custom_workspace1.set_label(buttons.default_icon)
    
    buttons.workspace1.get_style_context().remove_class('active')
    buttons.workspace1.set_label('󰊠')
    
    
    buttons.custom_workspace2.get_style_context().remove_class('active')
    buttons.custom_workspace2.set_label(buttons.default_icon)

    buttons.workspace2.get_style_context().remove_class('active')
    buttons.workspace2.set_label('󰊠')


    buttons.custom_workspace3.get_style_context().remove_class('active')
    buttons.custom_workspace3.set_label(buttons.default_icon)

    buttons.workspace3.get_style_context().remove_class('active')
    buttons.workspace3.set_label('󰊠')


    buttons.custom_workspace4.get_style_context().remove_class('active')
    buttons.custom_workspace4.set_label(buttons.default_icon)

    buttons.workspace4.get_style_context().remove_class('active')
    buttons.workspace4.set_label('󰊠')

    buttons.custom_workspace5.get_style_context().remove_class('active')
    buttons.custom_workspace5.set_label(buttons.default_icon)
    
    buttons.workspace5.get_style_context().remove_class('active')
    buttons.workspace5.set_label('󰊠')

    if workspace_num == 1:
        buttons.custom_workspace1.get_style_context().add_class('active')
        buttons.custom_workspace1.set_label(buttons.active_icon)

        buttons.workspace1.get_style_context().add_class('active')
        buttons.workspace1.set_label('󰮯')
        
    elif workspace_num == 2:
        buttons.custom_workspace2.get_style_context().add_class('active')
        buttons.custom_workspace2.set_label(buttons.active_icon)

        buttons.workspace2.get_style_context().add_class('active')
        buttons.workspace2.set_label('󰮯')

    elif workspace_num == 3:
        buttons.custom_workspace3.get_style_context().add_class('active')
        buttons.custom_workspace3.set_label(buttons.active_icon)

        buttons.workspace3.get_style_context().add_class('active')
        buttons.workspace3.set_label('󰮯')

    elif workspace_num == 4:
        buttons.custom_workspace4.get_style_context().add_class('active')
        buttons.custom_workspace4.set_label(buttons.active_icon)

        buttons.workspace4.set_label('󰮯')
        buttons.workspace4.get_style_context().add_class('active')

    elif workspace_num == 5:
        buttons.custom_workspace5.get_style_context().add_class('active')
        buttons.custom_workspace5.set_label(buttons.active_icon)

        buttons.workspace5.get_style_context().add_class('active')
        buttons.workspace5.set_label('󰮯')