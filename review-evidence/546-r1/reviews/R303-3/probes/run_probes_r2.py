#!/usr/bin/env python3
"""Round-2 reviewer probe addendum for PR #554 (issue #546).

Usage: run_probes_r2.py <exported-head-tree> <work-dir> <verilator> [case ...]

Each case copies hdl/, tb/ and scripts/ of the exported exact-head tree into
its own work directory, applies zero or more textual edits (each anchor must
match exactly once, otherwise the case is not run), and runs one target:
  talker  -> make -C tb/verilator/crf_rx talker_step   (the committed harness)
  disc    -> make -C tb/verilator/crf_rx discontinuity
  mutants -> make -C tb/verilator/crf_rx mutants        (the committed campaign)
Verilator C++ builds are capped at -j 4 and at most two cases run at once
(8 jobs). A mutant counts as KILLED only on nonzero rc with a harness or
campaign failure printed; a build error is never a kill.
"""
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
TS = "tb/verilator/crf_rx/sim_talker_step.cpp"
MU = "tb/verilator/crf_rx/mutants.py"
LOWER = "(ts_spacing_ns_w < (64'(NOM_PDU_NS_C) - TS_JUMP_NS_C))"
UPPER = "(ts_spacing_ns_w > (64'(NOM_PDU_NS_C) + TS_JUMP_NS_C))"
CASES = [
    # name, target, [(file, anchor, replacement)], expect (clean|kill|report)
    ("N0_clean_talker", "talker", [], "clean"),
    # receiver defects against the committed connected harness
    ("N1_rx_no_detection", "talker",
     [(RX, "wire rate_break_w = w_acc && rate_seeded_r &&",
       "wire rate_break_w = 1'b0 && w_acc && rate_seeded_r &&")], "kill"),
    ("N2_jump_removed", "talker",
     [(RX, "tu_change_w || ts_jump_w ||", "tu_change_w || 1'b0 ||")], "kill"),
    ("N3_lower_bound_removed", "talker", [(RX, LOWER, "1'b0")], "kill"),
    ("N4_upper_bound_removed", "talker", [(RX, UPPER, "1'b0")], "report"),
    ("N5_upper_bound_removed_disc", "disc", [(RX, UPPER, "1'b0")], "kill"),
    # harness observation: reading validity after the accepting edge (the
    # round-1 shape) must now be rejected by the quiet control
    ("H1_post_edge_observation", "talker",
     [(TS, "observe(sampled_valid, boundary, writeback, old_integ);",
       "observe(dut->rate_valid_o, boundary, writeback, old_integ);")], "kill"),
    # the talker-only negative case with no step: integrator range under the
    # same alignment, to attribute the 0.020 ppm movement (informational)
    ("H2_neg_case_without_step", "talker",
     [(TS, 'gm_change("talker_only_neg", -150000, false, 0);',
       'gm_change("talker_only_neg", 0, false, 0);')], "report"),
    # the committed campaign must fail closed when a mutant survives
    ("M0_campaign_clean", "mutants", [], "clean"),
    ("M1_campaign_survivor", "mutants",
     [(MU, "(\"jump_removed\", \"tu_change_w || ts_jump_w ||\", \"tu_change_w || 1'b0 ||\",",
       "(\"jump_removed\", \"tu_change_w || ts_jump_w ||\", \"tu_change_w || ts_jump_w ||\",")],
     "kill"),
]


def run(src: Path, work: Path, verilator: str, case) -> str:
    name, target, edits, expect = case
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
    tbdir = root / "tb/verilator/crf_rx"
    goal = {"talker": "talker_step", "disc": "discontinuity", "mutants": "mutants"}[target]
    cmd = ["make", "-s", "-C", str(tbdir), goal, f"VERILATOR={verilator}"]
    env = {"VERILATOR": verilator, "PATH": "/usr/bin:/bin"}
    res = subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)
    out = res.stdout + res.stderr
    (work / f"{name}.log").write_text(out)
    if target == "mutants":
        # grade on the campaign's own tally line only; an embedded harness
        # tally (e.g. a surviving mutant's "failures: 0") must not count
        tally = re.search(r"== crf_rx mutants: checks: \d+\s+failures: (\d+) ==", out)
        built = tally is not None
        failed = res.returncode != 0 and tally is not None and int(tally.group(1)) > 0
    else:
        built = "RESULT:" in out
        failed = res.returncode != 0 and "RESULT: FAIL" in out
    if not built:
        verdict = "BUILD-OR-RUN-ERROR"
    elif expect == "clean":
        verdict = "PASS" if res.returncode == 0 else "UNEXPECTED-FAIL"
    elif expect == "kill":
        verdict = "KILLED" if failed else "SURVIVED"
    else:
        verdict = "FAILS" if failed else "PASSES"
    fails = sorted({l.strip() for l in out.splitlines() if "[FAIL]" in l})
    lines = [f"{name}: target={target} expect={expect} rc={res.returncode} -> {verdict}"]
    lines += [f"    {l}" for l in fails[:12]]
    lines += [f"    {l}" for l in out.splitlines()
              if l.startswith(("quiet:", "talker_only", "both_", "== "))]
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
