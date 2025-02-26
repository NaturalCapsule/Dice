import subprocess

def get_network():
    network = subprocess.Popen(['iwgetid', '-r'], text=True, stdout=subprocess.PIPE)
    ssid, _ = network.communicate()
    
    if not ssid:
        # return "No Connection"
        return False
    else:
        # return f"Connected to: {ssid.strip()}"
        return True

# ssid()

def ssid():
    network = get_network()
    
    network = subprocess.Popen(['iwgetid', '-r'], text=True, stdout=subprocess.PIPE)
    ssid_, _ = network.communicate()
    
    if network:
        return f'Connected to: {ssid_}'
    else:
        return 'No Connection'