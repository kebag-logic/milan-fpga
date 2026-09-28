#!/usr/bin/env python3
"""Run r2_probes (named probes + seeded randomized differential run) against
named mutants and compare every per-seed port-trace digest with the head RTL.
Usage: probe_mutants_r2.py <exported-tree> <scratch-dir> <receipt> <seeds> name...
Mutant names come from own_mutants_r2.MUTANTS or EXTRA below (the author's
declared equivalent controls, copied verbatim from retry_mutants.py).
"""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("om", here / "own_mutants_r2.py")
om = importlib.util.module_from_spec(spec); spec.loader.exec_module(om)
EXTRA = {
    "A_no_sticky_gp_window": [("(maap_busy_r || gp_valid_r) && maap_kill_w",
                               "maap_busy_r && maap_kill_w")],
    "A_accept_kill_zero": [(
        "        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]\n"
        "                       || pe_conflict_r[mreq_src_r]\n"
        "                       || (maap_conflict_valid_i\n"
        "                           && maap_conflict_src_i == mreq_src_r);",
        "        maap_kill_r <= 1'b0;")],
    "A_kill_no_pending_conflict": [(
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n"
        "                       || pe_conflict_r[maap_src_r]\n",
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n")],
}
src, scratch, receipt, seeds = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
rtl = Path("hdl/acmp/KL_acmp_talker.sv")


def run(name, text):
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    for d in ("hdl", "tb/acmp_talker", "tb/common"):
        shutil.copytree(src / d, tree / d, ignore=shutil.ignore_patterns("obj_dir"))
    (tree / rtl).write_text(text)
    r = subprocess.run([str(here / "run_r2_probes.sh"), str(tree), str(scratch / (name + "-build")), seeds],
                       capture_output=True, text=True, check=False)
    shutil.rmtree(tree); shutil.rmtree(scratch / (name + "-build"), ignore_errors=True)
    return r.returncode, r.stdout


base_text = (src / rtl).read_text()
rc0, out0 = run("head", base_text)
head = dict(re.findall(r"TRACE seed=(\d+) digest=(\w+)", out0))
lines = [f"== head (rc={rc0}) seeds={len(head)}", *[l for l in out0.splitlines() if not l.startswith("TRACE")]]
for name in sys.argv[5:]:
    reps = om.MUTANTS.get(name) or EXTRA[name]
    text = base_text
    for old, new in reps:
        assert text.count(old) == 1, name
        text = text.replace(old, new)
    rc, out = run(name, text)
    dig = dict(re.findall(r"TRACE seed=(\d+) digest=(\w+)", out))
    diff = sorted((int(s) for s in head if dig.get(s) != head[s]))
    named = [l for l in out.splitlines() if l.startswith(("PROBE-FAIL", "BEHAVIOR P7", "BEHAVIOR P8", "BEHAVIOR P9"))]
    lines.append(f"== {name} (rc={rc}) trace-differs-from-head in {len(diff)}/{len(head)} seeds"
                 + (f" first={diff[:5]}" if diff else ""))
    lines += ["   " + l for l in named]
    print(lines[-1 - len(named)], flush=True)
    for l in named: print("   " + l, flush=True)
receipt.write_text("\n".join(lines) + "\n")
