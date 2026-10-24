#!/usr/bin/env python3
"""Compare format_mutants.py's two-copy replacement lines with the reviewer
probe's, byte for byte, for both bundles. usage: compare_mutants.py <avtp_rxmon dir> <probe_sq_claims.py> <probe_lock_settle.py>"""
import ast, sys
from pathlib import Path
def consts(path, names):
    t = ast.parse(Path(path).read_text()); out = {}
    for n in ast.walk(t):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) in names:
            out[n.targets[0].id] = ast.literal_eval(n.value)
    return out
fm = consts(Path(sys.argv[1]) / "format_mutants.py", {"BOTH_COPIES", "REJECT_WB", "BUNDLES"})
pr = consts(sys.argv[2], {"MUTANTS", "ENG_ANCHOR", "REF_ANCHOR"})
src = Path(sys.argv[3]).read_text()
eng = (Path(sys.argv[1]) / "../../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv").read_text()
ref = (Path(sys.argv[1]) / "reference/KL_avtp_rx_monitor_ctx_ref.sv").read_text()
for b, anchor, text, label in (("cur_w", pr["ENG_ANCHOR"], eng, "engine"), ("cur_r", pr["REF_ANCHOR"], ref, "reference")):
    a = fm["REJECT_WB"].replace("BUNDLE", b)
    print(f"{label}: anchor identical to probe's: {a == anchor}; occurrences in source: {text.count(a)}")
pairs = {"mr seed set": "mr_seed_set", "mr seed clear": "mr_seed_clear"}
for name, rep, breaks in fm["BOTH_COPIES"]:
    short = name.split(":")[0]
    for b in fm["BUNDLES"]:
        mine = rep.replace("BUNDLE", b)
        if short in pairs:
            theirs = "            monst_r <= " + pr["MUTANTS"][pairs[short]].replace("%s", b)
            print(f"{short} [{b}]: identical to probe {pairs[short]}: {mine == theirs}")
        else:
            print(f"{short} [{b}]: {mine.strip()}  (present in probe_lock_settle.py: {mine.strip().replace(b, 'cur_w') in src or mine.strip() in src})")
