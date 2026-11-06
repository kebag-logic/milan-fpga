"""insert.py <sim_main.cpp> <block>: insert a probe block before the suite's tally line."""
import sys
f, blk = sys.argv[1], open(sys.argv[2]).read()
s = open(f).read()
key = '  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n  return fails ? 1 : 0;\n}\n\n}  // namespace'
assert s.count(key) == 1, "anchor"
open(f, "w").write(s.replace(key, blk + key))
