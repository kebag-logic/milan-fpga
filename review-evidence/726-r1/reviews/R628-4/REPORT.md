[R628] POSITIVE - exact head 1add0cfbcc778c5292a5935631ca7b47c612b990

# R628-4: internal cleared-context review of PR #729 (issue #726)

Reviewed head `1add0cfbcc778c5292a5935631ca7b47c612b990`, tree `11896ba0ce355e92ac33c444fb8b0f4aeb14554b`, source base `c6bd08c6`. Full diff `c6bd08c6..1add0cfb` (14 commits, 32 files); round 4 delta `e893e4d1..1add0cfb` (2 commits, 10 files).

**Result.** All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR is open. Two wording-only RESIDUE items and four optional SUGGESTIONs are recorded.

- R628-3-F2 (BLOCKER) is resolved:
  - Both required local commands pass.
  - The hosted Verilator shard 4/5 succeeded at this head.
  - Its `suite-logs-4` artifact carries all four counters legs' `RESULT: PASS`.
- R628-3-F1 (MAJOR) is resolved under the corrected cadence ruling [6132483068](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6132483068):
  - The fixture grades spacing and every consecutive gap from the first notification.
  - No fixed grid and no startup exclusion remain.
  - The verdict is invariant when the measurement start moves through one second. The fixture checks this exhaustively, my independent re-grade confirms it, and R628-3's shift runner confirms it unchanged.

This is a source verdict. It is not merge authorization, it is not candidate-merge validation, and it is not bench acceptance.

## Reconstruction

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md (sections 3, 5 and 6).
2. `docs/README.md`.
3. The issue #726 body (frozen acceptance items 1-4) and every maintainer and manager comment:
   - counter ruling 6125741685 and addendum 6125845117 (1722.1 decides where Milan is ambiguous);
   - assignment 6125784157, with its STOP bounds: a submodule change, more than +200 LUT, a timing or capture miss;
   - STOP ruling 6126028604 (no processor change);
   - rounds 2-4: 6129163001, 6131008329, and 6132483068, which corrects the cadence criterion;
   - the author's TAKEN, STOP and REVIEW READY comments.
4. The PR body at this head.
5. `git diff c6bd08c6..1add0cfb` and its history. The RTL, the datapath arbiter (`hdl/milan/milan_datapath.sv:3156-3171,3300-3322,7915-7995`) and the unchanged processor scheduler (`protocol-processor/hdl/aecp/KL_aecp_notify.sv:1098-1105,1444-1449`) were read for context.
6. Public evidence at `907f0116:review-evidence/726-r1/author-r4`, including the routed-area receipts.

I wrote my independent findings and ledger draft (`receipts/INDEPENDENT-DRAFT.md`) before I read any prior review text. Only after that did I read the prior findings (R628-1..3, R629-1..3) and fetch their probes.

## Executed evidence (this round, this head)

All builds used the pinned simulator 5.050 (`receipts/restore_and_identity.txt`), with at most 16 jobs. Every plant ran on a scratch copy.

| Campaign | Result | Receipt |
|---|---|---|
| `MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1` | rc 0, `RESULT: PASS` | `logs/inherited_w.log` |
| `make -C tb/verilator/milan_dp counters` from the repository root | rc 0; four legs print `RESULT: PASS` (shape 1 and 8, `uncertain` and `frames-only`) | `logs/counters_target.log` |
| Retained-log clean runs | 58 / 247 checks (`uncertain`) and 70 / 301 (`frames-only`), all 0 failures. FRAMES_TX equals the MAC census on every output: AAF 799/800, CRF 101. `frames-only` keeps TU/MR counters, the wire tu/mr bits and stops at 0, with one start | `receipts/runs/{clean,fo}_{1,8}/run.log` |
| Independent re-grade (`scripts/regrade_gaps.py`, my own code) | Every row passes spacing, refresh and the final wait. Shipping: 28 gaps, 1001.000-1001.867 ms, service at most 3.263 ms. Largest: 126 gaps, 1000.982-1012.029 ms, service at most 14.058 ms. The fixture's GAPS lines agree. Shifting the start through one second never changes a verdict | `receipts/regrade_*.txt` |
| `before` baseline (c6bd08c6 engines) | Shape 1: 12 failures; shape 8: 54. All are named TX, RX or CADENCE. Inputs get one notification, then about 4 s of silence; baseline FRAMES_TX is 5 against 799/800/101 | `receipts/runs/before_{1,8}/run.log` |
| The ten shipped parent plants | Each fails only its named group, then passes (rc 0) with only that group omitted. tx-interval 6 TX; rx-interval 1 RX; tx-reset 4 TX_RESET; aaf-reset 1 and crf-reset 1 RX_RESET; rx-saturation 1 RX; late 4 CADENCE; rate 8 RATE; tx-nodirty 4 OUTPUT_CADENCE (`frames-only`); fixed-grid 8 PHASE | `logs/mut_*.log`, `receipts/runs/mut_*/` |
| Mailbox (F5) path | Shapes 1 and 8: rc 0, gaps 1000-1002 ms. Plants: late 8 `[F5 CADENCE]`, rate 8 `[F5 RATE]`, fixed-grid 8 `[F5 PHASE]`; each omission escape rc 0 | `logs/f5_*.log`, `logs/f5mut_*.log`, `receipts/runs/f5*` |
| Reviewer plants (`scripts/own_plants.py`, through the PR's own detection and escape rule) | All escape with only their group omitted: AAF FRAMES_RX +1 per occupied interval gives 2 RX failures; restoring only the AAF engine's two pre-#726 healthy-dirty guards gives 2 CADENCE; dropping only the CRF per-AVTPDU dirty pulse gives 2 CADENCE; FRAMES_TX saturating at 0xFFFFFFFF gives 2 TX | `logs/own_*.log`, `receipts/runs/own_*/` |
| Measurement-start shift on the built clean models (`COUNTERS_WINDOW_SHIFT`) | Shape 1 at 1, 999, 500000, 999999 and 1000000 cycles: PASS. Shape 8 at 1, 999999 and 1000000: PASS. 1000001 is refused by name (`measurement start is within one second`) | `receipts/runs/shift{1,8}_*.log` |
| R628-3 `run_shift.sh`, unchanged (blob `6640d95e`) | 0, 200, 300, 800 and 900 µs at both shapes: PASS. Its `probe_fixture_instrumentation.diff` no longer applies (hunk 1 fails) because the fixture now prints NOTE and implements the start shift natively | `receipts/runs/rshift*.log`, `receipts/prior_probes/instrumentation_dryrun.txt` |
| R629-1 `reproduce_contract.py`, unchanged (blob `0c47cf07`) | rc 0. The bind-era scenario fails (rc 1) when I separately delete the CRF wipe of SEQ_NUM_MISMATCH, of FRAMES_RX, or of the TU seen flag. Each deletion was restored immediately | `logs/prior_reproduce_contract.log`, `logs/retained_reset_mutation.log` |
| R628-2 `probe_xside_law.py`, unchanged (blob `991835aa`) | Ruled pair 32000/32000: PASS with no findings. 4/32000: FAIL, with the finding against the talker. 4/4: FAIL, one finding per side. Stream sources are accepted | `logs/prior_probe_xside_law.log` |
| R629-2 `probe_snapshot.py`, unchanged (blob `b0f7cd04`) | Before publication, TV=3, TNV=0, FRAMES_RX=0 gives INFO with `ratio: null` and no division by zero. After publication, 3 gives PASS | `logs/prior_probe_snapshot.log`, `receipts/prior_probes/snapshot-rtl.log` |
| Behaviour gate `cd tests && python3 -m behave --no-capture -f plain` | 14 features, 406 scenarios, 1,977 steps; 0 failed or skipped | `logs/behave.log` |
| Grader `tb/tools/torture_campaign.py --self-test` | 80 tests OK | `logs/torture_selftest.log` |
| Unit suites | tkdiag: 99/0, plus 5/5 mutants. avtp_rxmon: 97/0; NxN 119/0; lockstep N=1 and N=8 36/0 each; lockstep mutants 5/5. crf_rx: 14,287/0; discontinuity 2,201/0; talker_step 69/0; mutants 10/0 | `logs/unit_*.log` |
| Documentation and source gates (34 commands, `scripts/docs_gates.sh`) | All rc 0. These include: `docs_check`; `check_em_dash --base c6bd08c6`; `check_doc_style`; the `gen_toc` checks; `check_doc_paths`; `measure_naming --check`/`--selftest`; `measure_test_evidence --check`/`--selftest`; the py, cpp, sv and sh idiom gates; `check_hygiene --check`; `measure_fail_fast --check`; `check_port_contracts`; `check_todo_ownership`; `check_nvm_capture`; `check_soc_sources`; `check_rtl_source_lists`; `pp_srcs --check --selftest`; `lint_rtl --check`; `git diff --check c6bd08c6 HEAD`. The only `scripts/` file the PR changes is `measure_test_evidence_readers.py`, so no budget was raised | `logs/docs_gates.log` |
| Hosted, exact head | Verilator shard 4/5: success (run 38311301025, job 115017606642, merge ref `fb261fdb` = head into `dc4d06cb`). `suite-logs-4` (zip sha256 `ce8ade11…`, equal to the artifact digest) shows `make counters` with four `RESULT: PASS` lines and no `RESULT: FAIL` anywhere in `milan_dp.log`. Also success: docs-check, docs-check-no-git, bdd-conformance, rtl-fast, verilator-lint, `elaborate`, yosys-elaboration, Yosys shards 0-3, the firmware jobs, publication-census, and Verilator shards 0 and 3. Verilator shards 1/5 and 2/5 were still running at 22:12Z | `receipts/hosted_shard4_counters_excerpt.txt`, `receipts/hosted_checks_final.tsv` |
| Area receipts (author, public) | The published routed utilization reads 49,427 LUT, 53,378 FF and 87.5 BRAM. Production `hdl/` from `acadfacd` to the head changes comments only (two comment hunks) | `receipts/evidence/AUTHOR-RECEIPTS.txt` |

## Findings

### R628-4-R1 - RESIDUE - Docs

**Where:** the PR body.
- Status: "Required hosted shard 4/5 success remains outstanding at this head."
- Round 4: "The required hosted shard still needs its new-head result."
- Known limitations: "Hosted shard 4/5 at this source head remains unverified."

**Why:** the hosted shard concluded success at this head, and its `suite-logs-4` carries the four counters `RESULT: PASS` lines. The three sentences are now stale.

**Exact fix:**
- Replace the Status sentence with: "Hosted Verilator shard 4/5 succeeded at this head (run 38311301025); `suite-logs-4` shows the four counters legs' `RESULT: PASS`."
- Delete the Round 4 sentence.
- Delete the Known-limitations bullet.

### R628-4-R2 - RESIDUE - Docs

**Where:** `tb/verilator/milan_dp/README.md:4-21`, which describes what `make`/`run` builds and runs.

**Why:** `Makefile:636` now ends `run` with `$(MAKE) counters`, four extra temporary elaborations described in `docs/testing/726_STREAM_COUNTERS.md`. The suite README does not mention that leg. The authoritative leg document exists and is indexed from `docs/README.md`, so this omission is wording only.

**Exact fix:** after the paragraph ending "The mutation driver starts only after every ordinary simulation succeeds.", add: "`run` then invokes `make counters`: four temporary `stream_counters.py` elaborations (shapes 1 and 8, `uncertain` and `frames-only`) under `TMPDIR`, each printing `RESULT: PASS`. See [the stream counter measurements](../../../docs/testing/726_STREAM_COUNTERS.md)."

### S1 - SUGGESTION - Tests

**Where:** `tb/verilator/milan_dp/Makefile:677-683` and `stream_counters.py:26-29`.

The shipped plants put the RX interval law on the CRF engine only (`rx-interval`). They restore the healthy-dirty suppression only jointly (`late` at the datapath, `before` for all three engines). My `aaf-interval`, `aaf-guard` and `crf-nodirty` plants show that the standing checks already catch each per-engine defect. Optional: add them to `counters-mutants` so that the per-engine coverage is itself standing.

### S2 - SUGGESTION - RTL, Robustness (carried from R628-3-S1)

**Where:** `hdl/ieee1722/crf/KL_crf_rx.sv:487-490` against `:644-689`.

A CRF AVTPDU accepted in the exact bind-rise cycle is wiped from the new era's FRAMES_RX. `KL_talker_diag_ctx.sv:249` and `KL_avtp_rx_monitor_ctx.sv:1159` keep the coincident event. The ordering is stated in the comment, and the loss is at most one packet per bind. Optional alignment.

### S3 - SUGGESTION - Tests (carried from R628-3-S3)

**Where:** `tb/verilator/milan_dp/sim_nxn.cpp:2596`.

The `10000000L` "below silence timeout" bound is tied to the notify build's clock. Optional: derive it from the clock parameter.

### S4 - SUGGESTION - Tests

**Where:** `tb/verilator/milan_dp/stream_counters.hpp:64-75,190-191`.

The refresh bound is 1000 ms plus the service delay measured in the same run, as the ruling defines it. A regression that delays every notification uniformly therefore widens its own bound. The run prints the service maxima (3.263 / 14.058 ms), so nothing is hidden today. Optional: also flag a service delay above a stated ceiling.

## Clean-lens lines

[R628] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:205-262`, `hdl/ieee1722/crf/KL_crf_rx.sv:484-520,644-689`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:329-330,640-643,950-953,982-985,1153-1175`, `tb/verilator/milan_dp/stream_counters.hpp:173-253`, issue #726 items 1, 2 and 4 - Checked against ruling 6125741685 with addendum 6125845117, STOP ruling 6126028604 and corrected ruling 6132483068:
- Item 1: FRAMES_TX counts per AVTPDU on AAF and CRF, with 32-bit wrap. It resets at each talker start and keeps a coincident first PDU. MEDIA_RESET and TIMESTAMP_UNCERTAIN are unchanged.
- FRAMES_RX counts per AVTPDU on AAF (coalesced publication, 32-bit batch) and on CRF. It resets on not-bound to bound and survives unbind. Each of these is planted and detected.
- Item 2: every changed Stream Input/Output marks itself dirty, and the unchanged scheduler remains the only limit. Spacing holds at or above 1000 ms. Every consecutive gap and the final wait stay within 1000 ms plus the measured service at both shapes, through the parent MAC. The AVB_INTERFACE path (`ctr_avb_dirty_w`) is untouched.
- No firmware implementation change, so no capture re-measure is due; `check_nvm_capture` passes.
- Item 3 and the reference-peer reset comparison are merge-turn bench work.

[R628] PASS RTL - the same RTL lines, plus `hdl/milan/milan_datapath.sv:3156-3171,3300-3322,7915-7995`, gitlinks at base and head, and the routed utilization receipt. Findings:
- Every register is reset. Widths: `frx_acc_r` and `frx_add_r` are 32-bit, with no truncation at `:643`.
- In the talker, the start edge's nonblocking assignment correctly overrides the per-PDU increment.
- The CRF strobe skid is unchanged and adequate at the documented event rates.
- Per-PDU dirty pulses coalesce in the arbiter's sticky pending bits and the processor's `ctr_dirty_r`.
- No CDC is added. Lint passes against its ratchet.
- Submodule gitlinks are identical at base and head.
- Production logic has changed only in comments since `acadfacd`. The published routed result there reads 49,427 LUT (author-reported +35, below the +200 STOP bound). S2 is optional.

[R628] PASS Robustness - the bind/unbind/rebind sequence (`stream_counters.hpp:256-281`), the start/stop/restart and near-wrap runs (`:283-308`), the 65,534+3 batch boundary (`:310-322`), the out-of-range shift refusal (`receipts/runs/shift1_1000001.log`), the inherited `-w` make flags (`stream_counters.py:144-163`), the `frames-only` and no-CRF generate branches (`milan_datapath.sv:7924-7929,3176-3180`), and the unpublished-zero snapshot. Each was exercised or planted. Saturation, reset and guard-restoration plants are all detected.

[R628] PASS Tests - `tb/verilator/milan_dp/stream_counters.{py,hpp}`, `stream_counter_f5.{py,cpp}`, the `Makefile` targets, the tkdiag, crf_rx and avtp_rxmon diffs, `tests/features/counters_contract_milan.feature`, and `tb/tools/torture_campaign.py`:
- All 13 shipped plants fail by name and escape with only their check omitted. My 4 extra plants are detected.
- The baseline yields only the named groups.
- The phase check and the `fixed-grid` plant fail as claimed, both in the parent fixture and in the mailbox.
- The behaviour gate, grader, unit suites and campaigns are green.
- The standing target runs green in the hosted shard at this head.

[R628] PASS Docs - `docs/testing/726_STREAM_COUNTERS.md:10-221` (every figure re-derived from my runs), `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218-235`, `docs/reference/REGISTER_MAP.md:145-153,866-872,919,963`, `sw/firmware/ctrl/aecp/README.md:55-65` (COUNTERS bit 3, value 8, verified against `aecp.h:172-174`), the design notes in the four HDL files, and the five dated findings notes:
- The historical traceability row is pinned to the base.
- `tb/verilator/milan_dp/README.md:465,499-501,587-602,1158` and the feature law table match the rulings and the corrected criterion.
- No live non-history text still states the one-per-interval packet law (`scratch` grep, summarized in the limits below).
- R1 and R2 are residue.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | four counter engines; datapath arbiter; parent fixture runs and independent re-grade at both shapes; rulings 6125741685, 6125845117, 6126028604 and 6132483068 | R628-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| RTL | CLEAN | RTL lines above; lint; gitlinks; comment-only delta since `acadfacd`; routed utilization receipt | R628-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Robustness | CLEAN | bind/unbind/rebind, restart/wrap, batch boundary, shift refusal, inherited make flags, condition branches, snapshot probe, reset and guard plants | R628-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Tests | CLEAN | behave 406; grader 80; 10+3 shipped plants with escapes; 4 reviewer plants; baseline; unit suites and campaigns; prior probes unchanged; hosted shard 4/5 `suite-logs-4` | R628-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |
| Docs | CLEAN (R1, R2 residue) | 726_STREAM_COUNTERS.md; audit; REGISTER_MAP; AECP README; milan_dp README; HDL notes; findings notes; feature file; PR body; 34 local gates; hosted docs-check | R628-4 | 1add0cfbcc778c5292a5935631ca7b47c612b990 |

## Prior public review findings: status at this head

| Finding | Status and evidence |
|---|---|
| R628-3-F2 (BLOCKER, Tests, Robustness) | **Resolved.** `stream_counters.py:144-163` captures with `--no-print-directory`. The inherited `-w` leg and the recursive target both pass locally. The hosted shard 4/5 succeeded at this head, with four counters `RESULT: PASS` lines in `suite-logs-4`. |
| R628-3-F1 (MAJOR, Conformance, Tests, Docs) | **Resolved** under corrected ruling 6132483068: <ul><li>`stream_counters.hpp:173-193` grades spacing, every consecutive gap and the final wait from the first notification. There is no grid and no startup exclusion.</li><li>`:195-208` proves the verdict invariant across 1,000,001 start positions. The `fixed-grid` plant fails `PHASE` and escapes, in both the parent fixture and the mailbox.</li><li>R628-3's `run_shift.sh`, unchanged, passes at 0/200/300/800/900 µs at both shapes.</li><li>The texts state the corrected criterion: `726_STREAM_COUNTERS.md:31-39,55-62,76-86`, the PR body, and the audit at `:228-235`.</li></ul> |
| R628-3-S1 | Retained, as S2. |
| R628-3-S2 | **Resolved.** Notifications after `measurement_end_cyc` are excluded (`stream_counters.hpp:178,215`). |
| R628-3-S3 | Retained, as S3. |
| R628-3-R1 / R629-3-R01 (RESIDUE) | **Resolved.** The PR body says "Round 4 source head", and the "remain local" sentence is gone. |
| R628-1-F1 / R629-1-F01 (MAJOR) | Remains resolved. `reproduce_contract.py` gives rc 0, and each of the three removed retained resets fails it. Behave 406/0. Hosted bdd-conformance success. |
| R629-1-F02 (RESIDUE) | Remains resolved. |
| R628-1-F2, F3, F4 (MINOR) | Remain resolved: <ul><li>`frames-only` legs at both shapes; `tx-nodirty` fails `OUTPUT_CADENCE` and escapes; `before` requires TX/RX/CADENCE.</li><li>The four README passages are current.</li><li>The law table, trap (3), the Table 7.157 grader and the interval-rate FAIL scenario all pass.</li></ul> |
| R628-2-F1 (MAJOR, docs workflow) | Remains resolved. The 34 local gates return rc 0 with no budget raised. `dirty_p_o` names its unit (`KL_avtp_rx_monitor_ctx.sv:187`). Hosted docs-check success at this head. |
| R628-2-F2 (MINOR) | Remains resolved: `probe_xside_law.py`, unchanged, gives PASS for the ruled pair and FAIL against the interval-rate side. |
| R629-2-F01 (MINOR) | Remains resolved: `probe_snapshot.py`, unchanged, passes, and the standing scenario exists (`counters_contract_milan.feature:198-205`). |
| R628-2 RS1-RS5 (RESIDUE) | Remain resolved. Nothing in their scope changed in round 4. |
| R628-1-S1/S2 and R628-2-S1..S4 | S1 (drift) became R628-3-F1, now resolved. The others are carried as S2/S3 above, or resolved as R628-3-S2. |

## Real limits

- No hardware, bench or physical calibration was run. Field skips are not hardware proof. The parent runs are finite five-second compressed-time simulations (1 ms = 1000 cycles) with two recipients, not maximum fanout and not a physical link.
- I ran no Vivado. Area and timing are author-reported. I read 49,427 LUT, 53,378 FF and 87.5 BRAM in the published routed report. I did not reproduce the 49,392-LUT base or the WNS/WHS (+0.451/+0.036 ns). The published copies of the utilization report and the area log hash differently from the values `IMAGE-ARTIFACTS.tsv` records for the originals. They are a few bytes larger, which is consistent with path sanitization. The grade file matches exactly (`receipts/evidence/AUTHOR-RECEIPTS.txt`).
- Local Python is 3.14.7, not the documented 3.12.3. The renderer wheels came from a local environment. I ran 34 commands from the docs workflow. Not run locally: `gen_hdl_reference`, the wavedrom/diagram/PNG gates, the builder/RV32 SDK steps, `make -C gptp-processor docs`, and `act_ci.py --selftest`. The hosted docs-check success covers the complete workflow at this head.
- The hosted Verilator shards 1/5 and 2/5 were still in progress at 22:12Z. Hosted and act acceptance belong to the manager.
- The F5 mailbox check injects `aecp_changed()` calls. It does not prove that a production caller raises the COUNTERS event. The PR states this.
- I did not retrieve the standards texts; the maintainer rulings govern.
- Stale-law sweep: a grep of tracked non-history text found only historical findings that carry dated notes, history-pinned rows, CHANGELOG history, and test comments still valid under both laws.

## Pending manager duties

- Accept the remaining exact-head hosted contexts (Verilator shards 1/5 and 2/5).
- Build the current-dev merge candidate (source base `c6bd08c6`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`) with the builder and native banks, and link the receipts. No manager source bank ran at this head, and none is claimed.
- Merge-turn bench work:
  - the controller shows DUT FRAMES_TX at the packet rate and Stream Input refresh, side by side with the reference peer;
  - the talker-start and bind reset comparison with the peer;
  - per-descriptor intervals on the link tap at both shapes.
- Carry R628-4-R1 and R628-4-R2 to the residue checklist.

## Restore verification

From `receipts/restore_and_identity.txt`:
- HEAD is `1add0cfb…`, tree `11896ba0…`.
- 0 untracked or ignored entries, 0 index or worktree differences.
- 1,300 tracked regular files re-hashed equal to their index blobs.
- Modes: 1,252 × 100644, 48 × 100755, 5 × 160000.
- No assume-unchanged or skip-worktree flags.
- The `ls-files -s` and `ls-tree -r` digests are equal (`c4559ad6…`).
- All five gitlinks equal the base.
- The checked-out submodules are clean at their gitlinks.
- I removed the build products and Python caches I created, including one in `protocol-processor`. Plants ran on scratch copies, except the three single-line retained-reset deletions, each restored by `git checkout` before the next.

## Reproduction

Set `VERILATOR` to the pinned 5.050 executable and `PACKET` to this directory. Then:
- `scripts/launch.sh NAME DIR CMD…` and `scripts/wait.sh SECS NAME…` run campaigns in the background and wait on them.
- `scripts/own_plants.py REPO VARIANT WORK` runs the reviewer plants.
- `scripts/shift_probe.sh WORK SHIFT LOG` reruns a built model at a shifted start.
- `scripts/regrade_gaps.py RUNLOG` re-grades a run log independently.
- `RENDERER_SITE=… scripts/docs_gates.sh REPO TMP` runs the documentation gates.

The prior probes' identities are in `receipts/prior_probes/PROBE-IDENTITY.txt`.

R628-4 FINISHED
