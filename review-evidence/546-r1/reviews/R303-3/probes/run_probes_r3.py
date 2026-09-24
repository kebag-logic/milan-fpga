#!/usr/bin/env python3
"""Round-3 reviewer probe addendum for PR #554 (issue #546): the U13 PI-resume check.

Usage: run_probes_r3.py <exported-head-tree> <work-dir> <verilator> [case ...]

Each case copies hdl/, tb/ and scripts/ of the exported exact-head tree into
its own work directory, applies zero or more textual edits (each anchor must
match exactly once, otherwise the case is not run), and runs one target:
  unit    -> make -C tb/verilator/mmcm_servo unit-build, then the unit harness
  mutants -> make -C tb/verilator/crf_rx mutants        (the committed campaign)
Verilator C++ builds are capped at -j 4 and at most two cases run at once
(8 jobs). A unit mutant counts as KILLED only on harness rc 1 with the named
check printed as [FAIL]; a build error is never a kill. A campaign case is
KILLED only on nonzero rc with a nonzero campaign failure tally.
"""
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SV = "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
UT = "tb/verilator/mmcm_servo/sim_main.cpp"
MU = "tb/verilator/crf_rx/mutants.py"
RESUME = "[U13] valid offset resumes PI trim"
ENGINE = "  always_ff @(posedge clk_i) begin : servo_engine"
GATE = "\n                           && crf_rate_valid_i;"
LATCH = """  logic invalid_seen_r;
  always_ff @(posedge clk_i) begin : latch_invalid_sample
    if (!rst_n) invalid_seen_r <= 1'b0;
    else if (!crf_rate_valid_i) invalid_seen_r <= 1'b1;
  end
"""
# PI resumes, but only 2^22 clk_i cycles (83.9 ms at the unit's 50 MHz) after
# the last invalid sample: a slow, not a permanent, failure to resume.
SLOW = """  logic [21:0] hold_r;
  always_ff @(posedge clk_i) begin : slow_resume
    if (!rst_n) hold_r <= '0;
    else if (!crf_rate_valid_i) hold_r <= '1;
    else if (hold_r != '0) hold_r <= hold_r - 1'b1;
  end
"""
U13_PRINT = '        ck("[U13] valid offset resumes PI trim", trim() > resumed + 5 * 16, 1);'
U13_NEW = """        ck("[U13] valid offset resumes PI trim", trim() > resumed + 5 * 16, 1);
        ck("[U13] valid offset stays LOCKED", state(), 4);
        dut->crf_rate_i = clean;
        run_ms(24);
        ck("[U13] original rate recovers LOCKED", state(), 4);
"""
CASES = [
    # name, target, [(file, anchor, replacement)], expect (clean|kill|report), named check
    ("S0_unit_clean_margin", "unit",
     [(UT, U13_PRINT, '        printf("  probe: U13 trim resumed=%d after=%d delta=%d (need > 80)\\n",'
                      ' resumed, trim(), trim() - resumed);\n' + U13_PRINT)], "clean", None),
    # the committed mutant, run directly so every failing check is visible
    ("S1_latched_off", "unit",
     [(SV, ENGINE, LATCH + ENGINE), (SV, GATE, GATE[:-1] + " && !invalid_seen_r;")],
     "kill", RESUME),
    # independent variants: a slow resume, and a loop whose lock count runs
    # while its trim and integrator writeback stay frozen
    ("S2_slow_resume_84ms", "unit",
     [(SV, ENGINE, SLOW + ENGINE), (SV, GATE, GATE[:-1] + " && (hold_r == '0);")],
     "kill", RESUME),
    ("S3_trim_frozen_lock_counts", "unit",
     [(SV, ENGINE, LATCH + ENGINE),
      (SV, "              if (pp_du_r > 32'(SLEW_MAX_P))\n",
       "              if (invalid_seen_r) begin end\n"
       "              else if (pp_du_r > 32'(SLEW_MAX_P))\n"),
      (SV, "              integ_r <= pp_ig_r;",
       "              if (!invalid_seen_r) integ_r <= pp_ig_r;")],
     "kill", RESUME),
    # the round-2 harness shape (U13 without the round-3 resume lines) must
    # let the latched-off mutant through: the new check is load-bearing
    ("S4_latched_off_round2_harness", "unit",
     [(SV, ENGINE, LATCH + ENGINE), (SV, GATE, GATE[:-1] + " && !invalid_seen_r;"),
      (UT, """        // A +10 ppm talker offset stays within the 16 ppm unit lock band.
        // Demand >5 ppm trim movement, beyond the unit's sampling ripple;
        // a PI loop latched off during invalidity must fail this check.
        const int16_t resumed = trim();
        dut->crf_rate_i = rate_for_ppm(+90.0);
        run_ms(24);
""" + U13_NEW, "")],
     "report", None),
    # the committed campaign must fail closed when its resume mutant is a no-op
    ("S5_campaign_resume_noop", "mutants",
     [(MU, 'anchor[:-1] + " && !invalid_seen_r;"', 'anchor[:-1] + ";"')], "kill", None),
]


def run(src: Path, work: Path, verilator: str, case) -> str:
    name, target, edits, expect, named = case
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for part in ("hdl", "tb", "scripts"):
        shutil.copytree(src / part, root / part, symlinks=True,
                        ignore=shutil.ignore_patterns("obj_*"))
    for rel, anchor, repl in edits:
        path = root / rel
        text = path.read_text()
        if text.count(anchor) != 1:
            return f"{name}: ANCHOR-COUNT {text.count(anchor)} in {rel} (not run)"
        path.write_text(text.replace(anchor, repl))
    for mk in (root / "tb/verilator/crf_rx/Makefile", root / "tb/verilator/mmcm_servo/Makefile"):
        mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 4"))
    env = {"VERILATOR": verilator, "PATH": "/usr/bin:/bin"}
    if target == "unit":
        sdir = root / "tb/verilator/mmcm_servo"
        b = subprocess.run(["make", "-s", "-C", str(sdir), "unit-build",
                            f"VERILATOR={verilator}"],
                           capture_output=True, text=True, check=False, env=env)
        if b.returncode:
            res_rc, out = b.returncode, b.stdout + b.stderr + "\nBUILD FAILED\n"
        else:
            r = subprocess.run([str(sdir / "obj_dir/Vservo_sim")],
                               capture_output=True, text=True, check=False)
            res_rc, out = r.returncode, r.stdout + r.stderr
        built = "KL_mmcm_drp_servo:" in out
        failed = res_rc == 1 and (named is None or f"[FAIL] {named}" in out)
    else:
        r = subprocess.run(["make", "-s", "-C", str(root / "tb/verilator/crf_rx"), "mutants",
                            f"VERILATOR={verilator}"],
                           capture_output=True, text=True, check=False, env=env)
        res_rc, out = r.returncode, r.stdout + r.stderr
        tally = re.search(r"== crf_rx mutants: checks: \d+\s+failures: (\d+) ==", out)
        built = tally is not None
        failed = res_rc != 0 and tally is not None and int(tally.group(1)) > 0
    (work / f"{name}.log").write_text(out)
    if not built:
        verdict = "BUILD-OR-RUN-ERROR"
    elif expect == "clean":
        verdict = "PASS" if res_rc == 0 else "UNEXPECTED-FAIL"
    elif expect == "kill":
        verdict = "KILLED" if failed else "SURVIVED"
    else:
        verdict = "FAILS" if res_rc != 0 else "PASSES"
    fails = sorted({l.strip() for l in out.splitlines() if "[FAIL]" in l})
    lines = [f"{name}: target={target} expect={expect} rc={res_rc} -> {verdict}"]
    lines += [f"    {l}" for l in fails[:12]]
    lines += [f"    {l.strip()}" for l in out.splitlines()
              if l.strip().startswith(("probe:", "KL_mmcm_drp_servo:", "== crf_rx mutants",
                                       "[U13]", "[ ok ] [U13]"))]
    return "\n".join(lines)


def main() -> int:
    src, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    verilator = sys.argv[3]
    work.mkdir(parents=True, exist_ok=True)
    cases = [c for c in CASES if len(sys.argv) < 5 or c[0] in sys.argv[4:]]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda c: run(src, work, verilator, c), cases))
    print("\n".join(results))
    bad = [r for r in results if " -> " in r and r.split(" -> ")[1].split("\n")[0]
           in ("SURVIVED", "UNEXPECTED-FAIL", "BUILD-OR-RUN-ERROR")]
    bad += [r for r in results if "ANCHOR-COUNT" in r]
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
