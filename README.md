# Markdown-Toc

Create table of contents (TOC) for markdown files and append them to file.

- singleFile: Will take a single file as a parameter and create/update the TOC for that file. 
- iterateDir: Will update the TOC's for all files in the directory it is run from.

Both methods of running the program must be run from the directory of the files to update.
 
## The problem

Note files are written in markdown using vim. The TOC is very valuable as files can get very large. 
There does not appear to be a vim plugin to handle updating a files TOC.
The goal of this script is to automate that process.

## Known issues 

- Terminal output is currently not very helpful.
- Script does not handle empty or 'non-standard' files (e.g. placeholder files). 
- Script does not validate files passed in are markdown files. 

## Future features

- Markdown files are written using vim. The desire is to run the TOC script when a file is written to.  

## References

This script was based of code from the following project:
https://github.com/CribberSix/markdown-toc-extract
