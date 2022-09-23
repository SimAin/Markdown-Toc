import inspect, os
import subprocess
import hashlib
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

# Iterate for files in a specified path:

for root, dirs, files in os.walk(path_of_the_directory):
    for name in files:
        if re.search(re_hidden, name):
            with open(os.path.join(root,name), "rb") as f:
                Omd5 = hashlib.md5(f.read()).hexdigest()
            subprocess.run(["python3", script_path + "/markdownToc.py", os.path.join(root, name)])
            with open(os.path.join(root,name), "rb") as f:
                Nmd5 = hashlib.md5(f.read()).hexdigest()
            if Omd5 != Nmd5:
                print("INFO: TOC updated: ") 
                print(os.path.join(root, name)) 

            #TODO: Add below as verbose option
            #else:
                #print("INFO: No Change: ") 
                #print(os.path.join(root, name)) 
