import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import os
from agent import create_refactor_agent
import re
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
def refactor_cli_ascii_art():
    ascii_art = """
    
██████╗ ███████╗███████╗ █████╗  ██████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝ ╚══██╔══╝██╔═══██╗██╔══██╗
██║  ██║█████╗  █████╗  ███████║██║  ███╗   ██║   ██║   ██║██████╔╝
██║  ██║██╔══╝  ██╔══╝  ██╔══██║██║   ██║   ██║   ██║   ██║██╔═══╝ 
██████╔╝███████╗███████╗██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     
╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     
Watching for changes in your codebase...                                                                  
    """
    print(ascii_art)

def main():
   
  


    parser = argparse.ArgumentParser(description="A CLI tool to watch file saves.")
    parser.add_argument("watch", type=str, help="The directory to watch: now")
    args = parser.parse_args()
    refactor_cli_ascii_art()

    changed_files_map = set()
    currentDirectory = os.getcwd()
    watch_directory(currentDirectory, changed_files_map)

if __name__ == "__main__":
    main()