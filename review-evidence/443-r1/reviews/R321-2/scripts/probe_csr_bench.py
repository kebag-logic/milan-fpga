#!/usr/bin/env python3
"""Round-2 reviewer probes for issue #443 / RENDER_STAT (0x8DC).

These target the checks round 2 added: the standalone CSR bench at N=1
(tb/verilator/csr/sim_main.cpp -> obj_dir/Vcsr_sim), the NxN window bench
at N_LISTENERS_P=4 (sim_win.cpp -> obj_win/Vcsr_win), and the milan_dp aclk
leg (--render-csr-only). Each probe copies a clean exact-head tree into a
disposable directory, applies exact textual substitutions to milan_csr.sv
(each anchor must occur exactly once), builds the one executable through
the suite's own Makefile recipe and runs it. A mutant is CAUGHT when the
run exits non-zero with a [FAIL] line naming a RENDER_STAT / RENDER-CSR
check or a 0x8DC neighbour; it SURVIVES when the run passes. Clean probes
are positive controls. The source tree is never modified; each copy
(without build directories, and without .git for the CSR-bench legs) is deleted after its run.

usage: probe_csr_bench.py <clean-head-tree> <scratch-dir> [probe ...]
Verilator is whatever `verilator` resolves to on PATH (record its version).
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CSR = "hdl/common/csr/milan_csr.sv"
SEL = "if (!strm_dir_r && (32'(strm_idx_r) == s))"
MUX = "live_mux = i_render_status[s*32 +: 32];"
WIN = "(rd_addr_q == A_RENDER_STAT) ||"
CASE = "      A_RENDER_STAT: begin"

WINDOW_SEM = "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))"
LSN0_KEEP_DIR = "if (!strm_dir_r && (strm_lsn0_r ? (s == 0) : (32'(strm_idx_r) == s)))"

# name: (leg, [(anchor, replacement), ...])
MUTANTS = {
    "window_sem": [(SEL, WINDOW_SEM)],
    "lsn0_keep_dir": [(SEL, LSN0_KEEP_DIR)],
    "ignore_direction": [(SEL, "if ((32'(strm_idx_r) == s))")],
    "alias_listener0": [(MUX, "live_mux = i_render_status[0 +: 32];")],
    "drop_read_window": [(WIN, "")],
    "rails_truncated": [(MUX, "live_mux = {16'd0, i_render_status[s*32 +: 16]};")],
    "neighbour_alias": [(CASE, "      A_RENDER_STAT, A_RENDER_STAT + 'h4: begin"),
                        (WIN, "(rd_addr_q == A_RENDER_STAT) || "
                              "(rd_addr_q == A_RENDER_STAT + 'h4) ||")],
}

LEGS = {
    "main": (["make", "-s", "-C", "tb/verilator/csr", "obj_dir/Vcsr_sim"],
             ["./obj_dir/Vcsr_sim"], "tb/verilator/csr"),
    "win": (["make", "-s", "-C", "tb/verilator/csr", "obj_win/Vcsr_win"],
            ["./obj_win/Vcsr_win"], "tb/verilator/csr"),
    "aclk": (["make", "-s", "-C", "tb/verilator/milan_dp", "aclk-build"],
             ["./obj_aclk/Vmilan_dp_aclk", "--render-csr-only"], "tb/verilator/milan_dp"),
}

NAMED = ("RENDER_STAT", "RENDER-CSR", "0x8E0", "0x8F4")


def parse(name: str) -> tuple[str, str]:
    """Split '<mutant>@<leg>' (or 'clean@<leg>')."""
    mutant, leg = name.split("@")
    return mutant, leg


def run_probe(name: str, src: Path, scratch: Path, jobs: int) -> dict:
    """Copy, mutate, build and run one probe; return its record."""
    mutant, leg = parse(name)
    subs = [] if mutant == "clean" else MUTANTS[mutant]
    tree = scratch / f"probe2-{mutant}-{leg}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(src, tree, symlinks=True,
                    # the milan_dp recipe derives its processor source list
                    # through git, so only the CSR-bench copies drop .git
                    ignore=shutil.ignore_patterns(
                        *(("obj_*",) if leg == "aclk" else ("obj_*", ".git"))))
    rec = {"probe": name, "leg": leg, "file": CSR if subs else None,
           "substitutions": subs}
    path = tree / CSR
    text = path.read_text()
    for anchor, repl in subs:
        if text.count(anchor) != 1:
            rec["result"] = f"ANCHOR-COUNT-{text.count(anchor)}"
            return rec
        text = text.replace(anchor, repl)
    path.write_text(text)
    build_cmd, run_cmd, cwd = LEGS[leg]
    b = subprocess.run(build_cmd + [f"VERILATOR_JOBS={jobs}"], cwd=tree,
                       capture_output=True, text=True)
    rec["build_rc"] = b.returncode
    if b.returncode != 0:
        rec["result"] = "BUILD-FAILED"
        rec["build_tail"] = (b.stdout + b.stderr)[-1500:]
        shutil.rmtree(tree)
        return rec
    r = subprocess.run(run_cmd, cwd=tree / cwd, capture_output=True, text=True)
    out = r.stdout + r.stderr
    (scratch / f"probe2-{mutant}-{leg}.log").write_text(out)
    shutil.rmtree(tree)  # disk budget: keep the log, drop the copy
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    rec.update(run_rc=r.returncode, fail_lines=fails[:8],
               summary=[ln.strip() for ln in out.splitlines()
                        if "checks:" in ln or "checks," in ln][-2:])
    named = any(any(k in f for k in NAMED) for f in fails)
    if mutant == "clean":
        rec["result"] = "PASS" if r.returncode == 0 and not fails else "CLEAN-FAILED"
    else:
        rec["result"] = ("CAUGHT" if r.returncode != 0 and named
                         else "SURVIVED" if r.returncode == 0 and not fails
                         else "FAILED-UNNAMED")
    return rec


def main() -> int:
    """Run the selected probes, at most four at a time."""
    src, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    names = sys.argv[3:]
    jobs = int(os.environ.get("PROBE_VERILATOR_JOBS", "2"))
    with ThreadPoolExecutor(max_workers=int(os.environ.get("PROBE_PARALLEL", "4"))) as pool:
        recs = list(pool.map(lambda n: run_probe(n, src, scratch, jobs), names))
    for rec in recs:
        print(json.dumps(rec))
    bad = [r for r in recs if r["probe"].startswith("clean") and r["result"] != "PASS"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
