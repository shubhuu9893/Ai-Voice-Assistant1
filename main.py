import os
import eel
import subprocess
import socket

from engine.features import *
from engine.command import *

def find_free_port():
    """Find a free port to use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port

def start():
    
    # Initialize eel with the web files directory
    eel.init("www", allowed_extensions=['.js', '.html'])

    playAssistantSound()
    @eel.expose
    def init():
        try:
            subprocess.call([r'device.bat'])
        except Exception as e:
            print(f"Error running device.bat: {e}")
        eel.hideLoader()
        speak("Please enter your password")
        
    @eel.expose
    def verify_password(password):
        if password == "Shubham@123":
            speak("Password Authentication Successful")
            speak("Hello, Welcome Sir")
            eel.hideStart()
            playAssistantSound()
            return True
        else:
            speak("Password Authentication Failed")
            return False
    
    # Find a free port
    port = find_free_port()
    print(f"Using port: {port}")
            
    os.system(f'start msedge.exe --app="http://localhost:{port}/index.html"')

    # Start the eel application with proper error handling
    try:
        eel.start('index.html', mode=None, host='localhost', port=port, block=True)
    except Exception as e:
        print(f"Error starting eel: {e}")

if __name__ == "__main__":
    start()