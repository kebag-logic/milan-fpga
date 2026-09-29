#!/usr/bin/env python3
"""Print a module's parameter and port declarations (comments stripped, whitespace normalised).
usage: port_list.py <file.sv> <module>   (reads the text between 'module <name>' and the header's ');')
"""
import re, sys
text = open(sys.argv[1]).read()
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
text = re.sub(r"//[^\n]*", "", text)
m = re.search(r"\bmodule\s+" + re.escape(sys.argv[2]) + r"\b(.*?)\)\s*;", text, flags=re.S)
hdr = m.group(1)
for line in hdr.splitlines():
    line = " ".join(line.split())
    if line:
        print(line)
