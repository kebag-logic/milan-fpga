#!/usr/bin/env python3
"""usage: strip_sv_comments.py <file>  - print the SystemVerilog source with //
and /* */ comments removed (string literals kept) and blank lines dropped."""
import re, sys
s = open(sys.argv[1]).read()
tok = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', re.S)
s = tok.sub(lambda m: m.group(0) if m.group(0).startswith('"') else
            ("\n" * m.group(0).count("\n")), s)
print("\n".join(l.rstrip() for l in s.splitlines() if l.strip()))
