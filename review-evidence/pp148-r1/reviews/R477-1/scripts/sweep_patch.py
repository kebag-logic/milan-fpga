#!/usr/bin/env python3
"""Reviewer sweep probe: make tb/pp_top run_spacing() run CS at every start in
[R477_LO, R477_HI) (environment), printing each run's closest gap. Scratch only."""
import sys
p = sys.argv[1]
s = open(p).read()
old = ('  CounterSpacingPhase{h}.run("CS2a", 0);\n'
       '  CounterSpacingPhase{h}.run("CS2b", 30);\n'
       '  CounterSpacingPhase{h}.run("CS2c", 95);\n')
assert s.count(old) == 1
new = ('  const char* lo_s = std::getenv("R477_LO");\n'
       '  const char* hi_s = std::getenv("R477_HI");\n'
       '  const long lo = lo_s ? std::atol(lo_s) : 0, hi = hi_s ? std::atol(hi_s) : 0;\n'
       '  for (long s = lo; s < hi; ++s) {\n'
       '    char id[32];\n'
       '    std::snprintf(id, sizeof id, "SW%ld", s);\n'
       '    CounterSpacingPhase{h}.run(id, s);\n'
       '  }\n')
s = s.replace(old, new)
if "#include <cstdlib>" not in s:
    s = "#include <cstdlib>\n#include <cstdio>\n" + s
open(p, "w").write(s)
