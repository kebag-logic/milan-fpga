#!/usr/bin/env python3
"""Reviewer-owned disposable controls against tb/pp_top section DN (R502-2).

Each arm copies hdl/, tb/common/ and tb/pp_top/ from TREE into OUT/<arm>,
plants one exact text edit (refusing if the anchor is not unique), builds
`make gsi-build` and runs `./obj_dir/Vpp_top_sim --domain-notify-only`.
An arm is KILLED when the run exits non-zero, prints its tally, and every
named check fails. The golden (no edit) must PASS.
Usage: extra_dn_mutants.py TREE OUT VERILATOR [JOBS]
"""
import concurrent.futures
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

tree, out, vl = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 3
TOP = "hdl/top/protocol_processor_top.sv"
LINK = "|| (link_up_i != link_q_r) || gsi_avb_chg_i),\n"
DOM = "      .ev_avb_i              (gm_change_i || srp_evt_domain_change_w\n"

ARMS = {
    "golden": (None, ()),
    # the link term also held as a level while the link is down: a stream of
    # GET_AVB_INFO in DN4b's window. Grades "exactly one" against duplicates.
    "link_level_while_down": ((TOP, LINK, "|| (link_up_i != link_q_r) || !link_up_i || gsi_avb_chg_i),\n"),
                              ("DN4b:",)),
    # the link term on the rising edge only: link down sends nothing.
    "link_rise_only": ((TOP, LINK, "|| (link_up_i && !link_q_r) || gsi_avb_chg_i),\n"),
                       ("DN4b:", "DN4c:")),
    # ev_avb_i also takes the ADOPTED level: after <bench-switch-model> a stream of
    # notifications with no DOMAIN_CHANGE. DN3 must see frames reach A.
    "avb_takes_adopted_level": ((TOP, DOM, "      .ev_avb_i              (gm_change_i || srp_evt_domain_change_w || srp_domain_adopted_w\n"),
                                ("DN1b:", "DN3:")),
}
TALLY = re.compile(r"^\[build \w+, SRP_DOM_DEF_VID_P 0x[0-9a-f]+, DESC_LINE_BYTES_P \d+\] \d+ checks, \d+ failures$", re.M)


def run(name):
    edit, named = ARMS[name]
    w = out / name
    if w.exists():
        shutil.rmtree(w)
    for d in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(tree / d, w / d, ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    if edit:
        f, old, new = edit
        p = w / f
        s = p.read_text()
        if s.count(old) != 1:
            return {"arm": name, "verdict": "REFUSED", "count": s.count(old)}
        p.write_text(s.replace(old, new, 1))
    log = out / f"{name}.log"
    with log.open("w") as fh:
        b = subprocess.run(["make", "gsi-build", "VERILATOR=" + vl], cwd=w / "tb/pp_top",
                           stdout=fh, stderr=subprocess.STDOUT).returncode
        r = subprocess.run(["./obj_dir/Vpp_top_sim", "--domain-notify-only"], cwd=w / "tb/pp_top",
                           stdout=fh, stderr=subprocess.STDOUT).returncode if b == 0 else None
    text = log.read_text(errors="replace")
    fails = [l[6:] for l in text.splitlines() if l.startswith("FAIL: ")]
    done = bool(TALLY.search(text))
    missing = [c for c in named if not any(f.startswith(c) for f in fails)]
    if not edit:
        verdict = "PASS" if (r == 0 and done and not fails) else "BROKEN"
    else:
        verdict = "KILLED" if (r not in (0, None) and done and not missing) else "SURVIVED"
    shutil.rmtree(w)
    return {"arm": name, "build_rc": b, "run_rc": r, "completed": done, "named": list(named),
            "missing": missing, "failing_checks": fails, "verdict": verdict}


out.mkdir(parents=True, exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    res = list(pool.map(run, ARMS))
(out / "results.json").write_text(json.dumps(res, indent=1) + "\n")
for r in res:
    print(json.dumps({k: r.get(k) for k in ("arm", "verdict", "missing", "failing_checks")}))
ok = all(r["verdict"] in ("PASS", "KILLED") for r in res)
print("extra DN controls:", "ALL AS EXPECTED" if ok else "UNEXPECTED")
sys.exit(0 if ok else 1)
