Status: REVIEW READY (12:55). The 4x4/1if image qualifies with the control CPU at 100 MHz:
- The route meets the floor at every corner (ExtraPostPlacementOpt +0.049 / +0.012 ns).
- The rule's row (125 / 5 / 1250) meets every owner bound on the link-rate census: load 0.469, ACMP 28.52, txL 48.72, last 117.68 ms, SHARE 1.733 ms.
- The 100 Mb/s egress grade passes (527.04 of 1000 us).
- Every gate passes, the builder suite included (gate 11 NOT RUN, no calibration report on disk); the 1x1 and ALINX images are byte-identical.
ETA: done. Next: independent review, the decisions below, and the bench (latency pair at 100 MHz).

[A863], round 3: the 100 MHz path. Worktree `$LANES/arty-4x4`, branch `arty-4x4-1127`, head `ac0ed29bc` (gates at the heads named in REPORT.md section 4). Nothing pushed or posted; no bench, no flash.

## Round-3 commits

- `8b7ba27b7` the 4x4 configuration at sys 100 MHz; the basis row from round 1's cycles at 100 MHz; per-point Arty clocks.
- `45de3bc59` the rule's row from census 2.
- `a64c88bd2` documents at 100 MHz; the latency pair stated as the 80 MHz measurement.
- `f33bfcebf` merge of #1004 round 10 (`640699e68`): the link-rate census and `egress_mii.py`.
- `e7bc55f8a` the CRF output counted in the 100 Mb/s stream load.
- `00f1fcd9d` the rule's row from the link-rate census: `CTRL_LOOP_TX_MS` 29; no firmware byte changes.
- `d0f402ee5` the 4x4 bind bounds by the Arty rule (550 ms, 4 saves).
- `41166c346` the fixed-path bench at another sys clock (300.0 ns at 100 MHz).
- `ac0ed29bc` FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY section 15: the 4x4 qualification.

## Decisions needed

1. **Held-egress ledger at `arty-4x4`** (none stated). The rows measure 61.56 to 63.33 ms; #878's rule would give 61.65 to 63.50 ms.
2. **Bind bounds**: PR #1004's rule applied at the new point (550 ms, 4 saves); confirm.
3. **Dependency**: this branch carries #1004 round 10 (unpushed, REVIEW READY). It must follow #1004 if that changes.
4. **Latency pair at 100 MHz**: owed to the bench (the model does not use it).
5. **Thin margins**: txL 0.28 ms, SHARE 0.27 ms, setup +0.019 ns over the floor on one of three directives.

Files: REPORT.md, PR-BODY.md, receipts/INDEX.md. Scratch `$VALIDATION_STORAGE/arty4x4-a863`, about 8.2 GB; census traces archived as `c1..c4-*.tar.zst`.
