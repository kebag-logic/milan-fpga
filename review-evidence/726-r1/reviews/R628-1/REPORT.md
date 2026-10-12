[R628] NEGATIVE - exact head acadfacd52c6daabf892d6ebe99da11ca06748cb

# R628-1: internal cleared-context review of PR #729 (issue #726)

Exact head `acadfacd52c6daabf892d6ebe99da11ca06748cb`, tree `c1decf8ae9177a4cc5d3b7700404214f064b494b`, source base `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Reviewer: R628 (internal, cleared context, own detached clone). All five lenses applied.

The counter RTL is correct as far as this round could test it. FRAMES_TX on AAF and CRF counts every transmitted AVTPDU. FRAMES_RX counts every received AVTPDU. Both wrap at 32 bits, both resets hold, and the healthy-update dirty events restore one notification per window through the unchanged processor scheduler. Every number the author published for the parent window measurement reproduces exactly.

The verdict is NEGATIVE because:
- the change turns a required CI gate red (finding F1, MAJOR);
- three test and documentation defects stay open (F2, F3 and F4, each MINOR).

## Reconstruction

Read in this order:
1. AGENTS.md and CONTRIBUTING.md (sections 1, 3 and 6).
2. docs/README.md.
3. Issue #726: body and frozen acceptance 1-4.
4. The maintainer rulings: 6125741685 (counter law), 6125845117 (1722.1 is the reference where Milan is ambiguous; the objection is withdrawn), 6126028604 (no processor change, cadence judged per one-second window, the spacing is the rate limit).
5. Assignment 6125784157, the author's TAKEN, STOP and REVIEW READY comments, and the PR #729 body.
6. `git diff c6bd08c6..acadfacd` (26 files, 2 commits) and the surrounding RTL: `milan_datapath.sv` talker feed `:3155-3322` and descriptor arbiter `:7900-8000`, `KL_crf_rx.sv` accept and bind paths, `KL_avtp_rx_monitor_ctx.sv` commit and flag fold.
7. Published evidence tree `885f0527:review-evidence/726-r1` (area, timing and implementation-input hashes), and the hosted check runs at the exact head.

There is no submodule change: the gitlinks for protocol-processor `2ad2f845`, gptp-processor `7dda9c3b`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8` and external `efeb541a` are identical at base and head (`receipts/identity_and_submodules.txt`). There is no firmware C change: the only path changed under `sw/` is `sw/firmware/ctrl/aecp/README.md`, and `check_nvm_capture.py` exits 0.

## Executed evidence (this round, this head)

The toolchain was the scoped Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`). All runs used a scratch copy of the exact head. The review clone was never written to; see "Restore verification" below.

| Campaign | Result | Receipt |
|---|---|---|
| `make` tkdiag / crf_rx / avtp_rxmon / aaf / crf_tx (includes their mutant campaigns) | all rc 0. tkdiag 99/0; KL_crf_rx 14287/0 + discontinuity 2201/0 + talker_step 69/0 + mutants 10/0; avtp_rxmon 97/0, NxN 119/0, lockstep 36/0 x2; aaf 27/0 + start 34020/0 + NxN lane 42/0; crf_tx 127/0 | `receipts/unit_*.log/.rc` |
| `stream_counters.py --shape 1` / `--shape 8` | rc 0; 98/0 and 427/0 checks | `receipts/runs/clean-{1,8}.run.log` |
| `stream_counters.py --variant before`, shapes 1 and 8 | rc 1 as required. Failures: 20 (TX, RX, CADENCE) and 90 | `receipts/runs/before-{1,8}.run.log` |
| Eight author plants (`tx-interval rx-interval tx-reset aaf-reset crf-reset rx-saturation late rate`) | each: named-group failure, then rc 0 escape with that group omitted | `receipts/mut_*.log`, `receipts/runs/mut-*` |
| `stream_counter_f5.py`, shapes 1 and 8, plus the `late` and `rate` plants | clean rc 0. 40 and 180 row-windows each hold 1; gaps 1000-1002 ms. Each plant: named failure, then escape | `receipts/f5_*.log`, `receipts/runs/f5-*` |
| Seven doc and source gates: `docs_check`, `check_doc_style`, `check_doc_paths`, `check_rtl_source_lists`, `pp_srcs --check`, `check_soc_sources`, `check_nvm_capture` | rc 0 | `receipts/gate_*.log` |
| `lint_rtl --check` and `git diff --check c6bd08c6 HEAD` | rc 0 | `receipts/gate_*.log` |
| `gen_toc --check` and `check_em_dash --base c6bd08c6` | rc 0. These need the pinned renderer, which was installed into a private disposable venv under scratch from the repository's hash-locked requirements | `receipts/gate_gen_toc*`, `receipts/gate_check_em_dash*` |
| `behave` (tests/, the rtl-fast BDD gate) at head | **rc 1: 403 passed, 1 failed** | `receipts/gate_behave.log` |
| `behave` at base `c6bd08c6` (scratch checkout) | rc 0: 404/404 | `receipts/gate_behave_base_c6bd08c6.log` |
| Nine reviewer fault probes (below) | see table | `receipts/probe_*` |

Window figures reproduced from my runs (`receipts/window_summary.txt`, produced by `scripts/windows.py`):

| Shape | Graded row-windows | Each holds | Min gap | Max gap | Max service | Baseline empty input row-windows |
|---|---:|---|---:|---:|---:|---:|
| Shipping TDM8 (2 in / 2 out) | 24 | 1 | 1000.996 ms | 1001.867 ms | 3.263 ms | 12 |
| Largest TDM32 (9 in / 9 out) | 108 | 1 | 1000.982 ms | 1012.029 ms | 14.058 ms | 54 |

These match `docs/testing/726_STREAM_COUNTERS.md` and the PR body exactly. Wire versus counter: AAF 799/799 and CRF 101/101 at shipping. At the largest shape it is 800/800 on every AAF output and 101/101 on CRF. Restart runs match the wire, and the seeded wrap `0xFFFFFFFA` plus 64 AAF / 9 CRF PDUs lands on 58 / 3.

Reviewer probes. Each is one exact-once source edit in a disposable copy; diffs are in `receipts/probe_*.diff` and `scripts/probe.py`.

| Probe | What it breaks | Parent fixture | Unit suite |
|---|---|---|---|
| `tx-saturate` | FRAMES_TX saturates instead of wrapping | FAIL `[726 TX] restart and wrap follow wire` (x2) | - |
| `crf-unbind-reset` | CRF FRAMES_RX also zeroes on unbind (5.3.8.10 forbids) | FAIL `[726 RX_RESET] unbind preserves total` | - |
| `crf-tx-lost` | CRF output PDU strobe never reaches the talker counters | FAIL `[726 TX]` and `[726 CADENCE]` | - |
| `crf-rx-nodirty` | healthy CRF FRAMES_RX advances raise no event | FAIL `[726 CADENCE]` (x6) | crf_rx FAIL `[dirty-a1/a2/b1/b2]` |
| `aaf-rx-nodirty` | both pre-#726 AAF healthy-update exclusions restored | FAIL `[726 CADENCE]` (x6) | avtp_rxmon FAIL `[DV2/DV4/DV4b/DV4c/DV5b]` |
| `tx-start-coincident` | a PDU in the exact start cycle is dropped | escapes (rc 0) | tkdiag FAIL `T11 phase 0` (covered) |
| `tx-nodirty` | healthy transmitted PDUs raise no Stream Output event | **escapes (rc 0)** | tkdiag FAIL `T14 each healthy AVTPDU pulses dirty` |
| `tu0` (control) | talker counters see `tu` clear, which is the locked-PHC shipping condition | rc 0, 12/12 output row-windows hold 1 | - |
| `tx-nodirty-tu0` | `tx-nodirty` under the `tu0` condition | **FAIL: 12 output row-windows empty** `[726 CADENCE]` | - |

## Findings

### F1 - MAJOR - Tests

**Where:** `tests/steps/counters_contract_steps.py:629`, the era-wipe step, run by `tests/features/counters_contract_milan.feature:515`.

**Authority and evidence:**
- The step still requires `iv_frx_r <= 1'b0;` in `KL_crf_rx`'s bind block. This PR deletes `iv_frx_r` from `hdl/ieee1722/crf/KL_crf_rx.sv`: its declaration at `:424`, its reset, its fold, and its bind-block clear.
- Offline behave at the exact head gives 403/404 with `ASSERT FAILED: interval seen flags left standing across the era wipe ...: iv_frx_r`. The base `c6bd08c6` gives 404/404.
- The hosted `bdd-conformance` job 114913979852 ran on head `acadfacd` and concluded `failure` with the same assertion (`receipts/hosted_bdd_conformance_114913979852_extract.txt`). The job is part of the rtl-fast workflow (`.github/workflows/rtl-fast.yml:118-122`).
- The PR's "How to validate" list omits this gate, but states "every gate exits zero".

**Impact:** the exact head has no successful rtl-fast verdict (AGENTS.md section 7), so the PR cannot merge. "Existing regressions remain green" is false at this head.

**Required outcome:**
- At a new head, the BDD suite passes.
- The era-wipe step still proves that the bind edge clears the six remaining anomaly seen flags and zeroes FRAMES_RX (`pdu_count_o`). The check is updated, not dropped.
- The PR's validation list names the BDD gate and its result.

**Verification:** offline `behave` at the new head gives 404/404 or the new total with 0 failed. The hosted `bdd-conformance` succeeds on that exact head. As a negative control, re-plant a surviving `iv_uf_r` across the bind; the step must still fail.

### F2 - MINOR - Tests, Docs

**Where:**
- `tb/verilator/milan_dp/stream_counters.hpp:119-141`, the output-row CADENCE grading.
- `docs/testing/726_STREAM_COUNTERS.md:65-66`.
- `tb/verilator/milan_dp/stream_counters.py:151-153` with `docs/testing/726_STREAM_COUNTERS.md:122`.

**Authority and evidence:**
- AGENTS.md section 6 (Tests): each new test can fail for the defect it claims to detect. Assignment 6125784157 item 4 asks for a cadence check with a plant.
- (a) In the parent fixture, the talker stamps `tu` on every PDU, so TIMESTAMP_UNCERTAIN closes an interval every second. That interval commit already marks each Stream Output dirty. Removing the new per-AVTPDU output event (`tx-nodirty`) therefore passes the whole fixture.
- Under the shipping locked-PHC condition (`tu0`), the same removal empties all 12 graded output row-windows (`tx-nodirty-tu0`). With the event intact under that condition, all 12 hold one (`tu0`).
- So the parent measurement's output rows do not exercise the FRAMES_TX path. The evidence document presents them, "Output row-windows already contain one each. After the change all input and output row-windows contain one each", without stating the `tu` condition that produces them.
- The per-AVTPDU pulse itself is pinned at unit level (tkdiag T14 fails under `tx-nodirty`). The gap is integration coverage and the evidence statement, not the RTL.
- (b) The document says the `before` driver "requires the baseline executable to report the reproduced defects". The driver accepts any `[FAIL]` with rc 1. It does not check that the TX, RX and CADENCE groups are the ones that fail. The current baseline logs do show those groups (this round's `before-1` and `before-8`).

**Impact:**
- A regression in the Stream Output change event, the exact path this issue moved from interval-close to per-AVTPDU, escapes the parent cadence check under the fixture's condition.
- The published output measurement reads as evidence for the shipping condition when it is not.
- A baseline that fails for an unrelated reason would still be accepted as reproducing the defect.

**Required outcome:**
- The Stream Output cadence is graded under a condition where FRAMES_TX is the only changing output counter (`tu` clear, no `mr` toggle), at least at the shipping shape. A plant that removes the per-AVTPDU output event fails by name there and escapes with that check omitted.
- The evidence document states the condition each output row was measured under.
- Either the `before` driver requires the named groups, or the document states what it actually requires.

**Verification:** rerun with the new output leg and its plant at the new head. Expect a named CADENCE failure for the plant and rc 0 for the escape, and the document's sentence matching the driver.

### F3 - MINOR - Docs

**Where:** `tb/verilator/milan_dp/README.md` at four places:
- `:465-466`, "FRAMES_TX read 16 ... the documented semantics".
- `:498`, row `[F]`: "FRAMES_TX counts observation intervals since STREAM_START, far fewer than the PDUs".
- `:586-603`, section "FRAMES_TX is an interval count", ending "a continuously bound output should read ... FRAMES_TX equal to the seconds it has streamed".
- `:1157`, "FRAMES_RX (interval law)" for the CRF input.

**Authority and evidence:**
- This PR changes the `[F]` assertions in `tb/verilator/milan_dp/sim_crf_licence.cpp:1002,1014` to "FRAMES_TX follows wire PDUs". It changes the CRF input wrap check in `sim_nxn.cpp:5531` to per-AVTPDU.
- Ruling 6125741685 and its addendum 6125845117 fix both counters as per-AVTPDU.
- The suite README, which documents those legs, still states the superseded clause law and what the old checks asserted.
- AGENTS.md section 6 (Docs): changed contracts are reflected in authoritative docs. The text carries a Table 5.4 / Table 5.6 law claim, so it is not wording-only.

**Impact:** a reader of the suite documentation is told the opposite of what the leg now checks and what the RTL now does.

**Required outcome:** the four passages describe the per-AVTPDU law and the current `[F]` and CRF-wrap checks, or carry a dated note to the ruling as the findings pages do.

**Verification:** read the README at the new head against `sim_crf_licence.cpp` `[F]` and `sim_nxn.cpp` `[CTRS-CRF]`. The doc gates stay green.

### F4 - MINOR - Docs, Tests

**Where:**
- `tests/features/counters_contract_milan.feature:324`, the law table: `FRAMES_RX | per-interval | Milan v1.2 Table 5.6`, under the statement at `:284-289` that "the RTL and the bench grader are both held to this table".
- The same file at `:42-52`, trap (3): "Both are legitimate".
- `tb/tools/torture_campaign.py:507`, `COUNTER_LAW["FRAMES_RX"] = per-interval`, with the grader at `:625-660`. A per-frame FRAMES_RX grades INFO. An interval-rate FRAMES_RX grades PASS.

**Authority and evidence:**
- Rulings 6125741685 and 6125845117 decide per-AVTPDU for FRAMES_RX and FRAMES_TX. Table 7.157 decides because Milan's wording is ambiguous.
- Acceptance 4 requires the AECP counter docs to record the ruling. `tests/README.md` is the AECP test strategy, and this feature is its counter contract.
- The B14 findings page (`docs/findings/B14_BENCH_5603C353.md:490`) already names this feature file's interval reading.
- The PR body acknowledges the gap: "The legacy bench classifier still accepts historical readings".

**Impact:**
- The project's executable counter-law table states the law the ruling replaced.
- The bench grader would PASS a regression to one count per interval and only INFO the ruled behavior. Merge-turn acceptance 3 depends on a reader knowing to ignore it.

**Required outcome:** one of the following.
- The law table, trap (3) and the grader's FRAMES_RX law follow the ruling, with a scenario in which an interval-rate FRAMES_RX on a flowing stream is a FAIL.
- Or the maintainer explicitly rules this classifier outside #726. In that case the finding is withdrawn, not deferred.

**Verification:** `behave` passes at the new head with the changed law rows. A one-per-interval FRAMES_RX example grades FAIL.

### S1 - SUGGESTION - Robustness

**Where:** `hdl/ieee1722/crf/KL_crf_rx.sv:641-648`.

The bind-rise branch is ordered after the accept branch, so an accepted CRF PDU in the exact bind-rise cycle is not counted in the new era's FRAMES_RX. The AAF engine keeps the bind-cycle event (`KL_avtp_rx_monitor_ctx.sv:1155-1158`), and the talker keeps the start-cycle PDU (`KL_talker_diag_ctx.sv:248`). The ordering is stated in the source and the effect is at most one packet per bind. It is optional to align with the AAF rule or record the asymmetry.

### S2 - SUGGESTION - Tests

**Where:** `tb/verilator/milan_dp/sim_nxn.cpp:2596`.

The "below silence timeout" bound `10000000L` equals 100 ms only at the 100 MHz default clock the notify build elaborates. It is correct today, but deriving it from the clock parameter would keep it true if that build pins 50 MHz.

## Clean-lens lines

[R628] PASS Conformance - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:205-258`, `hdl/ieee1722/crf/KL_crf_rx.sv:487-490,641-690`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:946-953,983-985,1155-1172`, `hdl/milan/milan_datapath.sv:3155-3322`, the runs `clean-1/8`, `before-1/8`, `mut-*` and `probe-*` - Checked against Table 7.159 and 7.157 per-AVTPDU, the Table 5.4 start reset, the 5.3.8.10 bind reset and unbind survival, 32-bit wrap, and ruling 6126028604's window test. Per-window one notification at minimum spacing of at least 1000 ms, with maximum gap at most 1000 ms plus measured service, at both shapes. AVB_INTERFACE producer and processor scheduler untouched. Physical acceptance 1 (peer reset comparison) and 3 (controller display) are merge-turn work, not claimed.

[R628] PASS RTL - the same RTL lines - Widths: `frx_acc_r`/`frx_add_r` 32-bit with no truncation at `:639-642`. Every register is reset, and the removed `seen_f_r`/`iv_frx_r` leave no dangling use (lint and source-list gates rc 0). NBA ordering: the start and bind writes come last. No CDC added. The PDU feed is single-strobe with a deferred CRF skid (`milan_datapath.sv:3155-3170`), and the census shows no lost strobe. The arbiter's per-descriptor pending bits coalesce the per-PDU pulses (`:7969-7975`). Area 49,427 LUT routed (+35 against the supplied 49,392); WNS +0.451 ns and WHS +0.036 ns from the published utilization and signoff reports, whose input hashes equal this head's bytes (`receipts/implementation_inputs_head_sha256.txt`).

[R628] PASS Robustness - the probes `crf-unbind-reset`, `tx-saturate`, `tx-start-coincident` and `crf-tx-lost`, plus the fixture's unbind/rebind and restart legs - Covered: minimum and maximum values (wrap seed, the 65,534 + 3 batch boundary), invalid ordering (start-cycle PDU, which tkdiag T11 phase 0 covers), repeated bind and unbind, stop and restart, reset, and the feature-dependent CRF descriptor presence (`frame_idx` at or above `N_CTX_P` is ignored). S1 is optional.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | RTL lines above; rulings 6125741685, 6125845117, 6126028604; acceptance 1-4; parent and firmware window runs; author plants; reviewer probes | R628-1 | `acadfacd52c6daabf892d6ebe99da11ca06748cb` |
| RTL | CLEAN | four RTL files and the datapath feed and arbiter; lint, source-list and capture gates; published route utilization and signoff reports (hash-matched inputs) | R628-1 | `acadfacd52c6daabf892d6ebe99da11ca06748cb` |
| Robustness | CLEAN (S1 optional) | reset, bind and start ordering paths; wrap and batch boundaries; probes | R628-1 | `acadfacd52c6daabf892d6ebe99da11ca06748cb` |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR, F4 MINOR) | 5 unit suites, stream_counters and f5 fixtures, 8+2 plants, 9 probes, behave at head and base, hosted bdd-conformance | R628-1 | `acadfacd52c6daabf892d6ebe99da11ca06748cb` |
| Docs | UNCLEAN (F2, F3, F4 MINOR) | `726_STREAM_COUNTERS.md`, REGISTER_MAP, the Milan v1.2 audit, the firmware AECP README, five findings notes, design notes in the four RTL files, `milan_dp/README.md`, the counters-contract feature, the PR body; doc gates | R628-1 | `acadfacd52c6daabf892d6ebe99da11ca06748cb` |

## Prior public review findings

At the start of this round, PR #729 carried no review findings, only the two REVIEW STARTED comments. After my verdict and ledger were written, I read the one review published in the meantime: the external R629-1 NEGATIVE at this exact head (PR comment 6128905694). Its findings at this head:

- **R629-1-F01 (MAJOR, Tests), the era-wipe step requiring the removed `iv_frx_r`: RETAINED.** It is the same defect as F1 above, reached independently: offline behave gives 403/404 at head and 404/404 at base, and the hosted job 114913979852 fails. Its required outcome is compatible with F1's.
- **R629-1-F02 (RESIDUE, Docs), PR body Status sentence "No push or PR action has been performed.": RETAINED as RESIDUE.** The sentence is still in the PR body at this head and is stale because the PR exists. Exact fix: delete the sentence. It is wording only, so it does not affect Docs coverage. Docs is UNCLEAN here because of F2, F3 and F4, not because of this residue.

I record Docs as UNCLEAN where R629-1 records it CLEAN. The disagreement is over F2 (the output-cadence evidence statement), F3 (`tb/verilator/milan_dp/README.md`) and F4 (the counters-contract law table and grader). R629-1's Docs line does not examine those artifacts. Under AGENTS.md section 7, coverage is per lens and per head, so the Docs lens is not covered clean at this head.

## Real limits

- The simulation compresses protocol time: 1000 cycles per protocol ms at a 50 MHz parameter. It shows protocol behavior, not physical link timing.
- Only two recipients were registered, so maximum controller fanout is not measured.
- Startup windows 0 and 1 are recorded but not graded. In my runs, an input row empty in window 0 or 1 is a phase effect: the row's gaps across the whole run stay at most 1001.0 ms at shipping.
- No Vivado run was made in this round. Area and timing are the author's published reports. Their implementation-input hashes equal this head's bytes. The +35 LUT delta rests on a supplied baseline figure (49,392) that this round did not re-derive.
- No manager source bank exists at this head, and none is claimed or inferred. No full parent, PP, gPTP or Yosys bank, Docker or act was run in this round. The hosted Verilator shards, docs-check, elaborate, firmware-unit and publication-census were still in progress when inspected. The hosted Yosys shards, verilator-lint and yosys-elaboration had succeeded. Physical gPTP was skipped, and a skip is not evidence.
- `ctrl_app_aecp_changed()` has no production caller in the opt-in F5 build. The README's "must call `aecp_changed()`" is an integration contract, and F5's window check drives the core directly. This is outside #726's frozen scope and is not a finding.
- The two doc gates that need the pinned Markdown renderer ran from a private disposable venv built from the repository's hash-locked requirements, not from a shared install.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- The current-dev merge-candidate validation (builder and native banks), and its receipts on the PR.
- Hosted and act acceptance, including the final state of the in-progress contexts above and a green `bdd-conformance` at the merge head.
- Merge-turn bench: acceptance 1's reference-peer reset comparison, acceptance 2's link-tap per-descriptor interval, and acceptance 3's controller display side by side with the reference peer, judged under the packet ruling (see F4).
- Re-review of the corrected head under every lens whose scope the fix touches.
- Carry the retained RESIDUE (R629-1-F02, the stale PR-body sentence) to the residue checklist.

## Restore verification

The clone was not written. HEAD and tree are unchanged. The index hash before and after is identical (`4017ecdf...`). `git status --porcelain --untracked-files=all` is empty, and `git diff --quiet HEAD` passes. The five gitlinks are stage 0 at their pinned SHAs, and the initialised submodules are clean (`receipts/clone_restore_verification.txt`).

## Reproduction

The scripts in `scripts/` are portable:
- `bg.sh` and `wait.sh` launch and poll detached runs.
- `probe.py <exact-head-copy> <scratch> <name>` plants one probe.
- `windows.py <run.log>...` summarises the window CSV.

The stock commands are those in `docs/testing/726_STREAM_COUNTERS.md`, plus `cd tests && behave --no-capture -f plain`.

R628-1 FINISHED
