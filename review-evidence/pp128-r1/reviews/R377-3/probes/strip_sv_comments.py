#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print a SystemVerilog file with // and /* */ comments and blank lines removed (strings respected)."""
import re, sys
src = open(sys.argv[1]).read()
out = re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', lambda m: m.group(0) if m.group(0).startswith('"') else '', src, flags=re.S)
print("\n".join(l.rstrip() for l in out.splitlines() if l.strip()))
