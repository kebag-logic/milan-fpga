#!/usr/bin/env python3
"""Reviewer fault probes for issue #443 / RENDER_STAT (0x8DC).

Portable: pass the candidate checkout, the simulator wrapper and a scratch
directory. Each mutant is a text substitution applied to a COPY of one RTL
file; the copy is built through the suite's own recipe with only the source
list and the object directory overridden. Tracked sources are never written.

Usage:
  render_csr_probes.py --repo R --verilator V --scratch S [--jobs 8] [case...]

Verdicts reuse tb/verilator/milan_dp/render_mutants.py's verdict(): 'caught'
requires a failing named check, 'pass' a clean exit with no failure.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# (name, file, old, new, suite, mode, named check or None = expected survive)
CASES = [
    ("csr_dir_ignored", "hdl/common/csr/milan_csr.sv",
     "if (!strm_dir_r && (32'(strm_idx_r) == s))",
     "if ((32'(strm_idx_r) == s))",
     "dp", "--render-csr-only", "RENDER-CSR: talker selection reads zero"),
    ("csr_idx_aliased_to_0", "hdl/common/csr/milan_csr.sv",
     "if (!strm_dir_r && (32'(strm_idx_r) == s))",
     "if (!strm_dir_r && (s == 0))",
     "dp", "--render-csr-only", "RENDER-CSR: out-of-range listener reads zero"),
    ("csr_idx_aliased_to_0_multi", "hdl/common/csr/milan_csr.sv",
     "if (!strm_dir_r && (32'(strm_idx_r) == s))",
     "if (!strm_dir_r && (s == 0))",
     "multi", None, "RENDER-CSR-MULTI"),
    ("csr_window_term_dropped", "hdl/common/csr/milan_csr.sv",
     "                      (rd_addr_q == A_RENDER_STAT) ||\n",
     "",
     "dp", "--render-csr-only", "RENDER-CSR: prefill mirrors taps"),
    ("csr_selector_reset_idx1", "hdl/common/csr/milan_csr.sv",
     "strm_dir_r <= 1'b0; strm_idx_r <= 4'd0; strm_lsn0_r <= 1'b0;",
     "strm_dir_r <= 1'b0; strm_idx_r <= 4'd1; strm_lsn0_r <= 1'b0;",
     "dp", "--render-csr-only", "RENDER-CSR: prefill mirrors taps"),
    ("dp_prefill_converged_swapped", "hdl/milan/milan_datapath.sv",
     "{rsp_rails_w, 6'd0, rsp_converged_w[s], rsp_prefill_w[s],",
     "{rsp_rails_w, 6'd0, rsp_prefill_w[s], rsp_converged_w[s],",
     "dp", "--render-csr-only", "RENDER-CSR: prefill mirrors taps"),
    ("dp_rails_from_underruns", "hdl/milan/milan_datapath.sv",
     "{rsp_rails_w, 6'd0, rsp_converged_w[s], rsp_prefill_w[s],",
     "{rsp_underruns_w, 6'd0, rsp_converged_w[s], rsp_prefill_w[s],",
     "dp", "--render-csr-only", "RENDER-CSR: rail mirrors taps"),
    # expected to SURVIVE (cross-check of another round's finding): give
    # RENDER_STAT the 0x800 window's STRM_SEL[9] meaning (force listener 0),
    # which the page says this word does NOT have; only index 0 is graded
    ("csr_lsn0_window_semantics", "hdl/common/csr/milan_csr.sv",
     "if (!strm_dir_r && (32'(strm_idx_r) == s))",
     "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))",
     "dp", "--render-csr-only", None),
    ("csr_lsn0_window_semantics_multi", "hdl/common/csr/milan_csr.sv",
     "if (!strm_dir_r && (32'(strm_idx_r) == s))",
     "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))",
     "multi", None, None),
    # expected to SURVIVE: no leg reaches 256 rails, so the upper rail byte
    # is proven by static width review only
    ("dp_rails_upper_byte_zero", "hdl/milan/milan_datapath.sv",
     "{rsp_rails_w, 6'd0, rsp_converged_w[s], rsp_prefill_w[s],",
     "{8'd0, rsp_rails_w[7:0], 6'd0, rsp_converged_w[s], rsp_prefill_w[s],",
     "dp", "--render-csr-only", None),
]


def srcs(suite_dir: Path) -> list[str]:
    out = subprocess.run(
        ["make", "-s", "--no-print-directory", "-C", str(suite_dir),
         "--eval", "r320-srcs: ; @echo $(SRCS)", "r320-srcs"],
        capture_output=True, text=True, check=True)
    return out.stdout.split()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("--jobs", default="8")
    ap.add_argument("cases", nargs="*")
    a = ap.parse_args()
    repo = a.repo.resolve()
    dp_dir = repo / "tb/verilator/milan_dp"
    mr_dir = repo / "tb/verilator/milan_dp_render"
    sys.path.insert(0, str(dp_dir))
    from render_mutants import run_leg, verdict  # noqa: E402
    failures = 0
    for name, rel, old, new, suite, mode, named in CASES:
        if a.cases and name not in a.cases:
            continue
        work = a.scratch / name
        work.mkdir(parents=True, exist_ok=True)
        text = (repo / rel).read_text()
        if text.count(old) != 1:
            print(f"[PROBE-ERROR] {name}: anchor count {text.count(old)}")
            failures += 1
            continue
        mut = work / Path(rel).name
        mut.write_text(text.replace(old, new))
        suite_dir = dp_dir if suite == "dp" else mr_dir
        base = srcs(suite_dir)
        target = (suite_dir / (repo / rel).relative_to(repo)).name
        swapped = [str(mut) if Path(s).name == target else s for s in base]
        assert swapped.count(str(mut)) == 1, name
        mdir = work / "obj"
        if suite == "dp":
            cmd = ["make", "-s", "-C", str(suite_dir), "aclk-build",
                   f"ACLK_MDIR={mdir}"]
            exe = mdir / "Vmilan_dp_aclk"
        else:
            cmd = ["make", "-s", "-C", str(suite_dir), "tdm8render-multi-build",
                   f"TDM8RM_MDIR={mdir}"]
            exe = mdir / "Vmilan_dp_tdm8rm"
        cmd += [f"VERILATOR={a.verilator}", f"VERILATOR_JOBS={a.jobs}",
                "SRCS=" + " ".join(swapped)]
        b = subprocess.run(cmd, capture_output=True, text=True)
        (work / "build.log").write_text(b.stdout + b.stderr)
        if b.returncode != 0 or not exe.is_file():
            print(f"[PROBE-ERROR] {name}: build rc={b.returncode}")
            failures += 1
            continue
        if mode is None:
            p = subprocess.run([str(exe)], cwd=str(suite_dir),
                               capture_output=True, text=True)
            rc, log = p.returncode, p.stdout + p.stderr
        else:
            rc, log = run_leg(exe, mode)
        (work / "run.log").write_text(log)
        fails = [ln.strip() for ln in log.splitlines()
                 if ln.strip().startswith("[FAIL]")]
        if named is None:
            answer = verdict(rc, log, None)
            ok = answer == "pass"
            label = "SURVIVED (expected)" if ok else f"unexpected: {answer}"
        elif named.endswith("MULTI"):
            hit = [f for f in fails if named in f]
            ok = rc != 0 and bool(hit)
            label = "caught" if ok else f"rc={rc}, no {named} failure"
        else:
            answer = verdict(rc, log, named)
            ok = answer == "caught"
            label = answer
        print(f"[{'PROBE-OK' if ok else 'PROBE-UNEXPECTED'}] {name}: rc={rc} "
              f"{label}; named={named}")
        for f in fails[:4]:
            print(f"    {f}")
        failures += not ok
    print(f"render_csr_probes: {failures} unexpected outcome(s)")
    return int(failures != 0)


if __name__ == "__main__":
    sys.exit(main())
