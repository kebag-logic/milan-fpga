#!/usr/bin/env python3
"""page_fence.py CHECKOUT PAGE MARKER OUTFILE: write the sh fence of PAGE that holds MARKER, unedited."""
import re, sys
from pathlib import Path
text = (Path(sys.argv[1]) / sys.argv[2]).read_text()
fences = [f for f in re.findall(r'```sh\n(.*?)```', text, re.S) if sys.argv[3] in f]
assert len(fences) == 1, len(fences)
Path(sys.argv[4]).write_text(fences[0])
