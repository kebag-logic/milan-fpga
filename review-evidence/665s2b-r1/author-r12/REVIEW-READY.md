[A683o] REVIEW READY
Commit: `c954b8a91e720f87d2dfa9294c8501058dc55df3` on `665-s2b-cycles` (local, not pushed), on A683n's `668126b3`: one merge of `dev-soft-core` `a68536fa`, then sixteen commits. No rebase, no force, one merge base. PR target `dev-soft-core`, `Relates to #665`.

Changed:
- **The merge** (`8b448143`), both sides kept. A683n's uncommitted README edit is kept (`7e5b95a2`). Three semantic conflicts, each its own commit: the merged boot simulation still drove the CPU from the Milan clock (`08618784`, `392ba9bc`); the platform image was built RV32I against the split link, and no longer linked (`99f51950`, `bc50a190`, `ff2e855f`); the merged campaign file was over the 1,000-line limit (`82efbe36`).
- **An SRP link change takes two passes** (`584bdad2`, `452976c8`): it withdraws in the pass that takes it, the next pass's poll builds, and SRP's receive waits. This was the one 8x8 pass over the 2.0 ms share, 2.21 and 2.22 ms; six and four events a pass left it at 2.207 and 2.108 ms.
- **The store's read-back is 128 bytes a step** (`4c0805b5`): a whole page through the product's uncached window with lwSRP's periodic tick was 2.256 ms at 8x8. A save's read-back now takes twice as many ticks.
- **The harness** (`7dd0ef04`, `f7f2f006`): the product's uncached flash window but in hybrid-XIP (the cached one gave 12.39 ms at 8x8, 4.07 at 1x1); AECP frames paced to the token bucket (3 and 15 probes were refused at 100 MHz); backlog windows open on a drained event ring.
- **Docs** (`103ac6d5`, `66cfe88f`, `c954b8a9`): the split CPU on `sys`, sections 11 to 13 as dated records, new section 14.

Every measured row and pass fits, with the CPU on `sys` at 100 MHz, the bus on the same clock, each family against min(T_svc = 20 ms, its ceiling); ms, arm A / arm B, bold over the bound:

| Row | Bound | 1x1/1if | 1x1/1if, drafts | 8x8/2if | 8x8/2if, drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| Passes over the 2.0 ms share, longest | 2 | 0, 1.07 / 0, 1.07 | 0, 0.98 / 0, 0.98 | 0, 1.97 / 0, 1.92 | 0, 1.77 / 0, 1.77 |
| The three egress-held rows | 20 | **over** | **over** | **over** | **over** |

Arm A also ran every group: 18 and 17 groups, 0 refusals, 0 of 7,837 and 0 of 8,477 work passes over the share. The egress-held rows stay with tsn-c-stack #26. Out of context on `sys` at 10 ns: WNS +1.605 ns, WHS +0.070 ns, 3,543 LUTs, 5,643 FFs, 9.5 tiles, against 3,948, 6,879 and 14.5 behind the crossing.

**The two windows (item 3):** the window's definition was wrong, not the firmware. With k records held only 16 - k + 1 of the fifteen grandmaster changes commit, and it waited a fixed time for a drained ring. At 1x1, 4 KiB, at 100 MHz, all four windows hold 0 records at opening and commit 15 of 15. The composed maximum is no longer partial: at least 40.25 ms, a lower bound because two windows close with SRP records unreleased.

**32x32, an estimate, not a measurement** (`SPLIT_CONTROL_MEMORY.md` section 14). U is the assigned 4 x 8x8/2if, L the measured line, S the slope at one interface. Over by, ms, S / L / U:
- last AECP record, 20 ms: 5.8 / 12.8 / 40.6;
- last SRP record, 18 ms: 13.1 / 18.4 / 45.8;
- longest pass, 2.0 ms share: 1.7 / 3.0 / 5.9;
- under U alone: first SRP record 3.4, last ACMP 11.9, last ADP 3.4, last MAAP 3.3, ACMP command behind a full ring 6.9.

**One CPU, measured on `sys` at 100 MHz, arm A.** Cacheless RV32IM at 8x8: AECP 26.83, SRP 30.26, 62 passes over, longest 3.61 ms. Cacheless RV32I at 8x8: AECP 28.51, SRP 34.52, 64 passes over, 3.85 ms. At 1x1 RV32IM fits every row (SRP 17.98 of 18) with 3 passes over; RV32I misses SRP at 21.63. The split placement already has one hart.

**gPTP, a labelled assumption, not measured:** 2.5 % of the CPU (1.2 to 6.2), 1.6 ms on a row, 0.8 ms on a pass. F6's stack in this harness, with those frames on both ports, would measure it.

Validation, all rc 0 on clean clones of the head unless noted:
- every `run:` step of `docs.yml`: 64 ran, 31 not run with a reason, 0 bad; `test_builder.py --require-rv32` `ALL GATES PASS EXCEPT 2 NOT RUN` (gates 1b and 11); `cd tests && behave` 508 scenarios;
- the full sweep, four shards: 65 of 65 suites, 2,613,655 checks, 0 failures;
- `test_ctrl_firmware.py --require-rv32 --self-test`, four shards: 603 of 603 control mutants and every SRP defect caught; `test_ctrl_nvm.py --self-test` 110 planted defects; `fw_coverage.py --check` 38 files; `ctrl_boundary.py`, both steps;
- the harness self-test: 0 failures, 101 mutants; its controls caught; the split boot at both shapes, 24.660 and 64.271 ms, with its plants;
- the harness at both points and all 14 legs ran at `4c0805b5`: docs and the matrix are the only change since, and both images rebuilt at the head are byte-identical.

First failures, each kept in the receipts: the sweep at `103ac6d5` failed `tsn_fuzz` on a stale `MODULE_MATRIX.md` (fixed in `c954b8a9`, all four shards re-run). `boundary_b` failed on my missing `--no-print-directory`. Two SDK steps failed on my copied HOME. Firmware shard 3 refused three moved anchors (fixed in `452976c8`). #833 did not appear.

Acceptance criteria: this round's are met. #665 stays open.

Open risks/questions, for the manager; none decided here:
1. **32x32:** the last AECP and SRP records and the share miss under every reading. The levers are the contract's rings and buckets, D4(b)'s two records a pass, the share and the per-stream polls.
2. **Which CPU lever 4 means.** The charter counts 3,948 LUTs of split CPU on top of the 3,249 the 52,008 holds, but `MilanSoC` builds one hart under `--ctrl-mailbox`, so its 3.55k is an accounting correction. The cacheless core would save about 300 LUTs and 5 tiles and does not fit 8x8.
3. **A clock past 100 MHz or a second hart,** if the firmware's levers do not close 32x32.
4. **A pass no group stages:** a save's read-back step in a composed window's heaviest pass would be about 2.67 ms. Derived, not measured; the rows' margin holds it. The longest measured pass, 1.97 ms, leaves the share 0.03 ms.
5. **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing there.

Handoff, receipts and PR body are in the lane's output directory (`HANDOFF.md`, `PR-BODY.md`, `receipts/INDEX.md`).
