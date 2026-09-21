import os
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# grab the downloads folder (this is where most of the junk ends up)
downloads_dir = Path.home() / "Downloads"

# here's where we map out what goes where
folder_rules = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "PDFs": [".pdf"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".json", ".xml"],
    "Documents": [".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
    "Executables": [".exe", ".msi", ".bat", ".ps1"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".avi", ".mkv", ".mov"]
}

def guess_folder(ext):
    """figures out which folder this extension belongs to"""
    for folder, extensions in folder_rules.items():
        if ext.lower() in extensions:
            return folder
    return "Other"

class CleanupBot(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.handle_new_file(Path(event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            self.handle_new_file(Path(event.src_path))

    def handle_new_file(self, filepath):
        # sanity check: is the file still there?
        if not filepath.exists():
            return

        # browsers take a sec to finish downloading, so give it a beat
        time.sleep(1)
        
        name = filepath.name
        ext = filepath.suffix
        
        # skip stuff without extensions or weird temp download files
        if not ext or ext.lower() in [".tmp", ".crdownload", ".part"]:
            return
            
        target_folder_name = guess_folder(ext)
        dest_dir = downloads_dir / target_folder_name
        
        # create the folder if it's the first time we've seen this type
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
            
        dest_path = dest_dir / name
        
        # if there's already a file with this name, tack a number on the end
        num = 1
        while dest_path.exists():
            dest_path = dest_dir / f"{filepath.stem}_{num}{ext}"
            num += 1
            
        try:
            shutil.move(str(filepath), str(dest_path))
            print(f"🧹 Swept away {name} -> {target_folder_name}/")
        except PermissionError:
            print(f"Oops, can't move {name} right now (it's probably still downloading or open in another app)")
        except Exception as err:
            print(f"Yikes, something broke trying to move {name}: {err}")

if __name__ == "__main__":
    if not downloads_dir.exists():
        downloads_dir.mkdir(parents=True, exist_ok=True)
        
    print(f"Alright, keeping an eye on: {downloads_dir}")
    print("Press Ctrl+C to stop it.")
    
    bot = CleanupBot()
    watcher = Observer()
    watcher.schedule(bot, str(downloads_dir), recursive=False)
    watcher.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the watcher. See ya!")
        watcher.stop()
    watcher.join()
