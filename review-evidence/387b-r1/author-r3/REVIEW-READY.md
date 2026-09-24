[A277] REVIEW READY

Commit: `0f003fab3303858ba4db955ad3c0512e67a8018b` (local head on `387-media-rebase`; not pushed).

Round 3 implements assignment [5820585975](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975): the 3600-second deadline and its contract, nested recipe freshness for both positive legs, the three documentation scope corrections, both requested RTL comments, the decided PR-body citations, and the live-CSR settime render check. The hosted shards already allow 120 minutes. No functional RTL changed this round.

Validation: all assigned commands exited 0. The chunked default `milan_dp` sweep ran 44 commands, 9785 checks, 0 failures; `gmstep-mutants` passed 13/13; tkdiag passed 96/96 with all four mutants caught. The reviewer's unchanged GNU make 4.3 repro prints `is_fresh: True` inside the parent recipe. Both positive legs also pass nested assertions, and the old behavior fails them. The settime omission control fails the named render check.

Both documentation CI modes, the requested static gates, and 344 behavior scenarios pass. The full builder without an RV32 compiler rejects 189/189 applicable mutations; compiler-dependent instruments and physical calibration remain explicitly NOT RUN. The deadline contract and its 101-check self-test pass. The em-dash gate used base `57456af96b3127b9d309a995bbbd35a6113ce52d`.

`HANDOFF.md`, the full replacement `PR-BODY.md`, and command/exit receipts are prepared in the assigned output packet. No PR edit or push was made. Independent re-review, publication, hosted/candidate validation, and merge remain pending. Issue #387 acceptance 4 remains the manager's #117 bench step after merge.
