[A817] REVIEW READY
Commit: e816c74da53a5822f2ddc1661e5ffae297f1b3aa (branch `pf-969-1`, pushed as `969-srp-kept-talkers`, PR #971; round 2, answering R886-1 and R885-1 at `f863258d`, after the [A10] ruling on the round's STOP)

Changed:
- **R886-1-F1 / R885-1-F3 (MAJOR, the stale kept count).**
  - `count_kept` now counts again before a receive when a binding changed, or when one kept may have ended and a pool block was returned since. `SRP_KEPT_PENDING` is set by a Talker kept now, by an unbound registration's end, and by a counted one whose Registrar left.
  - `reset_interface` zeroes the count with the participants it destroys. A receive therefore starts from exactly the kept attributes, below the bound as at it. With nothing pending, a returned block owes no count.
  - The invariant comment and `srp/README.md` are corrected. The storage bound, bound StreamIDs' precedence, the filter's non-reentry and the unbound walk policy are unchanged.
  - The zeroing sits in the hot `reset_interface`, which grows 16 B, so the 152 hot functions after it each start 16 B later; nothing else in the hot section moves. Every alternative was inexact or put a registrar visit on every receive (HANDOFF's design note).
- **R886-1-F2 / R885-1-F4 (MINOR).** The 8x8/1if SRP campaign plants every early defect, and each SRP plant's result line names its shape.
- **R886-1-F3 / R885-1-F2 (MINOR).** Every memory-doc line both rounds list now states the ledger's figures.
- **R885-1-F1 (MAJOR, CPU budget), with the ruling's disposition.**
  - Two arm-A groups, in `kept_window.py`, run at every point: `srp-kept` runs the changed paths, and `srp-bound`, the bound path the base has, sends the same MRPDU with every input bound.
  - A record that registers more than one or two Talkers is past `CTRL_LOOP_SRP_UNIT_US` on both paths. That cost is owed to #977 (the [A10] ruling on #969, option 1), and nothing is restated.
  - `kept_grade.py` names each such record, and the bound group's walk, polls base and pass over THE SHARE, as `OWED #977` with the issue's link. `run.py` gives its STATED and SHARE lines the same disposition (`kept_grade.Disposition`).
  - Either one fails if a condition breaks: kept <= bound on the same image; no work pass of `srp-kept` over THE SHARE; every build pass of both within its stated cost; both groups graded together, every probe with its record. `kept_grade.py --selftest` plants each breach.

Validation:
- **Failing first:** the round's tests and both reviewers' probes, the final adapter against `f863258d`'s, at 1x1 and 8x8 with one and two interfaces. With the fix all 21 tests and the 5 external probes pass. At `f863258d`, the reset, freed-block and never-registered-Leave cases and both reviewers' reset and reclaim probes fail at every arm. The controls pass at both.
- **`test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4`:**
  - shard 0 PASS at `5dba2089` (88 arms; the one commit since changes only `kept_grade.py`);
  - shard 3 PASS at `ecd5bf41` (591 caught, 0 escaped; 48 early-plant results, 16 at each of 1x1 with one interface, 1x1 with two, and 8x8/1if);
  - shards 1 and 2 PASS at `f02d44cd` (827 of 827; 385 caught); nothing they read changed since.
  - Shard 3's first run at `f02d44cd` had 3 escapes, all `feedback-early-reset-counted`: its test's admission left the count pending. `ecd5bf41` refreshes first, so only the reset's zeroing passes it.
- **`fw_coverage.py --check`:** PASS at `ecd5bf41`; `srp_mbx.c` 861/861 lines and 779/779 branches, recorded in the ratchet.
- **`plat_ledger.py` and `test_ctrl_memory.py`:** PASS: 1x1/1if 45.5, 1x1/2if 46, 8x8/1if 58.5, 8x8/2if 63.5 RAMB36. The size fixture's 8x8/1if stand-in is 56.0 (130,960 B of 131,072).
- **Twin, twin-plants, twin-maps, twin-maps-plants:** PASS at `f02d44cd` (0 findings).
- **CPU budget, `run.py --groups srp-kept,srp-bound` at 1x1/1if and 8x8/1if (each in one build at `5dba2089`):** exit 0, every #977 line printed `OWED` with its link. `kept_grade.py` (final head) PASS at both:
  - kept <= bound: 34,497 / 32,224 / 36,859 against 38,956 at 1x1/1if; 137,352 / 68,692 / 142,909 against 153,208 at 8x8/1if;
  - no `srp-kept` pass over THE SHARE (worst 0.53 and 1.63 ms);
  - build passes within their stated cost (`srp-kept` 39,123 of 73,500 and 82,768 of 147,500).
  - Round 1's five groups at `f02d44cd`: the base's same 7 owed backlog-owed misses, no work pass over the share.
- **Harness self-tests and graders:** `run.py --self-test` 0 failures (`5dba2089`); `kept_grade.py --selftest` PASS; `load_grade.py --selftest` 28 of 28.
- **Stated-figure graders:** `flip_grade.py --check` (1x1/1if, 8x8/1if), `load_grade.py --check` and `shape_costs.py --check` PASS (last 127.31/130 ms, ACMP 29.06/30, txL 47.88/49; 8x8/1if load 0.744/0.75, THE TRANSMIT 76.81/77).
- **Docs workflow, 103 commands:** 99 PASS at the final head; the 4 rows that need the CI environment refuse as on the base.
- **Routes (firmware final, `f02d44cd`; the gating recipe's ExtraPostPlacementOpt):** #818's floor met at every corner, worst WNS/WHS +0.128/+0.032 ns at 1x1/1if and +0.096/+0.036 ns at 8x8/1if; image identity PASS.

Acceptance criteria:
- A binding made or restored while the Talker is registered declares its Listener within one transmit of the probe's success, after a power-on settle and after a bind while bound, at 8x8/1if and 1x1/1if, on every STREAM_INPUT: met on the host model, as in round 1 (`Early.S13`, `Early.S14`, `SrpEarlyTalker`). Round 2 adds one receive of every input's Talker after a reset or a freed kept block, which is kept whole. The bench re-run is the manager's.
- A host test covers both orders, with a planted defect for each: met. 16 early plants, at 1x1 with one and two interfaces and at 8x8/1if, plus `early-talker-ignored` in the control campaign.
- REGISTERING / REGISTERING_FAILED in GET_STREAM_INFO follow: met (S13).

Open risks/questions:
- **The share condition.** The ruling says "no pass over THE SHARE". The grader holds it on `srp-kept`, the change under review: no work pass over it at either point (worst 0.53 ms and 1.63 ms). `srp-bound`, the bound path the base has, has one pass over it at 8x8/1if (224,540 CPU cycles, 2.245 ms: the bound path's registrations and ACMP's response to them), which the grader names as owed to #977, not held. If the condition was meant for the bound reference too, it needs #977's fix first. Please say if that reading is wrong.
- The size fixture's 8x8/1if stand-in has 112 B of `rom` left within 56 RAMB36.
- The CPU budget was re-measured on the two #977 groups and round 1's five groups at both points, not on every group. The hot section's 16 B shift after `reset_interface` is measured only there.
- The bench re-run after merge is the physical check; there was no bench access here.
