#!/usr/bin/env python3
"""classify_ok.py LOG CHECKOUT: classify every top-level `[ok]` line of a firmware gate log.

Classes: a normal arm outcome (`[ok] arm ...`), a control-source mutant (`[ok] mutant ...`),
an AECP or SRP campaign mutant (its name is a quoted string in `aecp_mutants.py`, or in one
of the `srp*mutants.py` tables, at the checkout), or a dependency-pin refusal control
(`[ok] lwSRP pin, ...`). A name present in both tables takes the campaign of the nearest
preceding unambiguous campaign line, because each campaign's lines are contiguous in the log;
every such resolution is listed. Anything else is unclassified, and the script then exits 1.
"""
import collections
import json
import re
import sys
from pathlib import Path


def names(path: Path) -> set[str]:
    """Every quoted kebab-case literal in a campaign table source."""
    return set(re.findall(r"""["']([a-z0-9][a-z0-9-]*[a-z0-9])["']""", path.read_text()))


def main() -> int:
    log, checkout = Path(sys.argv[1]), Path(sys.argv[2])
    test = checkout / "sw/firmware/ctrl/test"
    aecp = names(test / "aecp_mutants.py")
    srp = set().union(*(names(path) for path in sorted(test.glob("srp*mutants.py"))))
    counts = collections.Counter()
    bad, resolved = [], []
    current = None
    for line in log.read_text().splitlines():
        if not line.startswith("[ok] "):
            continue
        rest = line[5:]
        if rest.startswith("arm "):
            counts["normal arm outcome"] += 1
        elif rest.startswith("mutant "):
            counts["control-source mutant"] += 1
        elif rest.startswith("lwSRP pin, "):
            counts["dependency-pin refusal control"] += 1
        else:
            name = rest.split(":", 1)[0]
            hits = [label for label, table in (("AECP mutant", aecp), ("SRP mutant", srp)) if name in table]
            if len(hits) == 1:
                counts[hits[0]] += 1
                current = hits[0]
            elif len(hits) == 2 and current is not None:
                counts[current] += 1
                resolved.append({"line": line[:120], "campaign": current})
            else:
                bad.append(line[:120])
    total = sum(counts.values()) + len(bad)
    mutants = counts["control-source mutant"] + counts["AECP mutant"] + counts["SRP mutant"]
    report = {"top_level_ok_lines": total, "classes": dict(sorted(counts.items())),
              "source_mutant_executions": mutants,
              "resolved_by_campaign_order": resolved, "unclassified": bad}
    print(json.dumps(report, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
