[R601] POSITIVE - exact head ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937

# R601-1: external review of PR #719 (issue #640, Mark II lane M6, plan L9)

- Reviewer: [R601], external, cleared context. Round R601-1.
- Exact head: `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`, tree `fd457d2d4b18363e5bae2913c5da29f9734de544`.
- Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86`. The measured product commit is `930340145`. `git diff 930340145 ee0fc6fd9 -- hdl` is empty, so the routed RTL is the head's RTL.
- Overall verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. There are three SUGGESTIONs and one RESIDUE, and every lens is CLEAN at this head.

## Reconstruction (public state only)

I read the following, in this order:
1. `AGENTS.md` and `CONTRIBUTING.md`.
2. The frozen acceptance in the #640 issue body.
3. Manager rulings D1/D3/D7/D8 (5990755268) and the owner decisions of 2026-10-05 (D2: diagnostics stay in the shipping image).
4. The lane M6 assignment (6098405082), the executor's TAKEN (6098443919) and REVIEW READY (6103630528).
5. The PR #719 body.
6. `git diff e8454e27..ee0fc6fd9` and the eight commits, each one line with no trailers.
7. The published evidence `review-evidence/640-m6-r1` at `2d62247a`. I downloaded `author/HANDOFF.md` and `author/PR-BODY.md`, and their SHA-256 match its `MANIFEST.json` (`receipts/environment.txt`).

No private material was used. When my pass started, the PR held only the two review-start notices and no reviews (see "Prior public findings").

## What was executed (exact head, reviewer-run, in disposable exports)

Tool: scoped Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; `--version` prints `Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 in `receipts/environment.txt`). Host: CPython 3.14.7 and GNU make 4.4.1. These differ from the hosted pins (CPython 3.12.3, make 4.3).

The trees are `git archive` exports of the head and the base, plus the pinned submodule contents (under `scratch/`, not published). The protocol-processor copy was made into a throwaway local git repository because `scripts/pp_srcs.py` needs `git ls-files`.

| Run (head) | rc | Checks (failures) | Receipt |
|---|---:|---:|---|
| `make -C tb/verilator/avtp_rxmon` (incl. lockstep N=1, N=8 and `lockstep_mutants.py`) | 0 | 292 (0); lockstep 36/36 at each shape; mutants `5 checks: 5 PASS, 0 FAIL` | `receipts/head/avtp_rxmon.log` |
| `make -C tb/verilator/chmap_capture` (incl. lockstep 4 slots/1 LB stream and 32 slots/8 LB streams, mutants) | 0 | 847 (0); mutants `4 checks: 4 PASS, 0 FAIL` | `receipts/head/chmap_capture.log` |
| `make -C tb/verilator/tkdiag` | 0 | 101 (0) | `receipts/head/tkdiag.log` |
| `make -C tb/verilator/render_setpoint` | 0 | 277 (0) | `receipts/head/render_setpoint.log` |
| `make -C tb/verilator/milan_dp` (1x1 TDM8, N=4, divergent, N=8 loopback, pruned, gptp, gmstep legs) | 0 | 12,065 (0) | `receipts/head/milan_dp.log` |
| `make -C tb/verilator/capture_coherence VERILATOR_JOBS=4` (4 CPUs by affinity) | 0 | 21,194 (0); mutants `30 checks: 30 PASS, 0 FAIL`, including both re-anchored junction mutants (log lines 2024-2025) | `receipts/head/capture_coherence_VERILATOR_JOBS=4.log` |
| `python3 -I scripts/suite_tally.py receipts/head` | 0 | 34,776 checks, 0 in-suite failures | re-runnable |

Every count equals the executor's published HANDOFF table.

At the base (`receipts/base/`), the unchanged suites give the same counts: tkdiag 101 and render_setpoint 277. The changed suites differ only by their new legs:
- avtp_rxmon: 292 = 215 + 2 x 36 lockstep + 5 mutant checks.
- chmap_capture: 847 = 805 + 2 x 19 + 4.

Gates (`receipts/gates/`), each rc 0:
- In the export: `lint_rtl.py --check` (90 <= 90), `pp_resource_gate.py check-baseline`, `check_rtl_source_lists.py`, `docs_check.py`, `check_doc_style.py`, `gen_module_matrix.py --check`.
- Read-only, in the review clone, because they need git: `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sv_idiom.py`, `check_port_contracts.py`, `measure_test_evidence.py --check` (PASS; "can be lowered to 68"), `check_hygiene.py --check`, `check_doc_paths.py`, `DOC_MAP.gen.py --check` and `git diff --check e8454e27 HEAD`.

Not run: `gen_toc.py --check` and `check_em_dash.py` both exit 2 because the pinned Markdown renderer (html5lib) is absent on this host, and a shared install is not allowed. Hosted `docs`/`docs-check` are green at the head (see below).

Reference identity (`receipts/ref_identity.txt`, `scripts/ref_identity.sh`): each `reference/*_ref.sv` is the dev `e8454e27` module with only the module declaration renamed. The diff lines that remain are a header comment and an `$error` string: the lane left them unrenamed, and my rename rewrote them.

### Independent planted defects (reviewer-spelled, distinct from the lane's)

Each plant is applied by `scripts/probe_mutants.py` to a copy of the RTL. The copy is built through the suite's own `make lockstep-build` with the source and Mdir overridden, and both shapes run (`receipts/probes/`; wrap plants in `receipts/probes_wrap/`). All 17 plants were CAUGHT:

| Plant | Defect | First failing checks |
|---|---|---|
| RX-A-cap3 | penq admits a third waiting bundle (ring overwrites the one in service) | `[H1]` exact SI count, `[LS] H1`, `[GC] H1` |
| RX-B-ring2 | ring aliased to 2 slots | `[LS] H1/H4/SO` |
| RX-C-popidx | queued dispatch serves the second-oldest bundle | `[LS] H1/H4/SO` |
| RX-D-mircol | mirror write one column high | `[GC]` seeded signatures |
| RX-E-tvswap | TIMESTAMP_VALID column serves TNV | `[GC] H1/H2/H3` |
| RX-F-engonly | mirror ignores window writes | `[GC]` seeded signatures |
| RX-G-rowstride | read row stride 8, not 16 | N=8: `[GC]` seeded signatures (N=1 equivalent by construction) |
| RX-H-wpnoreset | ring write pointer survives reset | `[LS] H4/SO` |
| RX-I-wrapzero | mirror drops a write of zero | `[H3] MEDIA_LOCKED/STREAM_INTERRUPTED/MEDIA_UNLOCKED wraps ...` |
| RX-J-wrap31 | mirror keeps 31 bits | `[H3] FRAMES_RX adds the interval's 11 frames across the wrap` |
| CM-A-bank2 | beat bank aliased to 2 slots | `[SK]` three-channel, `[LS] SK/SO` |
| CM-B-bank3 | beat bank cycles 3 slots (overwrite only with 4 live beats) | `[LS] SO` at both shapes (the soak reaches a full skid) |
| CM-C-enq1slot | second commit of a beat names the next slot | `[SK]` mono and three-channel |
| CM-D-stashsmp1 | stash-closing commit takes smp1 | `[SK]` three-channel |
| CM-E-loopidxh | LOOP row ignores idxh | 32-slot/8-stream: `[LS] SO` (1 stream: equivalent) |
| CM-F-i2sswap | I2S L/R rows swapped | `[ST]` by value |
| CM-G-tdmbound | TDM bound `<=` (pair N reads a LOOP row) | `[LS] SO` |

The `milan_datapath` quadlet map was probed with `scripts/dp_probe.sh`, which builds the N=4 `sim_nxn` leg with `DP_SRC` set to a planted copy (`receipts/dpprobe/`):
- Clean control: 1,967/0.
- Quadlets 6/7 swapped (TV/TNV): caught by `[CTRS] @24 TIMESTAMP_VALID carries the tally` and `@28 ... is zero`.
- Reserved quadlets leaking the ML column: caught by `[CTRS] counters_valid = 0xFFF`, `the unclaimed quadlets 12..31 are zero` and `[CTRS-CRF]`.

One extra shape (`scripts/shape_probe.sh`, `receipts/shape/`): the capture lockstep at the shipping 8x8 capture parameters, `N_SLOTS_P=32, N_LB_STREAMS_P=1, N_LB_CH_P=2`. This is `loopback_lane: false` in `configs/endstation_ax7101_8x8.yaml`, giving `milan_datapath.sv:1196-1197`. All six `[LS]` checks hold (identical every cycle). Two `[SK]` value checks fail only because the harness's oracle assumes an 8-channel bucket, and the reference fails them identically (see S2).

## Findings

### R601-1-S1 SUGGESTION - Tests - `tb/verilator/avtp_rxmon/lockstep_mutants.py:61-90` - the wrap case has no planted defect of its own

- **Authority/evidence:** the assignment (6098405082) lists four hazard cases, wrap among them, and four planted defects.
  - The lane maps lost increment to `[H1]`, torn read to `[H2]`, wrong stream index to a new `[GC]` case and missed reset to `[H4]`.
  - HANDOFF section 3 states publicly that `[H3]` wrap is "covered by [LS]/[GC] equality".
  - All four named defects are present, and each fails its named check (5/5). The manager's review brief lists the same mapping.
  - Reviewer plants RX-I-wrapzero and RX-J-wrap31 make `[H3]`'s own named checks fail, so the wrap case is live and able to fail.
- **Impact:** none on the product. The durable repository campaign does not itself prove that `[H3]` can fail, so a later edit that weakens `[H3]` would go unnoticed by `lockstep_mutants.py`.
- **Optional outcome:** add one wrap plant whose named break is an `[H3]` check, for example a mirror that drops a zero write.
- **Verification:** `make -C tb/verilator/avtp_rxmon` prints `6 checks: 6 PASS, 0 FAIL`.

### R601-1-S2 SUGGESTION - Tests, Robustness - `tb/verilator/chmap_capture/Makefile:33-51` - the "8x8" lockstep shape is the loopback-on test shape, not the shipping 8x8 capture

- **Authority/evidence:** the shipping 8x8 has `loopback_lane: false`, which gives `LB_STREAMS_C=1, LB_CH_C=2` (`hdl/milan/milan_datapath.sv:1196-1197`).
  - The second lockstep shape is 32 slots with 8 streams x 8 channels: the `obj_nxn8 -GLOOPBACK_P=1` test configuration.
  - The Makefile comment calls it "the 8x8 shape" and HANDOFF calls it "the 8x8 parameters". The PR body states the parameters accurately ("32 slots/8 streams").
  - `receipts/shape/ship8x8.run.log` shows every `[LS]` identical at the shipping parameters. The milan_dp N=4 and 1x1 legs build the loopback-off datapath and pass.
- **Impact:** none found. The feature-disabled configuration is equivalent by reasoning and by the reviewer's probe, but the lane's own leg does not pin it.
- **Optional outcome:** either add the shipping 8x8 parameter set as a third lockstep shape, judging `[LS]` and `[ST]` and skipping the 8-channel `[SK]` oracles, or name the second shape "32 slots, eight loopback streams (the milan_dp `obj_nxn8` shape)".
- **Verification:** the lockstep passes at the added shape.

### R601-1-S3 SUGGESTION - Docs - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:299-300` - a stale word in an unchanged comment

- **Evidence:** the comment reads "served to the AECP mirror slices 10/11". The 12-word `diag_cnt_o` slices no longer exist. TV/TNV are now GET_COUNTERS columns 10/11 of `diag_q_o` (`:780-784`) and bypass `cnt_mirror_r`.
- **Impact:** wording only. No behaviour or claim changes.
- **Optional outcome:** "served as GET_COUNTERS columns 10/11 (`diag_q_o`) and the window's virtual LCTX words 26/27 from here".

### R601-1-R1 RESIDUE - Docs - PR #719 body, "Status" - the commit the sweep ran at is not stated

- **Evidence:** the body says "GREEN at `ee0fc6fd9`: full sweep 61 suites, 2,185,957 checks ...". HANDOFF section 3 shows the sweep ran at `8b209daa7`. `git diff --stat 8b209daa7 ee0fc6fd9` touches only `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md`, so RTL and tests are identical and no figure changes.
- **Exact fix:** "GREEN: full sweep at `8b209daa7` (RTL and tests identical to the head `ee0fc6fd9`, which adds two docs files): 61 suites, 2,185,957 checks, 0 in-suite failures (...)".

## Lens results (artifact-specific)

`[R601] PASS Conformance - KL_avtp_rx_monitor_ctx.sv:218-220,749-790; milan_datapath.sv:3444-3533,6334-6344; syn/ooc/pp_resource_baseline.json route-1x1 - GET_COUNTERS values and indexing unchanged against the base module and the Table 7-157 offset map.`

- **Quadlet map:** the table at `:3511-3528` maps quadlets 0..11 to the same `MON_*` columns as the base `ctr_blk_w` case. Quadlet 32 is still `CTR_VALID_SIN_C = 0xFFF`, every other quadlet is 0, and the `ctr_sin_w` index guard is unchanged.
- **Answer equality:** composed with the lockstep's per-cycle `dut_diag_q_o(col) == ref_diag_cnt_o[col]` (every sink plus out-of-range index 15, at N=1 and N=8), the answer equals the base answer. The integration `[CTRS]` checks catch both datapath plants.
- **Counter semantics:** the read is combinational in both forms, so latency is unchanged (D3). The commit interval, wrap and reset are covered by `[LS]`, `[GC]`, `[H3]`, `[H4]` and the soak, with the interval tick in the stimulus.
- **No interface change:** no register-map, wire-format or parameter-default change. No file under `hdl/common/csr`, `configs`, `constraints`, `syn` or `sw` changed, and no `parameter` line changed.
- **Route figures:** the base route figures (50,267 / 54,413 / 15,779 / 74+27 / +0.299 / +0.031) equal the committed `route-1x1` record. The route deltas and the credits are consistent with HANDOFF section 5: 418 = 175 + 243 and 468 = 212 + 256 LUT, 839 FF, and 552 = 167 + 385 out of context. The 49,561 LUT / WNS +0.141 >= 0.03 floor / gate PASS / no exception is the executor's published claim and is not reproduced here (see limits).

`[R601] PASS RTL - KL_avtp_rx_monitor_ctx.sv:285-297,418-475,772-788,856-873; KL_chan_map_capture.sv:732-749,826-881,1005-1081,1277-1332 - storage forms checked for invariants, widths and equivalence.`

- **Monitor ring:** `pq_wp_r == pq_rp_r + pq_cnt_r` holds on every enqueue and dispatch arm. A write happens only when `pq_cnt_r <= 1`, so the written slot is never `cur_idx_r == pq_rp_r - 1`; on the fast path `pq_wp_r == pq_rp_r`. The unreset ring and mirror are read only through slots written first, and reset clears every pointer and count (plants RX-B, RX-H and RX-A caught).
- **Mirror:** `MIRW_C = clog2(N*16)` is correct for N = 1, 4 and 8. Columns 10/11 bypass to the flops, and `milan_datapath` never presents columns 12..15.
- **Beat bank:** admission needs free >= 1, so at most 3 older live entries remain, from at most the 3 newest beats. The slot written belongs either to the beat 4 back or to the head being drained in that cycle (plants CM-A, CM-B and CM-C caught).
- **Source table:** the rows equal the old bucket/pair/half resolver for every source class, including the TDM and LOOP range guards. The LOOP index stays below `LB_PAIRS_C` under `lbok_f`, so dropping the old `LBPW_C'` truncation is equivalent. The Verilator 5.050 workaround resets are functionally invisible.
- **Other:** single clock, no CDC. Lint passes 90/90, and the hosted Yosys elaboration and shards are green. No block-RAM tile is added.

`[R601] PASS Robustness - receipts/probes/*, receipts/shape/ship8x8.run.log, sim_lockstep.cpp (both) - malformed, boundary, reset, capacity and configuration paths.`

- **Out-of-range and malformed input:** sink index 15 is read every cycle, and the soak includes out-of-range match indexes and malformed FSH.
- **Capacity:** third-bundle refusal is pinned by `[H1]` (RX-A caught).
- **Reset:** reset at every offset into a burst is covered by `[H4]` (RX-H caught).
- **Overflow and flush:** the soak sends faster-than-wire beats that overflow the skid, and flush kills; the skip counter moves. CM-B is caught only by a full skid.
- **Wrap:** wrap at 2^32 is covered (RX-I and RX-J caught).
- **Configuration:** the loopback-off capture holds `[LS]` (S2). The N=4 monitor is exercised in the avtp_rxmon NX stack and the milan_dp N=4 legs.

`[R601] PASS Tests - tb/verilator/{avtp_rxmon,chmap_capture}/{sim_lockstep.cpp,*_lockstep_wrap.sv,lockstep_mutants.py,Makefile}; tb/verilator/capture_coherence/mutants.py:169-178 - new tests can fail for their defects; existing regressions remain green.`

- **Mutant campaigns:** the lane's campaigns score 5/5 and 4/4. All 17 independently spelled plants are caught, including one per hazard class, two for wrap and two that only a full skid exposes.
- **Case quality:** each lockstep has positive, negative and boundary cases, with liveness guards on every case and soak.
- **Re-anchored mutants:** the capture_coherence junction mutants are still caught with their named breaks (30/30).
- **Regressions:** six suites pass at counts equal to the published table, and the unchanged suites match the base.
- **Oracle independence:** the references are frozen copies of the base, so the oracles are not the implementation. S1 and S2 are optional.

`[R601] PASS Docs - docs/testing/TESTING.md:582,587; docs/design/MARK_II_AREA_PLAN.md:555,888-932; docs/design/AREA_BUDGET.md:204-206; PR #719 body; review-evidence/640-m6-r1/author/HANDOFF.md - changed contracts and figures checked against code and receipts.`

- **Suite rows:** they describe the legs and plants as built.
- **Ledger tables:** they match HANDOFF and the record. The saving is stated as low in the 400-900 range, and the uncredited movement is disclosed.
- **Links:** the new anchor `#m6-intermediate-measurement` resolves (`docs_check`, `check_doc_paths` and `DOC_MAP` rc 0).
- **Port docs:** the new port is named at `KL_pp_shadow.sv:333`. No obsolete document was restored.
- **Wording:** R1 (RESIDUE) and S3 are wording only.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | monitor diag port and mirror; `milan_datapath` quadlet map and instance; route-1x1 record; issue and assignment acceptance; diff scope (no csr, config or parameter change); lockstep `[LS]`/`[GC]`; integration `[CTRS]` plants | R601-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| RTL | CLEAN | ring pointers and invariant, mirror table, beat-bank invariant, source-table decode, widths, reset and no-reset storage, lint 90/90 | R601-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Robustness | CLEAN | capacity and refusal, reset at every offset, overflow and flush, wrap, out-of-range indexes, loopback-off shipping 8x8 capture shape | R601-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Tests | CLEAN (S1, S2 optional) | both lockstep legs and mutant drivers, capture_coherence mutants, 6 suites at the head and 4 at the base, 17 reviewer plants and 2 datapath plants | R601-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Docs | CLEAN (R1 residue, S3 optional) | TESTING rows, the plan's M6 section and L9 pointer, AREA_BUDGET note, PR body, HANDOFF | R601-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |

## Prior public findings on PR #719

These were checked only after the verdict and ledger above were written. When this pass started, the PR held only the two review-start notices. The internal round [R600-1] (POSITIVE, published 2026-10-11T01:15:37Z during this pass) carries two findings. Both are resolved or retained at this head as follows, and neither changes my verdict or ledger:

- **R600-1-RES1 RESIDUE (Docs):** stale `KL_avtp_rx_monitor_ctx.sv` line citations at `docs/design/MEDIA_CLOCK_FOLLOWING.md:315, :317, :459, :960`. **Retained, independently reproduced.**
  - At base `e8454e27`, lines 465/491, 218, 486/491 and 173-174 hold the cited constructs: the start of `cnt_stream_interrupted_o`, `last_ts_o`, `f_subtype_w`/`fmt_ok_w`, and the SI/SM ports.
  - At the head the same constructs sit at 487/513, 221, 508/513 and 175-176.
  - This is a pointer-only defect that my own Docs pass did not catch. The executor's exact fix stands as published.
- **R600-1-S1 SUGGESTION (RTL):** at `KL_avtp_rx_monitor_ctx.sv:866`, `pdisp_new_w ? pq_wp_r : pq_rp_r` has equal arms, because `pdisp_new_w` implies `pq_cnt_r == 0`. **Retained, independently consistent:** my RTL pass reached the same equivalence and so did not plant the fast-path arm. It is optional.

## Hosted evidence at the exact head (snapshot 2026-10-11T01:17:59Z; `receipts/hosted_*.txt`)

- **Executed and green:**
  - `rtl-fast` (`firmware-unit`, `verilator-lint`, `yosys-elaboration`)
  - `elaborate`
  - `docs` (`docs-check`, `docs-check-no-git`, `wire-accountability`)
  - `bdd-conformance`, `changes`, `full-ci-gate`
  - Yosys shards 0-3/4
  - Verilator shards 0/5 and 3/5
- **Still in progress at the snapshot:** Verilator shards 1/5, 2/5 and 4/5 (`rtl-full`).
- **Skipped context, not executed:** `Physical gPTP (nightly and manual)`.

Hosted and act acceptance is the manager's.

## Real limits

- **Route and OOC not reproduced:** Vivado and builder banks are out of scope for this round. The 49,561 LUT / WNS +0.141 / gate PASS / no exception figures and the 418/468/552 credits rest on the executor's published HANDOFF. They were checked for arithmetic and against the committed record only. The route reports and gate output are not published; the checkpoint SHA-256 is.
- **Suites not run:** the full sweep, `milan_dp_gptp`, `csr`, `pp_shadow`, the `milan_dp_*` legs and the other shards. The executor's sweep at `8b209daa7` is the executor's claim.
- **Gates not run:** `gen_toc.py --check` and `check_em_dash.py` (html5lib absent). Host CPython 3.14.7 and make 4.4.1 differ from the hosted pins.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof.
- **Manager bank:** no manager source bank is claimed or inferred at this head.

## Pending manager duties

- Confirm hosted Verilator shards 1/5, 2/5 and 4/5 at this exact head.
- Build and validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, including the doc-anchor merge with the M2 lane in `MARK_II_AREA_PLAN.md` and `AREA_BUDGET.md`.
- Carry R601-1-R1 and the retained R600-1-RES1 to the residue checklist, and decide on S1-S3 and R600-1-S1.
- Decide on the shared mutation ratchet ("can be lowered to 68").
- D7: no re-record in this lane.

## Packet

- **Scripts:** `scripts/run_suite.sh`, `probe_mutants.py`, `dp_probe.sh`, `shape_probe.sh`, `ref_identity.sh` and `verify_clone.sh`.
- **Receipts:** under `receipts/`; every published file is listed in `MANIFEST.sha256`.
- **Build trees:** probe build trees and planted RTL copies were moved to `scratch/` after the runs and are not published. Each probe's `plant.diff` or log header records its exact edit.
- **Clone restored:** the review clone was restored and verified byte-exact (`receipts/verify_clone.txt`):
  - HEAD, tree, index and worktree are clean.
  - There are no untracked or ignored files.
  - The protocol-processor, gptp-processor and verilog-axis gitlinks match their checked-out heads, and those submodules are clean.

R601-1 FINISHED
