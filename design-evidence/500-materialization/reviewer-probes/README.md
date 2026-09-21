# The reviewers' probes, rerun against revision d

Both round-two reviews of PR #503 published their fault-injection probes in
the review archive, commit `7d9da8773c8baec0f705b08cea8b9e04d8c00b27`,
`review-evidence/503-round2/`, and both round-three reviews theirs in commit
`3d790bc1eacad2af0cb7d80c647f0c8eca186c46`,
`review-evidence/503-round3/reviews/`. This directory reruns them against
this evidence, in adapted copies, and grades the outcome against the
behaviour each reviewer demanded.

## Round two: the adaptations

The archive's README says the scripts carry explicit checkout and scratch
paths, to be adapted in copies. Each copy states its adaptations in its
docstring; in short:

| Copy | Original (sha256) | Adapted |
|---|---|---|
| `r217_probes.py` | `R217/probes.py` (`94de822b...52b`) | paths from `PROBE_OUT` and `EVIDENCE`; the reviewer's bridge seam (the first descriptor request accepted after an application answers 5,000 cycles late) is now the evidence's own knob `desc_delay_after_apply`, with the same trigger |
| `r218_probe_headers.py` | `R218/probe_headers.py` (`d713e83d...ad9`) | paths from `PROBE_OUT` and `EVIDENCE`; V18's anchor carries its comment line, because the line it patched now also occurs in H2 and H2b; the V1a slots come from a seed run of the probe's own build; the two original-trigger results also record their terminal defaults mismatches |

## Round three: the adaptations

| Copy | Original (sha256) | Adapted |
|---|---|---|
| `r217_r3_probe_preload.py` | `reviews/R217/REVIEW-evidence/probe_preload.py` (`6605c569...bc`) | paths from `PROBE_OUT` and `EVIDENCE`; the original PATCHED `d3_top.sv` to connect the unchanged pinned listener and drove its talker-event face with the pinned `acmp_nvm` suite's `evt_block_i` lever. Revision d instantiates that listener itself, behind the admission gate, so the lever is the harness's own talker-event producer, held as the same level (a droppable event, sink `0xffff`) from reset, for ever or to the same release cycle 100000. It runs its ten scenarios on the gate (`base-1x1`'s wiring) AND on `LG01_admission_deleted` (the pinned wiring) |
| `r218_r3_probe_stage1.py` | the Python snippet in `reviews/R218/REVIEW.md` (R3-F1) | paths from `PROBE_OUT`, `FULL_OUT` (the full run's `D3_OUT`) and `EVIDENCE`; besides the reviewer's `base-1x1` and `mut-R03_rollback_skips_desc_store`, the stage-1 build `base-1x1-stage1` and its deletion mutant `mut-ST1_stage1_rollback_skips_desc_store` |

Every other stimulus, variant, slot and case is the reviewer's.

## Grading

The reviewers' own checkers assert their COUNTEREXAMPLES. The
counterexamples are what each revision removes, so `r217_check.py`,
`r218_check.py`, `r217_r3_check.py` and `r218_r3_check.py` assert what each
reviewer demanded instead:

- round two: a header transport error in either pass or both ends with a
  failure verdict and complete defaults, never blank; a descriptor fault
  after an application rolls back to proven defaults, or ends CLOSED while
  the memory still fails; an image that cannot be proven at the start ends
  CLOSED; the original payload and timeout triggers keep rolling back;
- round three, R217: with the admission gate, a held and a finite talker
  event level leave the binding walk, the D3 terminal and the enable where
  the ready control leaves them, and the GET answers the saved value; the
  descriptor-boundary observations the reviewer recorded as safe are
  unchanged; with the gate deleted the counterexample comes back;
- round three, R218: stage 1's own roll-back scope recovers the 5,000- and
  16,000-cycle delays to proven DEFAULTS with the entity enabled and the
  owners released only after the late burst; removing the stage-1 recovery
  mechanism (ST1, and the reviewer's R03) ends CLOSED; the one-error
  control recovers either way.

`results.txt` also records each reviewer's own checker on the same results:
R217's round-two `check_probes.py` and round-three
`assert_review_observations.py` both exit 1, at their counterexample
assertions. On `LG01_admission_deleted`'s results the round-three checker's
held-preload assertion holds again; its finite assertion names the exact
cycle 107431, which the drained release of revision d moves to 107433.

## Rerun

From this directory, with the three submodules initialised, the tools the
evidence README names, and the full run's build tree:

    export PROBE_OUT=/path/to/empty/scratch
    export FULL_OUT=/path/to/the/full/run/D3_OUT
    python3 -B r217_probes.py && python3 -B r217_check.py
    python3 -B r218_probe_headers.py && python3 -B r218_check.py
    python3 -B r217_r3_probe_preload.py && python3 -B r217_r3_check.py
    python3 -B r218_r3_probe_stage1.py && python3 -B r218_r3_check.py

Each checker exits 0 only if every run holds, and prints one line per run.
The command record beside this directory lists the recorded outcome.
