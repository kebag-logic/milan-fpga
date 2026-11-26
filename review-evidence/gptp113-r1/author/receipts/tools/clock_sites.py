"""List each line of a file that the consumer's wall-clock rule matches (its own regexes, imported)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import measure_test_evidence as m  # noqa: E402

text = Path(sys.argv[2]).read_text()
code = m.strip_source(text, ".py")
print("uses_wall_clock:", m.uses_wall_clock(text, ".py"))
lines = code.splitlines()
for i, line in enumerate(lines, 1):
    kinds = []
    if m.PY_CLOCK.search(line):
        kinds.append("clock/sleep")
    if re.search(r"\btimeout\s*=", line):
        kinds.append("timeout=")
    if kinds:
        print(f"{i:4}: {'+'.join(kinds):12} {line.strip()[:100]}")
