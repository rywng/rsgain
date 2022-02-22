import os
import sys
import shutil
import glob
import subprocess

SCAN_ARGS = {'.flac': ['-a', '-k', '-s', 'e'],
             '.ogg': ['-a', '-k', '-s', 'e'],
             '.mp3': ['-I3', '-S', '-L', '-a', '-k', '-s', 'e'],
             '.m4a': ['-L', '-a', '-k', '-s', 'e'],
             '.opus': ['-a', '-k', '-s', 'e'],
             '.wma': ['-L', '-a', '-k', '-s', 'e'],
             '.wav': ['-I3', '-L', '-a', '-k', '-s', 'e'],
             '.aiff': ['-I3', '-L', '-a', '-k', '-s', 'e'],
             '.wv': ['-S', '-a', '-k', '-s', 'e'],
             '.ape': ['-S', '-a', '-k', '-s', 'e']}

def scan(directory):
    for root, subdirs, files in os.walk(directory):
        if len(files) == 0:
            print(f"No files found in directory {root}")
        else:
            extensions = list()
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension in SCAN_ARGS and extension not in extensions:
                    extensions.append(extension)
            length = len(extensions)
            if length == 0:
                print(f"No audio files found in directory {root}")
            elif length > 1:
                print(f"Multiple audio file types detected in directory {root}, skipping")
            else:
                album_extension = extensions[0]
                os.chdir(root)
                audio_files = glob.glob("*" + album_extension)
                command = ['loudgain'] + SCAN_ARGS[album_extension] + audio_files
                subprocess.run(command)

if __name__ == "__main__":
    if shutil.which("loudgain") is None:
        print("Error: loudgain executable not found. Make sure it's in your PATH before running this script")
        sys.exit(1)
    if (len(sys.argv)) < 2:
        print("Error: You must pass the path of the root directory to scan as an argument")
        print("$ python scan.py /path/to/some/directory")
        sys.exit(1)
    if os.path.isdir(sys.argv[1]) is False:
        print(f"Error: Directory {sys.argv[1]} does not exist")
        sys.exit(1)
    scan(sys.argv[1])
    sys.exit(0)
