[R628] NEGATIVE - exact head 37944f8ac9d1a2212a3a32f36d921434ea0cbdeb

# R628-2: internal cleared-context review of PR #729 (issue #726), round 2

Exact head `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb`, tree `037ca71afbbb78009f8116a6f1227b81d38af79b`, source base `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Round-2 delta `acadfacd..37944f8a` (5 commits). Reviewer: R628 (internal, cleared context, own detached clone). All five lenses were applied at this head.

The counter RTL is correct. FRAMES_TX on the AAF and CRF outputs counts every transmitted AVTPDU. FRAMES_RX on every input counts every received AVTPDU. Both wrap at 32 bits and both resets hold. Healthy updates mark their descriptor dirty, and the unchanged processor spacing is the only limit. Every round-1 finding is resolved at this head. Every number the author published for the parent, frames-only, baseline and firmware runs reproduces exactly.

The verdict is NEGATIVE for two reasons:
- **F1 (MAJOR).** The required `docs-check` context is red at this exact head. A docs-workflow ratchet fails on the PR's own change. Three more gates in the same workflow were skipped on the hosted run, and each fails locally on files this PR adds.
- **F2 (MINOR).** The bench grader's cross-device stream-counter helpers still enforce the superseded interval law. They file the ruled per-AVTPDU behavior as a deviation, and they pass a regression to one count per interval.

## Reconstruction

I read the sources in this order:
1. AGENTS.md and CONTRIBUTING.md (sections 1, 2.2, 3, 5 and 6), then `docs/README.md`.
2. Issue #726: the body and frozen acceptance 1-4.
3. The maintainer rulings: [6125741685](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685) (the counter law), [6125845117](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117) (1722.1-2021 decides where Milan is ambiguous) and the STOP ruling [6126028604](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604) (no processor change; cadence judged per window; the spacing is the rate limit).
4. The assignment [6125784157](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157), the round-2 assignment [6129163001](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6129163001), the author's TAKEN, STOP and both REVIEW READY comments, and the PR body.
5. `git diff c6bd08c6..37944f8a` (30 files, 7 commits) and the round-2 delta.
6. The surrounding RTL:
   - the `milan_datapath.sv` talker feed and CRF skid (`:3155-3322`) and the descriptor arbiter (`:7900-8000`);
   - the pinned scheduler, `KL_aecp_notify.sv:1098-1105` and `:1449`;
   - the split-build firmware event plumbing, `ctrl_app_aecp.c` and `aecp.h:171-174`.
7. Public executable evidence: the evidence tree at `995bc120:review-evidence/726-r1/author-r2` (area, timing, implementation-input hashes, gate and window receipts) and the hosted check runs at this exact head.

I read the prior public findings (R628-1 and R629-1) only after my own pass over the diff.

There is no submodule change. The five gitlinks are identical at base and head: protocol-processor `2ad2f845`, gptp-processor `7dda9c3b`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8` and external `efeb541a`. There is no firmware change either: the only path changed under `sw/` is `sw/firmware/ctrl/aecp/README.md`, and `check_nvm_capture.py` exits 0. No capture re-measure is triggered.

## Executed evidence (this round, this head)

Toolchain: the scoped pinned simulator reports `Verilator 5.050 2026-07-01 rev v5.050`. Python 3.14 runs the BDD suite and the gates. The two renderer-dependent doc gates used the existing hash-locked renderer environment; its package versions equal `tools/markdown/requirements.txt` (`receipts/md-venv-freeze.txt`). Every simulation build and probe ran in a scratch work directory or in a disposable export.

| Campaign | Result | Receipt |
|---|---|---|
| `cd tests && python3 -m behave --no-capture -f plain` | rc 0; 14 features, 405 scenarios, 1,971 steps, 0 failed, 0 skipped | `receipts/behave.log` |
| R629-1 `reproduce_contract.py` (sha256 `fdc8be18...`, identical to the author's copy) | rc 0 at head | `receipts/r629-reproduce-contract-head.*` |
| Bind-era contract plants against that reproduction: drop the FRAMES_RX wipe, drop the SEQ_NUM_MISMATCH wipe, leave `iv_uf_r` standing, wipe on any edge (unbind too), keep `locked_o` | clean rc 0; every plant rc 1 with the named assertion | `receipts/probe-bind-contract*` |
| `torture_campaign.py --self-test` | 78 tests OK | `receipts/torture-selftest.log` |
| `stream_counters.py` `--shape 1` / `--shape 8` (uncertain) | rc 0; 98/0 and 427/0 | `receipts/runs/clean-{1,8}` |
| `--output-condition frames-only`, shapes 1 / 8 | rc 0; 110/0 and 481/0. Every output: TU 0, MR 0, 1 start, 0 stops, wire tu 0, wire mr 0 | `receipts/runs/frames-{1,8}` |
| `--variant before`, shapes 1 / 8 | driver rc 0. The executables give rc 1 with 20 and 90 failures, all named TX / RX / CADENCE | `receipts/runs/before-{1,8}` |
| `make counters-mutants`, the nine driver plants run one by one at shape 1 | each fails by name, then escapes (rc 0) with only that group omitted: tx-interval 6, rx-interval 1, tx-reset 4, aaf-reset 1, crf-reset 1, rx-saturation 1, late 12, rate 32, tx-nodirty 16 (`OUTPUT_CADENCE`, frames-only) | `receipts/mut-*.log`, `receipts/runs/mut-*` |
| `stream_counter_f5.py` shapes 1 / 8, plus the `late` and `rate` plants | clean rc 0. 40 and 180 row-windows each hold 1; gaps 1000-1002 ms. Each plant fails by name (`[F5 CADENCE]`, `[F5 RATE]`) and escapes | `receipts/f5-*.log`, `receipts/runs/f5-*` |
| Unit suites in a disposable export: tkdiag, crf_rx, avtp_rxmon | all rc 0. tkdiag 99/0. KL_crf_rx 14,287/0, plus discontinuity 2,201/0, talker_step 69/0 and mutants 10/0. avtp_rxmon 97/0, NxN 119/0, lockstep 36/0 at both N=1 and N=8 | `receipts/unit-*.log` |
| `lint_rtl.py --check`, `pp_srcs.py --check --selftest`, `check_rtl_source_lists.py` (and `--selftest`), `check_soc_sources.py`, `check_nvm_capture.py`, `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` / `--verify-anchors`, `check_em_dash.py --base c6bd08c6`, `git diff --check c6bd08c6 HEAD` | rc 0 | `receipts/gate-*.log/.rc` |
| The docs-workflow steps the hosted run skipped: `check_port_contracts`, `measure_fail_fast --check`, `check_todo_ownership`, `check_hygiene --check`, `check_sv_idiom`, `check_sh_idiom`, `ci_events --check`, `check_archive` | rc 0 | `receipts/gate-*.log/.rc` |
| `measure_naming.py --check` / `measure_test_evidence.py --check` / `check_cpp_idiom.py` / `check_py_idiom.py` | **rc 1 each** (F1) | `receipts/gate-measure_naming-check.log`, `gate-test_evidence.log`, `gate-cpp_idiom*.log`, `gate-py_idiom*.log` |
| Reviewer probes (below) and grader demonstration | see tables | `receipts/runs/probe-*`, `receipts/probe-xside-law.jsonl` |

Window figures from my runs:

| Shape | Graded row-windows | Each holds | Min gap | Max gap | Max service | Baseline empty input row-windows |
|---|---:|---|---:|---:|---:|---:|
| Shipping TDM8 (2 in / 2 out) | 24 | 1 | 1000.996 ms | 1001.867 ms | 3.263 ms | 12 |
| Largest TDM32 (9 in / 9 out) | 108 | 1 | 1000.982 ms | 1012.029 ms | 14.058 ms | 54 |

These figures are identical under the frames-only condition. They match `docs/testing/726_STREAM_COUNTERS.md:58-61,79-86` and the PR body exactly. Wire against counter:
- Shipping: AAF 799/799 and CRF 101/101.
- Largest shape: every AAF output 800/800, CRF 101/101.
- Restart runs match the wire (64/64 AAF, 8/8 CRF).
- The `0xFFFFFFFA` seed plus 64 AAF and 9 CRF PDUs lands on 58 and 3.
- Every input reads 500 received packets, keeps that total across unbind and reads 0 after rebind.
- The 65,534 + 3 batch publishes 65,537.

An instrumented copy of the fixture prints each notification and eligibility time (`receipts/trace-instrumentation.diff`, `trace_counters.py`, `gap_attribution.py`). At both shapes, every row's maximum gap lies inside the measured window (`receipts/gap-attribution-trace3-clean-{1,8}.csv`). The tightest case is largest-shape output 7, recipient B: 1012.029 ms against a 1012.516 ms bound.

Reviewer probes. Each is one exact-once edit to the scratch RTL copy (`probe_counters.py`). Each reuses the driver's own rule: a named failure, then a clean escape with only that group omitted.

| Probe | What it breaks | Result |
|---|---|---|
| `aaf-rx-interval` | AAF FRAMES_RX publishes +1 per interval instead of the packet batch | `[726 RX]` x2, escape rc 0 |
| `crf-rx-nodirty` | a healthy CRF accepted PDU raises no event | `[726 CADENCE]` x6, escape rc 0 |
| `tx-saturate` | FRAMES_TX saturates at `0xFFFFFFFF` | `[726 TX]` x2, escape rc 0 |
| `crf-tx-noreset` | only the CRF output keeps FRAMES_TX across a start | `[726 TX_RESET]` x2, escape rc 0 |
| `crf-unbind-wipe` | CRF FRAMES_RX also zeroes on bound to not bound | `[726 RX_RESET]` x1, escape rc 0 |
| `aaf-tx-nodirty` | only AAF output 0 loses its per-AVTPDU event (frames-only) | `[726 OUTPUT_CADENCE]` x8, escape rc 0 |
| `tx-nodirty` at shape 8 (driver plant, extra shape) | all output packet events removed | 16+ `OUTPUT_CADENCE` failures, plus 2 `CADENCE` failures on input 0. **Not attributable** by the driver's rule; see S2 |

## Findings

### F1 - MAJOR - Docs, Tests, RTL

**Where:**
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:186-190`, the rewritten `dirty_p_o` port comment, against its candidate record `scripts/naming.budget:53`.
- `tb/verilator/milan_dp/stream_counters.py:32,38,108,177` (`replace_once`, `plant`, `run`, `main`) and `tb/verilator/milan_dp/stream_counter_f5.py:21` (`main`).
- `tb/verilator/milan_dp/stream_counters.hpp` (one file-scope mutable; `stream_counter_probe()` at `:71-226` is one long function).
- `tb/verilator/milan_dp/stream_counter_f5.cpp:41` (multi-declarator `uint32_t min_gap=5000,max_gap=0;`).
- The required `docs-check` context at this head.

**Authority and evidence:**
- `docs/testing/CI_WORKFLOWS.md:728-731` lists `docs-check` among the required contexts on `dev`. AGENTS.md section 7 requires the required gates to pass, and the Tests lens requires that existing regressions remain green.
- CONTRIBUTING.md section 5 says new code in each language "follows its own immediately". The per-language idiom contracts are gated in the documentation workflow, with downward-only ratchets.
- Hosted `docs-check` job [114954498944](https://github.com/kebag-logic/milan-fpga/actions/runs/38292139020/job/114954498944) on head `37944f8a` concluded `failure` at step 33, "Boundary-unit naming ratchet" (`python3 scripts/measure_naming.py --check`). Steps 34-51 were skipped.
- The same step passed on base `c6bd08c6` (job 114666531975) and failed on `acadfacd` (job 114913979984) (`receipts/hosted-docs-check-base-and-r1.tsv`). The failure arrived with commit `7b491e59`.
- Local reproduction at this head gives rc 1: `STRIPPED: hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:KL_avtp_rx_monitor_ctx:dirty_p_o is still declared under that name and is no longer a candidate only because its comment no longer names the unit ... NAMING RATCHET: FAIL (0 new, 1 stripped)` (`receipts/gate-measure_naming-check.log`).
- Three skipped steps also fail locally, and every offender is a file this PR adds:
  - `measure_test_evidence.py --check`: `tb/verilator/milan_dp/stream_counters.py: UNEXPLAINED` DUT-source reader, which exceeds ratchet 0.
  - `check_py_idiom.py`: 5 unannotated and 5 undocumented public functions, against ratchet 0. That is 4 in `stream_counters.py` and 1 in `stream_counter_f5.py` (`--list`).
  - `check_cpp_idiom.py`: file-scope mutable 1, multi-declarator 1 and long function 1, each against ratchet 0. The first and third are in `stream_counters.hpp`, the second in `stream_counter_f5.cpp` (`--list`).
- The REVIEW READY comment and the PR's "How to validate" list name five documentation gates. They omit these four, so the claim that the local gates are complete does not hold.

**Impact:**
- A required context is red at the exact head, so the PR cannot merge (AGENTS.md section 7).
- Once the naming step is fixed, the hosted run will reach the three further failing ratchets.
- The new standing fixture violates the mandatory Python and C++ idiom contracts that every new file owes immediately.
- The test-evidence ratchet records the new suite's production-HDL reader as unexplained.

**Required outcome:**
- At a new head, the complete docs workflow passes, including `measure_naming --check`, `measure_test_evidence --check`, `check_py_idiom`, `check_cpp_idiom` and every later step.
- No ratchet budget is raised. Two routes are acceptable for the naming candidate:
  - restore the unit documentation on the `dirty_p_o` boundary;
  - or remove the candidate on its merits under the gate's own rule. A stripped comment is not acceptable.
- `stream_counters.py` carries a disposition in the test-evidence contract, the same way its sibling drivers do.
- The PR's validation list names the docs-workflow gates and their results.

**Verification:**
- The hosted `docs-check` succeeds on that exact head.
- Locally, all four commands above exit 0.
- The `--list` outputs show zero for the new files.

### F2 - MINOR - Conformance, Tests, Docs

**Where:**
- `tb/tools/torture_campaign.py`:
  - `:68-77`, the module law text;
  - `:732-775`, `INTERVAL_SOURCES` and `assert_frame_accurate`;
  - `:807-828`, `_perframe_deviant_sides` and `_perframe_findings`;
  - `:830-940`, `_interval_ticks_verdict` and `interval_ticks_agree`;
  - `:942-950`, the `check_concurrent_flowing` contract;
  - `:1514-1531`, `A_XSIDE_INTERVAL_AGREE` and `A_XSIDE_PEER_SEMANTICS`;
  - `:1573-1577`, `LICENSED_STREAMING_ASSERTS`;
  - `:1586-1595`, `A_MULTI_ALL_FLOWING`;
  - `:4412-4466`, the self-test that pins this behavior.
- `tests/steps/torture_plan_steps.py:291-299`, which requires `xside.interval-ticks-agree` in every licence-owning plan step.
- `docs/testing/726_STREAM_COUNTERS.md:166`.

**Authority and evidence:**
- Ruling 6125741685 and its addendum 6125845117 fix FRAMES_TX (Table 7.159) and FRAMES_RX (Table 7.157) at one count per AVTPDU. The acceptance bench check "compares each counter's per-second delta with the reference peer's, on both stream directions".
- Round-2 item 4 ([6129163001](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6129163001)) requires the bench grader's FRAMES_RX law to follow the ruling. R628-1-F4 named the impact: the grader passing a regression to one count per interval while flagging the ruled behavior.
- This round fixed `STREAM_INPUT_COUNTER_LAW`, `check_tv_tnv` and `grade_counter_semantics`. The cross-device helpers still state and enforce the replaced law: "FRAMES_TX/FRAMES_RX is an OBSERVATION-INTERVAL tick", and a side "advancing at wire frame rate is keeping the IEEE 1722.1-2021 Table 7-157 per-frame semantics instead".
- The executed demonstration (`receipts/probe-xside-law.jsonl`, `probe_xside_law.py`), at 4 s windows:
  - **Ruled pair.** DUT FRAMES_TX 32,000 with peer FRAMES_RX 32,000 gives `SKIP`, plus two attributed findings, one against each side.
  - **Regression on the DUT.** DUT FRAMES_TX 4 (one per interval) with peer 32,000 gives `PASS` "interval-conformant", and files the finding against the peer.
  - **Both sides one per interval.** 4 / 4 gives `PASS` with no finding.
  - **Same module, other helper.** `grade_counter_semantics("FRAMES_RX", 4, 4.0, stream_flowing=True)` gives `FAIL`. The module contradicts itself.
- `assert_frame_accurate("stream_output")` raises `CounterSemanticError`.
- The self-test at `:4452-4454` asserts the two-findings `SKIP` for two per-frame sides.
- The PR body declares the scope cut itself ("Historical cross-device interval-comparison helpers remain outside this receive-rate correction"). No public decision records it.
- `726_STREAM_COUNTERS.md:166` states that "the bench grader applies IEEE 1722.1-2021 Table 7.157 to FRAMES_RX", without that limit.

**Impact:**
- The repository's bench plan contract still asks every licence-owning step for an interval-terms comparison. It grades the ruled behavior as a deviation on both stream directions and passes the exact regression this issue removes.
- Any campaign verdict built on these assertions, at the merge-turn bench or in release campaigns, misreports the counter law.
- The documented claim overstates what was changed.

This is not wording only: it changes verdicts.

**Required outcome:** one of the following.
- The cross-device helpers, their assertion texts and their self-tests follow the ruling:
  - per-AVTPDU stream FRAMES_TX/FRAMES_RX is the conformant reading;
  - an interval-rate side on a flowing stream is the attributed deviation;
  - a self-test shows an interval-rate DUT beside a per-frame peer graded as the DUT's defect.
- Or the maintainer explicitly rules these helpers outside #726. The document then states that limit at `:166`, and a public Issue owns the repair. Under AGENTS.md section 7, a deferral without a ruling does not resolve the finding.

**Verification:**
- `torture_campaign.py --self-test` passes with the new cases.
- `probe_xside_law.py <checkout>` shows the ruled pair graded clean and the interval-rate regression graded as a failure or attributed finding against the DUT side.

### Suggestions (optional; no effect on coverage)

**S1 - SUGGESTION - Conformance, Tests.** The ruling's first window bullet (one notification in every fixed one-second window) cannot hold over long runs with this scheduler.
- Every gap exceeds 1000 ms (minimum 1000.982 ms), so each row's phase drifts later by at least about 1 ms per notification. A fixed window is then necessarily skipped at least once per about 1,000 windows at the shipping shape. At the largest shape, where maximum gaps reach 1012 ms, it can happen more often.
- The short runs already show it. Input 0 at both shapes has an empty window 1 for recipient A (shape 8: both recipients) with gaps of at most 1001.0 ms (`receipts/runs/clean-{1,8}/run.log`). This is a phase effect seeded before t=0, not a startup service delay.
- `726_STREAM_COUNTERS.md:52` describes windows 0 and 1 only as the "registration and startup transient".
- Suggested: state the drift mechanism in the document. The manager should confirm before the merge-turn link-tap measurement that bullets 2 and 3 (spacing and gap ≤ 1000 ms + service) govern long runs (see pending duties).

**S2 - SUGGESTION - Tests.** `stream_counters.hpp:142-165` grades gaps over every notification in `uns_log`, including those after `counter_watch_on` is cleared (`:132`), where streams stop and service is no longer measured.
- In the driver's `tx-nodirty` plant at shape 8, input 0's last gap (4.002 s to 5.004 s, ending after the watch closes) is 1001.928 ms against a 1001.738 ms bound (`receipts/gap-attribution-trace3-tx-nodirty-8.csv`). So a defect on the output path also fails `CADENCE` on an unchanged input row, and the plant is not attributable at that shape.
- No clean measurement is affected; every clean maximum is in-window. The shipping-shape plant claim in the document is accurate.
- Suggested: grade only notifications up to the end of the measured window, or keep measuring service until grading.

**S3 - SUGGESTION - Robustness** (carried from R628-1-S1, not taken). `KL_crf_rx.sv:644-698`: an accepted CRF PDU in the exact bind-rise cycle is not counted in the new era, whereas the talker keeps its start-cycle PDU (`KL_talker_diag_ctx.sv:248`). The effect is at most one packet per bind, and the ordering is stated in source.

**S4 - SUGGESTION - Tests** (carried from R628-1-S2, not taken). `sim_nxn.cpp:2596`: the `10000000L` "below silence timeout" bound is tied to the notify build's default clock.

### Residue (wording only; does not affect the verdict or coverage)

- **RS1** `sw/firmware/ctrl/aecp/README.md:59`. The text says "must call `aecp_changed()` with bit 8". `aecp.h:171-172` defines COUNTERS as bit 3 (value 8), and bit 8 would be masked off. Exact fix: "with the COUNTERS event (bit 3, value 8)".
- **RS2** `tb/verilator/milan_dp/README.md:500-501`, rows `[G]` and `[H]`. "interval-counter reset" and "reset interval counters" name the three reset-on-start counters, one of which is now per-AVTPDU. Exact fix: "per-run counter reset" and "reset the per-run counters".
- **RS3** Stale harness banners and comments. The checks themselves are correct.
  - `tb/verilator/crf_rx/sim_main.cpp:616-621,623`: the section banner and its print still say a burst moves "the counter" by one at the tick.
  - `tb/verilator/crf_rx/sim_main.cpp:636-638`: "FRX +1".
  - `tb/verilator/avtp_rxmon/sim_main_nx.cpp:72-73`: "(... serving it read 8000x high at class A)".
  - Exact fix: state that FRAMES_RX counts each accepted PDU (+10, +3), while the anomaly counters keep +1 per interval.
- **RS4** `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:68` is a 131-column banner line. Exact fix: rewrap it at the banner width.
- **RS5** `tb/tools/torture_campaign.py:4192,4202,4230,4257`. Self-test name and docstrings still describe "two readings" and the "mandated per-frame/per-interval split". Exact fix: reword them to the per-AVTPDU law. The F2 repair may cover this.

## Clean-lens lines

[R628] PASS Robustness - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:205-261`, `hdl/ieee1722/crf/KL_crf_rx.sv:487-490,630-698`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:946-953,983-985,1148-1172`, `hdl/milan/milan_datapath.sv:3155-3170,7966-7999`, plus the `before`, `mut-*` and `probe-*` runs.
- Wrap and boundary values: the `0xFFFFFFFA` seed, the `tx-saturate` probe, and the 65,534 + 3 batch with the `rx-saturation` plant.
- Reset and edge behavior:
  - the start-cycle PDU (tkdiag T11) and the CRF-only start reset (`crf-tx-noreset`);
  - the bind wipe and unbind survival (`crf-unbind-wipe`; the five bind-contract plants);
  - repeated bind, unbind, stop and restart.
- Event loss and pressure: the CRF skid behind the AAF strobe (never both in a cycle; `tx_count_o` is monotonic between resets, so the delta detector cannot spuriously fire), and the sticky per-descriptor pending bits that coalesce per-PDU pulses without starvation.
- Shape dependence: a feature-absent CRF descriptor (`frame_idx_i >= N_CTX_P` is ignored), and the shipping and largest shapes. S3 is optional.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2 MINOR) | Rulings 6125741685, 6125845117, 6126028604 and round-2 6129163001; acceptance 1-4; the four counter RTL files and the datapath feed and arbiter; pinned scheduler `KL_aecp_notify.sv:1098-1105,1449`; parent, frames-only and firmware window runs; 9 driver plants and 6 reviewer probes; counter-law table, trap (3) and grader (`torture_campaign.py`), including the cross-device helpers | R628-2 | `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb` |
| RTL | UNCLEAN (F1 MAJOR: the `dirty_p_o` boundary documentation contract) | `KL_talker_diag_ctx.sv`, `KL_crf_rx.sv`, `KL_avtp_rx_monitor_ctx.sv` and `KL_avtp_rx_monitor.sv` (widths, reset, NBA order, no CDC, no dangling `seen_f_r`/`iv_frx_r`); `milan_datapath.sv:3155-3322,7900-8000`; lint (90 ≤ ratchet), source-list and capture gates; routed utilization 49,427 LUT (+35 against the supplied 49,392), 53,378 FF, 87.5 BRAM; WNS +0.451 / WHS +0.036 ns and no negative-slack path in the Slow and Fast corner reports. Implementation inputs are sha256-equal to this head (`receipts/image-input-hashes-at-head.txt`); naming ratchet | R628-2 | `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb` |
| Robustness | CLEAN (S3 optional) | See the PASS line above | R628-2 | `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb` |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | behave 405/0; hosted `bdd-conformance` success (job 114954498915); R629-1 reproduction and 5 bind plants; 3 unit suites; stream_counters clean, frames-only and before at both shapes; 9 driver plants, 6 probes and the extra-shape plant; f5 clean and plants; torture self-test; docs-workflow ratchets (4 red) | R628-2 | `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb` |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR; RS1-RS5 residue) | `726_STREAM_COUNTERS.md`; REGISTER_MAP `:145-153,866-872,919,963`; Milan v1.2 audit `:218-230`; firmware AECP README `:52-66`; five dated findings notes; history traceability row (pinned to base); `docs/README.md` row; `tb/verilator/milan_dp/README.md`; RTL design notes; counters-contract feature; PR body; hosted and local docs gates | R628-2 | `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb` |

## Prior public review findings: status at this head

| Finding | Status | Evidence |
|---|---|---|
| R628-1-F1 = R629-1-F01 (MAJOR), era-wipe step requiring the removed `iv_frx_r` | **RESOLVED** | `counters_contract_steps.py:602-625` checks ten registers including `pdu_count_o` and the six anomaly flags. behave 405/0; hosted `bdd-conformance` success at head; the R629-1 reproduction passes; removing a retained reset, a flag clear, the lock drop, or making the wipe fire on unbind, each fails by name. The PR names the BDD gate. |
| R628-1-F2 (MINOR), output cadence not exercising FRAMES_TX; `before` driver accepting any failure | **RESOLVED** | The frames-only condition runs at both shapes, with clear wire `tu`/`mr`, zero TU/MR and one start (110/0, 481/0). The `tx-nodirty` plant gives 16 `OUTPUT_CADENCE` failures at shipping and escapes; my `aaf-tx-nodirty` probe is also caught. `stream_counters.py:164-171` requires exactly the TX/RX/CADENCE groups, and `726_STREAM_COUNTERS.md:63-86,143-145` states each output row's condition. The extra-shape attribution gap is S2. |
| R628-1-F3 (MINOR), four `milan_dp/README.md` passages | **RESOLVED** | `:93`, `:465-467`, `:499` and `:587-601` describe the per-AVTPDU law and the current `[F]` checks; `:1158` is per-AVTPDU. RS2 is remaining wording. |
| R628-1-F4 (MINOR), law table, trap (3), grader FRAMES_RX law, interval FAIL scenario | **RESOLVED for its named artifacts** | Feature `:42-48` (trap 3), `:312` (law row), `:373`, `:396` and `:410-412` (interval-rate FRAMES_RX FAIL scenario); `STREAM_INPUT_COUNTER_LAW["FRAMES_RX"]` per-frame under Table 7.157; `grade_counter_semantics` FAILs 30/30 s and 7,545/7,531 s. Its stated impact persists in the cross-device helpers, which are filed as F2. |
| R628-1-S1, S2 (SUGGESTION) | Not taken; carried as S3 and S4 | Optional. |
| R629-1-F02 (RESIDUE), stale PR-body sentence | **RESOLVED** | The current PR body no longer contains "No push or PR action has been performed". |

## Real limits

- Simulation compresses protocol time to 1000 cycles per protocol ms at a 50 MHz parameter. It shows protocol behavior, not physical link timing. Only two recipients were registered, so maximum controller fanout is not measured. Only three steady windows per row are graded (S1).
- No implementation run was made in this round. Area and timing are the author's published reports, whose five implementation-input hashes equal this head's bytes. The +35 LUT delta rests on the supplied 49,392 reference, which this round did not re-derive. Only constrained-path timing is evidenced.
- No manager source bank exists at this head, and none is claimed or inferred. No full parent, processor, gPTP or Yosys bank, builder bank, Docker, act or act self-test was run.
- The hosted snapshot (`receipts/hosted-check-runs-at-head-final.tsv`, 19:14 UTC) shows:
  - `docs-check` failure;
  - `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, `publication-census`, and `firmware-unit`/`-aecp-`/`-control-mutants`: success;
  - Verilator shards 0-4, `elaborate` and `firmware-srp-mutants`: still in progress;
  - `Physical gPTP`: skipped. A skip is not evidence.
- `ctrl_app_aecp_changed()` has no production caller in the opt-in split build (F5). The firmware window check drives the core directly; it is the integration contract the README states, outside #726's frozen scope.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Route F1 and F2 to the executor; re-review the corrected head under every lens whose scope the fix touches.
- Decide, before the merge-turn link-tap measurement, how ruling 6126028604's first bullet is judged over runs longer than about 1,000 s (S1).
- Accept the hosted and act evidence, including a green `docs-check` and the in-progress Verilator shards at the merge head.
- Run the current-dev merge-candidate validation (builder and native banks) and link its receipts on the PR.
- Merge-turn bench:
  - acceptance 1: the reference-peer reset comparison;
  - acceptance 2: the link-tap per-descriptor interval at both shapes;
  - acceptance 3: the controller display side by side with the reference peer, judged under the packet ruling (see F2 before relying on the in-tree grader).
- Carry RS1-RS5 to the residue checklist.

## Restore verification

I made no edit, commit, push or GitHub write. My only writes into the clone were five `scripts/__pycache__` files, left by the renderer gate run; I removed them.

At the end, `verify_tree.py` proved the clone byte-identical to HEAD (`receipts/verify-tree-final.txt`, `receipts/verify-submodules-final.txt`):
- every one of 1,300 tracked blobs has the HEAD blob id and mode on disk and a matching stage-0 index entry, out of 1,305 tree entries in total;
- the five gitlinks are stage-0 records at their pinned SHAs;
- the initialised protocol-processor (562 blobs), gptp-processor (104) and verilog-axis (214) submodules are at their pins and byte-identical, with clean status;
- `git status --porcelain --ignored --untracked-files=all` is empty.

Probes and builds used scratch copies or the driver's own scratch work directories.

## Reproduction

The scripts at the packet root are portable:
- `bg.sh` launches a detached run with its log and rc.
- `probe_counters.py <clone> <probe> <work>` plants one reviewer probe through the clone's own driver.
- `probe_bind_contract.py <clone> <scratch> <reproduce_contract.py>` runs the bind-era plants.
- `probe_xside_law.py <clone>` gives the F2 demonstration.
- `trace_counters.py` and `gap_attribution.py` produce the instrumented gap attribution.
- `verify_tree.py <checkout>` gives the byte, mode, index and pin proof.
- `sanitize.py` replaces local paths in receipts.

The stock commands are those in `docs/testing/726_STREAM_COUNTERS.md`, plus `cd tests && python3 -m behave --no-capture -f plain` and the docs-workflow gate commands named in F1.

R628-2 FINISHED
