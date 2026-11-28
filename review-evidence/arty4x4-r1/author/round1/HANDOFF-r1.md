Status: STOP (19:40). No row of the Arty 4x4/1if point meets every owner bound. Census 1 is complete (159/159, all native PASS); by the rule, the least txL is 58.71 ms (49), ACMP 37.39 ms (30) and last notice 201.93 ms (140), with load 0.578. The egress replay passes (a) and (b); all three routes pass the floor; every other gate passes, the builder suite included (gate 11 NOT RUN, no calibration report on disk).
ETA: done. The next step needs an owner or manager decision (below).

[A863], round 1, desk only. Worktree `$LANES/arty-4x4`, branch `arty-4x4-1127`, head `11f903bd4`, on `aa53840d9`. Nothing pushed or posted; no bench, no flash.
Scratch `$VALIDATION_STORAGE/arty4x4-a863` (7.8 GB of 12; census traces kept for review).

## Commits

- `7aef00c4a` the 4x4 configuration, its generated shape include, the (1,5,5) row at the 1x1's statements.
- `1c158ec15` the `arty-4x4` harness point (tables at the 1x1's figures), `arty_grade --point`, the builder-suite registration, the tap-clock docs row.
- `4d6011177` docs (builder, build, harness README) and the two harness self-test point checks.
- `1e186eca6` AUDIO_UNIT 48 kHz alone (gate 36a); the builder suite's identity (gate 28b) and measured-latency (gate 36) entries.
- `11f903bd4` SPLIT_CONTROL_MEMORY.md section 15: the 4x4 point's census result and memory ledger.

## Decisions needed

1. **The STOP.** No rule-conforming row exists at 4x4/1if, 80 MHz. Even at the 1x1's costs the 4x4 counts alone leave no row. Options: a smaller Arty shape (2x2?), firmware cost work at this shape, or a clock ruling. None is taken here.
2. **SET_STREAM_FORMAT vs Milan v1.2 5.4.2.7.** 5.4.2.7 allows no bandwidth refusal of an advertised format. The image advertises only formats that fit four-up: 2ch/48 kHz outputs, the 48 kHz family on inputs, no 96/192 kHz. A bandwidth refusal at SET_STREAM_FORMAT would need a ruling.
3. **Held-egress ledger at (1,5,5).** No ledger is stated; its rows measure 61.92 to 64.13 ms.
4. **Egress grader.** The replay here is lane-local (`tools/egress_replay.py`, 13-case self-test). Its fixed path is an analytic 2 us, not measured on the shipping chain. #1004's in-tree grader should replace it.
5. **Bind bounds at the Arty points.** Still unruled (as in round 9); measured with sentinels only.

## Where things are

- REPORT.md (full results and tables), PR-BODY.md, receipts/INDEX.md.
- Tools: `receipts/tools/` (copies of the scratch tools).
