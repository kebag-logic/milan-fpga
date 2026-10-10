[R593] POSITIVE - exact head 9d42762c555118e3ea86665bf7d8c6ef673698d3

# R593-1: external review of PR #713 (issue #640, Mark II lane M7, plan L10a)

- Head `9d42762c555118e3ea86665bf7d8c6ef673698d3`, tree `4291b752854f3aebb6fa539cd834ef76c936033b`, source base dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Gitlinks at the head: `gptp-processor` `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (equal to the head of donor PR Mister-M-alt/FPGA-gPTP#78, base `5dce647a`), `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five are clean: no BLOCKER, MAJOR or MINOR is open.
- Open items: two RESIDUE wording items and three SUGGESTIONs, listed below.
- Prior public review findings on PR #713: none. At this round's start the PR held only the two manager review-start comments, so there was nothing to resolve or retain.

## Reconstruction

Read in this order:
1. AGENTS.md and CONTRIBUTING.md.
2. The issue #640 body and its decisions: D1, D3, D7 and D8 (5990755268), the owner's block-RAM decision, and the M7 lane assignment (6097272538).
3. The executor's TAKEN (6097298086) and REVIEW READY (6100339945) comments.
4. The PR #713 body.
5. The full diff `e8454e27..9d42762c` and its 12 commits, plus the submodule diff `5dce647a..18dd997b`.
6. The published evidence at `3e0f36b8`/review-evidence/640-m7-r1. The `MANIFEST.json`, `HANDOFF.md` and `PR-BODY.md` digests match the manifest's published digests; see `receipts/artifacts.txt`.

The frozen lane scope (plan L10a):
- Move eligible plane tables, or narrow their indices.
- Keep the dual-read operand files.
- Target about 500 LUT (300 to 700), reported honestly.
- Block-RAM growth only within the firmware ledger.
- Any read-latency change needs deterministic bounds.
- No change to gPTP behaviour, its register map or its timestamp path.
- Proof: the named suites, a per-table lockstep with planted defects, and the integrated route and gate through the M0s recipe. The record is not re-recorded before M9 (D7).

## Independent results at this head (receipts under `receipts/`)

| Run | Result | Receipt |
|---|---|---|
| `gptp_tables` lockstep, unmodified head (disposable copy, Verilator 5.050) | 21/21, rc 0; 29,100,030 cycles; rx 41,121 good / 33,528 overflow / 12,226 bad, lanes 0xff, 256 deep; tx 7,979 frames, counts 0x114, 27 deep; ledger heads 0xff, 3 deep; results heads 0xff; timer slots 0x3f | `tables-head.log` |
| Author's 15 planted controls (`mutants.py`, private copies) | 15/15 caught, each by its own table's named check | `driver-mutants.log` |
| Reviewer probe: TX decode `<` to `<=` | caught by `tx_fifo lockstep` (2,538,969 cycles) | `tables-tx_decode_off_by_one.log` |
| Reviewer probe: RX lane as popcount-1 (differs only for a non-contiguous tkeep) | caught by `rx_fifo lockstep` (101,132 cycles), so corrupted enables reach the comparison | `tables-rx_top_popcount.log` |
| Reviewer probe: RX FIFO DEPTH left in octets (8x deep) | caught by `rx_fifo lockstep` | `tables-rx_depth_octets.log` |
| Reviewer probe: result-queue sequence read from the ledger tail | caught by `results lockstep` | `tables-results_seq_from_tail.log` |
| Reviewer probe: ledger tag written constant 1 | NOT caught; explained in S-01 (the tag is 1 for every frame the engine can emit) | `tables-ledger_tag_constant.log` |
| Equivalent probe: timer skips the deadline write on disarm | stays 21/21, so the oracle does not over-constrain the storage | `tables-timer_skip_disarm_write_equiv.log` |
| Coverage probe: counters printed at each phase boundary (stimulus unchanged) | live after warm reset 1 (+4,708 programs, +1,839 results compared); after warm reset 2 the plane wedges in the known pre-existing fence defect (7 programs, 0 results compared) | `tables-phase_coverage_print.log` |
| `gptp_shadow` run | 309/309 | `gptp_shadow_run.log` |
| `gptp_shadow` controls (the `no_tag_check` anchor this PR moved) | 9/9, `no_tag_check` caught by its named check | `gptp_shadow_mutants.log` |
| `gptp_plane` run | 29/29 | `gptp_plane_run.log` |
| Donor engine bench (`gptp-processor/tb/verilator/engine`) | 1,613/1,613 in each of 3 shapes | `gp_engine.log` |
| Donor `make contract`, `lint`, `docs` | rc 0 each; source evidence 20 exact, 0 findings | `gp_contract.log`, `gp_lint.log`, `gp_docs.log` |
| Lane-count elaboration probe, `TDATA_WIDTH_P` 8/32/48/56/64/72/128 | the guard refuses 9 and 16 lanes; 1 to 8 elaborate | `lane_width_lint.log` |
| Exhaustive model of the TX count decode and RX highest-lane encoding, lane counts 1 to 8 (every gearbox index, every tkeep mask, plus the never-written word) | PASS, 0 mismatches | `lane_decode_enum.log` |
| Lint ratchet (`scripts/lint_rtl.py --check`) | PASS, 90 <= 90 | `lint_rtl_check.log` |
| Doc gates: `check_gptp_docs` (with and without submodule), module matrix, doc style, `docs_check`, submodule docs and diagram, time-sync diagram, `git diff --check` base..head, `pp_resource_gate.py check-baseline`, `check_rtl_source_lists` | rc 0 each | `gate_*.log` |

## Lens results (each with what was examined)

```text
[R593] PASS Conformance — issue #640 assignment 6097272538 vs hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:230-290,423-473,567-611,777-883, KL_gptp_txret.sv:328-360,530-600,630-720, gptp-processor hdl/common/KL_gptp_timer.sv:73-120, syn/ooc/pp_resource_baseline.json route-1x1, docs/design/AREA_BUDGET.md:395-411 — every frozen item checked. (1) Five tables moved, none narrowed; the dual-read rf_r is untouched. (2) Widths, depths and read latency are unchanged: both FIFOs keep ADDR_WIDTH = $clog2(BYTES/KEEP_W_C), every RAM keeps one write port and a combinational read. (3) The module ports, CSR face and timestamp path are unchanged: the diff touches no port list, no CSR file, and neither ts_arr nor the txret reconstruction arithmetic. (4) Block RAM is freed (RAMB18 27 to 25), never added. (5) The claimed route (49,898 LUT, 74/25 RAMB, WNS +0.122, WHS +0.019) is within every route-1x1 tolerance and floor: the WNS fall limit is 0.25 and the floor 0.049, so 0.122 passes. (6) The record is unchanged, consistent with D7. (7) The below-range saving (plane -107 to -253, plan 300-700) is stated as not met, in the PR, the issue and the plan. The decision on accepting it is the manager's.
[R593] PASS RTL — KL_gptp_shadow.sv:269-272,314-324,431-473,568-611,777-883; KL_gptp_txret.sv:339-357,537-541,587-599,633-645,693-737; KL_gptp_timer.sv:76-112; third_party/verilog-axis/rtl/axis_fifo.v:137,180-185,221-246,260-345,372-400 — the axis_fifo depth is in beats when KEEP_ENABLE=0, so the address width is unchanged at every lane count. tuser bit 0 alone is judged bad (mask/value 1). The FRAME_FIFO path never substitutes USER_BAD_FRAME_VALUE (MARK_WHEN_FULL=0). The RX highest-lane encoder is the base serializer's rule, applied before the FIFO instead of after it. The TX count decode equals the base gearbox mask for every reachable gb_idx_r: gb_keep_r was only ever lanes 0..idx-1, and no other path cleared gb_idx_r. ledger_ram, result_ram and deadline_ram take exactly the base write conditions; reads are combinational at the same addresses, so write-during-read returns the old word as the flip-flop arrays did. The only reads of never-written words are guarded by n_led_r != 0, txts_valid_o (the engine samples on accept only: KL_gptp_engine.sv:350,372,484-489), or armed_r. In 4-state sim each unguarded X term is ANDed with a 0. Single clock domain; no CDC touched.
[R593] PASS Robustness — receipts tables-head.log, tables-rx_top_popcount.log, tables-phase_coverage_print.log, lane_decode_enum.log, lane_width_lint.log — non-contiguous and all-clear tkeep give the same lane as before: proven exhaustively, and reached in simulation (popcount probe caught). Overflow, bad, runt and oversize frames resolve identically: rx strobes are compared every cycle, with 33,528 overflow and 12,226 bad. A warm reset in traffic leaves the RAMs uncleared, and each reader is gated to entries written after the reset: the ledger, results and timer are compared after reset 1 with live traffic. Backpressure: 11.2 M stalled TX cycles. Configuration: the new guard refuses more than 8 lanes; TXTS_CAP_N_P wraps explicitly, so non-power-of-two depths keep their index range. The pre-existing fence/tx_fifo wedge is the manager's separately filed issue: dev and head behave identically in it, and it is not counted here.
[R593] PASS Tests — tb/verilator/gptp_tables/{gptp_tables_wrap.sv,sim_main.cpp,mutants.py,README.md,Makefile}; receipts driver-mutants.log and tables-*.log — every oracle is the PREVIOUS storage form, not a copy of the new one. It uses an axis_fifo with KEEP_ENABLE=1, DEPTH 2048 octets and eight tkeep bits (wrap:168-210, 253-292), the old gearbox enables (wrap:236-247), and reset-cleared register arrays written under the base conditions from untouched signals (wrap:330-356, 382-391). The comparison gates are the consumers' real sampling conditions. The 15 author controls re-ran 15/15 by name. 4 of 5 independent reviewer defects were caught by the named check; the fifth is unobservable by construction (S-01); one equivalent change stays green. The suite is in the default sweep (`run_all_suites.sh --list`), so the hosted Verilator shards run it.
[R593] PASS Docs — docs/design/MARK_II_AREA_PLAN.md:560,672-717,851-852; docs/design/AREA_BUDGET.md:197-200,267-268; docs/testing/TESTING.md:150,409-410,601; tb/verilator/gptp_tables/README.md; regenerated MODULE_MATRIX and README-tests; donor docs/MANAGER.md:35-56 — every figure re-derived. Routed deltas: -369 LUT = -229 - 414 + 274, FF -1,193, slices -6, WNS -0.177, WHS -0.012. FIFO widths: 74/73 bits before, 69 after. Primitive counts: ledger 4 RAM32M + 1 RAM32X1D for 21 bits, results 16 + 1 for 89, timer 5 + 2 for 32. Firmware tiles: 87.5 to 86.5. Donor: -105 LUT, -256 FF, LUTRAM 466 to 490 = +24 = 5x4 + 2x2. The below-range saving is stated plainly, D7 is respected, and no authoritative page keeps a stale statement about the changed storage. All donor pin links name 18dd997b; the doc gates are rc 0. Two wording residues: R-01, R-02.
```

## Findings

### R-01: RESIDUE (Docs). A plan rationale sentence is broader than its evidence

- **Location:** `docs/design/MARK_II_AREA_PLAN.md:690`.
- **Authority/evidence:** The sentence reads "The remaining tables read two ports at once, write two at once, or read in parallel." The published hand-off section 2 gives other reasons for several tables:
  - `scratch_r` needs the same state-port merge as the bank;
  - `evq_pd_ctx_r` is read 144 bits whole at pop;
  - `evq_r` is read combinationally for dispatch, at its primitive's depth already;
  - `tsf_r`, single write and single read, was offered as a manager decision and not taken, because its debug output would lag one cycle.
  The PR body (`Known limitations`) carries the `tsf_r` option; the durable plan does not.
- **Impact:** Wording only. No figure, measurement, verdict, test or code changes. A later re-measure reading only the plan would not see that `tsf_r` stays convertible.
- **Exact fix:** Replace the sentence with: "The remaining tables were not converted: `rf_r` reads three ports at once, `ann_ctx_r` is written with the bank, `scratch_r` would need the bank's output merge, `evq_pd_ctx_r` is read 144 bits whole, and `evq_r` and the TX slot are already at their primitive's depth. `tsf_r` (32 x 64, one write, one read) could take the two freed RAMB18 for at most 44 LUTRAM sites at the cost of a one-cycle lag on its debug output; that option is left to a manager decision."
- **Verification:** `check_doc_style.py`, `docs_check.py` and `check_em_dash.py --base` rc 0.

### R-02: RESIDUE (Docs). Three source comments describe the FIFO output imprecisely

- **Locations:**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:238-239`: "count 0 is the all-clear tkeep an empty FIFO output presents";
  - `KL_gptp_shadow.sv:876-877`: "an empty FIFO's zero count presents the all-clear tkeep it always did";
  - `KL_gptp_shadow.sv:256-259`: still explains `TXF_BEATS_C` through "DEPTH in OCTETS when KEEP_ENABLE is set". KEEP_ENABLE is now 0 and DEPTH is in beats.
- **Authority/evidence:** `third_party/verilog-axis/rtl/axis_fifo.v:390-397` reloads its output register from `mem[rd_ptr]` whenever the stage is empty. An empty FIFO therefore presents the word at its read pointer: count 0 only until that slot is first written, and a stale beat's decoded tkeep afterwards. The base FIFO presented the same stale mask, and the decode is exact for every stored count, so behaviour is identical. The every-cycle `tx_fifo lockstep` comparison confirms it: tkeep is compared while invalid too.
- **Impact:** Comment wording only. No logic, figure or test changes.
- **Exact fix:**
  - At :238-239 and :876-877, say "a never-written FIFO word holds count 0, which decodes to the all-clear tkeep; any other word decodes to exactly the mask the eight-bit FIFO stored".
  - At :256-259, say "the pinned `axis_fifo` with KEEP_ENABLE=0 takes DEPTH in beats (`ADDR_WIDTH = $clog2(DEPTH)`) and rounds it up to a power of two".
- **Verification:** the `gptp_tables` 21/21 and lint ratchet stay unchanged (comment-only edit).

### S-01: SUGGESTION (Tests). The ledger tag column of the lockstep sees one value only

- **Location:** `tb/verilator/gptp_tables/gptp_tables_wrap.sv:363-366`; `README.md` table row `ledger`.
- **Evidence:**
  - Probe `ledger_tag_constant` (write 1 into `led_tag_r` always) stays 21/21.
  - `hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv:186,217` clears `tagged` only for a frame too short to reach its sequenceId octet (offset 45). The engine's TX slot never emits one.
  - So the tag stored for every reachable entry is 1. A stuck-at-0 or wrong-entry-to-0 defect is caught; a stuck-at-1 defect is unobservable in the lockstep and in the plane alike.
- **Suggested outcome:** state this in the README (or add a coverage line counting the tag values compared), so a reader does not take the tag column as two-valued evidence.

### S-02: SUGGESTION (Tests). No per-reset-segment coverage

- **Location:** `tb/verilator/gptp_tables/sim_main.cpp:107-116,458-477`.
- **Evidence:**
  - The coverage checks are cumulative and are all met before the first warm reset.
  - The phase probe shows the plane live after reset 1, but wedged after reset 2: 7 programs and 0 results compared over the last 3.5 M cycles. That is the known pre-existing fence/tx_fifo defect, which the manager files separately.
  - A future regression that silenced the plane after reset 1 would leave every check green. Post-reset reads are where the removed reset clears matter.
- **Suggested outcome:** once that issue is fixed, add a per-segment check (for example, results compared and timer sweeps compared after each warm reset), and note the current wedge in the README until then.

### S-03: SUGGESTION (RTL, Robustness). The new lane guard admits widths the plane cannot serve

- **Location:** `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:269`.
- **Evidence:**
  - `g_refuse_lanes` refuses more than 8 lanes, which is correct for the lane fields it guards.
  - The classifier (`:302`, EtherType at lanes 4 and 5) and the gearbox (`:816`, a beat completes at index 7) assume 8 lanes, so 8- and 32-bit widths elaborate with out-of-range selects (`receipts/lane_width_lint.log`).
  - This predates this lane: the base had no guard at all.
- **Suggested outcome:** a separate issue to refuse `TDATA_WIDTH_P != 64` (or to make the classifier and gearbox lane-generic).

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6097272538 and D7; the shadow, txret and timer RTL listed above; `pp_resource_baseline.json` route-1x1; `AREA_BUDGET.md:395-411`; REVIEW READY 6100339945 | R593-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| RTL | CLEAN | `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, `KL_gptp_timer.sv` (pin `18dd997b`), `axis_fifo.v` (pin `48ff7a7e`), `KL_gptp_engine.sv:350-489`; `lint_rtl_check.log` | R593-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Robustness | CLEAN | `tables-head.log`, `tables-rx_top_popcount.log`, `tables-phase_coverage_print.log`, `lane_decode_enum.log`, `lane_width_lint.log`, `gptp_shadow_run.log`, `gptp_plane_run.log` | R593-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Tests | CLEAN | `tb/verilator/gptp_tables/*`; `driver-mutants.log` (15/15); 6 reviewer probes; `gptp_shadow_mutants.log` (9/9); `gp_engine.log` | R593-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Docs | CLEAN (RESIDUE R-01, R-02 carried) | `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, `TESTING.md`, suite README, generated matrix and README-tests, donor `docs/MANAGER.md`, pin links; `gate_*.log` | R593-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |

## Real limits of this round

- **No integrated route.** I did not route the design or re-run the resource gate on route outputs: no Vivado run was made. The route figures, the gate `check` PASS, the post-synthesis and out-of-context attributions and the primitive census are the author's receipts. Their files are private scratch, and only their digests are listed in the published hand-off. I checked them only for arithmetic and against the committed record and tolerances.
- **Executor receipts I did not reproduce:** the full sweep (61 suites), `gptp_txts`, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, Yosys portability, xvlog, the builder, the donor's 40 engine mutants and the scratch differential hash. None of the 40 engine mutants targets the timer storage. The timer is covered here by the lockstep's three timer controls and by the engine bench.
- **Em-dash gate not run.** `check_em_dash.py --base` could not run on this host because the pinned Markdown renderer is absent (rc 2, `gate_em_dash.log`). The hosted docs job owns it.
- **Hosted CI incomplete.** At my snapshot (`receipts/hosted_checks.tsv`, 17:55 UTC), these were complete and successful: verilator-lint, Yosys shards 0-3, Verilator shard 3/5, docs-check-no-git, bdd-conformance, wire-accountability and full-ci-gate. The other Verilator shards, docs-check, elaborate, yosys-elaboration and firmware-unit were still in progress. Physical gPTP was skipped (a scheduled context).
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **No manager bank run is claimed.** This round claims no manager source bank and no candidate-merge validation.

## Pending manager duties

- Rule on accepting the below-range saving (plane -107 to -253 LUT against a 300-700 estimate), and on the `tsf_r` option offered and not taken.
- Publish the donor branch before the parent; the gitlink `18dd997b` equals donor PR #78's head.
- After FPGA-gPTP#77 (issue #621) moves the pin, run the merge round.
- Build and validate the current-dev merge candidate (live dev `f88df731`) with the builder and native banks.
- Confirm that the remaining hosted contexts at the exact head complete green.
- File the pre-existing fence/tx_fifo defect as its own issue (already announced). S-02 depends on it.
- Carry R-01 and R-02 to the residue checklist.

R593-1 FINISHED
