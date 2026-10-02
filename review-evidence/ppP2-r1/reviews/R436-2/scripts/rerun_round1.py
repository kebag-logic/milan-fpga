#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-1 probes re-run UNCHANGED at the R436-2 head (c0715410).

The edits are copied verbatim from the published round-1 scripts:
  R436-1 scripts/probe.py: W6, W15, W15b, W16
  R437-1 scripts/probes_set1.py: X12, X17, X18, X24, X24b
Each runs in a fresh copy of the exported head with `make -s run` in
tb/nvm_port (the elab guard, then the suite at 100 and at 37), under the
pristine harness and under the coincident-completion model. W6's anchor names
the round-1 count, which the head replaced; it is therefore also applied, still
unchanged, to the round-1 port source (70bf017d) under the head's harness,
alongside that round-1 source alone, so its verdict can be read at this head.

usage: rerun_round1.py <head export> <round-1 port source> <out dir> [--jobs N]
VERILATOR must name the pinned 5.050 wrapper.
"""
import argparse
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
from pathlib import Path

RTL = "hdl/packet_engine/KL_pp_nvm_port.sv"
SIM = "tb/nvm_port/sim_main.cpp"
TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")

PROBES = {
    # ---- R436-1 (scripts/probe.py, verbatim) ----
    "W6": [(RTL, "else if (!owe_w || prog_w) tmo_r <= '0;",
            "else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;\n    else if (!owe_w) tmo_r <= tmo_r;")],
    "W15": [(RTL, "S_RHREQ: if (!owed_r) begin", "S_RHREQ: begin")],
    "W15b": [(RTL, "S_WEREQ: if (!owed_r) begin", "S_WEREQ: begin")],
    "W16": [(RTL, "|| (dev_rvalid_i && dev_rready_o);", "|| (dev_rvalid_i && dev_rready_o && !owed_r);")],
    # ---- R437-1 (scripts/probes_set1.py, verbatim) ----
    "X12": [(RTL, "      end else if (dl_w && dev_cmd_owned_w) begin",
             "      end else if (dl_w && dev_cmd_owned_w && (state_r != S_WWAIT)) begin")],
    "X17": [(RTL, "                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
             "                  || (dev_done_i && dev_cmd_owned_w)")],
    "X18": [(RTL, "                  || (dev_rvalid_i && dev_rready_o);",
             "                  || (dev_rvalid_i && dev_rready_o && !owed_r);")],
    "X24": [(RTL, "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request",
             "        S_RHREQ: begin")],
    "X24b": [
        (RTL, "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RHREQ: begin"),
        (RTL, "        S_RPREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RPREQ: begin"),
        (RTL, "        S_WEREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WEREQ: begin"),
        (RTL, "        S_WWREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WWREQ: begin")],
    "head": [],
}
MODELS = {
    "pristine": [],
    "coincident": [(SIM, "  bool done_on_last_byte = false;", "  bool done_on_last_byte = true;")],
}


def run(head, r1rtl, out, name, edits, model, on_round1):
    tag = f"{name}{'@r1src' if on_round1 else ''}__{model}"
    work = out / "work" / tag
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(head, work, symlinks=True)
    if on_round1:
        shutil.copyfile(r1rtl, work / RTL)
    for rel, old, new in edits + MODELS[model]:
        p = work / rel
        t = p.read_text()
        n = t.count(old)
        if n != 1:
            (out / f"{tag}.log").write_text(f"ANCHOR {rel} occurs {n} times: {old!r}\n")
            shutil.rmtree(work, ignore_errors=True)
            return tag, f"ANCHOR occurs {n} times", []
        p.write_text(t.replace(old, new, 1))
    mk = work / "tb" / "nvm_port" / "Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 2"))
    p = subprocess.run(["make", "-s", "run", f"VERILATOR={os.environ['VERILATOR']}"],
                       cwd=work / "tb" / "nvm_port", capture_output=True, text=True, timeout=3600)
    log = p.stdout + p.stderr
    (out / f"{tag}.log").write_text(log)
    fails = [l for l in log.splitlines() if l.startswith("FAIL")]
    shutil.rmtree(work, ignore_errors=True)
    return tag, f"rc={p.returncode} tallies={TALLY.findall(log)}", fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head"); ap.add_argument("r1rtl"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    head, out = Path(a.head), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(n, e, m, False) for n, e in PROBES.items() for m in MODELS]
    jobs += [("W6", PROBES["W6"], m, True) for m in MODELS]
    jobs += [("round1-count", [], m, True) for m in MODELS]
    lines = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run, head, Path(a.r1rtl), out, n, e, m, r1) for n, e, m, r1 in jobs]
        for f in futs:
            tag, res, fails = f.result()
            names = sorted({re.sub(r"[: ].*", "", x[6:]) for x in fails})
            lines.append(f"{tag}: {res}\n    failing: {len(fails)} lines; check ids: {' '.join(names)}"
                         + ("\n    first: " + "\n    first: ".join(fails[:6]) if fails else ""))
    (out / "SUMMARY.txt").write_text("\n".join(sorted(lines)) + "\n")
    print("\n".join(sorted(lines)))


if __name__ == "__main__":
    main()
