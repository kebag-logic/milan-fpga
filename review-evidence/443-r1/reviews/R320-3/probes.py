#!/usr/bin/env python3
"""Reviewer-owned disposable mutation probes for PR #561 at the merge head.

Every mutant is written to a scratch copy and elaborated through the suites'
own Makefile recipes via their documented source overrides (DP_SRC, CSR_SRC)
and a scratch object directory; the tracked tree is never edited.
Usage: probes.py <clone> <scratch-dir>. Exit 0 iff every probe got the
expected outcome (clean control passes; each mutant fails the named check)."""
import os, subprocess, sys
from pathlib import Path

clone, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
DP = clone / "hdl/milan/milan_datapath.sv"
CSR = clone / "hdl/common/csr/milan_csr.sv"
ACLK = clone / "tb/verilator/milan_dp"
REND = clone / "tb/verilator/milan_dp_render"

def mutate(src: Path, old: str, new: str, name: str) -> Path:
    text = src.read_text()
    assert text.count(old) == 1, f"{name}: anchor count {text.count(old)}"
    out = scratch / f"{name}{src.suffix}"
    out.write_text(text.replace(old, new))
    return out

def sh(cmd, cwd, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr

def aclk(name, var, path, mode):
    mdir = scratch / f"obj_{name}"
    rc, log = sh(["make", "-s", "-C", str(ACLK), "aclk-build", f"{var}={path}",
                  f"ACLK_MDIR={mdir}", "VERILATOR_JOBS=8"], ACLK)
    if rc: return "build-failed", log[-3000:]
    return sh([str(mdir / "Vmilan_dp_aclk"), mode], ACLK)

def multi(name, csr_path):
    mdir = scratch / f"obj_{name}"
    env = dict(os.environ)
    if csr_path: env["CSR_SRC"] = str(csr_path)
    rc, log = sh(["make", "-s", "-C", str(REND), "tdm8render-multi-build",
                  f"TDM8RM_MDIR={mdir}", "VERILATOR_JOBS=8"], REND, env)
    if rc: return "build-failed", log[-3000:]
    return sh([str(mdir / "Vmilan_dp_tdm8rm")], REND)

def failed(log, named):
    return any(l.lstrip().startswith("[FAIL]") and named in l for l in log.splitlines())

sel = "if (!strm_dir_r && (32'(strm_idx_r) == s))"
probes = [
  # (name, runner, expected named failing check or None for a clean pass)
  ("multi_clean", lambda: multi("multi_clean", None), None),
  ("multi_alias_idx0", lambda: multi("multi_alias_idx0",
      mutate(CSR, sel, "if (!strm_dir_r && (s == 0))", "csr_alias_idx0")),
   "RENDER-CSR-MULTI: flushed listener 1 has empty prefill"),
  ("aclk_rails_zero", lambda: aclk("aclk_rails_zero", "DP_SRC",
      mutate(DP, "{rsp_rails_w, 6'd0,", "{16'd0, 6'd0,", "dp_rails_zero"),
      "--render-csr-only"), "RENDER-CSR: rail event reached the word"),
  ("aclk_flag_swap", lambda: aclk("aclk_flag_swap", "DP_SRC",
      mutate(DP, "rsp_converged_w[s], rsp_prefill_w[s],",
             "rsp_prefill_w[s], rsp_converged_w[s],", "dp_flag_swap"),
      "--render-csr-only"), "RENDER-CSR: prefill mirrors taps"),
]
bad = 0
for name, run, named in probes:
    rc, log = run()
    (scratch / f"{name}.log").write_text(f"rc={rc}\n{log}")
    if named is None:
        ok = rc == 0 and "failures: 0" in log
        got = "pass" if ok else "fail"
    else:
        ok = rc not in (0, "build-failed") and failed(log, named)
        got = "caught" if ok else "NOT caught"
    fails = [l.strip() for l in log.splitlines() if l.lstrip().startswith("[FAIL]")][:4]
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: rc={rc} {got}; expected={named}")
    for l in fails: print("    ", l)
    summ = [l for l in log.splitlines() if "checks" in l and "failures" in l]
    if summ: print("    ", summ[-1].strip())
    bad += not ok
print(f"probes: {len(probes)} run, {bad} unexpected")
sys.exit(1 if bad else 0)
