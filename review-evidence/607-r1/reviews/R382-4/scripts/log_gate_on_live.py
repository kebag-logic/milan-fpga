#!/usr/bin/env python3
"""Apply the head's check_implementation_log to a copied vivado.log beside a planted .bit."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from clock_constraints import check_implementation_log
p = Path(sys.argv[2])
try:
    check_implementation_log(p)
except RuntimeError as e:
    print("REFUSED:", str(e).splitlines()[0], len(str(e).splitlines()) - 1, "diagnostic lines")
else:
    print("ACCEPTED (unexpected)")
print(sorted(x.name for x in p.parent.iterdir()))
