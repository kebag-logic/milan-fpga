#!/usr/bin/env python3
"""Reader-level probe: which conditional directives gate 1b's readers find
in a C text, beside what the pinned GCC keeps of it at -std=gnu99 -E.
Usage: reader_vs_gcc.py <clone> <gcc> <file.c>..."""
import re, subprocess, sys
sys.path.insert(0, sys.argv[1] + "/sw/builder")
import test_builder as tb
hash_ = r"(?m)^[ \t]*#(?!#)[ \t]*"
cond = re.compile(hash_ + r"(if|ifdef|ifndef|elif|elifdef|elifndef|else|endif)\b")
anyd = re.compile(hash_ + r"([A-Za-z_]\w*)?")
for path in sys.argv[3:]:
    src = open(path, encoding="utf-8").read()
    view = tb._c_phases(src).view
    run = subprocess.run([sys.argv[2], "-std=gnu99", "-E", "-P", path],
                         capture_output=True, text=True)
    print(path)
    print("  readers, conditionals:", [m.group(1) for m in cond.finditer(view)])
    print("  readers, directive set:", [m.group(1) for m in anyd.finditer(view)])
    print("  gcc rc:", run.returncode, "keeps:", re.findall(r"\bint\s+(\w+)", run.stdout),
          "stderr lines:", len(run.stderr.splitlines()))
