"""
singleFile creates/updates the TOC for a single markdown file.
"""

import inspect
import os                                                                                                                                                                                       
import subprocess
import argparse

# Constructs argument parser
parser = argparse.ArgumentParser(
    prog="singlefile",
    description="Extracts the table of contents from a single markdown file.",
)

# an argument that results in a list of strings with one element ('file')
parser.add_argument(
    "file",
    nargs=1,
    help="Provide a markdown file from which to extract the toc.",
    type=str,
)

# Get path of current directory.  
path = os.getcwd() + "/" 
print("Current working dir: ")
print(path)

# Parse file name argument
args = parser.parse_args() 

# read file 
file_name = args.file[0] 
print("File to update TOC: ")
print(file_name)

# Get script path
script_path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
print("Script is running from: ")
print(script_path) 

subprocess.run(["python3", script_path + "/markdownToc.py",
                path + file_name])

