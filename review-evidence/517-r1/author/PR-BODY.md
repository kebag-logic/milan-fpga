[A178]

## Status

Local implementation at `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52` is ready for independent review.
Manager validation and both reserved reviews remain pending.

## Description

The ten ordinary milan_dp executables previously ran sequentially. A suite-local
runner now allows two children while keeping the five sim_nxn header writers
exclusive and ordered. Independent legs can overlap that group. SIM_JOBS=1
reproduces sequential execution; presence of MILAN_COUNTER_FRAME_OUT preserves
the original whole-set order. Per-child logs replay in legacy order. Failures
stop the recipe, and interruption terminates and reaps owned descendants.
Build recipes, gPTP prerequisites and render mutation phases are unchanged.
The inaccurate sim_nxn explanatory comment is corrected; executable tokens match.

## How to reproduce

With pinned Verilator 5.050 on PATH, compare the complete suite:

```sh
make -C tb/verilator/milan_dp clean
make -C tb/verilator/milan_dp run SIM_JOBS=1 VERILATOR_JOBS=8
make -C tb/verilator/milan_dp clean
make -C tb/verilator/milan_dp run SIM_JOBS=2 VERILATOR_JOBS=8
```

## How to validate

Run `python3 tb/verilator/milan_dp/test_sim_pool.py`, the existing phase controls,
and the complete real suite with its unchanged render campaign. Preserve logs
and use `scripts/suite_tally.py --verdict`. Controlled cold/warm and fault-test
receipts are supplied in the author handoff for a PR evidence comment. The
manager owns full native banks, trusted act, hosted timing/gates and candidate checks.

## DoD

Local scope and measured comparisons are recorded. R245/R246 review, manager
validation, authorized merge and post-merge containment remain open. No author
approval is claimed.

Closes #517
Relates to #270
