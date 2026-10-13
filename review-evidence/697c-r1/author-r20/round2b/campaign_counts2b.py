#!/usr/bin/env python3
"""Scratch: the verdicts of one test_ctrl_firmware.py --self-test log, campaign by campaign.

usage: campaign_counts2b.py <tree> <log>
Classifies each '[ok]'/'[ESCAPED]' line after the control campaign's total by the defect tables of <tree>:
aecp_mutants.DEFECTS (the AECP campaign), srp_mutants.DEFECTS (the SRP campaign at two interfaces, then
its one-interface subset, told apart by a name's second occurrence). Prints counts and the sorted names.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import aecp_mutants  # noqa: E402
import srp_mutants  # noqa: E402

lines = Path(sys.argv[2]).read_text(errors="replace").splitlines()
arms = [l for l in lines if re.match(r"^\[(ok|FAIL)\] arm ", l)]
total = next(l for l in lines if l.startswith("mutants: "))
end = lines.index(total)
aecp = {d.name for d in aecp_mutants.DEFECTS}
srp = {d.name for d in srp_mutants.DEFECTS}
# The campaigns run in order, each in its table's order: AECP, SRP at two interfaces, SRP's subset at one.
verdicts = [(m[1], m[2]) for l in lines[end + 1:]
            if (m := re.match(r"^\[(ok|ESCAPED)\] ([A-Za-z0-9][\w.-]*):", l)) and (m[2] in aecp or m[2] in srp)]
order = {"aecp": [d.name for d in aecp_mutants.DEFECTS], "srp2": [d.name for d in srp_mutants.DEFECTS]}
rows = {"aecp": verdicts[:len(order["aecp"])],
        "srp2": verdicts[len(order["aecp"]):len(order["aecp"]) + len(order["srp2"])],
        "srp1": verdicts[len(order["aecp"]) + len(order["srp2"]):]}
for key in ("aecp", "srp2"):
    if [n for _, n in rows[key]] != order[key]:
        raise SystemExit(f"{key}: the log's verdicts are not the table's names in order")
if any(n not in srp for _, n in rows["srp1"]):
    raise SystemExit("srp1: a verdict outside the SRP table")
ctrl_ok = sum(1 for l in lines if l.startswith("[ok] mutant "))
print(f"arms: {len(arms)} ({sum(a.startswith('[ok]') for a in arms)} ok)")
print(f"control campaign: {total}; [ok] {ctrl_ok}")
for key, label in (("aecp", "AECP campaign"), ("srp2", "SRP campaign (two interfaces)"),
                   ("srp1", "SRP campaign (one-interface subset)")):
    ok = sum(v == "ok" for v, _ in rows[key])
    print(f"{label}: caught {ok}, escaped {len(rows[key]) - ok} (table {len(aecp) if key == 'aecp' else len(srp)})")
print("lwSRP pin arms:", sum(1 for l in lines if l.startswith("[ok] lwSRP pin")), "ok")
print("verdict:", [l for l in lines if l.startswith("test_ctrl_firmware:") or l.startswith("exit=")])
