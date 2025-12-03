import time
import threading
import sys

class SimpleTimer:
    def __init__(self):
        self.is_paused = False
        self.is_running = True
    
    def pause_resume(self):
        """Kullanıcı input'u için thread"""
        while self.is_running:
            cmd = input()
            if cmd.lower() == 'p':
                self.is_paused = not self.is_paused
                if self.is_paused:
                    print("\n⏸ Stopped ('p for continue')\n")
                else:
                    print("\n▶ Continueing\n")

def timer(seconds):
    t = SimpleTimer()
    
    # Input thread başlat
    input_thread = threading.Thread(target=t.pause_resume, daemon=True)
    input_thread.start()
    
    print(f"\n started for {seconds} seconds ")
    print("'p' for Stop/Continue \n")
    
    elapsed = 0
    while elapsed < seconds:
        if not t.is_paused:
            mins = elapsed // 60
            secs = elapsed % 60
            hours = mins // 60
            mins = mins % 60
            
            print(f"\r{hours:02d}:{mins:02d}:{secs:02d}", end="", flush=True)
            
            time.sleep(1)
            elapsed += 1
        else:
            time.sleep(0.1)
    
    t.is_running = False
    print(f"\n\n✅ Timer has finished!")

# Kullanım
t = input("Kaç saniye? ")
try:
    t = int(t)
    timer(t)
except ValueError:
    print("Lütfen sayı girin!")