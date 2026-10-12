[R628] NEGATIVE - exact head e7d604faa0472d505d6459883b382c2b237ad06d

# R628-5: internal cleared-context review of issue #726 / PR #729

Head `e7d604faa0472d505d6459883b382c2b237ad06d`, tree
`641f45e32b484bb1da1d34379d5e19f0588f52b3`, source base `c6bd08c6`. This is a
full review of the PR plus the round 2-5 deltas. I wrote the verdict and the
ledger after my own pass over the diff and before reading any prior review
report. Prior findings are resolved or retained in the last table.

**Verdict basis.** One MINOR is open: R628-5-F1 (Tests). The parent-path
refresh check allows `1000 ms + service`, but "service" is measured in the
same run, so any delay after eligibility raises its own bound. Two disposable
plants with 1.9 s and 2.0 s refresh gaps both print `RESULT: PASS`. This
finding supersedes my own R628-4-S4 (an optional suggestion) on the strength
of these new escapes.

Conformance, RTL, Robustness and Docs are clean at this head. Six wording
items are recorded as RESIDUE, and four optional suggestions are carried.

## Findings

### R628-5-F1 - MINOR - Tests

**Where**
- `tb/verilator/milan_dp/stream_counters.hpp:72-73`: the fixture opens a
  service window when the DUT's dirty bit is set and its own stamp is at
  least 1000 ms old.
- `:61`: it records the largest open-to-MAC-tail time per descriptor.
- `:239` and `:190`: that same-run maximum becomes the refresh allowance,
  `max_gap <= 1000 ms + service_max`.
- `docs/testing/726_STREAM_COUNTERS.md:61-62` describes this bound.

**Authority and evidence**
- Assignment 6125784157 item 4 requires a standing check with a plant for "a
  changed counter goes unnotified for more than 1 s".
- Corrected ruling 6132483068 bounds every gap by 1000 ms plus the measured
  service delay. Ruling 6126028604 says what that delay was meant to be: the
  2 ms completion delay A605 measured, not an open-ended allowance.
- Here, any lateness after eligibility is booked as "service" and widens the
  bound by the same amount. Two disposable plants show this (script
  `scripts/probe_counters.py`, receipts `receipts/probes/`):
  - `sched-2000`, shape 8: a scratch copy of the processor scheduler waits
    2000 ms instead of 1000 ms. Every gap is about 2001 ms, the booked
    service is about 1001.7 ms, and the run prints `RESULT: PASS`
    (`probe_sched-2000_8.run.log`, GAPS lines). `sched-1600` at shape 1 also
    passes.
  - `egress-stall`, shapes 1 and 8: the parent's own control egress
    (`milan_datapath.sv`, scratch copy, ahead of `ctl_tx_mux`) holds a
    processor frame for 900 ms during the measurement. Gaps reach 1900.66 ms,
    the booked service is about 902 ms, and both shapes print
    `RESULT: PASS` with zero failures (`probe_egress-stall*.run.log`).
- Mitigation for one cause: the processor's own `aecp_notify` bench (section
  TW) catches the scheduler-constant plant. TW1, TW2 and DR3 fail, while the
  clean copy gives 45/45 (`receipts/procnotify_ppn_*.log`).
- No such check exists for the parent's own path between the processor's job
  and the MAC. That path is what this fixture measures end to end, and only
  this fixture streams every output at once while notifications run.

**Impact.** The #726 symptom, counters not refreshing every second, can come
back through a parent-side delay after eligibility, and the standing check
stays green. The published figures (3.263 / 14.058 ms service) are correct
today, but nothing enforces them.

**Required outcome.** The refresh grade must not be satisfiable by unbounded
lateness after eligibility. Either:
- bound the allowance beyond 1000 ms by a ceiling the run under test cannot
  raise, stated in the document (for example the measured maxima with a
  stated margin), and add a standing plant that delays notifications after
  eligibility in the parent path; it must fail `CADENCE` by name and escape
  with that check omitted; or
- the manager records a decision that lateness after eligibility is outside
  this check, and `726_STREAM_COUNTERS.md` states that limit.

**Verification.** At both shapes, re-run
`python3 -I scripts/probe_counters.py <checkout> egress-stall <shape> <work>`.
It must report a `CADENCE` failure. The four clean `make counters` legs must
still pass. The new plant must detect by name and escape when omitted.

### RESIDUE (wording only; each changes no test, figure, verdict or code behavior)

**R628-5-R1** (Docs, Tests): `tb/verilator/avtp_rxmon/sim_main_nx.cpp:548-549`
(block comment above `[IV]`) still says N events "move each of the seven
interval counters by EXACTLY 1". This is the same stale claim R629-4-F01
fixed in the IV8 printf. Exact fix: replace "each of the seven interval
counters" with "each of the six anomaly interval counters (FRAMES_RX counts
each accepted AVTPDU and may publish in a batch)".

**R628-5-R2** (Docs, Tests): `tb/verilator/crf_rx/sim_main.cpp:98`, "all
seven interval tallies are 32-bit WRAPPING". Exact fix: "all seven tallies
(FRAMES_RX per AVTPDU, six interval anomaly counters) are 32-bit WRAPPING".

**R628-5-R3** (Docs, RTL): the port comment at
`hdl/ieee1722/aaf/KL_aaf_packetizer.sv:181-184` (pre-existing, outside the
diff) still says "FRAMES_TX and the tu-qualified TIMESTAMP_UNCERTAIN are
per-OBSERVATION-INTERVAL counts". Ruling 6125741685 asks for such design
notes to follow the ruling. Exact fix: "FRAMES_TX counts each transmitted
PDU (#726) and the tu-qualified TIMESTAMP_UNCERTAIN is a
per-OBSERVATION-INTERVAL count over TRANSMITTED PDUs, so they need the
emission event, not a total".

**R628-5-R4** (Docs): `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:397-398`,
"including a healthy `FRAMES_TX` interval". Exact fix: append "(each
transmitted AVTPDU since #726; see the B4 correction)" after "interval".

**R628-5-R5** (Tests, Docs): `tests/features/counters_contract_milan.feature:396,418`
use the tag `@clause:17221-Table-7.157`, but `:92,183,197` spell it
`@clause:17221-Table-7-157`. No script, step or workflow reads clause tags.
Exact fix: spell both as `@clause:17221-Table-7-157`.

**R628-5-R6** (Docs): the PR body's Status says "Focused local validation
passes; two new commits await publication." The head is now published.
Exact fix: "Focused local validation passes; both commits are published at
this head."

### SUGGESTION (optional; no effect on coverage)

**R628-5-S1** (Tests; carried from R628-4-S1, not taken). The per-engine
plants are not in `counters-mutants`. My `aaf-guard`, `crf-guard` and
`aaf-rx-interval` plants were again detected (CADENCE 2, CADENCE 2, RX 2 at
shape 1; `aaf-guard` CADENCE 16 at shape 8 frames-only). Adding them would
make per-engine coverage standing.

**R628-5-S2** (RTL, Robustness; carried from R628-1-S1, R628-2-S3, R628-3-S1
and R628-4-S2). `hdl/ieee1722/crf/KL_crf_rx.sv:487-490` against `:644-689`:
a CRF PDU accepted in the exact bind-rise cycle is wiped from the new era.
The ordering is stated in the source, and the loss is at most one packet per
bind.

**R628-5-S3** (Tests; carried from R628-4-S3). `tb/verilator/milan_dp/sim_nxn.cpp:2596`:
the `10000000L` silence bound assumes the fixture's clock.

**R628-5-S4** (Tests, merge-turn bench tool). `tb/tools/torture_campaign.py:754-758`:
`snapshot_skew_frames` is 8000, one second at class A. It is the default
tolerance for `interval_ticks_agree`, which compares a DUT FRAMES_RX delta
with a FRAMES_TX delta. The DUT's coalesced publication can lag by up to one
interval at each snapshot, on top of the documented read skew of up to about
1 s, so the bench comparison could report a false packet-total FAIL.
Optional: allow publication lag separately, or document the read discipline
that keeps the combined skew under the tolerance.

## Clean-lens lines

[R628] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:192-262`, `hdl/ieee1722/crf/KL_crf_rx.sv:484-520,644-689`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:329-330,640-643,943-955,983-984,1154-1176`, `hdl/milan/milan_datapath.sv:3156-3171,3300-3322,7924-7995` (unchanged), `receipts/run_shape{1,8}_{uncertain,frames}.log`, issue #726 acceptance 1, 2 and 4, assignment 6125784157, rulings 6125741685, 6125845117, 6126028604 and 6132483068.
- **Counter law.** FRAMES_TX counts per AVTPDU on every output, AAF and CRF (the CRF strobe is deferred one cycle, never dropped). It wraps at 32 bits and resets at each talker start, keeping a PDU that completes in the start cycle.
- **Wire match.** FRAMES_TX equals the MAC count on every output: 799/101 at shipping, 800×8/101 at the largest shape.
- **FRAMES_RX.** It counts per AVTPDU: AAF through a 32-bit coalesced batch, CRF immediately. It resets on not-bound to bound and survives unbind (500 per input; RX_RESET checks).
- **Unchanged laws.** MEDIA_RESET and TIMESTAMP_UNCERTAIN keep their interval law.
- **Refresh.** Every changed Stream Input/Output marks itself dirty, and the unchanged scheduler is the only limit. `milan_datapath.sv` is not in the diff, so the AVB_INTERFACE #60 throttle (`ctr_avb_dirty_w`) is untouched.
- **Measured cadence.** Spacing is at least 1000 ms. Every consecutive gap and the final wait are within 1000 ms plus the measured service. Shipping: 28 gaps, 1001.000-1001.867 ms, service 3.263 ms. Largest: 126 gaps, 1000.982-1012.029 ms, service 14.058 ms. Both match the document; the method weakness is F1 (Tests).
- **Firmware.** There is no firmware implementation change (only `sw/firmware/ctrl/aecp/README.md`), so no capture re-measure is owed.
- **Bench.** Acceptance item 3 and the reference-peer reset comparison belong to the merge turn.

[R628] PASS RTL - the RTL lines above, `git ls-tree -r` gitlinks at base and head (identical), `scripts/lint_rtl.py --check` (90 <= 90), and the public routed receipts at `727f2928:review-evidence/726-r1/author-r2/evidence/` (`alinx_ax7101_utilization_route.rpt`: 49,427 LUT, 53,378 FF, 87.5 BRAM; route status 0 errors; the Slow_85C and Fast_0C negative-slack reports read "No timing paths found").
- Every new register is reset, and `frx_acc_r`/`frx_add_r` are 32 bits wide with no truncation at `:642-643`.
- At the talker start edge, the later nonblocking assignment correctly overrides the per-PDU increment.
- Per-PDU dirty pulses coalesce in the root arbiter's sticky pending bits and the processor's `ctr_dirty_r`.
- No CDC is added.
- Since `acadfacd` (the routed image), `hdl` has changed only in comments, so the published area applies. The author reports +35 LUT, under the +200 STOP bound; I did not rebuild the base image.

[R628] PASS Robustness - `stream_counters.hpp:256-322` (bind, unbind and rebind; start, stop and restart; near-wrap; the 65,534+3 batch), `receipts/shift/` (starts 0-1,000,000 cycles pass at both shapes; 1,000,001 is refused by name), `receipts/makeflags_w_shape1.log` (inherited ` -w` passes), and these disposable plants:
- `aaf-acc-bind` (the bind wipe keeps the old batch) escapes the parent fixture but fails the receive suite (`[M13e2]`, "new sid counts"; `receipts/rxmon_accbind.log`).
- `tx-start-drop` escapes the parent fixture but fails tkdiag T11 (`receipts/tkdiag_startdrop.log`).
- Each removed CRF retained reset (`pdu_count_o`, `seq_err_o`, `iv_tu_r`) fails the unchanged R629-1 contract.

[R628] PASS Docs - `docs/testing/726_STREAM_COUNTERS.md`, `docs/reference/REGISTER_MAP.md:145-153,866-872,919,963`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218-235`, `sw/firmware/ctrl/aecp/README.md:52-66`, the five dated findings notes, the `docs/history` link pinned to `c6bd08c6`, `tb/verilator/milan_dp/README.md` (round 5 `run` paragraph, `[F]` and the FRAMES_TX section), `docs/README.md`, the design notes in the four RTL files, and the PR body.
- They state the ruling, both resets, the corrected two-condition cadence criterion and the measured figures.
- Every figure I re-measured matches.
- The docs gates return 0 (`receipts/docs_gates.tsv`, 29 commands).
- Only RESIDUE R1-R6 remain.

Tests (UNCLEAN, R628-5-F1) was applied to:
- `stream_counters.{py,hpp}`, `stream_counter_f5.{py,cpp}`, the Makefile targets, and the tkdiag, crf_rx, avtp_rxmon (including the lockstep superset rule) and `sim_nxn`/`sim_crf_licence` diffs;
- the feature, the steps and `torture_campaign.py`.

Results:
- All 13 shipped plants fail by name and escape with only their group omitted.
- `before` gives 12 and 54 failures in exactly TX/RX/CADENCE.
- A planted pre-#726 FRAMES_RX law in the grader fails 6 named scenarios.
- Behave: 406 scenarios / 1,977 steps. The torture self-test runs 80 tests.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | RTL lines and rulings above; 4 clean parent runs; F5 shapes 1/8 | R628-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| RTL | CLEAN | four counter RTL files, datapath feed and arbiter, gitlinks, lint ratchet, routed receipts | R628-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Robustness | CLEAN | reset, wrap, batch boundary, bind-era, start-edge, shift and make-flag probes | R628-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Tests | UNCLEAN (R628-5-F1 MINOR) | 13 shipped plants, 2 baselines, 11 reviewer plants, 3 unit suites, behave, grader plant, prior probes | R628-5 | e7d604faa0472d505d6459883b382c2b237ad06d |
| Docs | CLEAN (RESIDUE R1-R6 only) | documents listed above; 29 docs and lint gates | R628-5 | e7d604faa0472d505d6459883b382c2b237ad06d |

## Round-specific checks (rounds 2-5)

| Item | Result at this head |
|---|---|
| R2: R629-1 `reproduce_contract.py` (blob `0c47cf07`, unchanged) | rc 0. Deleting the CRF bind wipe of `pdu_count_o`, `seq_err_o` or `iv_tu_r` gives rc 1 each, with the source restored byte-identical (`receipts/prior_probes/`). |
| R2: BDD gate | `python3 -m behave --no-capture -f plain`: 406 passed, 0 failed (`receipts/behave_all.log`). Hosted `bdd-conformance` succeeded at this head. |
| R2: output cadence, frames-only | Both shapes rc 0 (70 / 301 checks). OUTPUT_CONDITION rows show TU=MR=0, one start, no stop, and clear wire tu/mr. `tx-nodirty` fails OUTPUT_CADENCE (4) and escapes. |
| R2: law table, trap (3), grader | Table 7.157 per AVTPDU. The interval-rate FAIL scenario passes. Planting the old law fails 6 scenarios (`receipts/probe_grader_law.log`). |
| R3: docs workflow gates | 29 commands rc 0, including `measure_naming --check` (95 recorded), `measure_test_evidence --check`, `check_py_idiom` and `check_cpp_idiom`. The only budget-adjacent file changed is the reader-disposition entry. |
| R3: R628-2 `probe_xside_law.py` (blob `991835aa`) | Ruled 32000/32000 gives PASS. 4/32000 gives FAIL against the talker. 4/4 gives FAIL with one finding per side. |
| R3: R629-2 `probe_snapshot.py` (blob `b0f7cd04`) | Before publication 3/0/0 is INFO with `ratio: null`. After publication 3 is PASS. rc 0. |
| R4: inherited `-w` and recursive target | `MAKEFLAGS=" -w" ... --shape 1` rc 0. `make -C tb/verilator/milan_dp counters` rc 0 with four `RESULT: PASS`. |
| R4: shift invariance | 0, 200, 300, 800, 900 and 1,000,000 cycles pass at both shapes. 1,000,001 fails by name. `fixed-grid` fails PHASE (8) and escapes. |
| R4: texts | `726_STREAM_COUNTERS.md`, the audit `:218-235` and the PR body state spacing plus the consecutive-gap bound. No grid or startup exclusion remains in the grader. |
| R5: IV8 text and receive regression | `make run lockstep`: 97 single-sink, 119 NxN, 36+36 lockstep checks, 0 failures. IV1 publishes 9 to 15 (+6). IV2/3/4/6/8 bursts are +1. The IV8 text no longer lists FRX. |
| R5: R628-4-R1/R2, no assertion or RTL change | Applied. `1add0cfb..e7d604fa` changes one printf and the suite README only. |

## Prior findings at this head

| Prior finding | Disposition |
|---|---|
| R628-1-F1 = R629-1-F01 (MAJOR, Tests) | Resolved. The contract passes, and each retained-reset removal fails. |
| R628-1-F2, F3, F4 (MINOR) | Resolved. Frames-only legs and OUTPUT_CADENCE plant; README passages current; law table and grader per Table 7.157. |
| R629-1-F02 (RESIDUE) | Resolved. The sentence is absent from the PR body. |
| R628-2-F1 (MAJOR, docs workflow) | Resolved locally: 29 gates rc 0, no budget raised, `dirty_p_o` unit stated at `KL_avtp_rx_monitor_ctx.sv:187`. Hosted `docs-check` at this head was in progress when I checked (see limits). |
| R628-2-F2 (MINOR) | Resolved. `probe_xside_law.py` as above. |
| R629-2-F01 (MINOR) | Resolved. `probe_snapshot.py` as above; the standing scenario is at feature `:197-204`. |
| R628-3-F1 (MAJOR) | Resolved under ruling 6132483068: consecutive-gap grading, shift invariance, fixed-grid control. The service-bound weakness is the new, separate F1 above. |
| R628-3-F2 (BLOCKER) | Resolved in source; the local reproductions pass. Hosted shard 4/5 at this head was in progress when I checked. It succeeded at `1add0cfb` per ruling 6133625608, and nothing that shard runs changed since except printf text. |
| R629-3-R01, R628-3-R1, R628-2 RS1-RS5 | Resolved. The cited wording is present. |
| R629-4-F01 (MINOR) | Resolved. The IV8 printf is corrected and the receive regression passes. The same stale "seven interval counters" remains in the block comment at `sim_main_nx.cpp:548-549` (RESIDUE R1). |
| R628-4-R1, R628-4-R2 (RESIDUE) | Resolved as their exact fixes stated. |
| R628-4-S1, S2, S3 (SUGGESTION) | Not taken; carried as R628-5-S1, S2, S3. |
| R628-4-S4 (SUGGESTION) | Superseded by R628-5-F1 (MINOR) on demonstrated escapes. |
| R629-4 retained R628-2-F1 / R628-3-F2 pending hosted | Settled at `1add0cfb` by ruling 6133625608. At this head, see limits. |

## Evidence index

- **Toolchain.** Pinned Verilator 5.050 (`receipts/verilator_version.txt`: version string and wrapper sha256); CPython 3.14 for the host runs.
- **Clean parent runs.** `receipts/make_counters.log`, `makeflags_w_shape1.log` and `run_shape{1,8}_{uncertain,frames}.log`. `gap_summary.txt` is produced by `scripts/summarize_gaps.py`.
- **F5 mailbox fixture.** `receipts/f5_shape{1,8}.log` and `f5_mut_{late,rate,fixed-grid}.log`.
- **Shipped plants.** `receipts/mut_*.log` and `receipts/mutants/<variant>/{run,escape}.log`; baselines in `receipts/mutants/before_{1,8}.run.log`.
- **Reviewer plants.** `scripts/probe_counters.py` and `receipts/probes/*.run.log`, plus the processor bench pair `receipts/procnotify_ppn_{clean,plant}.log`.
- **Unit suites.** `receipts/rxmon_clean.log`, `crf_rx_clean.log`, `tkdiag_clean.log`, `tkdiag_startdrop.log` and `rxmon_accbind.log`.
- **Behave and grader.** `receipts/behave_all.log`, `torture_selftest.log`, `probe_grader_law.log` (`scripts/probe_grader.sh`) and `prior_probes/`.
- **Gates.** `receipts/docs_gates.tsv` (`scripts/docs_gates.sh`).
- **Hosted.** `receipts/hosted_checks_e7d604fa.tsv` and `hosted_runs_e7d604fa.tsv`.

All scripts take the checkout and work paths as arguments. Every probe copy
lives under the packet's scratch directory. At the end, the clone was
verified at the exact head with a clean status, the tracked index unchanged
and identical gitlinks (`receipts/final_tree_check.txt`).

## Real limits

- I did not wait for the hosted run at this head to finish. At my last poll
  (2026-10-12 22:47 UTC; `receipts/hosted_checks_e7d604fa.tsv`), Verilator
  shards 0/5 through 4/5, `docs-check`, `elaborate` and `publication-census`
  were still in progress. These had succeeded: Yosys shards 0/4 through 3/4,
  `full-ci-gate`, `yosys-elaboration`, `verilator-lint`, `bdd-conformance`,
  `docs-check-no-git`, `wire-accountability`, `changes`, `firmware-unit`,
  and the three firmware mutant jobs. The physical gPTP context is skipped
  by design.
- The crf_rx suite's default target completed (14,287 + 2,201 discontinuity
  + 10 mutant + 69 talker-step checks, 0 failures; `receipts/crf_rx_clean.log`).
  I did not run the `sim_nxn` integration legs (`obj_notify`,
  `obj_crflic`, and so on), the full parent, processor, gPTP or Yosys banks,
  the builder, or any Vivado run. Area and timing are read from the
  author's public receipts at the round-1 RTL, which has changed only in
  comments since.
- Physical calibration was NOT RUN. Simulation runs at compressed protocol
  time (1000 cycles per ms) with two recipients. This is not physical
  timing, maximum fanout or hardware proof.
- No manager source bank ran at this head, and I claim none.

## Pending manager duties

- Carry R628-5-F1 to the author. Decide whether the parent-path
  service-allowance ceiling is required, or whether its limit is recorded
  as out of scope.
- Carry R628-5-R1 to R6 to the residue checklist.
- Confirm hosted `docs-check`, `rtl-fast`, `elaborate` and `rtl-full`
  (Verilator shard 4/5 with the four counters `RESULT: PASS` in
  `suite-logs-4`) at this head, and the remaining required contexts.
- At the merge turn: build the current-dev candidate (source base
  `c6bd08c6`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`) with the
  builder and native banks, then run the bench check (acceptance item 3 and
  the reference-peer per-second deltas on both stream directions).

R628-5 FINISHED
