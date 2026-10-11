[R600] POSITIVE - exact head ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937

# R600-1: internal cleared-context review of PR #719 (issue #640, Mark II lane M6 / plan L9)

- Exact head: `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`, tree `fd457d2d4b18363e5bae2913c5da29f9734de544`
- Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (ancestor of the head; 8 one-line commits, no merges, no trailers)
- Measured product commit: `930340145`. `git diff 930340145 HEAD` touches no file under `hdl/`, `syn/`, `constraints/`, `sw/`, `configs/` or any submodule. Only tests, one reader table and docs change after it.
- Role: internal cleared-context reviewer. This round covers all five lenses.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head. There is one RESIDUE, a set of stale line citations in a design doc, given below with its exact fix. There is one SUGGESTION.

## What was reconstructed, in order

1. AGENTS.md and CONTRIBUTING.md: HDL style, the verification bar, the lens contract and the commit rule.
2. docs/README.md, the authority order.
3. Issue #640: the frozen body, the owner's 60 % decision, and the lane M6 assignment [6098405082](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098405082). That gives the scope (plan L9), the counter-semantics invariants, the 400-900 target, no register-map, wire-format or shipping-behaviour change, and the proof list.
4. Also from the issue: the TAKEN comment and REVIEW READY [6103630528](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6103630528).
5. `docs/design/MARK_II_AREA_PLAN.md` (L9 and the new "M6 intermediate measurement"), `docs/design/AREA_BUDGET.md`, and the gate record `syn/ooc/pp_resource_baseline.json` (route-1x1).
6. The STREAM_INPUT GET_COUNTERS face in `hdl/milan/milan_datapath.sv`, which follows the IEEE 1722.1 STREAM_INPUT counter block order and Milan Table 5.6.
7. Then the full diff `e8454e27..ee0fc6fd`, its history, and the published author evidence `review-evidence/640-m6-r1/author/{HANDOFF,PR-BODY}.md` at `2d62247a` (SHA-256 per its MANIFEST.json, checked).
8. Prior public review findings on the PR were read only after the verdict and the ledger below were written (last section).

## Independent analysis (summary)

**`KL_avtp_rx_monitor_ctx` PDU ring** (`hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:282-303, :467-475, :856-873`):

- Every accepted pulse writes `pq_ring_r[pq_wp_r]`. Dispatch happens only in `M_IDLE_S`, and sets `cur_idx_r` to the fresh slot (`pdisp_new_w`, when `pq_cnt_r == 0`, so `pq_wp_r == pq_rp_r`) or the oldest waiting slot.
- `penq_w` still refuses at `pq_cnt_r == 2` (`:418-419`). While a bundle is in service at `cur_idx_r = rp-1`, a write lands at `rp + cnt` with `cnt <= 1`, so it never hits the slot in service. If enqueue and dispatch happen in the same cycle at `cnt == 2`, the write goes to `rp+2` while the old in-service slot is `rp-1`; distinct modulo 4.
- `cur_w` is read only in `M_PDEC_S` and `M_PWR_S` (`:493-587`, `:603-617`, `:1004-1017`), all reached through a dispatch. So the unreset ring is never read before it is written.
- `pq_cnt_r` keeps its old transition table, so capacity and refusal are unchanged. Reset clears `pq_wp_r`, `pq_rp_r`, `cur_idx_r`, `pq_cnt_r` and `pq_s_r` (`:795-799`).

**Counter table** (`:774-788`):

- One `N x 16` write-through table is written at `{stream, cntw_col_w}` with `cntw_col_w` in 0..9. It is read asynchronously at `{diag_ridx_w, diag_col_i}`.
- Columns 10 and 11 come from the TV/TNV flops, exactly as before. An out-of-range sink still clamps to 0.
- The read stays combinational, so GET_COUNTERS latency is unchanged.

**`milan_datapath` quadlet map** (`hdl/milan/milan_datapath.sv:3507-3533`):

- `MON_*_C` (`:3444-3446`) equals the monitor's `C_*_C` (`KL_avtp_rx_monitor_ctx.sv:241-249`). Quadlets 0..11 map to the same columns as the old slice select: @24 TV, @28 TNV, @32 UF, @36 LT, @40 ET, @44 FRX.
- Quadlet 32 is still `CTR_VALID_SIN_C = 0x0FFF`, and every other quadlet still reads 0. The register is the same `ctrq_word_r`, so the AECP read timing is unchanged.
- No CSR, register-map or wire-format file changed. The only `KL_pp_shadow.sv` change is a comment.

**`KL_chan_map_capture` source table** (`hdl/ieee1722/aaf/KL_chan_map_capture.sv:1269-1332`):

- The row order is 0 silence, then 1/2 I2S `[47:24]`/`[23:0]`, then 3 tone, then TDM `4+2p+half`, then LOOP `CAND_LOOP_C+2(idxh*PPS+idx)+half`. This reproduces the old bucket, pair and half selection for every class.
- Disabled, illegal and out-of-build entries resolve to row 0. `SRC_TONE_C` gives the same sample on both halves.

**Skid and beat bank** (`:826-864, :1005-1008, :1054-1069`):

- Admission is unchanged (`:870-881`). `enq1` implies `enq0`.
- Live entries are a FIFO suffix and each admitted beat contributes at least one entry. So with `n >= 1` new entries, at most `4 - n <= 3` older beats are live after the same-cycle drain, and `beat_wp_r` never names a live beat.
- The head drained in the cycle its slot is overwritten is read combinationally before the edge. Killed heads are skipped with `push_ram_w = 0`.

The two ways a beat can commit are reconstructed exactly from `{cm0_l_w, smp0, smp1}` captured at enqueue. No parameter default or port width changed.

## Reviewer executions (all at the exact head, pinned simulator)

The simulator was identified first: `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version` prints `Verilator 5.050 2026-07-01 rev v5.050`.

All runs used a disposable clone of the head with the `protocol-processor` (`2ad2f845`), `gptp-processor` (`5dce647a`) and `verilog-axis` (`48ff7a7e`) gitlinks checked out. Receipts are under `receipts/`.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/avtp_rxmon` (legacy, NX, lockstep N=1 and N=8, `lockstep_mutants.py`) | rc 0. Lockstep N=1 36/0 and N=8 36/0. Mutants `5 checks: 5 PASS, 0 FAIL`; each named check failed (H1, H2, GC, H4). | `avtp_rxmon_run.log/.rc` |
| `make -C tb/verilator/chmap_capture run` (base sim, netcheck, lockstep 4 and 32 slots, mutants) | rc 0. Lockstep 19/0 and 19/0. Mutants `4 checks: 4 PASS, 0 FAIL` (ST, SK mono, SK three-channel). | `chmap_capture_run.log/.rc` |
| `make -C tb/verilator/tkdiag` | rc 0, 96/0, mutants 5/5 | `suite_tkdiag.log/.rc` |
| `make -C tb/verilator/render_setpoint` | rc 0, 131/0, mutants 15/15 | `suite_render_setpoint.log/.rc` |
| `make -C tb/verilator/capture_coherence all` on 4 CPUs (the hosted runner's count) | rc 0. Junction 20,832/0, dp 332/0, mutants `30 checks: 30 PASS, 0 FAIL`, including the two re-anchored junction mutants (`ce550952` stage read, no walk snapshot) | `suite_capture_coherence.log/.rc` |
| milan_dp `sim_nxn` 4x4 (Arty entity, N=4), through the suite's own recipe | rc 0, 1967/0 | `nxn4_clean.log/.rc`, recipe `scripts/nxn_only.mk` |
| milan_dp `sim_nxn` 8x8 (`-GN_STREAMS=8 -GLOOPBACK_P=1`, the suite's obj_nxn8 flags) | rc 0, 3751/0 | `nxn8_clean.log/.rc` |
| `python3 scripts/lint_rtl.py --check` (pinned simulator) | rc 0, `90 violation(s) <= ratchet 90` | `lint_rtl_check.log/.rc` |
| `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | rc 0, 50 files. None of the changed RTL except `KL_pp_shadow.sv` (comment only), so the PR-BODY's "ooc endpoints not re-run" reason holds. | `ooc_pp_shadow_srcs.txt` |

### Reviewer plants, independently spelled (`scripts/r600_plants.py`; diffs and logs in `receipts/plant_*`)

| Plant | Defect | Result |
|---|---|---|
| R1 | monitor: the queued dispatch serves `pq_rp_r + 1` (wrong ring slot) | caught at N=1 and N=8, `[LS]` |
| R2 | monitor: `pq_rp_r` survives reset (missed reset, pointer form) | caught at N=1 (`[LS] H4`) and N=8 |
| R3 | monitor: the counter mirror writes sink 0's rows only (wrong stream index, write side) | caught at N=8 (`[GC] every sink answers its own row and column`). N=1 has a single sink, so the plant is equivalent there and correctly not caught. |
| R4 | monitor: column TV serves the TNV tally | caught at N=1 and N=8, `[GC]` |
| C1 | capture: a LOOP entry ignores its half bit | caught at both shapes, `[SK]` |
| C2 | capture: the beat bank stores smp1/smp0 swapped | caught at both shapes, `[SK]` |
| C3 | capture: the second commit of a beat names the next bank slot | caught at both shapes, `[SK]` |
| C4 | capture: the I2S rows are swapped in the source table | caught at both shapes, `[ST]` |
| P1 | datapath: quadlets @24 and @28 swapped (TV and TNV) | caught by milan_dp nxn 4x4: `[CTRS] @24 TIMESTAMP_VALID carries the tally` and `[CTRS] @28 TIMESTAMP_NOT_VALID is zero` |
| P2 | datapath: reserved quadlets serve a counter (`counters_valid` kept) | caught by milan_dp nxn 4x4: `[CTRS] the unclaimed quadlets 12..31 are zero` |

A plant counts as caught only when the binary exits non-zero AND prints a `[FAIL]` line. P1 and P2 used the same rule (rc 2 with named `[FAIL]` lines). The datapath plant diffs are in `receipts/datapath_plants.diff`.

### Published measurement, checked for consistency (not re-measured; see limits)

- The base row equals the gate record `route-1x1`: 50,267 LUT, 54,413 FF, 15,779 slices, 74/27 RAMB, WNS +0.299, WHS +0.031 (`syn/ooc/pp_resource_baseline.json`).
- The candidate deltas are -706 LUT, -958 FF, +12 slices, 0 RAMB, WNS -0.158 and WHS -0.013. All are within the recorded tolerances (LUT 500, FF 600, SLICE 80, RAMB 0, WNS/WHS 0.25), and +0.141 / +0.018 are above the floors of 0.03 / 0.0. That is consistent with the published gate PASS with no exception.
- The credited figures add up:
  - post-synthesis 418 = (993-818) + (1,107-864);
  - routed 468 = (966-754) + (1,069-813);
  - FF 839 = (1,353-691) + (1,360-1,183);
  - OOC 552 = 167 + 385.
- All three sit low in 400-900, below the 600 central figure, as the plan and the PR state. Only the changed blocks are credited.

### Hosted at the exact head (inspected only; the manager owns hosted acceptance)

Polled read-only; the final poll is at the UTC time in `receipts/hosted_check_runs.polled_utc`, with the table in `receipts/hosted_check_runs.tsv`.

- Completed success: `changes`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3/4, Verilator shard 3/5.
- `Physical gPTP (nightly and manual)` completed as skipped. That is a skipped context, not an executed job.
- Still in progress at the final poll, so no verdict was read for them: `firmware-unit`, `elaborate`, Verilator shards 0, 1, 2 and 4/5.

## Findings

### R600-1-RES1: RESIDUE (Docs, wording only): stale code line citations to the monitor

- Location: `docs/design/MEDIA_CLOCK_FOLLOWING.md:315, :317, :459, :960`.
- Evidence: these rows cite `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:465-491`, `:218`, `:486-491` and `:173-174`. They were exact at base `e8454e27` (the format family compare, `last_ts_o`, `fmt_ok_w`, and the SI/SM counter ports). This PR's insertions shift them: at the head they land on the ring write port, `diag_idx_i`, the `f_*` fields and the ML/MU ports.
- Impact: none on any figure, verdict, test, code or clause claim. The statements stay true, but the pointers lead a reader to the wrong lines.
- Exact fix in `docs/design/MEDIA_CLOCK_FOLLOWING.md`:
  - `:315`: `KL_avtp_rx_monitor_ctx.sv:465-491` -> `KL_avtp_rx_monitor_ctx.sv:487-513`
  - `:317`: `KL_avtp_rx_monitor_ctx.sv:218` -> `KL_avtp_rx_monitor_ctx.sv:221`
  - `:459`: `KL_avtp_rx_monitor_ctx.sv:486-491` -> `KL_avtp_rx_monitor_ctx.sv:508-513`
  - `:960`: `:173-174` -> `:175-176`
- Verification: `sed -n` at each new range shows the cited construct.
- The same document's `milan_datapath.sv` citations were already off at base and are not attributed to this PR.

### R600-1-S1: SUGGESTION (RTL): redundant select on the dispatch slot

- Location: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:866`.
- `cur_idx_r <= pdisp_new_w ? pq_wp_r : pq_rp_r;`. `pdisp_new_w` implies `pq_cnt_r == 0`, so `pq_wp_r == pq_rp_r`, and both arms are equal. `cur_idx_r <= pq_rp_r;` is equivalent and removes a 2-bit mux that synthesis cannot prove redundant.
- Optional; no coverage impact.

No BLOCKER, MAJOR or MINOR finding.

## Lens results (each with its examined artifacts at this head)

[R600] PASS Conformance: `hdl/milan/milan_datapath.sv:3444-3533`, `KL_avtp_rx_monitor_ctx.sv:241-249, :736-788`, plants P1/P2, lockstep `[GC]/[H1]-[H4]`.

- The quadlet-to-column map equals the old slice map for all twelve STREAM_INPUT counters (1722.1 block offsets @0..@44). Quadlet 32 is `counters_valid` 0x0FFF, and the rest read 0.
- Counter values, commit interval, wrap, reset and read-during-update coherence are equal to dev `e8454e27` in every cycle at N=1 and N=8.
- No register-map, wire-format or parameter-default change (diff of `hdl/common/csr`, `docs/reference/REGISTER_MAP*.md` and all `parameter` lines is empty).
- Acceptance: lockstep, hazard cases, the five named suites, the route and gate under the M0s recipe, and the saving reported honestly. All met by evidence. The route is published-only; see limits.

[R600] PASS RTL: `KL_avtp_rx_monitor_ctx.sv:282-303, :418-475, :774-873, :903-1023`, `KL_chan_map_capture.sv:729-881, :1002-1072, :1269-1332`.

- The ring slot-liveness and capacity proofs hold. Every unreset LUT-RAM (ring, counter table, beat bank) is read only after its own write, and every pointer is reset.
- Widths are sound: `MIRW_C`, `CANDW_C`, the 2-bit ring and bank pointers and the 3-bit skid count.
- The case statements are complete. The single write port of each new memory is inferred as LUT-RAM, which matches the published primitive mapping (RAM32M/RAM32X1D, no new RAMB).
- WNS +0.141 is above the floor, with the worst path in the unchanged processor.

[R600] PASS Robustness: lockstep `[SO]` soaks at both shapes in both legs, `[H4]`, `[H1]`, plants R1/R2/C3.

- Covered: resets at every offset into a burst, a third waiting bundle refused, out-of-range sink 15 compared every cycle, and malformed formats, `tv`/`tu`/`mr` toggles and late/early stamps in the soak.
- Also covered: faster-than-wire loopback beats with skid refusal, flushes and recentres, and illegal and reserved map entries.
- Feature-off: the capture with `LOOPBACK_P=0` elaborates and passes in the nxn 4x4 leg.

[R600] PASS Tests: `tb/verilator/avtp_rxmon/{sim_lockstep.cpp,avtp_rxmon_lockstep_wrap.sv,lockstep_mutants.py,reference/}`, `tb/verilator/chmap_capture/{sim_lockstep.cpp,chmap_lockstep_wrap.sv,lockstep_mutants.py,reference/}`, `tb/verilator/capture_coherence/mutants.py:171-178`.

- Both references are byte-identical to the base files apart from the module name (`diff` against `git show e8454e27:<path>`).
- Every lane mutant fails its named check, and eight independent reviewer plants are caught.
- The datapath quadlet map is pinned by milan_dp `[CTRS]` checks (plants P1/P2).
- The two re-anchored capture_coherence junction mutants are still caught.

[R600] PASS Docs: `docs/testing/TESTING.md:582,587`, `docs/design/MARK_II_AREA_PLAN.md:555, :888-932`, `docs/design/AREA_BUDGET.md:204-206`, the module headers in both RTL files, `scripts/measure_test_evidence_readers.py:62-70`, the PR body and the HANDOFF.

- Every figure matches the published measurement and adds up. The scope not taken (talker counters, render set-point) is stated with its reason.
- The suite rows describe the harnesses as they are. The new ports are documented inline.
- RES1 is wording only and does not leave this lens unclean.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:3444-3533`, monitor `:241-249,:736-788`, plants P1/P2, lockstep GC/H1-H4 at N=1/8 | R600-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| RTL | CLEAN | monitor `:282-303,:418-475,:774-873,:903-1023`; capture `:729-881,:1002-1072,:1269-1332` | R600-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Robustness | CLEAN | `[SO]` soaks both legs/shapes, `[H4]`, `[H1]`, plants R1/R2/C3, nxn 4x4 (loopback off) and 8x8 | R600-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Tests | CLEAN | both lockstep legs, references, lane mutants, 8 reviewer plants, P1/P2, capture_coherence re-anchored mutants | R600-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Docs | CLEAN (RES1 is RESIDUE) | TESTING.md rows, MARK_II_AREA_PLAN M6 section, AREA_BUDGET note, RTL headers, reader table, PR body, HANDOFF | R600-1 | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |

## Real limits

- The integrated route, the post-synthesis and OOC figures, and the gate `check --endpoint route-1x1` were not reproduced. They are the author's published receipts at `930340145`, whose RTL is byte-identical to this head. They were checked here for internal and arithmetic consistency and against the recorded tolerances only.
- The base route's reports were removed by their owner. The base row was matched to the gate record, not to those reports.
- Not run by this reviewer: the full milan_dp target (only the 4x4 and 8x8 `sim_nxn` legs were run, through its own recipe), csr, pp_shadow, the full sweep, the parent/processor/gPTP/Yosys/builder banks, `xvlog_gate.py`, and act. No manager source bank ran at this head, and none is claimed.
- Physical calibration was NOT RUN. Field skips (for example `tsn_fuzz`'s declared skips) are not hardware proof.
- The talker-counter and render set-point blocks are unchanged by design. The plan records that, and no saving is credited for them.

## Clone integrity after probes

- Every probe and plant ran in a disposable clone under `scratch/`. The review clone was never edited.
- Final state of the review clone (`receipts/clone_integrity.txt`):
  - HEAD is `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`, and both the tree and the index tree are `fd457d2d4b18363e5bae2913c5da29f9734de544`;
  - `git status --porcelain`, `git diff-index --cached HEAD` and `git diff-files` are all empty, and no assume-unchanged or skip-worktree flag is set;
  - the `protocol-processor` (`2ad2f845`), `gptp-processor` (`5dce647a`) and `third_party/verilog-axis` (`48ff7a7e`) gitlinks are mode 160000, stage 0, and checked out at those revisions;
  - `external` and `third_party/lwSRP` are uninitialised, exactly as at the start.

## Pending manager duties

- Hosted acceptance of `rtl-fast` and the exact-head Verilator shards. Several were still in progress at this reviewer's last poll.
- Validating the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`): builder and native banks, with receipts linked on the PR.
- Carrying R600-1-RES1 to the residue checklist.
- The external review ([R601]), and post-merge containment.
- The author notes that `measure_test_evidence.py --check` reports that the shared mutation ratchet could be lowered. That is left to the manager.

## Prior public review findings on PR #719

This section was read after the verdict and the ledger above were written. At the time of reading, PR #719 had two issue comments and no review or inline comment:

- `6103802261`, the R600-1 start notice;
- `6103827835`, the R601-1 start notice.

Issue #640's thread has no review finding for lane M6. No prior public finding exists on this PR, so none is resolved or retained. The external round R601-1 is running independently and was not read.

R600-1 FINISHED
