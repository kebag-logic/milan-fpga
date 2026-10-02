#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned planted defects in KL_pp_nvm_port's deadline count (R436-2).

Each plant edits ONE copy of the port (every anchor must occur exactly once),
then, concurrently:
  * builds tb/nvm_port at MEM_TIMEOUT_CYC_P = 100 (`make primary`) under the
    pristine harness and under each named model switch, and records the tally
    and every failing check name;
  * builds the reviewer's pause_fuzz.cpp at the listed bounds and runs its
    legal, silent and resume modes over several seeds.

usage: plant.py <head export dir> <work dir> <receipt dir> [--jobs N] [--only a,b]
VERILATOR must name the pinned 5.050 wrapper.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

WAITS = ("                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n"
         "                       || (state_r == S_RPWAIT)) && !done_seen_r)")


def drop_wait(state):
    """The latched-terminal exemption taken from one wait state only."""
    rest = [s for s in ("S_WEWAIT", "S_WWAIT", "S_RHWAIT", "S_RPWAIT") if s != state]
    new = (f"                  || (state_r == {state})\n"
           f"                  || (((state_r == {rest[0]}) || (state_r == {rest[1]})"
           f" || (state_r == {rest[2]})) && !done_seen_r)")
    return [(WAITS, new)]


TMO_CLR = "    else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;"
TMO_INC = "    else if (owe_w && !tmo_hit_w)           tmo_r <= tmo_r + TMO_W_C'(1);"

PLANTS = {
    # ---- the reviewer's own plants in the pause logic ----
    "Q1-wewait-latched-owes": drop_wait("S_WEWAIT"),
    "Q2-rhwait-latched-owes": drop_wait("S_RHWAIT"),
    "Q3-wwait-latched-owes": drop_wait("S_WWAIT"),
    "Q4-rpwait-latched-owes": drop_wait("S_RPWAIT"),
    "Q5-count-runs-unowed": [(TMO_INC,
        "    else if (!tmo_hit_w)                    tmo_r <= tmo_r + TMO_W_C'(1);")],
    "Q6-rready-drop-clears": [(TMO_CLR,
        "    else if (prog_w || (state_r == S_IDLE) || ((state_r == S_RPPUMP) && !nvm_rready_i)) tmo_r <= '0;")],
    "Q7-wvalid-drop-clears": [(TMO_CLR,
        "    else if (prog_w || (state_r == S_IDLE) || ((state_r == S_WDPUMP) && !nvm_wvalid_i)) tmo_r <= '0;")],
    "Q8-holding-states-clear": [(TMO_CLR,
        "    else if (prog_w || (state_r == S_IDLE) || (state_r == S_WHDR) || (state_r == S_RHFWD)) tmo_r <= '0;")],
    "Q9-verdict-on-paused-cycle": [("  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
        "  assign dl_w = !prog_w && tmo_hit_w && (state_r != S_IDLE) && (state_r != S_FIN);")],
    "Q10-zero-at-fin-not-idle": [(TMO_CLR,
        "    else if (prog_w || (state_r == S_FIN))  tmo_r <= '0;")],
    # ---- the gate's own rows, as a calibration of the fuzz ----
    "D24": [(TMO_CLR, "    else if (prog_w || !owe_w)             tmo_r <= '0;")],
    "D25": [(TMO_CLR, "    else if (prog_w)                        tmo_r <= '0;")],
    "D26": [("                       || (state_r == S_RPWAIT)) && !done_seen_r)",
             "                       || (state_r == S_RPWAIT)))")],
    "D20": [("                  || (dev_rvalid_i && dev_rready_o);",
             "                  || (dev_rvalid_i && dev_rready_o && !owed_r);")],
    "D21": [("                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
             "                  || (dev_done_i && dev_cmd_owned_w)")],
    "pristine": [],
}

MODELS = {
    "pristine": None,
    "coincident": ("  bool done_on_last_byte = false;", "  bool done_on_last_byte = true;"),
    "unsolicited": ("  bool unsol_model = false;", "  bool unsol_model = true;"),
    "lazy": ("  bool lazy_erase = false;", "  bool lazy_erase = true;"),
}

FUZZ_TMOS = (37, 3)
FUZZ_SEEDS = (11, 12, 13)
FUZZ_OPS = 600
TALLY_RE = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def edit_once(path, old, new):
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path.name}: anchor occurs {n} times: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1))


def make_tree(head, work, plant, model):
    d = work / f"{plant}__{model}"
    if d.exists():
        shutil.rmtree(d)
    (d / "hdl").mkdir(parents=True)
    shutil.copytree(head / "hdl" / "packet_engine", d / "hdl" / "packet_engine")
    (d / "tb").mkdir()
    shutil.copytree(head / "tb" / "nvm_port", d / "tb" / "nvm_port",
                    ignore=shutil.ignore_patterns("obj_dir", "obj_alt"))
    shutil.copytree(head / "tb" / "common", d / "tb" / "common")
    rtl = d / "hdl" / "packet_engine" / "KL_pp_nvm_port.sv"
    for old, new in PLANTS[plant]:
        edit_once(rtl, old, new)
    if MODELS.get(model):
        edit_once(d / "tb" / "nvm_port" / "sim_main.cpp", *MODELS[model])
    return d, rtl


def run_suite(head, work, plant, model):
    d, _ = make_tree(head, work, plant, model)
    mk = d / "tb" / "nvm_port" / "Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 2"))
    p = subprocess.run(["make", "-s", "primary", f"VERILATOR={os.environ['VERILATOR']}"],
                       cwd=d / "tb" / "nvm_port", capture_output=True, text=True)
    out = p.stdout + p.stderr
    m = TALLY_RE.findall(out)
    fails = [l[6:] for l in out.splitlines() if l.startswith("FAIL: ")]
    res = {"plant": plant, "kind": "suite", "model": model, "rc": p.returncode,
           "tally": m[-1] if m else None, "fails": fails}
    shutil.rmtree(d, ignore_errors=True)
    return res


def run_fuzz(head, work, plant, tmo):
    d, rtl = make_tree(head, work, plant, f"fuzz{tmo}")
    out = d / "fz"
    b = subprocess.run([str(HERE / "build_fuzz.sh"), str(rtl), str(tmo), str(out)],
                       capture_output=True, text=True)
    res = {"plant": plant, "kind": "fuzz", "tmo": tmo, "build_rc": b.returncode, "runs": []}
    if b.returncode == 0:
        for mode in ("legal", "silent", "resume"):
            for seed in FUZZ_SEEDS:
                try:
                    r = subprocess.run([str(out / "Vfuzz"), mode, str(seed), str(FUZZ_OPS)],
                                       capture_output=True, text=True, timeout=900)
                    lines = r.stdout.splitlines()
                    res["runs"].append({"mode": mode, "seed": seed, "rc": r.returncode,
                                        "tally": TALLY_RE.findall(r.stdout)[-1:] or None,
                                        "summary": [l for l in lines if l.startswith("pause_fuzz")],
                                        "first_fails": [l for l in lines if l.startswith("FAIL")][:3]})
                except subprocess.TimeoutExpired:
                    res["runs"].append({"mode": mode, "seed": seed, "rc": "timeout"})
    shutil.rmtree(d, ignore_errors=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head"); ap.add_argument("work"); ap.add_argument("receipts")
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    head, work, rec = Path(a.head), Path(a.work), Path(a.receipts)
    work.mkdir(parents=True, exist_ok=True); rec.mkdir(parents=True, exist_ok=True)
    names = [n for n in PLANTS if not a.only or n in a.only.split(",")]
    jobs = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for n in names:
            for mdl in MODELS:
                jobs.append(ex.submit(run_suite, head, work, n, mdl))
            for t in FUZZ_TMOS:
                jobs.append(ex.submit(run_fuzz, head, work, n, t))
        results = [j.result() for j in jobs]
    (rec / "plants.json").write_text(json.dumps(results, indent=1))
    # a compact table
    lines = ["| plant | suite pristine | coincident | unsolicited | lazy | fuzz 37 (legal/silent/resume fails) | fuzz 3 |",
             "|---|---|---|---|---|---|---|"]
    for n in names:
        row = [n]
        for mdl in MODELS:
            r = next(x for x in results if x["plant"] == n and x["kind"] == "suite" and x["model"] == mdl)
            t = r["tally"]
            row.append(f"{t[2]} of {t[0]}: " + ", ".join(sorted({f.split(' ')[0] for f in r['fails']}))[:120]
                       if t else f"no tally rc {r['rc']}")
        for t in FUZZ_TMOS:
            r = next(x for x in results if x["plant"] == n and x["kind"] == "fuzz" and x["tmo"] == t)
            per = {}
            for run in r["runs"]:
                f = int(run["tally"][0][2]) if run.get("tally") else -1
                per.setdefault(run["mode"], []).append(f)
            row.append("/".join(str(sum(v)) if min(v) >= 0 else "ERR" for v in per.values())
                       if per else f"build rc {r['build_rc']}")
        lines.append("| " + " | ".join(row) + " |")
    (rec / "plants.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
