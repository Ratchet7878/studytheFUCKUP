import os
import time
import platform
from pynput import mouse, keyboard

#CONFIG (These will be consts)
MAX_USAGE_SECONDS = 10
CHECK_INTERVAL = 1

is_active = False
accumulated_usage = 0


def on_activity(*args, **kwargs):
    """Callback function triggered by any mouse or keyboard input."""
    global is_active
    is_active = True

def lock_screen():
    """Identifies the OS and executes the native screen lock command."""
    os_name = platform.system()
    print(f"\n[!] Usage limit reached! Locking screen for {os_name}...")
    
    if os_name == 'Windows':
        import ctypes
        ctypes.windll.user32.LockWorkStation()
    elif os_name == 'Darwin': # macOS
        os.system('pmset displaysleepnow')
    elif os_name == 'Linux':
        # Works for most common Linux desktop environments (GNOME, KDE, etc.)
        os.system('xdg-screensaver lock')
    else:
        print("[!] Unsupported OS for automatic locking.")

def main():
    global is_active, accumulated_usage
    
    print(f"=== Study Enforcer Started ===")
    print(f"Usage limit: {MAX_USAGE_SECONDS / 60} minutes of active screen time.")
    print(f"Emergency termination: Press Ctrl+C in this terminal to quit.\n")

    # Start non-blocking listeners for mouse and keyboard
    mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)
    keyboard_listener = keyboard.Listener(on_press=on_activity)
    
    mouse_listener.start()
    keyboard_listener.start()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            
            if is_active:
                accumulated_usage += CHECK_INTERVAL
                is_active = False # Reset flag for the next second
                
                # Optional: Print progress so you know it's working
                if accumulated_usage % 60 == 0:
                    print(f"Active usage: {accumulated_usage // 60} minute(s)")
            
            # Check if limit is reached
            if accumulated_usage >= MAX_USAGE_SECONDS:
                lock_screen()
                # Reset counter after locking so it starts fresh when you unlock
                accumulated_usage = 0 
                # Give the system a few seconds to process the lock before resuming tracking
                time.sleep(5) 

    except KeyboardInterrupt:
        print("\n=== Emergency Termination Triggered ===")
        print("Study Enforcer safely shut down.")
    finally:
        # Clean up listeners when the program exits
        mouse_listener.stop()
        keyboard_listener.stop()

if __name__ == "__main__":
    main()