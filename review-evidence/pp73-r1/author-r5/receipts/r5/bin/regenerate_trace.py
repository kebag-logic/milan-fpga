"""Render traceability records from the unchanged requirement gate's readers and rules."""
import importlib.util
from pathlib import Path
import re
import sys
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("req_records", root / "scripts/check-req-tags.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
review = (root / gate.REVIEW).read_text()
verify = (root / gate.VERIFY).read_text()
rows = gate.read_rows(review)
problems = []
waivers = gate.read_waivers(verify, rows, problems)
tags = gate.read_tags(root, rows, problems)
states = gate.row_states(rows, tags, waivers, problems)
if problems:
    raise SystemExit("\n".join(problems))
def cov(match):
    cells = match[0].split("|")
    req = cells[1].strip()
    cells[5] = " " + rows[req].cov[0] + "; " + states[req] + " "
    return "|".join(cells)
review = re.sub(r"^\| REQ-[A-Z]+-\d{3} \|.*$", cov, review, flags=re.M)
records = [gate.RECORD_HEADER, "|---|---|---|"]
for state in ("traced", "no check"):
    for ver in (*gate.NEEDS_CHECK, *gate.NO_CHECK):
        names = [req for req, row in rows.items() if states[req] == state and row.ver == ver]
        for at in range(0, len(names), 21):
            records.append(f"| {state} | {ver} | {', '.join(names[at:at + 21])} |")
a = verify.index(gate.RECORD_HEADER, verify.index(gate.RECORD_ANCHOR))
b = verify.index("\n\n", a)
verify = verify[:a] + "\n".join(records) + verify[b:]
(root / gate.REVIEW).write_text(review)
(root / gate.VERIFY).write_text(verify)
print(f"Regenerated {len(states)} Cov states and {len(records) - 2} coverage rows from the requirement gate")
