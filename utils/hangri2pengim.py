#!/usr/bin/env python3

import sys
import os
import argparse
from collections import defaultdict

# Default location for dictionary file
# assumes script is placed in subfolder 'utils'
dictfile = os.path.normpath(
    os.path.join(
        os.path.dirname(
            sys.argv[0]), '..', 'dieziu.dict.yaml'))

# CJK punctuation to Western
PUNCDICT = {
    '，' : ',',
    '。' : '.',
    '、' : ',',
    '！' : '!',
    '？' : '?',
    '；' : ';',
    '：' : ':',
    '「' : '‘',
    '」' : '’',
    '【' : '[',
    '】' : ']',
    '（' : '(',
    '）' : ')',
    '《' : '“',
    '》' : '”',
        }

def read_dictfile(filename):
    """Read table of characters/peng'im to a dict
    """
    char2pengim = defaultdict(list)
    # assume that a character may have more than one reading
    with open(filename, "r") as fh:
        for line in fh:
            spl = line.rstrip().split("\t")
            if len(spl) == 2:
                char2pengim[spl[0]].append(spl[1])
    return(char2pengim)


def rubify(char, chardict):
    return(f"<ruby>{char}<rt>{'<br />'.join(chardict[char])}</rt></ruby>")


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser(
        description="Annotate Chinese characters with Teochew pronunciation")
    parser.add_argument(
        "-d", "--dict", default=dictfile,
        help="TSV file with characters (column 1) and peng'im (col 2)")
    parser.add_argument(
        "-f", "--format", default='html',
        help="Format for output, either 'html' or 'text'")
    args = parser.parse_args()

    # Read dictionary file
    chardict = read_dictfile(args.dict)

    # Output html
    if args.format == 'html':
        print("<!DOCTYPE html>\n<html>\n<body>")
        for line in sys.stdin:
            outline = []
            for i in line.rstrip():
                if i in chardict:
                    outline.append(rubify(i, chardict))
                else:
                    outline.append(i)
            print("<p>" + "".join(outline) + "</p>")
        print("</body></html>")

    # Output plain text
    else:
        for line in sys.stdin:
            outline = []
            for i in line.rstrip():
                if i in chardict:
                    # characters with Pengim, if multiple join with /
                    outline.append("/".join(chardict[i]) + " ")
                elif i in PUNCDICT:
                    # CJK punctuation to western
                    outline.append(PUNCDICT[i] + " ")
                else:
                    # outline.append("X")
                    outline.append(i)
            if line.rstrip() == "".join(outline):
                print(line.rstrip())
                print("---")
            else:
                print(line.rstrip())
                print("".join(outline))
                print("---")
