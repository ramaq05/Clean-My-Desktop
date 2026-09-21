# Clean My Desktop

Clean my desktop automatically organizes your files based on their extensions.

## How it works

The Python script uses the `watchdog` package to monitor your `Downloads` directory (the default) for any newly created or modified files. Once a file is completely written, the script detects its extension and routes it into the corresponding category folder (e.g., PDFs, Images, Code, etc.). 
- The script automatically handles duplicate file names by appending a counter.
- The target folders will be created automatically inside the `Downloads` directory if they don't already exist.

## How to use it

1. Make sure Python is installed on your computer.
2. Open a terminal (PowerShell or Command Prompt) and navigate to the project directory:
   ```powershell
   cd d:\Projects\FileManager
   ```
3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the script:
   ```powershell
   python clean_desktop.py
   ```
5. You can test it by downloading or dropping a file into your `Downloads` directory. The terminal will log output when files are successfully moved.

If you want it to run on system boot, you can use the Windows Task Scheduler to launch `clean_desktop.py` silently whenever you log in!

