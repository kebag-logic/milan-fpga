"""Probe the emitter-VID guard of tb/common/gen_declaration_fixture.py.

Usage: python3 -B probe_vid_guard.py <base-tree> <head-tree> <work-dir>

1. Predicate equivalence: the retired assert condition and the new raise
   condition (both copied verbatim from the two commits and checked against
   the files) must accept exactly the same values over integers -5..5000 and
   a set of non-integer values.
2. Execution: the head script is run on fixtures carrying valid and invalid
   emitter VIDs under normal and optimized Python. Valid VIDs must succeed
   with headers byte-identical to the base script's output; invalid VIDs must
   exit non-zero with ValueError under BOTH modes. Header comparison drops
   the single banner line that records the per-run config path (the base assert disappears
   under -O, which is the point of the change).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

base, head, work = (Path(a).resolve() for a in sys.argv[1:4])
OLD = "assert type(vid) is int and 1 <= vid <= 4094 and vid != 2"
NEW = "if type(vid) is not int or not 1 <= vid <= 4094 or vid == 2:"
src_old = (base / "tb/common/gen_declaration_fixture.py").read_text()
src_new = (head / "tb/common/gen_declaration_fixture.py").read_text()
result = {"old_line_present_in_base": OLD in src_old,
          "new_line_present_in_head": NEW in src_new,
          "old_line_absent_in_head": OLD not in src_new}


def old_accepts(vid):
    return type(vid) is int and 1 <= vid <= 4094 and vid != 2


def new_refuses(vid):
    return type(vid) is not int or not 1 <= vid <= 4094 or vid == 2


values = list(range(-5, 5001)) + [True, False, 1.0, 73.0, "73", None, [73], 2**64]
mismatch = [repr(v) for v in values if old_accepts(v) == new_refuses(v)]
result["predicate_values_checked"] = len(values)
result["predicate_mismatches"] = mismatch

runs = []
cases = [1, 73, 4094, 2, 0, 4095, -1, True, 73.0, "73", None]
for tree_tag, tree in (("base", base), ("head", head)):
    for vid in cases:
        for opt in (False, True):
            name = f"{tree_tag}-{'O' if opt else 'n'}-{vid!r}".replace("'", "q").replace(" ", "")
            fx = work / f"{name}.yaml"
            fx.parent.mkdir(parents=True, exist_ok=True)
            fx.write_text("base: configs/endstation_arty_current.yaml\n"
                          f"emitter_srp_vid: {json.dumps(vid) if vid is not None else 'null'}\n")
            out = work / f"{name}.out"
            cmd = [sys.executable, "-B"] + (["-O"] if opt else []) + [
                "tb/common/gen_declaration_fixture.py", str(fx), str(out)]
            p = subprocess.run(cmd, cwd=tree, capture_output=True, text=True)
            rec = dict(tree=tree_tag, vid=repr(vid), optimized=opt, rc=p.returncode,
                       error=(p.stderr.strip().splitlines() or [""])[-1])
            if p.returncode == 0:
                # The header banner records the per-run config path
                # ("//  Source      : <outdir>/config.yaml"); drop that one
                # line so runs in different output directories compare.
                rec["headers"] = {h: hashlib.sha256(b"".join(
                    line for line in (out / "gen" / h).read_bytes().splitlines(True)
                    if not line.startswith(b"//  Source      :"))).hexdigest()
                    for h in ("adp_shape_defaults.svh", "lwsrp_csr_defaults.svh")}
            runs.append(rec)
result["runs"] = runs

valid = {1, 73, 4094}
checks = []
for r in runs:
    vid_ok = r["vid"] in {repr(v) for v in valid}
    if r["tree"] == "head":
        if vid_ok:
            checks.append(r["rc"] == 0)
        else:
            checks.append(r["rc"] != 0 and r["error"].startswith("ValueError"))
# valid headers identical base vs head for the same vid and mode
for vid in valid:
    for opt in (False, True):
        b = [r for r in runs if r["tree"] == "base" and r["vid"] == repr(vid) and r["optimized"] == opt][0]
        h = [r for r in runs if r["tree"] == "head" and r["vid"] == repr(vid) and r["optimized"] == opt][0]
        checks.append(b["rc"] == 0 and b.get("headers") == h.get("headers"))
# VID must actually reach the emitted header (not a no-op fixture)
h73 = [r for r in runs if r["tree"] == "head" and r["vid"] == "73" and not r["optimized"]][0]
h1 = [r for r in runs if r["tree"] == "head" and r["vid"] == "1" and not r["optimized"]][0]
checks.append(h73["headers"] != h1["headers"])
result["base_optimized_invalid_accepted"] = sorted(
    r["vid"] for r in runs if r["tree"] == "base" and r["optimized"] and r["rc"] == 0
    and r["vid"] not in {repr(v) for v in valid})
ok = all(checks) and not mismatch and all(
    result[k] for k in ("old_line_present_in_base", "new_line_present_in_head", "old_line_absent_in_head"))
result["verdict"] = "PASS" if ok else "FAIL"
print(json.dumps(result, indent=1))
sys.exit(0 if ok else 1)
