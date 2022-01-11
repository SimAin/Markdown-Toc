import argparse
from typing import List, Tuple
from os.path import exists
import regex as re
import os


def remove_code_blocks(content: List[str]) -> List[str]:
    """
    Removes lines starting with "```" (=code blocks) from the markdown file.
    Since code blocks can contain lines with leading hashtags
    (e.g. comments in python) they need to be removed before
    looking for headers.
    :param content: file contents as a list of strings
    :return: Cleaned file contents as a list of strings
    """
    content_cleaned = []
    code_block = False

    for x in content:
        if x[:3] == "```":
            code_block = not code_block
        elif not code_block:
            content_cleaned.append(x)

    return content_cleaned


def remove_toc_header(lines: List[str]) -> List[str]:
    """
    Filters a list of lines to remove the existing toc header.
    Identifies toc header using regex pattern.
    :param lines: List of toc header and text lines.
    :returns: List of text lines.
    """

    toc_elements = []
    re_toc_header = r"^\#\ (Table\ of\ Contents\ *|TOC*)$"
    toc_cleaned = []

    for i, line in enumerate(lines): 
        # identify toc elements by pattern 
        if re.search(re_toc_header, line): 
            toc_elements.append(line)
        else:
            toc_cleaned.append(line) 

    return toc_cleaned 


def remove_toc_elements(lines: List[str]) -> str:
    """
    Filters a list of lines to remove the existing toc.
    Identifies toc elements using regex patterns.
    :param lines: List of toc and text lines.
    :returns: List of text lines.
    """

    toc_elements = []
    re_toc = r"^(\ *|\t*)(\d*\.|-)\ \[.*\]\(\#.*\)$"
    re_toc_header = r"^\#\ (Table\ of\ Contents\ *|TOC*)$"
    toc_cleaned = []

    for i, line in enumerate(lines): 
        # identify toc elements by pattern 
        if re.search(re_toc, line) or re.search(re_toc_header, line): 
            toc_elements.append(line)
        else:
            toc_cleaned.append(line) 

    # Join lines as string with line endings
    content_without_toc = ("\n".join(toc_cleaned))
            
    return content_without_toc 


def identify_headers(lines: List[str]) -> List[str]:
    """
    Filters a list of lines to the header lines.
    Identifies headers of the 'leading-hashtag' type.
    :param lines: List of header and text lines.
    :returns: List of header lines.
    """

    headers = []
    re_hashtag_headers = r"^#+\ .*$"

    for i, line in enumerate(lines): 
        # identify headers by leading hashtags
        if re.search(re_hashtag_headers, line): 
            headers.append(line)
            
    return headers


def format_header(header: str) -> Tuple[str, int, str]:
    """
    Calculates the level of the header, removes leading and trailing 
    whitespaces and creates the markdown-link.
    :param header: header line from the markdown file
    :return: a tuple consisting of the cleaned header, the header level and the
        formatted markdown link.
    """

    # determine the level of the header 
    level = 0
    while header[0] == "#":
        level += 1
        header = header[1:]

    # create clickable link by allowing only certain characters in the link, 
    # by replacing whitespaces with hyphens and by removing colons
    headerlink = "#" + re.sub(r'[^a-zA-Z0-9 -]', '', header).lower().strip().replace(" ", "-").replace("--", "-")
    return (header.strip(), level, headerlink)


def create_toc(
        toc_levels: List[Tuple[str, int, str]], 
        level_limit: int) -> List[str]:
    """
    Creates a list of strings representing the items in the table of content.
    :param toc_levels:  A list of Tuples consisting of the header,
        the level of the header and a formatted markdown-link to the header.
                    Example for toc_levels:
                            [
                                ('First Header', 1, '#First-Header')
                                ('Second level', 2, '#Second-level')
                                ('First level again', 1, '#First-level-again')
                            ]
    :param level_limit: Limit to the number of levels included in the TOC
    :return: Ordered line items of the table of contents.
    """

    toc = ["# TOC"]
    # create a dict to store the header numbering for each level
    max_header_level = max([x[1] for x in toc_levels]) + 1
    headerlevels = dict.fromkeys(range(1, max_header_level), 1)
    previous_level = 1
    for i, (h, level, link) in enumerate(toc_levels):

        # reset lower header-levels if current header level is higher than prev
        if previous_level > level:
            for x in range(level + 1, previous_level + 1):
                headerlevels[x] = 1

        # construct TOC element
        if level <= level_limit:
            toc.append(
                "\t" * (level - 1) + f"{headerlevels[level]}. [" + 
                    h + f"]({link})"
            )

        # increment matching header level
        headerlevels[level] = headerlevels[level] + 1
        previous_level = level

    return toc


def main():
    """
    Script:
    This script was written to generate and add a table of contents to markdown
    files.
    Function:
    Main execution function.
    """

    parser = argparse.ArgumentParser(
        prog="extracttoc",
        description="Extracts the table of contents from a markdown file.",
    )

    # an argument that results in a list of strings with one element ('file')
    parser.add_argument(
        "file",
        nargs=1,
        help="Provide a markdown file from which to extract the toc.",
        type=str,
    )
    # an argument whose passed value is stored in an integer variable ('limit')
    parser.add_argument(
        "-l",
        "--levels",
        dest="limit",
        default=7,
        type=int,
        help="Set the number of levels which will be included in the TOC.",
    )

    args = parser.parse_args()

    # read file
    file_name = args.file[0]

    print(file_name)

    if not exists(file_name):
        raise ValueError(f"File " + file_name + " could not be found")

    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read().split("\n")

    # Find and remove code blocks
    content_cleaned = remove_code_blocks(content)
    
    # Find and remove TOC header (To avoid it being in TOC)
    toc_cleaned = remove_toc_header(content_cleaned)

    # Identify headers
    headers = identify_headers(toc_cleaned)

    # Correctly format each header
    toc_levels = [format_header(h) for h in headers]

    # Create TOC.
    toc = create_toc(toc_levels, args.limit)

    # Output TOC to cmd
    #print("INFO: TOC to be printed into file:")
    #for line in toc:
    #    print(line)
    
    # Insert TOC into file
    # Write contents
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read().split("\n")

    # Remove old TOC's from file contents
    content_without_toc = remove_toc_elements(content)
    content_with_toc = "\n".join(toc) + "\n" + content_without_toc

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content_with_toc)


main()
