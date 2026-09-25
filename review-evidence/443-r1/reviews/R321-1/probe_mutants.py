#!/usr/bin/env python3
"""Reviewer probes for issue #443 / RENDER_STAT (0x8DC).

Each probe copies a clean exact-head tree into a disposable directory,
applies ONE exact textual substitution (the anchor must occur exactly once),
builds the named leg through the suite's own Makefile recipe and runs it.
A mutant is CAUGHT when the leg exits non-zero with a [FAIL] line naming a
RENDER-CSR check; it SURVIVES when the leg passes. The clean probe is the
positive control. The source tree is never modified.

usage: probe_mutants.py <clean-head-tree> <scratch-dir> [probe ...]
Verilator is whatever `verilator` resolves to on PATH (record its version).
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DP = "hdl/milan/milan_datapath.sv"
CSR = "hdl/common/csr/milan_csr.sv"
SEL = "if (!strm_dir_r && (32'(strm_idx_r) == s))"

# name: (leg, file, anchor, replacement)
PROBES = {
    "clean_aclk": ("aclk", None, None, None),
    "dp_rails_from_underruns": ("aclk", DP, "{rsp_rails_w, 6'd0,", "{rsp_underruns_w, 6'd0,"),
    "dp_prefill_conv_swapped": ("aclk", DP, "rsp_converged_w[s], rsp_prefill_w[s],",
                                "rsp_prefill_w[s], rsp_converged_w[s],"),
    "csr_ignore_direction": ("aclk", CSR, SEL, "if ((32'(strm_idx_r) == s))"),
    "csr_row_select_zeroes": ("aclk", CSR, SEL,
                              "if (!strm_dir_r && !strm_lsn0_r && (32'(strm_idx_r) == s))"),
    "csr_drop_read_window": ("aclk", CSR, "(rd_addr_q == A_RENDER_STAT) ||", ""),
    "csr_row_select_as_window_aclk": ("aclk", CSR, SEL,
                                      "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))"),
    "csr_row_select_as_window_multi": ("multi", CSR, SEL,
                                       "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))"),
    "clean_multi": ("multi", None, None, None),
    "csr_alias_to_listener0": ("multi", CSR, "live_mux = i_render_status[s*32 +: 32];",
                               "live_mux = i_render_status[0 +: 32];"),
}

LEGS = {
    "aclk": (["make", "-s", "-C", "tb/verilator/milan_dp", "aclk-build"],
             ["tb/verilator/milan_dp/obj_aclk/Vmilan_dp_aclk", "--render-csr-only"],
             "tb/verilator/milan_dp"),
    "multi": (["make", "-s", "-C", "tb/verilator/milan_dp_render", "tdm8render-multi-build"],
              None, "tb/verilator/milan_dp_render"),
}


def multi_exe(tree: Path) -> list[str]:
    """The multi leg's executable, found after its build."""
    hits = sorted(tree.glob("tb/verilator/milan_dp_render/*/Vmilan_dp_tdm8rm"))
    return [str(hits[0])] if hits else []


def run_probe(name: str, src: Path, scratch: Path, jobs: int) -> dict:
    """Copy, mutate, build and run one probe; return its record."""
    leg, rel, anchor, repl = PROBES[name]
    tree = scratch / f"probe-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(src, tree, symlinks=True,
                    ignore=shutil.ignore_patterns("obj_*"))
    rec = {"probe": name, "leg": leg, "file": rel, "anchor": anchor, "replacement": repl}
    if rel:
        path = tree / rel
        text = path.read_text()
        if text.count(anchor) != 1:
            rec["result"] = f"ANCHOR-COUNT-{text.count(anchor)}"
            return rec
        path.write_text(text.replace(anchor, repl))
    build_cmd, run_cmd, cwd = LEGS[leg]
    b = subprocess.run(build_cmd + [f"VERILATOR_JOBS={jobs}"], cwd=tree,
                       capture_output=True, text=True)
    rec["build_rc"] = b.returncode
    if b.returncode != 0:
        rec["result"] = "BUILD-FAILED"
        rec["build_tail"] = (b.stdout + b.stderr)[-1500:]
        return rec
    exe = [str(tree / run_cmd[0])] + run_cmd[1:] if run_cmd else multi_exe(tree)
    r = subprocess.run(exe, cwd=tree / cwd, capture_output=True, text=True)
    out = r.stdout + r.stderr
    (scratch / f"probe-{name}.log").write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    csr = [ln for ln in out.splitlines() if "RENDER-CSR" in ln]
    rec.update(run_rc=r.returncode, fail_lines=fails[:8], render_csr_lines=len(csr),
               summary=[ln.strip() for ln in out.splitlines()
                        if "checks," in ln or "checks:" in ln][-2:])
    named = any("RENDER-CSR" in f for f in fails)
    if name.startswith("clean"):
        # the render harness prints only failures, so a clean pass is its
        # RESULT line; the aclk harness must also have printed its CSR checks
        printed = bool(csr) or leg == "multi"
        rec["result"] = ("PASS" if r.returncode == 0 and not fails and printed
                         and "RESULT: PASS" in out else "CLEAN-FAILED")
    else:
        rec["result"] = ("CAUGHT" if r.returncode != 0 and named
                         else "SURVIVED" if r.returncode == 0 and not fails
                         else "FAILED-UNNAMED")
    return rec


def main() -> int:
    """Run the selected probes, at most four at a time."""
    src, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    names = sys.argv[3:] or list(PROBES)
    jobs = int(os.environ.get("PROBE_VERILATOR_JOBS", "2"))
    with ThreadPoolExecutor(max_workers=int(os.environ.get("PROBE_PARALLEL", "4"))) as pool:
        recs = list(pool.map(lambda n: run_probe(n, src, scratch, jobs), names))
    for rec in recs:
        print(json.dumps(rec))
    bad = [r for r in recs
           if (r["probe"].startswith("clean") and r["result"] != "PASS")]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
