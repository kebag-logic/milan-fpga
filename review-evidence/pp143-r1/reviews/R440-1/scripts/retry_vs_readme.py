#!/usr/bin/env python3
"""Compare a retry_mutants.py summary's KILLED counts with tb/acmp_talker/README.md's table."""
import re
import sys
readme = open(sys.argv[1]).read()
summary = open(sys.argv[2]).read()
table = dict(re.findall(r"^\| `(\w+)` \| killed, (\d+) failures \|", readme, re.M))
run = dict(re.findall(r"^KILLED (\w+): rc=\d+, (\d+) assertion failures$", summary, re.M))
diff = {k: (table.get(k), run.get(k)) for k in set(table) | set(run) if table.get(k) != run.get(k)}
print(f"README rows {len(table)}, KILLED lines {len(run)}, mismatches {diff}")
sys.exit(bool(diff))
