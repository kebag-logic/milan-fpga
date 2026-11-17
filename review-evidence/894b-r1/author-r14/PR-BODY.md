[A781]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

**Review ready at `e1ecce20`, round 14.** Round 14 answers R843-6 (NEGATIVE, one MINOR) and R844-5 (POSITIVE, one wording residue), both at round 13's `d0a2a160`, with two commits on it. Under the owner's batch rule this is the last delta before #914 freezes; the composition lane takes this head. Published source head: `e1ecce20`. The manager owns composition, merge and the base synchronization for PR #914 (`894-8x8-1if` -> `dev-soft-core`).

- **Round 14 (`60389719`, `e1ecce20`).**
  - FR_NFR 3.4.1 gives 8x8/1if's hold-off at the head's figures: 2,027 cs for its 75 ms figure and 74.26 ms tx row, held by `flip_grade.py --check` (`tx_held`). Its 2,026 cs at 70 ms is marked historical.
  - A new flip control runs `--check --point 8x8/1if` itself on a 70 ms plant (`CHECK_HELD_CONTROL`). A new harness mutant leaves `tx_held` out of `--check`, and that control then fails by name.
  - The wording residues take their exact fixes. No firmware byte changes: all eight images are byte-identical to `d0a2a160`'s.

Round 13 (`a840c14d`, `32a9242f`, `d0a2a160`):


- **THE TRANSMIT's figure at 8x8/1if is held in the tree.** `flip_grade.py --check` now holds 8x8/1if's `CTRL_LOOP_TX_MS` at or over its tx row by every source (`tx_held`), separately from that point's reported rows. The row is derived in the tree from 8x8/1if's own polls, notices and builds. The self-test refuses the figure planted at 60, 69 and 74 ms by name.
- **The figure is restated to 75 ms.** The row is now 74.26 ms by every source, so 70 ms was under it. The withdrawn Talker's hold-off at 8x8/1if follows, from 2,026 to 2,027 cs. That keeps IEEE 802.1Q-2018 35.2.2.8's two LeaveAllTime periods after the Leave's latest departure: 20,005.74 ms remain, against 20,000.
- **Images.** The six images at 1x1/1if, 1x1/2if and 8x8/2if (the size fixture's and the target platform's) are byte-identical to `8883d499`'s. Each 8x8/1if image differs in that one immediate (`li a3,2026` to `li a3,2027`) and nothing else.
- **Re-measurement.** The 8x8/1if legs that reach the change were measured again on the new image. Every simulation log is byte-identical to round 10's on `46cf2a7d`'s image.
- **Section 13 and MAILBOX_SPLIT** now state each figure with the image or derivation it comes from.

Author packets: [`review-evidence/894b-r1/author-r5` to `author-r13`](https://github.com/kebag-logic/milan-fpga/tree/894-review-evidence/review-evidence/894b-r1) on branch `894-review-evidence` (archive `48b6c3a2`); round 14's is `author-r14` beside them.

## Linked Issue / roles

Closes #930
Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R843]`, latest R843-6 at `d0a2a160`, NEGATIVE on one MINOR, answered in round 14; re-review of this head is owed.
External reviewer: `[R844]`, latest R844-5 at `d0a2a160`, POSITIVE with one wording residue, answered in round 14; that verdict does not cover this head.

## Description

The lane gives 8x8/1if its own shape, scheduling costs and acceptance evidence. #930's fix copies Listener changes where the split SRP adapter receives them. That removes the registrar walk from each Listener record while keeping callback order, arguments and published state. No donor implementation changes.

### Round 14: R843-6 and R844-5

| Finding | Disposition | Commit, evidence |
|---|---|---|
| R843-6-F1, MINOR (Conformance, Docs): `FR_NFR.md:420` gives 8x8/1if's hold-off as 2,026 cs for 70 ms and a 69.84 ms row, as current | The report's text: "and 2,027 at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 74.26 ms rounded up, 75 ms, held to that row by `flip_grade.py --check` (`tx_held`; 2,026 at 70 ms before the row reached 74.26)". The tree is swept again for 69.84, 2,026, 2026 cs, `li a3,2026` and 70 ms beside 8x8/1if or THE TRANSMIT, and each remaining occurrence is explicitly historical. Section 13's composed-image immediate, which the bullet scoped, now names `d1c9023b`'s image. | `60389719`; `receipts/sweep-e1ecce20.txt` |
| R843-6-S1, SUGGESTION (Tests): `--check`'s use of `tx_held` is held by no self-test | Taken, with `--check`'s wiring unchanged. `flip_grade.check_held_control` runs `main` as `--check --point 8x8/1if` does, with 8x8/1if's figure planted at 70 ms in the text `tx_held` reads and nowhere else. It requires exit 1 and `OVER 8x8/1if: CTRL_LOOP_TX_MS states 70 ms`, giving 616 controls, from 615. The harness mutant `flip: --check does not call tx_held, so 8x8/1if's THE TRANSMIT figure goes unheld` runs `main` with `tx_held` finding nothing for its duration only. Under it the three earlier controls stay refused, and only `the flip check refuses --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms` fails, by name. That gives 260 mutants, from 259. | `e1ecce20`; `receipts/gates/harness-selftest-e1ecce20.txt`, `receipts/gates/check-held-mutant-e1ecce20.txt` |
| R843-6-R1, RESIDUE: `flip_grade.py:64-65` "two of the review's" | The exact fix. | `e1ecce20` |
| R843-6-R2, RESIDUE: `srp_mbx.c:34-35`'s guard named garbled | The exact fix, on the same two lines; every image byte-identical. | `60389719`; `receipts/images/img-identity-e1ecce20.txt` |
| R843-6-R3, RESIDUE: `srp_talker.cpp:53` "20,230 ms at one interface, 20,300 at two" | The exact fix: 20,230 ms at 1x1/1if, 20,270 at 8x8/1if and 20,300 at two interfaces. | `60389719` |
| R843-6-R4, RESIDUE: section 13 "At 70 ms the check refuses the head's costs, 74.26 ms." | The exact fix: "A 70 ms figure is refused against the head's tx row, 74.26 ms." | `60389719` |
| R843-6-R5 and R844-5-R1, RESIDUE (PR text): "Nothing has been pushed", the base `894-tiers`, and the publication prerequisite | Status now names the published head and the base `dev-soft-core`. The prerequisite sentence before the fetch commands is removed. | this body |

### Round 13: R843-5 and R844-4

| Finding | Disposition | Commit, evidence |
|---|---|---|
| R843-5-F1, MINOR (Tests, Docs): 8x8/1if's `CTRL_LOOP_TX_MS` is held by no in-tree gate, though `ctrl_loop.h` says it is | **Option (a).** `rows_grade` now holds 8x8/1if's own entry (`ROW_COSTS`: 8x8/2if's LINK, whose records and events that point takes, `load_grade.NEAREST`). `rows_grade.point_inputs` and `costs` read each point's polls and notices at its own shape (`shape_costs.of_point`, `shape_costs.notices_most`): 40 notices at 8x8/1if, where the header gave 12. `rows_tiers.point_inputs` takes the datapath events at the nearest point. So the tx row is derived in the tree. `flip_grade.tx_held` runs `rows_tiers.tx_statements` at 8x8/1if from `--check`, separately from that point's reported rows. 8x8/1if's other grading is unchanged: it stays `REPORTED`. `TX_HELD_CONTROLS` plant 60, 69 and 74 ms, and each is refused by name: 615 controls, from 612. `ctrl_loop.h`, section 13 and the SRP README name `tx_held` as the guard. | `a840c14d`, `32a9242f`; `receipts/model/tx-held-controls-d0a2a160.txt`, `receipts/model/rows-8x8-1if-d0a2a160.txt`, `receipts/reviews/r843-tx-plant-probe-*-d0a2a160.txt` |
| R844-4-F1, MAJOR (all five lenses): the tx row is 74.26 ms, the figure 70 ms, so the hold-off leaves 19,995.74 ms after the Leave's latest departure | **`CTRL_LOOP_TX_MS` 75 ms at 8x8/1if**, the row rounded up. It is derived in the tree, not mirrored, and the head's figure passes `tx_held`. `SRP_REDECLARE_CS` there is 2,027 cs. At 70 ms the check refuses the tree by name. R844-4's `transmit_contract_probe.py` at the head: `tx_statements` empty, 20,005.74 ms remaining, `MODEL ENVELOPE CHECK: PASS`. The images are as in Status, and the legs that reach the change were measured again (below). `srp_talker.cpp`'s `kHoldOffMs` derives from the constant, so its tests and plants follow the figure unchanged. They run at 1x1/1if and 8x8/2if, whose images are byte-identical. Every comment and document that said 69.84, 70 or 2,026 for the head now says 74.26, 75 or 2,027, or is labelled historical. | `32a9242f`, `d0a2a160`; `receipts/reviews/r844-transmit-contract-d0a2a160.txt`, `receipts/images/`, `receipts/harness/legs-32a9242f/` |
| R844-4-F2, MINOR (Conformance, Docs): section 13 and MAILBOX_SPLIT give older images' figures as the head's | Each figure is now stated with its image or derivation. Round 5's SRP record and retry rounds are labelled `a15345f7`'s. The image with the Listener copies gives the current ones: SRP 32,936 cycles, 2,403,014 rounds, last notice 25.625 ms. The rows by every source are the tree's own derivation at 8x8/1if: R4 21.39, R5 136.64, R6 132.93, first 18.98, last 387.95, R4L 208.55, ACMP 52.76, ADP 52.64, MAAP 53.91, tx 74.26 and txL 159.82 ms. `af2c4d7a`'s rows are kept as historical, as is the composed image's 69.84 and 70 ms. The largest-command load is 1.034, with 0.969 labelled as `af2c4d7a`'s. THE SHARE is two passes on `46cf2a7d`'s image, longest 222,434 cycles. MAILBOX_SPLIT gives the 1x1/1if slice as 0.9 ms. | `d0a2a160`; `receipts/model/rows-8x8-1if-d0a2a160.txt` |
| R843-5-R1, RESIDUE: `load_grade.py`'s header calls the donor column "owed to the pin move" | The exact fix: `Load at the donor's measured costs (the pin carries tsn-c-stack#32)`. | `d0a2a160` |
| R843-5-R2, RESIDUE: the packet index named the wrong round | `index.py` now takes the round from the directory name; this packet's index says round 13. | packet `scripts/index.py` |
| R843-4-R1, RESIDUE, retained: FR_NFR 3.4.1's "as on each image before it" | R843-5's exact fix. The head's measurement "holds, as the image that merges dev-soft-core `70f4056f` (#901's Talker declarations) and round 3's image (...) each did at their own figures". The head's own 8x8/1if image is named: the hold-off's one immediate restated, and the legs it reaches measured again. | `d0a2a160` |

### The 8x8/1if legs on the 75 ms image

On a clean clone of `32a9242f`, which builds the same images as `d0a2a160`, these legs ran:
- `srp-talker-held`, `srp-talker` and `srp-talker-loss` (the `valid-destinations` arm);
- the `transmit-aged` control.

Each exits 0 with no STATED line. Every group's simulation log is byte-identical, by sha256, to its round 10 measurement on `46cf2a7d`'s image. Every graded table and text is the same too.

The one value that differs in each grade is the stated reclaim limit: 40 us, which the ruling on round 10's STOP restated, against the 35 us then. It is a statement, not a measurement.

The groups arm the hold-off when they withdraw a Talker. Each ends before a hold-off it arms runs out, 20.27 s after the withdrawal, so no measured row moves.

The gate over the three positive legs:
- SRP 10.869 ms, MRPDU 3.109 ms;
- the Talker declaration rows at most 189.638 ms against 220;
- joins 187.576 to 190.335 ms;
- no STATED line, 0 instances over budget.

Its only findings are the seven held-egress ledger rows. These groups do not measure them; arm A's `backlog-owed` does, on `46cf2a7d`'s image (round 10). The control is caught in 8 of 8 groups, 71.564 to 72.119 ms, as in round 10.

Evidence: `receipts/harness/legs-32a9242f/`, the gate `gate-8x8-1if-valid-destinations.txt` and the comparison `legs-against-46cf2a7d.txt`.

### #930 targets and measured figures

They were measured on `46cf2a7d`'s image (round 10). The head's 1x1/1if, 1x1/2if and 8x8/2if images are byte-identical to it, and its 8x8/1if images differ only in the hold-off's immediate (above).

| Target | Before the fix | Fixed measurement | Required |
|---|---:|---:|---:|
| 1x1/1if SRP record | 27,170 CPU cycles, 290 us by the rule | 23,503 cycles, 250 us by the rule; stated 280 us | At most 280 us / 26,660 cycles |
| 1x1/1if last queued notice, by every source | 157.09 ms after restating costs | 136.65 ms | At most 140 ms |
| 8x8/1if load at the pin | 0.783 after restating costs | 0.735 | At most 0.75 |
| Measured CPU-decided rows at both points, including `srp-talker-held` | New group exposed the understated SRP cost | Each within its own bound | Each row's bound |

At 8x8/1if the SRP record falls from 42,663 to 32,936 cycles, 350 us by the rule against 365 stated. The retained retry is stated at 345 us from 32,618 cycles. At 1x1/1if the retained retry is stated at 280 us from 23,144 cycles. These figures return to each point's earlier statements, never below them. The 8x8/1if reclaim is stated at 40 us from 3,446 cycles. The ruling accepts these restatements.

R4 by every source at 8x8/1if is **21.39 ms against 20 ms**, owed to #872. The other every-source rows reported there remain owed too: R5 136.64 ms, the last queued notice 387.95 ms and txL 159.82 ms. tx is 74.26 ms, now within THE TRANSMIT's 75 ms figure, which `tx_held` holds; the MRPDU's 49 ms bound by every source stays owed with the rest. Measured acceptance does not turn those derived misses into passes.

### Gates at the round 14 head

Each ran on a fresh clean clone of `e1ecce20`. By the round's brief, no campaign and no leg was re-run: round 14 changes no firmware byte.

| Gate | Result | Receipt |
|---|---|---|
| Harness self-test with its mutants (`run.py --self-test`) | PASS: 932 checks, from 931; 260 mutants caught, from 259; 0 failures; the clone unchanged after. The new mutant is caught by `the flip check refuses --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms`. | `receipts/gates/harness-selftest-e1ecce20.txt` |
| The new control and its mutant, by name | Refused at the wiring. Under the mutant only that check fails; the three earlier controls stay refused. Refused again after. | `receipts/gates/check-held-mutant-e1ecce20.txt` |
| The flip gate | `--check` at 1x1/1if and at 8x8/1if PASS, the latter with its HELD line (75 ms against 74.26 ms); `--selftest` 616 of 616 refused. 8x8/2if's check exits 1, by design. | `receipts/gates/quick-checks-e1ecce20.txt` |
| Quick checks | 22 rc 0, plus the 8x8/2if flip check's rc 1, by design. They cover: the shape table; rows_tiers (1,033); the load gate (28, and `--check`); the record classes (14); the mixed-point probe; the ledger's 15 mutants; docs_check, and the Python and C++ idiom gates; the comment scans over the PR's, round 13's and round 14's delta and R844-1's audit, 0 lines; the diff checks. | same |
| Docs jobs (`docs.yml`: wire-accountability, docs-check-no-git, docs-gates-0, 1 and 2, docs-check) | PASS: 61 steps rc 0, 34 not run with a stated reason, 0 bad | `receipts/gates/verify-docs-yml-e1ecce20.txt`, `receipts/gates/workflow/` |
| Images | All eight byte-identical to `d0a2a160`'s, by ELF and loadable sha256, both 8x8/1if images among them | `receipts/images/img-identity-e1ecce20.txt` |
| The sweep (R843-6-F1) | 19 hits for 69.84, 2,026, 2026 cs, `li a3,2026`, and 70 ms beside 8x8/1if or THE TRANSMIT. Each is historical, a plant or refusal, or unrelated. | `receipts/sweep-e1ecce20.txt` |

### Gates at round 13's head, `d0a2a160`

Each ran on a fresh clean clone of `d0a2a160`:

| Gate | Result | Receipt |
|---|---|---|
| Harness self-test with its mutants (`run.py --self-test`) | PASS: 931 checks, 259 mutants caught, 0 failures; the clone unchanged after | `receipts/gates/harness-selftest-d0a2a160.txt` |
| The flip gate | `--check` at 1x1/1if and at 8x8/1if PASS, the latter with its HELD line; `--selftest` 615 of 615 refused, the three new controls refused by name. 8x8/2if's check exits 1, by design (its rows are reported). | `receipts/gates/quick-checks-d0a2a160.txt`, `receipts/model/` |
| The load gate | `--check` PASS (8x8/1if 0.735 at the pin); `--selftest` 28 of 28 refused | same |
| Quick checks | 20 rc 0, plus the 8x8/2if flip check's rc 1, by design. They cover: the shape table; rows_tiers (1,033); the record classes (14); the mixed-point probe; the ledger's 15 mutants; docs_check and the idiom gates; the comment scans over the PR's and this round's delta, and R844-1's audit, 0 lines; the diff checks. | `receipts/gates/quick-checks-d0a2a160.txt` |
| Every grader against 8883d499's | Identical exit codes. The only differences are 8x8/1if's figure 70 to 75 ms in the shape table, the HELD line, the control count 612 to 615 and the load table's header. | `receipts/model/graders-8883d499-against-d0a2a160.txt` |
| Docs jobs (`docs.yml`: wire-accountability, docs-check-no-git, docs-gates-0, 1 and 2, docs-check) | PASS: 61 steps rc 0, 34 not run with a stated reason (the hosted-only bookkeeping steps), 0 bad | `receipts/gates/verify-docs-yml-d0a2a160.txt`, `receipts/gates/workflow/` |
| SRP campaign (`rtl-fast.yml` `firmware-srp-mutants`) | PASS: 436 caught, 0 escaped, the Talker hold-off plants and the 8x8/1if Listener copy campaign among them; every step rc 0 | `receipts/gates/srp-campaign-plants-d0a2a160.txt` |
| Firmware suites and coverage (`rtl-fast.yml` `firmware-unit`) | PASS. The control-plane suites and RV32 builds pass, among them `srp_talker.cpp` at 1x1/1if and 8x8/2if and `srp_listeners.cpp` at 8x8/1if; so do the saved-state store suites. `fw_coverage --check` covers 39 files, `srp_mbx.c` 746 of 746 lines. | `receipts/gates/workflow/rtl-fast__firmware-unit__*` |
| Images | The six at 1x1/1if, 1x1/2if and 8x8/2if identical to 8883d499's; each 8x8/1if image one instruction apart (above). The check's control, 8883d499 against itself, fails at 8x8/1if as it must. | `receipts/images/` |
| The reviewers' probes | R844-4's: PASS. R843-5's, its plant pointed at the head's 75u: refused by name at 60 ms and at 70 ms. | `receipts/reviews/` |
| `twin`, `twin-plants` | FAIL, owed to PR #935 (the base's `split-talker-failed` row); not re-run | round 11's evidence |

Not re-run at `d0a2a160`: the control and AECP campaigns, the boundary and simulation jobs, the verilator shards and the lane gates. They ran at `05a7ea82` (round 11), and the SRP campaign and six shards at `8883d499` (round 12). Round 13's source changes are limited to the following, and each has its own gate above:
- THE TRANSMIT's figure in `ctrl_loop.h`'s 8x8/1if block, read only by `SRP_REDECLARE_CS` (its images and legs above) and by `srp_talker.cpp`, whose arms run at 1x1/1if and 8x8/2if, where the figure did not change, and pass in `firmware-unit` above;
- two comments;
- the graders `flip_grade.py`, `rows_grade.py`, `rows_tiers.py` and `load_grade.py`'s header, whose checks and self-tests ran above.

### Earlier rounds

Round 12 retargeted the two escaped SRP plants to the Listener's indication, `asking-is-ready` and `readyfailed-ignored`, where #930 moved the behaviour. Both are caught by name. It also recorded the `twin` and `twin-plants` failures as owed to PR #935: the base's stale `split-talker-failed` row. Round 11 moved `backlog-owed.service.aecp.last.if0` at 8x8/1if to the rule's 62.16 ms by ruling. The ledger states the three measurements: merged 61.84625, composed 61.75319 and Listener copies 62.04905 ms. The earlier findings' dispositions, R844-1 to R844-3 and R843-1 to R843-4, stand as round 12's body gives them. R843-4-R1 is closed above.

## Authoritative references

- R843-5 ([PR #914 issuecomment-6940020752](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6940020752)) and R844-4 ([PR #914 issuecomment-6940102979](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6940102979)): the findings this round answers.
- IEEE 802.1Q-2018 35.2.2.8 (two LeaveAllTime periods after the Leave) and Table 10-4; the SRP adapter contract (`srp_mbx.c`, `SRP_REDECLARE_CS`); FR_NFR 3.4.1; SPLIT_CONTROL_MEMORY sections 11 and 13.
- [#894 round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6938589932): the retargeted plants, the twin rows owed to PR #935.
- [#894 round-11 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411): the 62.16 ms ledger move, the accepted #930 targets and #872's R4 debt.
- [#930](https://github.com/kebag-logic/milan-fpga/issues/930) and [the preceding ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6918853411): fix the SRP cost inside the split adapter; the bounds do not move.
- [The composition ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6914952893): THE TRANSMIT's figure keyed on the shape.
- [Held-egress ruling, item (a)](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905) and [ledger ruling, items 2 and 3](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049).
- [Shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227) and [egress bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126).
- PR #935: the base's `split-talker-failed` row restated.
- #818: the timing floor, +0.030 ns setup and 0 ns hold, best of three directives.

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach e1ecce20
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

## How to validate

On a clean clone with the pinned prerequisites:

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 3/4
git diff --check 8883d499 HEAD
```

Expected result / pass criteria:

- **The 8x8/1if flip check** passes and prints `HELD 8x8/1if: THE TRANSMIT's figure CTRL_LOOP_TX_MS 75 ms against its tx row by every source 74.26 ms`. With the figure edited to 70 ms, or to 60, it fails with `OVER 8x8/1if: CTRL_LOOP_TX_MS states 70 ms, under the built design's tx row 74.26 ms`.
- **The flip self-test** refuses 616 of 616 controls. Among them are the three named `8x8/1if's CTRL_LOOP_TX_MS planted at 60/69/74 ms, under its tx row` and `--check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms`.
- **The 1x1/1if flip check and the load gate** pass: 1x1/1if's last queued notice by every source is 136.65 ms, and 8x8/1if's load at the pin 0.735.
- **The harness self-test** passes every check and catches every mutant, 260 of them, `flip: --check does not call tx_held, ...` among them, and **the ledger's self-test** refuses 15 of 15 mutants.
- **The SRP campaign** (`--shard 3/4`) prints no `[ESCAPED]`.
- **`make -C tb/verilator/milan_dp twin` and `twin-plants`** fail on `split-talker-failed` until PR #935 lands.

## Known limitations / out of scope

- **`twin` and `twin-plants`** fail on the base's stale `split-talker-failed` row, owed to PR #935 by the ruling on round 11's STOP.
- **The every-source rows at 8x8/1if** stay owed to #872, as ruled: R4 21.39 ms against 20, among others. Only THE TRANSMIT's figure is held there, since the hold-off uses it. The held-egress rows stay recorded misses, limited by their ledger.
- **The timing floor** is #818's: +0.030 ns setup and 0 ns hold, on the best of the three directives. This lane routes no bitstream and claims no new timing result.
- **`Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if** is the previously disclosed test outside the selected arm; its historical reproduction is in both reviews.
- **Not done in this round:** no hardware, bench, flashing, donor edit, merge or base synchronization. No hosted or merge-candidate pass is claimed.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (#930's targets, as ruled)
- [x] Changed behavior has self-checking tests, and every new control is refused by name
- [x] Required local verification bar passes, but `twin` and `twin-plants`, owed to PR #935
- [ ] Self-test evidence is posted in a PR comment
- [x] Requirement and interface changes are documented
- [ ] Internal cleared-context review is positive at the candidate
- [ ] External review is positive at the candidate
- [ ] Blocking findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [x] Authoritative documentation states each figure with its image
- [ ] Post-merge containment is clean before the Issue moves to Done

