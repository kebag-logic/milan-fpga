#!/usr/bin/env python3
"""Round-2 reviewer probes on KL_aaf_clock_meter (PR #634, head d81198c2).

Each probe is a set of exact source replacements (each anchor must occur
exactly once) applied to a scratch copy of the meter RTL; the checkout is never
edited. Each probe is built with the meter suite's own `make build` recipe and
run on the named case. Verdict per probe:
  CAUGHT   - build ok, harness exits 1 with RESULT: FAIL (the failing checks
             are printed);
  ESCAPED  - build ok, harness exits 0 with RESULT: PASS;
  INVALID  - an anchor is missing/duplicated, the build fails, or the run
             neither passes nor fails cleanly.

Usage: reviewer_meter_probes_r2.py <repo> <scratch-dir> [jobs]
VERILATOR / VERILATOR_JOBS are taken from the environment.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROBES = (
    # the era start no longer clears the largest deviation (port doc: "a level,
    # cleared by an era start")
    ("P1_max_dev_not_cleared_at_era",
     (("        mr_toggle_p_o <= 1'b0;\n        max_dev_r     <= '0;\n",
       "        mr_toggle_p_o <= 1'b0;\n"),),
     ("rates", "restarts", "beyond", "step_in_gap")),
    # the largest deviation wraps instead of saturating at 65535
    ("P2_max_dev_wraps",
     (("          if (s2_abs_w > 32'd65535)            max_dev_r <= 16'hFFFF;\n"
       "          else if (16'(s2_abs_w) > max_dev_r)  max_dev_r <= 16'(s2_abs_w);\n",
       "          if (16'(s2_abs_w) > max_dev_r)  max_dev_r <= 16'(s2_abs_w);\n"),),
     ("rates", "beyond", "step_in_gap")),
    # the deviation verdict deferred by ONE PDU (not to PDU 15)
    ("P3_deviation_verdict_one_pdu_late",
     (("  logic        pdu_restart_r;\n",
       "  logic        pdu_restart_r;\n  logic        dev_late_r;\n"),
      ("      pdu_restart_r <= 1'b0;\n      max_dev_r <= '0; restart_cnt_r <= '0;\n",
       "      pdu_restart_r <= 1'b0; dev_late_r <= 1'b0;\n"
       "      max_dev_r <= '0; restart_cnt_r <= '0;\n"),
      ("            grp_act_r     <= 1'b0;\n            pdu_restart_r <= 1'b1;\n",
       "            grp_act_r     <= 1'b0;\n            dev_late_r    <= 1'b1;\n"),
      ("        if (s2_tu_edge_w) pdu_restart_r <= 1'b1;\n      end",
       "        if (s2_tu_edge_w) pdu_restart_r <= 1'b1;\n"
       "        if (dev_late_r) begin pdu_restart_r <= 1'b1; dev_late_r <= 1'b0; end\n"
       "      end")),
     ("beyond", "step_in_gap")),
    # a change of the followed listener raises a disruption pulse
    ("P4_listener_change_pulses_disrupt",
     (("      if (tout_fire_w && locked_o) begin",
       "      if ((tout_fire_w || idx_chg_w) && locked_o) begin"),),
     ("restarts",)),
    # the meter's tu edge detector sees only the rising edge
    ("P5_tu_rising_edge_only",
     (("  wire        s2_tu_edge_w = tu_seeded_r && (s2_tu_r != prev_tu_r);",
       "  wire        s2_tu_edge_w = tu_seeded_r && s2_tu_r && !prev_tu_r;"),),
     ("restarts",)),
    # an idx change does not clear the lock but the entry does (variant of the
    # author's listener_change_keeps_lock, through the era path instead)
    ("P6_bind_edge_not_an_era_start",
     (("wire era_start_w = en_rise_w || idx_chg_w || bind_rise_w || tout_fire_w;",
       "wire era_start_w = en_rise_w || idx_chg_w || tout_fire_w;"),),
     ("restarts",)),
)


def mutate(src: str, edits) -> str | None:
    for anchor, repl in edits:
        if src.count(anchor) != 1:
            return None
        src = src.replace(anchor, repl)
    return src


def one(repo: Path, scratch: Path, probe) -> str:
    name, edits, cases = probe
    here = repo / "tb/verilator/aaf_clock_meter"
    rtl = repo / "hdl/ieee1722/crf/KL_aaf_clock_meter.sv"
    src = mutate(rtl.read_text(), edits)
    if src is None:
        return f"{name}: INVALID (anchor not found exactly once)"
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    path = work / "KL_aaf_clock_meter.sv"
    path.write_text(src)
    mdir = work / "obj"
    cmd = ["make", "-s", "-C", str(here), "build", f"METER_RTL={path}", f"MDIR={mdir}",
           f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}",
           f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '2')}"]
    b = subprocess.run(cmd, capture_output=True, text=True, check=False)
    (work / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return f"{name}: INVALID (build failed rc={b.returncode})"
    exe = mdir / "Vmeter_sim"
    lines = [f"{name}:"]
    for case in cases:
        r = subprocess.run([str(exe), case], capture_output=True, text=True, check=False)
        out = r.stdout + r.stderr
        (work / f"run_{case}.log").write_text(out)
        fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
        if r.returncode == 0 and "RESULT: PASS" in out:
            v = "ESCAPED"
        elif r.returncode == 1 and "RESULT: FAIL" in out and fails:
            v = "CAUGHT"
        else:
            v = f"INVALID rc={r.returncode}"
        lines.append(f"  case {case}: {v}")
        for f in fails[:6]:
            lines.append(f"    {f}")
    return "\n".join(lines)


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for text in pool.map(lambda p: one(repo, scratch, p), PROBES):
            print(text, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
