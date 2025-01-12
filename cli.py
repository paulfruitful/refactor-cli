import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import os
from agent import create_refactor_agent
import re
import shutil
import ctypes
import winreg

def clean_code(agent_response):
    """
    Removes language wrappers like ```language ... ``` from the agent's returned code.
    """
    cleaned_code = re.sub(r"```[a-zA-Z]+\n", "", agent_response)  
    cleaned_code = re.sub(r"```", "", cleaned_code)             
    return cleaned_code.strip()

class FileSaveHandler(FileSystemEventHandler):
    def __init__(self, filesChanged):
        super().__init__()
        self.filesChanged = filesChanged

    def on_created(self, event):
        self.filesChanged.add(event.src_path)
        print(f"You did it!  File saved: {event.src_path}")
    
    def on_modified(self, event):
        refactor_agent = create_refactor_agent()
        if not event.is_directory:
            self.filesChanged.add(event.src_path)
            print(f"You did it! File saved: {event.src_path}")

def refactor_files(filesChanged):
    refactor_agent = create_refactor_agent()
      
    for file in filesChanged:
        with open(file, "r") as fil:
            language = fil.name.split(".")[-1] 
            current_code = fil.read()
            refactored_code = refactor_agent({"code": current_code, "language": language})
        
        with open(file, "w") as fil:
            print(f"File changed: {file}")
            stripped_code = clean_code(refactored_code)
            fil.write(stripped_code.strip())
            print("\nRefactored Code:\n")
            print(refactored_code)
    filesChanged.clear()

def watch_directory(path, filesChanged):
    print(f"Watching for file changes in: {path}")
    event_handler = FileSaveHandler(filesChanged)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        refactor_files(filesChanged)
        observer.stop()
    observer.join()

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_path(directory):
    """Add a directory to the system PATH environment variable."""
    try:
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as sub_key:
                path_value, _ = winreg.QueryValueEx(sub_key, "Path")
                
                if directory not in path_value:
                    new_path_value = f"{path_value};{directory}" if path_value else directory
                    winreg.SetValueEx(sub_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_value)
                    print(f"Added {directory} to the system PATH.")
                else:
                    print(f"{directory} is already in the system PATH.")
    except Exception as e:
        print(f"Failed to update PATH: {e}")

def move_exe_to_path(exe_path, target_dir):
    """Move the executable to a directory in the PATH."""
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"Created directory: {target_dir}")

        exe_name = os.path.basename(exe_path)
        target_path = os.path.join(target_dir, exe_name)
        shutil.move(exe_path, target_path)
        print(f"Moved {exe_name} to {target_dir}.")

        add_to_path(target_dir)
    except Exception as e:
        print(f"Failed to move executable: {e}")

def main():
   
    if os.name == "nt":  
        if not is_admin():
            print("This script requires administrator privileges. Please run it as an administrator.")
            time.sleep(5)
            return

        exe_path = os.path.join(os.getcwd(), "cli.exe")

        target_dir = os.path.join(os.environ["ProgramFiles"], "RefactorCLI")

        move_exe_to_path(exe_path, target_dir)

        print("Installation complete. You can now run 'refactor-cli' from any terminal.")
        time.sleep(5)

    


    parser = argparse.ArgumentParser(description="A CLI tool to watch file saves.")
    parser.add_argument("watch", type=str, help="The directory to watch: now")
    args = parser.parse_args()

    changed_files_map = set()
    currentDirectory = os.getcwd()
    watch_directory(currentDirectory, changed_files_map)

if __name__ == "__main__":
    main()