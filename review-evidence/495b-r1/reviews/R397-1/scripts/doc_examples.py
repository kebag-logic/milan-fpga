#!/usr/bin/env python3
"""Every quoted MAC/hex-looking example in tracked Markdown, with the head
parser's verdict, for comparison with the verdict its page states.
Usage: doc_examples.py <tree>"""
import re, subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]); sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
files = subprocess.run(["git", "-C", str(tree), "ls-files", "*.md"], text=True, capture_output=True).stdout.split()
pat = re.compile(r'`"([^"`]{1,40})"`|(?:mac_address|stream_dmac_base|entity_id|entity_model_id|model_id_pin|vendor_oui|entity_capabilities|crf_format|format)\s*:\s*"([^"]{1,40})"')
for rel in files:
    for n, line in enumerate((tree / rel).read_text(errors="replace").splitlines(), 1):
        for m in pat.finditer(line):
            s = m.group(1) or m.group(2)
            if not re.fullmatch(r"[0-9A-Fa-fxX:_\-+ ]+", s) or not re.search(r"\d", s):
                continue
            def v(f):
                try: f(); return "accept"
                except eb.ConfigError as e: return "refuse(" + str(e)[:60] + ")"
            print(f"{rel}:{n}: {s!r}: MAC {v(lambda: eb._mac48(s, 'mac'))}; HEX64 {v(lambda: eb._eui64(s, 'hex'))}")
