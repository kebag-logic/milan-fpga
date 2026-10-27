#!/usr/bin/env python3
"""Copy a log into the receipts with host paths replaced by placeholders: the lane checkout by
<checkout>, the lane's scratch and build directories by <scratch>, the home directory by $HOME.
usage: sanitize.py SRC DST"""
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(errors='replace')
for path, name in (('$LANES/665-s2c-icache', '<checkout>'), ('$VALIDATION_STORAGE/scratch/665s2c-a685c', '<scratch>'),
                   ('$VALIDATION_STORAGE/665s2c-a685c', '<scratch>'), ('$WORKSPACE_HOME', '$HOME')):
    text = text.replace(path, name)
Path(sys.argv[2]).write_text(text)
