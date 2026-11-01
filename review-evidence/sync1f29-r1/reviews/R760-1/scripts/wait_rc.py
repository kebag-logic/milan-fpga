#!/usr/bin/env python3
"""Wait up to N seconds for each named run's rc file."""
import sys, time
from pathlib import Path
limit, logs, names = float(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
end = time.monotonic() + limit
while time.monotonic() < end and not all((logs / f'{n}.rc').exists() for n in names):
    time.sleep(10)
print({n: ((logs / f'{n}.rc').read_text().strip() if (logs / f'{n}.rc').exists() else None) for n in names})
