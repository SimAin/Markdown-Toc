# Markdown-Toc

Create table of contents (TOC) for markdown files and append them to file.

## The problem

Note files are written in markdown using vim. The TOC is very valuable as files can get very large. 
There does not appear to be a vim plugin to handle updating a files TOC.
The goal of this script is to automate that process.

## Known issues 

- Script currently repeats TOC elements numbered 10 and greater. Although only at the second level. 
- Terminal output is currently not very helpful.
- Script does not handle empty or 'non-standard' files (e.g. placeholder files). 

## Future features

- Markdown files are written using vim. Want to run TOC script when a file is written to.  

## References

This script was based of code from the following project:
https://github.com/CribberSix/markdown-toc-extract
