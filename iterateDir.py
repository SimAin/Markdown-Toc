import inspect, os
import subprocess
import regex as re

# Script to execute python script on all markdown files in current directory.

# Script dir
print("Script running from")
print(os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe()))))

script_path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))

path_of_the_directory = os.getcwd()
re_hidden = r"^.*\.md$"

print("Files and directories in a specified path:")

for root, dirs, files in os.walk(path_of_the_directory):
    for name in files:
        if re.search(re_hidden, name):
            print("INFO: File found: ") 
            print(os.path.join(root, name)) 
            subprocess.run(["python3", script_path + "/markdownToc.py", os.path.join(root, name)])
