import os
import winreg

def restore_task_manager():
    try:
        # Metode 1: Menggunakan Registry
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        
        try:
            # Buka key registry
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                key_path, 
                0, 
                winreg.KEY_ALL_ACCESS
            )
            
            # Hapus value DisableTaskMgr
            try:
                winreg.DeleteValue(key, "DisableTaskMgr")
            except FileNotFoundError:
                pass
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry error: {e}")
        
        # Metode 2: Perintah Command
        os.system('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /f')
        
        # Metode 3: Restart Explorer
        os.system('taskkill /F /IM explorer.exe')
        os.system('start explorer.exe')
        
        # Metode 4: Restart Windows Explorer Service
        os.system('net stop explorer')
        os.system('net start explorer')
        
        print("Task Manager has been restored successfully!")
        
    except Exception as e:
        print(f"Error restoring Task Manager: {e}")

def additional_cleanup():
    # Hentikan proses terkait virus
    os.system('taskkill /F /IM python.exe')
    os.system('taskkill /F /IM pythonw.exe')
    
    # Tutup aplikasi yang dibuka virus
    apps_to_close = [
        'msedge', 'explorer', 'ms-windows-store', 
        'notepad', 'calc', 'mspaint', 'wordpad',
        'write', 'charmap', 'snippingtool', 
        'magnify', 'osk'
    ]
    
    for app in apps_to_close:
        os.system(f'taskkill /F /IM {app}*')

def main():
    restore_task_manager()
    additional_cleanup()
    print("Virus cleanup complete!")

if __name__ == "__main__":
    main()