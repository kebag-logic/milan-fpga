#!/usr/bin/env python3
"""Check stored command dispositions and named mutation/omission receipts."""
import json
import re
from pathlib import Path

p = Path(__file__).resolve().parent
rcs = sorted(x for x in p.rglob("*.rc") if "scratch" not in x.relative_to(p).parts)
assert len(rcs) == 112, len(rcs)
assert all(x.read_text().strip() == "0" for x in rcs)
mutations = []
for escape in sorted(p.glob("*-escape.log")):
    name = escape.name.removesuffix("-escape.log")
    run = p / (name + "-run.log")
    if not run.exists():
        assert name == "guard"
        continue
    text = run.read_text()
    failures = [line for line in text.splitlines() if "[FAIL]" in line]
    assert failures and "RESULT: FAIL" in text, name
    groups = [re.search(r"\[(?:726|F5) ([A-Z_]+)\]", line) for line in failures]
    assert all(groups), (name, failures)
    found = {match[1] for match in groups}
    assert len(found) == 1, (name, found)
    escaped = escape.read_text()
    assert "RESULT: PASS" in escaped and "[FAIL]" not in escaped, name
    mutations.append({"task": name, "failing_group": sorted(found)[0],
                      "named_failures": len(failures), "omission_escape": "PASS",
                      "driver_rc": int((p / (name + ".rc")).read_text())})
assert len(mutations) == 22, len(mutations)
(p / "mutation-summary.json").write_text(json.dumps(mutations, indent=2) + "\n")
summary = {"successful_command_rc_receipts": len(rcs),
           "rc_paths": [str(x.relative_to(p)) for x in rcs],
           "named_mutation_omission_pairs": len(mutations),
           "recursive_counter_pass_legs": (p / "make-counters.log").read_text().count("RESULT: PASS"),
           "removed_bind_resets_detected": len(json.loads((p / "contract-mutations.json").read_text())),
           "shift_receipts": len(list(p.glob("shift-*.log")))}
assert summary["recursive_counter_pass_legs"] == 4
assert summary["removed_bind_resets_detected"] == 16
assert summary["shift_receipts"] == 12
(p / "execution-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print({k: v for k, v in summary.items() if k != "rc_paths"})
