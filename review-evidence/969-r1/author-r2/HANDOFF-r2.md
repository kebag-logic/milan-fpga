# HANDOFF r2: [A817] #969 / PR #971 correction round (R886-1 NEGATIVE, R885-1 NEGATIVE at `f863258d`)

Status: **REVIEW READY** (22:30 CET 2026-11-22) at `e816c74d`. The round-2 STOP (#969 issuecomment-7083505751) was
answered by the manager's ruling (option 1): the registration cost is a pre-existing gap, issue #977, owed and not
restated. Since: `33ae95f9` (srp-bound beside srp-kept in kept_window.py; kept_grade's #977 disposition, run.py's
STATED and SHARE lines given it), `5dba2089` (harness README), `e816c74d` (kept_grade: a group with no graded result
is a finding). Both groups ran in one build at each point at `5dba2089`: run.py exit 0, every #977 line OWED, and
kept_grade PASS (kept <= bound; no srp-kept pass over THE SHARE; builds within). One open question for the manager
(REVIEW-READY.md): the share condition is held on srp-kept; srp-bound's own pass over it at 8x8/1if is named owed to
#977. Nothing of this lane is running.
REVIEW READY posted: #969 issuecomment-7086009278 (text: REVIEW-READY.md).

Lane: `/data-2/milan/lanes/fix-969`, branch `pf-969-1` (pushed by the manager as `969-srp-kept-talkers`), from
`f863258d` (PR #971's reviewed head). Local commits only; nothing pushed.

## Findings and their fixes

| Finding | Fix | Evidence |
|---|---|---|
| R886-1-F1 / R885-1-F3 MAJOR: a stale kept count after a reset or a reclaim refuses an in-bound Talker | `count_kept` recounts when a binding changed (`SRP_KEPT_BOUND`), or when one counted or kept since may have ended and a block was returned since (`SRP_KEPT_PENDING`: one kept now, an unbound registration's end, a counted one left); `reset_interface` zeroes the count with the participants it destroys | both reviewers' probes and 3 new tests fail at `f863258d` and pass at the head, at 1x1 and 8x8, one and two interfaces (receipts/failing-first/) |
| R886-1-F2 / R885-1-F4 MINOR: the 8x8/1if campaign plants no early defect | `test_ctrl_firmware.run_srp_mutants` plants `srp_early_mutants.PREFIX` at 8x8/1if too; every SRP plant's result line names its shape | shard 3: 48 early-plant results, 16 a shape (receipts/firmware/early-plants-by-shape-ecd5bf41.txt) |
| R886-1-F3 / R885-1-F2 MINOR: memory docs state the old entries and plants | every line both reviewers list, with the final figures | docs workflow 99/103 (receipts/docs/) |
| R885-1-F1 MAJOR: the CPU budget evidence does not execute the changed paths | two groups in arm A at every point: `srp-kept` (the changed paths) and `srp-bound` (the bound path the base has, the same MRPDU with every input bound); `kept_grade.py` and `run.py` grade both as owed to #977 (the ruling), held at kept <= bound, no srp-kept pass over THE SHARE, every build pass within its stated cost | the STOP's measurement, then the ruling; the final same-image runs (gate table) |

## Design decision: where a reset zeroes the count

A reset destroys the participants with no indication (lwSRP `mrp_app_destroy`), so only `reset_interface` sees it.
`85e3f854` zeroed the count in `create_participants`, inlined into the hot `open_interface`: 130 hot functions moved.
Each way that leaves the hot list untouched is inexact or dearer: the 16-bit RX mark and a participant's address can
repeat across a reset; a held-table or registered-state look-up of the first kept one misses an unbinding's one-kind
registration (never held) and a Leave window (LV is not IN), each a registrar visit on every receive meanwhile. So
`reset_interface` zeroes it beside its release of the interface's held StreamIDs: it grows 16 B, the 152 hot functions
after it each start 16 B later, and nothing else in the hot section moves or changes size
(receipts/budget/hot-section-f02d44cd.txt; round 1's head moved none). The CPU budget runs measure that image.

## Changes (file:line at the final head, reason)

| Where | Reason |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c:32-36` `SRP_KEPT_BOUND`, `SRP_KEPT_PENDING` | what owes the next receive a count |
| `srp_mbx.c:290-294` `talker_changed` | an unbound registration's end may be a kept one's, freed later: pending |
| `srp_mbx.c:465-491` `keep_talker` | one kept now may never register (a Leave lwSRP creates it for, an allocation refused): pending |
| `srp_mbx.c:820` `srp_mbx_bind` | a binding change owes the count (the flag renamed) |
| `srp_mbx.c:934-955` `kept_visited` | a counted one whose Registrar left (MT) keeps the count pending until its block's return |
| `srp_mbx.c:957-977` `count_kept` | the trigger and the corrected invariant: the count a receive starts from is exactly the kept |
| `srp_mbx.c:1333-1339` `reset_interface` | the count zeroed with the destroyed participants |
| `srp_mbx.h:201-210` | `kept_due` replaces `kept_owed` (same size; `held` stays last), the invariant |
| `sw/firmware/ctrl/test/srp_mbx.cpp:2203-2226, 2350-2353, 2449-2564` | `every_input`, `expect_every_input_declares`; a refresh before the unbinding (so the unbinding alone owes the count); 7 tests |
| `srp_early_mutants.py`, `srp_mutants.py:985-988`, `test_ctrl_firmware.py:162, 228-236` | 5 plants of the count's triggers; the early plants at 8x8/1if; each line's shape |
| `tb/verilator/ctrl_service_budget/kept_window.py`, `kept_grade.py`, `scenario.py:993-998`, `run.py:907, 938, 982-984`, `README.md` | the srp-kept and srp-bound groups, the #977 disposition (kept_grade.Disposition) and its self-test; run.py's STATED and SHARE lines given it |
| `sw/firmware/ctrl/srp/README.md`, `plat/README.md`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py:10`, `sw/firmware/gtest/coverage.ratchet` | the count's exactness; the memory figures; 861/861 lines, 779/779 branches |

## New checks (planted mutant, failing words)

| Plant | Test | Failing words |
|---|---|---|
| feedback-early-reset-counted (reset_interface's zeroing removed) | SrpEarlyTalker.AResetLeavesNoKeptRegistrationCounted | after a reset, one vector of every input is kept whole |
| feedback-early-end-unowed (talker_changed's pending removed) | SrpEarlyTalker.AKeptRegistrationWhoseBlockIsFreedIsCountedNoMore | a kept one freed below the bound: one vector of every input is kept |
| feedback-early-unregistered-unowed (keep_talker's pending removed) | SrpEarlyTalker.AKeptLeaveOfAStreamNeverRegisteredIsCountedNoMoreOnceFreed | a Leave kept for a StreamID never registered |
| feedback-early-left-seen-unowed (kept_visited's pending removed) | SrpEarlyTalker.AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed | once its block is freed, another is kept |
| feedback-early-refresh-counted-again (R885's kept-unlisted: kept without listing) | SrpEarlyTalker.AKeptRegistrationRefreshedIsCountedOnce | a kept registration refreshed in one receive |
| feedback-early-freed-uncounted (re-anchored: the pending return condition false) | SrpEarlyTalker.AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed | once its block is freed, another is kept |
| feedback-early-unbinding-uncounted (re-anchored: `SRP_KEPT_BOUND` not set) | SrpEarlyTalker.AnUnboundRegistrationIsKeptAndCountedAgainstTheBound (a refresh added so that no pending masks it) | an unbound registration is kept and counted |
| kept_grade.py --selftest | a record one cycle past the unit; a probe with no record | (its own lines) |

## Gate table

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Failing first: new tests and both reviewers' probes, final adapter vs `f863258d`'s | tests `ecd5bf41`, adapter `f02d44cd` | final: 21 + 5 pass at 1x1/8x8 x 1/2if; `f863258d`: AResetLeaves..., AKeptRegistrationWhoseBlock..., AKeptLeaveOfAStreamNever... and both reviewers' reset/reclaim probes fail at every arm; the controls pass at both | receipts/failing-first-final/ (failing-first/ is the first run, superseded) |
| Firmware gate shard 0/4 (suites) | `5dba2089` (and `ecd5bf41`, `f02d44cd`) | PASS: 88 arms (the one commit since changes only kept_grade.py) | receipts/firmware/firmware-gate-5dba2089-shard0.log |
| Firmware gate shard 1/4 (control campaign) | `f02d44cd` (no arm it judges by reads what changed since) | PASS: 827 of 827 | receipts/firmware/firmware-gate-f02d44cd-shard1.log.gz |
| Firmware gate shard 2/4 (AECP campaign) | `f02d44cd` | PASS: 385 caught | receipts/firmware/firmware-gate-f02d44cd-shard2.log.gz |
| Firmware gate shard 3/4 (SRP campaigns) | `ecd5bf41` | PASS: 591 caught, 0 escaped; 48 early-plant results, 16 a shape (1x1 one and two interfaces, 8x8/1if) | receipts/firmware/firmware-gate-ecd5bf41-shard3.log.gz, early-plants-by-shape-ecd5bf41.txt |
| Shard 3 first run | `f02d44cd` | FAIL: feedback-early-reset-counted escaped at the three shapes (the test's admission left the count pending); fixed in `ecd5bf41` | receipts/firmware/firmware-gate-f02d44cd-shard3-FAILED-reset-plant-escaped.log.gz |
| fw_coverage --check | `f02d44cd`, `2bfa95b4`, `ecd5bf41` | PASS (40 files); srp_mbx.c 861/861, 779/782 raw (779/779 after 3 exclusions), in the ratchet | receipts/firmware/fw_coverage-check-*.log |
| plat_ledger + test_ctrl_memory | `f02d44cd`; memory test again at `dcd02916` | PASS (0 findings): 1x1/1if 45.5 (127,376 B rom), 1x1/2if 46 (128,984), 8x8/1if 58.5 (140,136), 8x8/2if 63.5 (141,720); the size fixture's 8x8/1if stand-in 56.0 (130,960 B of 131,072) | receipts/ledger/ |
| Hot section, base vs final | `f02d44cd` | 152 functions after reset_interface each 16 B later; reset_interface +16 B; nothing else | receipts/budget/hot-section-f02d44cd.txt |
| Twin, twin-plants, twin-maps, twin-maps-plants | `f02d44cd` | PASS: 0 findings, every plant caught | receipts/twin/ |
| Docs workflow, 103 commands | `e816c74d` (and `5dba2089`, `2bfa95b4`) | 99 PASS; the 4 CI-environment rows refuse as on the base | receipts/docs/docs-workflow-e816c74d.txt |
| flip_grade (1x1/1if, 8x8/1if), load_grade --check/--selftest, shape_costs --check, kept_grade --selftest, run.py --self-test | `5dba2089` (kept_grade --selftest at `e816c74d` too) | PASS on the stated figures; run.py --self-test 0 failures | receipts/budget/grader-*-5dba2089.txt, harness-selftest-run.py_--self-test-5dba2089.log.gz |
| CPU budget: srp-kept + srp-bound in one build at 1x1/1if and 8x8/1if (run.py --groups srp-kept,srp-bound), graded as owed to #977 | `5dba2089`; kept_grade at `e816c74d` | PASS: run.py exit 0 at both, every #977 line OWED with its link, no STATED or SHARE left; kept_grade PASS: kept <= bound (34,497 / 32,224 / 36,859 against 38,956; 137,352 / 68,692 / 142,909 against 153,208), no srp-kept pass over THE SHARE (worst 0.53 and 1.63 ms), builds within their stated costs; srp-bound's pass over THE SHARE at 8x8/1if (224,540 CPU cycles) named owed to #977 | receipts/budget/run-summary-5dba2089-*-srp-kept-srp-bound.txt, kept_grade-e816c74d-on-5dba2089-*.txt |
| CPU budget before the ruling: srp-kept + round 1's five groups (run.py), kept_grade | `f02d44cd` | the STOP's measurement: every srp-kept record over the unit; the five groups: the same 7 owed misses as the base, no work pass over the share | receipts/budget/run-summary-f02d44cd-*.txt, kept_grade-f02d44cd-*.txt, per-probe-base-vs-f02d44cd.txt |
| CPU budget, scratch: every input bound, then the same MRPDU | `2bfa95b4` scratch copy | FAIL as on the bound path: 38,956 (410 us) and 153,208 (1,610 us); run.py: an SRP record's apply over its stated cost, and at 8x8/1if a tier-2 slice of 157,372 over 147,500 | receipts/budget/srp-bound-scratch-*.txt |
| The unit restated by the rule, scratch | `2bfa95b4` scratch copy | 1x1/1if last 185.89 ms over 130 (and the owner's 140); 8x8/1if load 1.309 over 0.75; a 1,505 us record over the 1,475 us slice | receipts/budget/restated-unit-scratch.txt |
| Routes (#818 floor), ExtraPostPlacementOpt | `f02d44cd` | PASS: 1x1/1if worst WNS +0.128 / WHS +0.032 ns (81 of 135 BRAM tiles); 8x8/1if +0.096 / +0.036 ns (94.5 of 135); 0 routing errors; image identity PASS; the images' rom the ledger's | receipts/routes/ |

## Commits (one-line subjects, no body, no trailers)

| # | Commit | What |
|---|---|---|
| 18 | `85e3f854` | the kept count's triggers (pending), first with the reset in create_participants |
| 19 | `0af78f68` | tests: one receive of every input after a reset, a freed kept block, a kept Leave, a refresh; flood and UNBIND/BIND controls |
| 20 | `528ad178` | plants of the count's triggers, the early plants at 8x8/1if, each SRP plant's shape named |
| 21 | `1dde2d6f` | SRP README: the count's exactness |
| 22 | `40b15f49` | the CPU budget group srp-kept and kept_grade.py |
| 23 | `4c929e55` | the reset's zeroing moved to reset_interface (out of the hot open_interface) |
| 24 | `f02d44cd` | the reset plant re-anchored |
| 25 | `dcd02916` | memory docs: entries, planted ledgers, rom figures |
| 26 | `203433bc` | coverage ratchet: 861/861, 779/779 |
| 27 | `3685c0a5` | kept_grade.py --selftest |
| 28 | `2bfa95b4` | harness README: the srp-kept group |
| 29 | `ecd5bf41` | the reset test refreshes the kept one first, so only the reset's zeroing passes it |
| 30 | `33ae95f9` | srp-bound beside srp-kept; both graded as owed to #977 (kept_grade.Disposition, run.py) |
| 31 | `5dba2089` | harness README: srp-bound and the #977 disposition |
| 32 | `e816c74d` | kept_grade: a #977 group with no graded result is a finding (THE SHARE never left unchecked) |

REVIEW READY e816c74da53a5822f2ddc1661e5ffae297f1b3aa
