#!/usr/bin/env python3
"""Reviewer probes of tb/verilator/csr against mutated COPIES of milan_csr.sv.

usage: csr_bench_probes.py --tree T --verilator V --scratch S [case...]

T is a disposable checkout; the mutant is written under S and passed to
run_csr_bench.sh as the SRCS override. Tracked sources are never written.
A case with a named check is 'caught' only when the bench exits nonzero AND
prints a [FAIL] line containing that name; a case with None must pass clean.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ARM = """      A_RENDER_STAT: begin
        live_mux = 32'd0;
        for (int unsigned s = 0; s < N_LISTENERS_P; s++) begin
          if (!strm_dir_r && (32'(strm_idx_r) == s))
            live_mux = i_render_status[s*32 +: 32];
        end
      end
"""
TERM = "                      (rd_addr_q == A_RENDER_STAT) ||\n"
SEL = "if (!strm_dir_r && (32'(strm_idx_r) == s))"

# (name, [(old, new)...], named check or None)
CASES = [
    # round-1 recipe: the whole A_RENDER_STAT decode removed
    ("nodecode", [(ARM, ""), (TERM, "")],
     "RENDER_STAT driven prefill reset word"),
    ("dir_ignored", [(SEL, "if ((32'(strm_idx_r) == s))")],
     "RENDER_STAT talker selection reads zero"),
    ("idx_aliased_to_0", [(SEL, "if (!strm_dir_r && (s == 0))")],
     "RENDER_STAT out-of-range listener reads zero"),
    ("lsn0_window_semantics",
     [(SEL, "if (strm_lsn0_r ? (s == 0) : (!strm_dir_r && (32'(strm_idx_r) == s)))")],
     "RENDER_STAT bit 9"),
    ("upper_rails_zeroed",
     [("live_mux = i_render_status[s*32 +: 32];",
       "live_mux = {8'd0, i_render_status[s*32 +: 24]};")],
     "RENDER_STAT"),
    ("window_term_dropped", [(TERM, "")], "RENDER_STAT"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True, type=Path)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("cases", nargs="*")
    a = ap.parse_args()
    runner = Path(__file__).resolve().parent / "run_csr_bench.sh"
    src = (a.tree / "hdl/common/csr/milan_csr.sv").read_text()
    bad = 0
    for name, subs, named in CASES:
        if a.cases and name not in a.cases:
            continue
        text = src
        for old, new in subs:
            if text.count(old) != 1:
                print(f"[PROBE-ERROR] {name}: anchor count {text.count(old)}")
                bad += 1
                break
            text = text.replace(old, new)
        else:
            work = a.scratch / f"csr_{name}"
            work.mkdir(parents=True, exist_ok=True)
            mut = work / "milan_csr.sv"
            mut.write_text(text)
            p = subprocess.run([str(runner), str(a.tree), a.verilator, str(mut)],
                               capture_output=True, text=True)
            log = p.stdout + p.stderr
            (work / "run.log").write_text(log)
            fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
            built = log.count("checks:") > 0
            if not built:
                ok, label = False, f"no bench output (rc={p.returncode})"
            elif named is None:
                ok = p.returncode == 0 and not fails
                label = "SURVIVED (expected)" if ok else "unexpected failure"
            else:
                hit = [f for f in fails if named in f]
                ok = p.returncode != 0 and bool(hit)
                label = "caught" if ok else f"rc={p.returncode}, no '{named}' failure"
            tallies = re.findall(r"checks: (\d+)\s+failures: (\d+)", log)
            print(f"[{'PROBE-OK' if ok else 'PROBE-UNEXPECTED'}] {name}: rc={p.returncode} "
                  f"{label}; named={named}; legs={tallies}")
            for f in fails[:4]:
                print(f"    {f}")
            bad += not ok
    print(f"csr_bench_probes: {bad} unexpected outcome(s)")
    return int(bad != 0)


if __name__ == "__main__":
    sys.exit(main())
