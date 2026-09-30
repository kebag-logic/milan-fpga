#!/usr/bin/env python3
"""Reviewer-owned extra mutants, judged by tb/pp_top/notify_mutants.py's own judge().
A mutant here names NO check (checks=()), so the verdict reads: KILLED = the run
failed at least one check; SURVIVED = every check of the suite still passes.
Usage: extra_mutants.py TREE OUTPUT VERILATOR JOBS [NAME...]
"""
import concurrent.futures, json, sys
from pathlib import Path
tree, out, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(tree / "tb/pp_top"))
import notify_mutants as nm  # noqa: E402
N = nm.NTFY
EXTRA = [
    # the identify arm no longer yields to the registry machine's own arm sites:
    # a collision drops the IDENT-BURST/REARM arm and parks the sequencer
    nm.Mutant("x_ident_arm_ignores_core_arm", nm.IDENT, (
        (N, "    assign id_arm_gnt_w      = (armb_r || armr_r) && !core_arm_w;\n",
            "    assign id_arm_gnt_w      = (armb_r || armr_r);\n"),), ()),
    # the REARM generation is never flipped: a stale REARM can pass for the current one
    nm.Mutant("x_ident_rearm_single_generation", nm.IDENT, (
        (N, "                gen_r   <= !gen_r;\n", ""),), ()),
    # the synchroniser loses its second flop (a CDC hygiene control, not a function change)
    nm.Mutant("x_ident_no_sync_second_flop", nm.IDENT, (
        (N, "        btn_q2_r <= btn_q1_r;\n", "        btn_q2_r <= identify_button_i;\n"),), ()),
]
known = {m.name: m for m in EXTRA}
chosen = [known[n] for n in sys.argv[5:]] if sys.argv[5:] else EXTRA
out.mkdir(parents=True, exist_ok=True)
work = (tree, out, verilator)
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for rec in pool.map(lambda m: nm.judge(m, work), chosen):
        (out / f"{rec['mutant']}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(json.dumps({k: rec.get(k) for k in ("mutant", "verdict", "run_rc", "completed")}),
              "failing:", len(rec.get("failing_checks") or []), flush=True)
