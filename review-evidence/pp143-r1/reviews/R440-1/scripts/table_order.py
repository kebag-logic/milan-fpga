#!/usr/bin/env python3
"""Check whether each README table that a driver's docs call 'the table's order' lists the arms in declared order."""
import importlib.util
import re
import sys
from pathlib import Path
ROOT = Path(sys.argv[1])


def load(rel):
    spec = importlib.util.spec_from_file_location("m", ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rows(readme, start, names):
    text = (ROOT / readme).read_text()
    text = text[text.index(start):]
    found = []
    for line in text.splitlines():
        cell = re.match(r"^\|\s*`?([\w\-.]+)`?", line)
        if cell and cell.group(1) in names and cell.group(1) not in found:
            found.append(cell.group(1))
        if len(found) == len(names):
            break
    return found


def check(label, declared, readme, start):
    seen = rows(readme, start, set(declared))
    order = [n for n in dict.fromkeys(declared) if n in seen]
    print(f"{label}: declared {len(dict.fromkeys(declared))}, table rows found {len(seen)}, "
          f"same order: {seen == order}")
    if seen != order:
        for i, (a, b) in enumerate(zip(seen, order)):
            if a != b:
                print(f"   first difference at row {i}: table {a!r} vs declared {b!r}")
                break


check("retry", list(load("tb/acmp_talker/retry_mutants.py").MUTATIONS), "tb/acmp_talker/README.md",
      "| Mutant | Result |")
check("adp", [x[0] for x in load("tb/adp_engine/mutants.py").MUTANTS], "tb/adp_engine/README.md",
      "## Mutation campaign")
check("maap", [x[0] for x in load("tb/maap/mutants.py").MUTANTS], "tb/maap/README.md",
      "| Arm (patch) |")
check("aecp", [x[0] for x in load("tb/pp_top/aecp_mutants.py").MUTANTS], "tb/pp_top/README.md",
      "### AECP deadline and hazard-class controls")
check("dispatch", [x[0] for x in load("tb/pp_top/aecp_dispatch_mutants.py").MUTANTS],
      "tb/pp_top/README.md", "### AECP dispatch and response negative controls")
check("gsi", [v[0] for v in load("tb/pp_top/gsi_mutants.py").mutations()], "tb/pp_top/README.md",
      "| Mutation | Required failing check |")
