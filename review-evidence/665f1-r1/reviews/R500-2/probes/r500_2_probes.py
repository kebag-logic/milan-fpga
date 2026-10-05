#!/usr/bin/env python3
"""R500-2 reviewer probes for PR #669 (#665 F1) at the exact head.

Run from the root of a checkout of the head under review:

    python3 /path/to/r500_2_probes.py <scratch-dir>

It imports the lane's own bench (sw/firmware/ctrl_nvm/test) read-only,
plants reviewer-owned defects into COPIES of sw/firmware/ctrl_nvm under
<scratch-dir>, and runs named checks or raw runner scripts on them at the
shipping 1x1 shape. It never writes into the checkout.

Each probe prints one PROBE line: its name, what it plants or runs, and the
observed result.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import nvm_mutants                                       # noqa: E402
import test_ctrl_nvm as gate                             # noqa: E402
from nvm_bench import TREE, shape_inputs                 # noqa: E402
from nvm_checks import binding_ids                       # noqa: E402
from nvm_mutants import Mutant                           # noqa: E402

SHAPE = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
STORE = nvm_mutants.STORE
LITESPI = nvm_mutants.LITESPI

#: Reviewer-planted defects: (name, seams, checks to grade).
PLANTS = (
    # the fallback's own re-stage judgment dropped: after the first pick
    # fails its re-stage, the second pick is applied without being re-judged
    ("fallback_restage_unchecked",
     ((STORE, "\t\tif (chosen != NVM_NONE && !nvm_stage_slot(chosen))\n\t\t\tchosen = NVM_NONE;",
       "\t\tif (chosen != NVM_NONE)\n\t\t\t(void)nvm_stage_slot(chosen);"),),
     list(gate.BOOT_PORTS)),
    # chip select left asserted after a stalled window
    ("cs_kept_on_stall",
     ((LITESPI, "\t\tok = ls_xfer(i < n ? cmd[i] : data[i - n]) >= 0;\n\tls_close();",
       "\t\tok = ls_xfer(i < n ? cmd[i] : data[i - n]) >= 0;\n\tif (ok)\n\t\tls_close();"),),
     ["port_stall", "first_commit_bytes", "media_failures"]),
    # DR2a boundary: a change to the very record the capture examines next
    ("taken_off_by_one",
     ((STORE, "r.id >= nvm.cursor.id;", "r.id > nvm.cursor.id;"),),
     ["debounce"]),
    # DR2c: four attempts per unchanged set
    ("four_attempts",
     ((STORE, "\tif (nvm.st.attempts >= NVM_TXN_ATTEMPTS) {", "\tif (nvm.st.attempts > NVM_TXN_ATTEMPTS) {"),),
     ["media_failures", "dr2c_unchanged_set", "dr2c_console"]),
    # DR2c: a backoff of 500 ms (the producer's figure) in place of 1,000 ms
    ("half_backoff",
     ((STORE, "\tnvm.retry_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);",
       "\tnvm.retry_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS / 2u);"),),
     ["media_failures", "dr2c_console", "time_base"]),
    # the exhaustion flag not cleared by a changed set
    ("exhausted_sticks",
     ((STORE, "\t\tnvm.st.attempts = 0;\n\t\tnvm.st.exhausted = 0;\n", "\t\tnvm.st.attempts = 0;\n"),),
     ["recovers_after_failure", "dr2c_unchanged_set", "dr2c_console"]),
    # a stalled status poll read as "still busy" instead of a fault
    ("busy_stall_as_busy",
     ((LITESPI, "\tif (status < 0)\n\t\treturn -1;\n", "\tif (status < 0)\n\t\treturn 1;\n"),),
     ["port_stall"]),
    # no-progress bound raised 16x (still bounded, 65,536 reads a wait)
    ("poll_max_16x",
     ((LITESPI, "#define LS_POLL_MAX 4096u", "#define LS_POLL_MAX 65536u"),),
     ["port_stall", "service_bound"]),
    # the binding walk skipped when the model is unproven is the head's
    # behaviour; this plant runs the binding walk before the model check,
    # as D3 section 8.1 orders steps 4 and 6, to show which check encodes it
    ("bindings_before_model_check",
     ((STORE, "\tif (!state->model_ready(state->ctx)) {\n"
              "\t\t/* nothing can be judged: AECP stays held until reset */\n"
              "\t\tnvm.st.cause = NVM_C_MODEL;\n",
       "\tif (!state->model_ready(state->ctx)) {\n"
       "\t\t/* nothing can be judged: AECP stays held until reset */\n"
       "\t\tif (nvm_choose() != NVM_NONE)\n\t\t\tnvm.st.bind_terminal = nvm_walk_bind();\n"
       "\t\tnvm.st.cause = NVM_C_MODEL;\n"),),
     list(gate.BOOT_PORTS)),
)


def plant(name: str, seams, dest: Path) -> None:
    """Copy the store's tree to dest and plant the seams."""
    nvm_mutants.plant(Mutant(name, seams, ()), dest)


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    inputs = shape_inputs(SHAPE, work / "inputs")
    # ---- raw runs on the unmodified head ----
    b = gate.bench_for(inputs, work / "head")
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid = max(b.frames)
    plen = len(b.frames[rid]) - 8
    new = bytes((rid * 13 + j * 11 + 99) & 0xFF for j in range(plen)).hex()
    head = ["--litespi", "--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new}"]
    for label, stall in (("two waits slowed (the suite's case)", "tx:2:0:4000"),
                         ("every TX wait slowed by 4,000 reads", "tx:100000:0:4000"),
                         ("every RX wait slowed by 4,000 reads", "rx:100000:0:4000"),
                         ("every TX wait slowed by 4,095 reads", "tx:100000:0:4095")):
        r = b.run(*head, "--until-phase", "7", "--ls-stall", stall, "--until-idle")
        s = r.s
        print(f"PROBE slow_master [{label}] stall={stall}: ok={s['ok']} failed={s['failed']} "
              f"max_call_us={s['max_call_us']} ls_stalled={s['ls_stalled']} "
              f"ls_max_withheld={s['ls_max_withheld']} ls_hung={s['ls_hung']} "
              f"(suite CALL_BOUND_US=1000)", flush=True)
    r = b.run("--slot-b", g, "--not-ready", "--boot", "--dump-state", "st.txt")
    print(f"PROBE unproven_model_bindings: terminal={r.s['terminal']} sm_applies={r.s['sm_applies']} "
          f"bind_terminal={r.s.get('bind_terminal')} binding records in shape={len(binding_ids(b))}",
          flush=True)
    # ---- reviewer-planted defects ----
    for name, seams, checks in PLANTS:
        tree = work / name / "tree"
        plant(name, seams, tree)
        mb = gate.bench_for(inputs, work / name, tree)
        res = gate.grade(mb, checks)
        red = {k: v for k, v in res.items() if v}
        verdict = "CAUGHT" if red else "SURVIVED"
        print(f"PROBE plant {name}: {verdict} by {sorted(red) or 'none'} of {len(checks)} graded",
              flush=True)
        for k, v in sorted(red.items()):
            print(f"    {k}: {v[0][:220]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
