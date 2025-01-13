import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import os
from agent import create_refactor_agent
import re
import re

def clean_code(agent_response):
    """
    Removes language wrappers like ```language ... ``` from the agent's returned code.
    Handles multiple code blocks and ensures proper whitespace handling.

    Args:
        agent_response (str): The string containing code blocks wrapped in triple backticks.

    Returns:
        str: The cleaned code with all language wrappers removed.
    """
    code_block_pattern = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
    
    cleaned_code = "\n".join(code_block_pattern.findall(agent_response))
    
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
 ▄▄▄▄▄▄   ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   
█   ▄  █ █       █       █      █       █       █       █   ▄  █  
█  █ █ █ █    ▄▄▄█    ▄▄▄█  ▄   █       █▄     ▄█   ▄   █  █ █ █  
█   █▄▄█▄█   █▄▄▄█   █▄▄▄█ █▄█  █     ▄▄█ █   █ █  █ █  █   █▄▄█▄ 
█    ▄▄  █    ▄▄▄█    ▄▄▄█      █    █    █   █ █  █▄█  █    ▄▄  █
█   █  █ █   █▄▄▄█   █   █  ▄   █    █▄▄  █   █ █       █   █  █ █
█▄▄▄█  █▄█▄▄▄▄▄▄▄█▄▄▄█   █▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄█  █▄█

Ctrl + C to refactor files and exit.
Made By: @paulfruitful
.....Watching for changes in your codebase...                                                                  
    """
    print(ascii_art)

def main():
    refactor_cli_ascii_art()
    parser = argparse.ArgumentParser(description="A CLI tool to watch file saves.")
    parser.add_argument("watch", type=str, help="The directory to watch: now")
    args = parser.parse_args()
   

    changed_files_map = set()
    currentDirectory = os.getcwd()
    watch_directory(currentDirectory, changed_files_map)

if __name__ == "__main__":
    main()