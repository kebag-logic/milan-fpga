#!/usr/bin/env python3
"""plant.py FILE OLD NEW: replace OLD by NEW in FILE; refuse unless OLD occurs exactly once."""
import sys
from pathlib import Path
p, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text()
n = t.count(old)
if n != 1:
    sys.exit(f"plant: pattern occurs {n} times in {p}, expected 1")
p.write_text(t.replace(old, new))
print(f"plant: {p.name} mutated")
