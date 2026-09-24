#!/usr/bin/env python3
"""Ask the pinned GCC which `int` names survive -E for directive spellings
outside gate 1b's 55-entry lexer corpus. Usage: gcc_spellings.py <gcc> <workdir>"""
import json, re, subprocess, sys
from pathlib import Path

gcc, work = sys.argv[1], Path(sys.argv[2])
cases = {
    "control: plain #ifdef": "int a;\n#ifdef FOO\nint b;\n#endif\nint z;\n",
    "control: the %: digraph": "int a;\n%:ifdef FOO\nint b;\n%:endif\nint z;\n",
    "a splice inside the %: digraph": "int a;\n%\\\n:ifdef FOO\nint b;\n%\\\n:endif\nint z;\n",
    "a splice with a space inside the %: digraph": "int a;\n%\\ \n:ifdef FOO\nint b;\n%\\ \n:endif\nint z;\n",
    "a form feed before the %: digraph": "int a;\n\f%:ifdef FOO\nint b;\n\f%:endif\nint z;\n",
    "a UTF-8 BOM before # at file start": "﻿#ifndef FOO\nint a;\n#endif\nint z;\n",
}
out = {}
for i, (label, text) in enumerate(cases.items()):
    src = work / f"s{i}.c"
    src.write_bytes(text.encode("utf-8"))
    run = subprocess.run([gcc, "-std=gnu99", "-E", "-P", str(src)], capture_output=True)
    kept = None if run.returncode else re.findall(r"\bint\s+(\w+)\s*;", run.stdout.decode("utf-8", "replace"))
    out[label] = {"text": text, "gcc_rc": run.returncode, "gcc_keeps": kept,
                  "stderr": run.stderr.decode("utf-8", "replace").strip()[:300]}
print(json.dumps(out, indent=1))
