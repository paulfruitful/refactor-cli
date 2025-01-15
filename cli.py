import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import os
from agent import create_refactor_agent
import re
import keyboard
EXCLUDED_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", 
    "node_modules", "dist", ".next", "out", "build", ".cache",
    "env", "venv", ".pytest_cache", "migrations", "staticfiles",
    "collected_static", "media", "vendor", "storage",
    "target", ".gradle", ".mvn", "bin", "obj", 
    ".sass-cache", ".parcel-cache", ".turbo", ".nuxt", ".vercel",
    "public", "cache", ".eleventy-cache"
}

def clean_code(agent_response):
    code_block_pattern = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
    cleaned_code = "\n".join(code_block_pattern.findall(agent_response))
    return cleaned_code.strip()

class FileSaveHandler(FileSystemEventHandler):
    def __init__(self, filesChanged):
        super().__init__()
        self.filesChanged = filesChanged

    def is_excluded(self, path):
        parts = path.split(os.sep)
        return any(part in EXCLUDED_DIRS or part.startswith('.') for part in parts)

    def on_created(self, event):
        if not self.is_excluded(event.src_path):
            self.filesChanged.add(event.src_path)
            print(f"File created: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory and not self.is_excluded(event.src_path):
            self.filesChanged.add(event.src_path)
            print(f"File modified: {event.src_path}")
def chunk_code(code, max_lines=500):
    """Splits code into manageable chunks based on the max number of lines."""
    lines = code.split('\n')
    for i in range(0, len(lines), max_lines):
        yield '\n'.join(lines[i:i + max_lines])

def refactor_large_file(file_path, refactor_agent):
    """Refactor large files by processing them in chunks."""
    try:
        with open(file_path, "r") as file:
            language = file.name.split(".")[-1]
            current_code = file.read()
        
        refactored_chunks = []
        for chunk in chunk_code(current_code):
            refactored_chunk = refactor_agent({"code": chunk, "language": language})
            cleaned_chunk = clean_code(refactored_chunk)
            refactored_chunks.append(cleaned_chunk.strip())
        
        with open(file_path, "w") as file:
            file.write('\n'.join(refactored_chunks))
            print(f"Successfully refactored and saved file: {file_path}")
    
    except Exception as e:
        print(f"Error processing large file {file_path}: {e}")

def refactor_files(filesChanged):
    """Refactor files in the set."""
    refactor_agent = create_refactor_agent()
    for file in filesChanged:
        if os.path.getsize(file) > 200_000: 
            print(f"Large file detected: {file}")
            refactor_large_file(file, refactor_agent)
        else:
            try:
                with open(file, "r") as fil:
                    language = fil.name.split(".")[-1]
                    current_code = fil.read()
                    refactored_code = refactor_agent({"code": current_code, "language": language})

                with open(file, "w") as fil:
                    print(f"File changed: {file}")
                    stripped_code = clean_code(refactored_code)
                    fil.write(stripped_code.strip())
                    print("\nRefactored Code:\n", stripped_code)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
    filesChanged.clear()

def watch_directory(path, filesChanged):
    print(f"Watching for file changes in: {path}")
    event_handler = FileSaveHandler(filesChanged)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("------------------Press CTRL + R to refactor files and exit.-------------")
    try:
        while True:
            time.sleep(1)
            if(keyboard.is_pressed('ctrl+r')):
                 print('Refactoring codebase...')
                 refactor_files(filesChanged)
                 break
    finally:
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

Made By: @paulfruitful                                                              
    """
    print(ascii_art)

def main():
    refactor_cli_ascii_art()
    parser = argparse.ArgumentParser(description="A CLI tool to watch file saves.")
    subparsers = parser.add_subparsers(dest="command")

    watch_parser = subparsers.add_parser("watch", help="The directory to watch")
   
    touch_parser = subparsers.add_parser("touch", help="To refactor a particular file")
    touch_parser.add_argument("file", type=str, help="The file to refactor")

    args = parser.parse_args()

    
    if args.command=="watch":
        changed_files_map = set()
        watch_directory(os.getcwd(), changed_files_map)

    elif args.command=="touch":
        try:
            with open(args.file, 'r') as change_file:
                language = change_file.name.split(".")[-1]
                agent = create_refactor_agent()
                print(f'.........Refactoring {args.file}')
                code = change_file.read()
                refactor_code = agent({"code": code, "language": language})
                refactored_code = clean_code(refactor_code)

            if os.path.getsize(args.file) < 200_000:
                with open(args.file, 'w') as file:
                    print('...........Almost Done...........')
                    file.write(refactored_code)
                    print('Refactor complete!!!!!!!!!')
                    return
            else:
                refactor_large_file(args.file, agent)
                return
        except Exception as e:
            print(f'An Error Occurred: {e}')




if __name__ == "__main__":
    main()
