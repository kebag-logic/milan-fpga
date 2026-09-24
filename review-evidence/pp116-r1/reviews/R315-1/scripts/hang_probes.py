#!/usr/bin/env python3
"""Hang-oriented probes for the three runners whose host deadlines PR #117
drops. Each probe copies the processor tree at the head under review into a
disposable directory, plants ONE edit chosen to make the DUT stop answering
(or to flood/freeze an output), then runs the harness command exactly as its
runner would. A probe PASSES when the harness exits on its own and prints its
tally. The only host deadline here is a reviewer-side guard (GUARD seconds):
a harness killed by it would be recorded as HANG, i.e. evidence against the
termination argument.

usage: hang_probes.py <processor-tree> <scratch-dir> <out-dir> [probe ...]
Needs a `verilator` on PATH (the pinned 5.050 wrapper).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

GUARD = 560
TALLY = re.compile(r"^(?:\[build [^\]]*\] )?\d+ checks[:,].*$", re.M)

GUARD_SV = "hdl/aecp/KL_aecp_desc_mem_guard.sv"
TOP_SV = "hdl/top/protocol_processor_top.sv"
ADM_SV = "hdl/srp/KL_srp_admission.sv"

# name: (file, [(old, new, count)], [(suite dir, command)])
DESC_RUN = [("tb/desc_mem_guard", ["make", "run", "GUARD_SRC=../../" + GUARD_SV,
                                   "OBJ_DIR=obj_probe", "ARGS=--late-only"])]
GSI_RUN = [("tb/pp_top", ["make", "gsi-build"]),
           ("tb/pp_top", ["./obj_dir/Vpp_top_sim", "--gsi-internal-only"])]
SRP_RUN = [("tb/srp_admission", ["make", "run", "N=2"]),
           ("tb/srp_admission", ["make", "run", "N=8"]),
           ("tb/srp_top", ["make", "run"])]
PROBES = {
    # memory responses never reach the store and are never accepted
    "desc-memory-mute": (GUARD_SV, [
        ("assign s_rsp_valid_o = m_rsp_valid_i;", "assign s_rsp_valid_o = 1'b0;", 1),
        ("assign m_rsp_ready_o = s_rsp_ready_i;", "assign m_rsp_ready_o = 1'b0;", 1)],
        DESC_RUN),
    # debt never clears: every request after the first is held for ever
    "desc-debt-forever": (GUARD_SV, [
        ("                 && (m_rsp_last_i || m_rsp_err_i)) begin\n      owed_r <= 1'b0;",
         "                 && (m_rsp_last_i || m_rsp_err_i)) begin\n      owed_r <= 1'b1;", 1)],
        DESC_RUN),
    # restore never completes: the listener is never released
    "gsi-restore-never-done": (TOP_SV, [
        ("assign restore_done_o = nvm_walk_done_w && lsn_released_w;",
         "assign restore_done_o = 1'b0;", 1)],
        GSI_RUN),
    # the MAC TX arbiter never presents a byte: no response ever leaves
    "gsi-tx-silent": (TOP_SV, [
        ("      SH_IDLE: begin\n        if (arb_tx_valid_w && sh_need_r) begin",
         "      SH_IDLE: begin\n        if (1'b0) begin", 1),
        ("          tx_valid_o     = arb_tx_valid_w;", "          tx_valid_o     = 1'b0;", 1),
        ("        tx_valid_o     = arb_tx_valid_w;", "        tx_valid_o     = 1'b0;", 2)],
        GSI_RUN),
    # admission never completes a round and never grants
    "srp-round-never": (ADM_SV, [
        ("          round_done_o <= 1'b1;", "          round_done_o <= 1'b0;", 1),
        ("      sr_admitted_o[s]       = grant_r[s] && req_i[s];",
         "      sr_admitted_o[s]       = 1'b0;", 1)],
        SRP_RUN),
    # admission verdict toggles every clock (tries to flood the FSMs)
    "srp-verdict-toggles": (ADM_SV, [
        ("      sr_admitted_o[s]       = grant_r[s] && req_i[s];",
         "      sr_admitted_o[s]       = req_i[s] && round_done_o;", 1)],
        SRP_RUN),
}


def run_probe(src: Path, scratch: Path, out: Path, name: str) -> dict:
    filename, edits, steps = PROBES[name]
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    for d in ("hdl", "tb/common", "tb/desc_mem_guard", "tb/pp_top", "tb/srp_admission",
              "tb/srp_top"):
        shutil.copytree(src / d, tree / d,
                        ignore=shutil.ignore_patterns("obj*", "__pycache__"))
    path = tree / filename
    text = path.read_text()
    for old, new, count in edits:
        if count == 0:
            continue
        if text.count(old) != count:
            raise SystemExit(f"{name}: expected {count} copies of {old!r}")
        text = text.replace(old, new)
    path.write_text(text)
    record = {"probe": name, "file": filename, "legs": []}
    for suite, cmd in steps:
        tag = re.sub(r"[^A-Za-z0-9=]+", "_", " ".join(cmd[:3]))
        log = out / f"{name}-{Path(suite).name}-{tag}.log"
        start = time.monotonic()
        try:
            with log.open("w") as stream:
                rc = subprocess.run(cmd, cwd=tree / suite, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=GUARD).returncode
            verdict = "TERMINATED"
        except subprocess.TimeoutExpired:
            rc, verdict = None, "HANG"
        text = log.read_text()
        leg = {"suite": suite, "cmd": " ".join(cmd), "rc": rc, "verdict": verdict,
               "seconds": round(time.monotonic() - start, 1),
               "tallies": TALLY.findall(text),
               "first_fail": next((l for l in text.splitlines() if l.startswith("FAIL")), "")}
        record["legs"].append(leg)
        print(json.dumps(leg), flush=True)
        if verdict == "HANG" or (cmd[0] == "make" and "build" in cmd[1] and rc != 0):
            break
    shutil.rmtree(tree)
    return record


def main() -> int:
    src, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
    names = sys.argv[4:] or list(PROBES)
    # at most eight CPUs, as the campaign runners pin themselves
    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    results = [run_probe(src, scratch, out, n) for n in names]
    with (out / "results.jsonl").open("a") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    hung = [r["probe"] for r in results for l in r["legs"] if l["verdict"] == "HANG"]
    print("HANG: " + ", ".join(hung) if hung else "all probes terminated on their own")
    return 1 if hung else 0


if __name__ == "__main__":
    raise SystemExit(main())
