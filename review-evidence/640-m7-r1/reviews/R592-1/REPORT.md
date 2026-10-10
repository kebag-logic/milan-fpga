[R592] NEGATIVE - exact head 9d42762c555118e3ea86665bf7d8c6ef673698d3

# R592-1: internal review of PR #713 (issue #640, Mark II lane M7, plan L10a)

- Head `9d42762c555118e3ea86665bf7d8c6ef673698d3`, tree `4291b752854f3aebb6fa539cd834ef76c936033b`, source base dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (12 commits).
- Gitlinks at the head:
  - `gptp-processor` `18dd997b2459699e41e5ce9bceca1181e41fa5fe`. This equals the head of donor PR Mister-M-alt/FPGA-gPTP#78, whose base `5dce647a` is the donor `main` tip.
  - `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`; `external` and `third_party/lwSRP` are unchanged.
- Lenses applied: Conformance, RTL, Robustness, Tests and Docs.
- **One MINOR is open (F1, Tests), so the verdict is NEGATIVE.** Conformance, RTL, Robustness and Docs are clean.
- Other open items: three RESIDUE wording items (F2, F3, F5) and one SUGGESTION (F4).
- The product RTL is behaviour-preserving at this head as far as this round could test it. F1 is a gap in the new suite's evidence, not a product defect.

## Reconstruction

Read in this order:
1. `AGENTS.md` and `CONTRIBUTING.md`, then `docs/README.md`.
2. The issue #640 body and its decisions: manager rulings D1, D3, D7 and D8, and the owner's block-RAM decision.
3. The M7 assignment (issue comment 6097272538), the executor's TAKEN (6097298086) and REVIEW READY (6100339945).
4. The PR body.
5. `git diff e8454e27..9d42762c` and its history, plus the donor diff `5dce647a..18dd997b` (`KL_gptp_timer.sv`, `docs/MANAGER.md`).
6. The interface authorities the change touches: `third_party/verilog-axis/rtl/axis_fifo.v`, and the engine's result face in `KL_gptp_engine.sv`.
7. The public evidence at `3e0f36b8`/`review-evidence/640-m7-r1`. Its two files match the manifest's published digests.

Prior public review findings were read only after this round's verdict and ledger were written; `receipts/verdict_before_prior_findings.md` is the time-stamped snapshot.

## Independent executions at this head

All runs used the pinned Verilator 5.050, identity checked with `--version`. Each ran on private copies or in this clone with build products removed afterwards.

| What | Result | Receipt |
|---|---|---|
| `gptp_tables` (`make run`) | 21/21 checks over 29,100,030 cycles. Results queue at most **1 deep**, ledger 3 deep, TX lane counts 0x114 | `receipts/gptp_tables_head_run.log` |
| `gptp_tables/mutants.py`, all 15 author controls re-applied | 15/15, each caught by its own table's named check | `receipts/gptp_tables_mutants_author15.log` |
| 6 reviewer controls (`scripts/extra_mutants.py`) | 4 caught by the named check: ledger write at head, RX lane as popcount (non-contiguous tkeep only), timer write alias, results sequence read from the ledger tail. **2 survived:** results written at head (F1), TX decode wrong for odd counts (F4) | `receipts/gptp_tables_mutants_reviewer.log`, `receipts/suite_logs/extra_mut_*` |
| Results-written-at-head control on the existing suites | Survives `gptp_shadow` 309/309 and `gptp_txts` 85/85 | `receipts/suite_probe.log`, `receipts/suite_logs/suite_*` |
| Results-queue depth probe: engine acceptance throttled in a private copy (bench-only instrumentation) | Queue reaches 3 deep. Unmutated head stays 21/21. The results-written-at-head control fails `results lockstep`: 1,267,065 mismatching cycles | `receipts/results_depth_probe.log` |
| Ledger tag stuck-at controls (checking a prior suggestion) | Stuck-at-1 survives; stuck-at-0 is caught | `receipts/tag_probe.log` |
| `gptp_shadow`, `gptp_txts`, `gptp_plane` at head | 309/309, 85/85, 29/29 | `receipts/suite_logs/suite_*_head.log` |
| Exhaustive lane encode/decode, K = 1..8 lanes (`scripts/lane_probe.sv`) | 582 checks, 0 errors: TX count decode equals the old gearbox mask for every gearbox index and count 0; RX highest lane equals the old serializer's for every K-bit tkeep, non-contiguous included. The negative control (`<=` decode) fails | `receipts/lane_probe.log`, `receipts/lane_probe_negative_control.log` |
| Lane guard elaboration at TDATA 8/32/64/72 | `g_refuse_lanes` fires at 72 (9 lanes) only | `receipts/lane_guard_elab.log` |
| Idle-output probe on the transmit FIFO | With tvalid low after traffic, `tx_tkeep_o` = 11111111 (stale count 8). The old-form reference shows the same 11111111 | `receipts/idle_keep_probe.log` |
| Open-tool mapping (`scripts/yosys_map.sh`, xc7) | txret 1,249 -> 369 FF with 22 RAM32M; timer 324 -> 68 FF with 6 RAM32M. Each frame FIFO goes from 3 RAMB18 to 1 RAMB36 | `receipts/yosys_map.log` |
| Donor `make contract`, `make lint`, `make docs` | rc 0 / 0 / 0 | `receipts/gp_contract.*`, `gp_lint.*`, `gp_docs.*` |
| Donor engine bench, then its mutant campaign | 1,613 checks x3 PASS. Mutants: control plus 33/33 caught | `receipts/gp_engine_tb.log`, `receipts/gp_engine_mutants.log` |
| Parent `scripts/lint_rtl.py --check` | PASS, 90 violations against a ratchet of 90 | `receipts/parent_lint.*` |
| 18 doc, generator and idiom gates, plus `git diff --check` base..head | All rc 0 | `receipts/doc_gates.log` |
| Hosted runs at the head, read 18:45Z | `rtl-fast`, `elaborate` and `docs` succeeded. Verilator shards 0, 1, 3 and 4 succeeded; shard 2/5 and `rtl-full` were still in progress. Physical gPTP was skipped | `receipts/hosted_runs_at_head.tsv` |
| Clone restored after the round | 0 status entries including ignored; index (mode, blob, path) equals the HEAD tree; gitlinks as above | `receipts/clone_restore_check.log` |

## Findings

### R592-1-F1: MINOR (Tests). The results-queue lockstep never holds two results, so a write-index defect in the new result RAM goes undetected

- **Location:**
  - `tb/verilator/gptp_tables/sim_main.cpp:10-12`, which claims each table is "written, read, filled, wrapped and reset";
  - `sim_main.cpp:473-474`: the results coverage checks set no depth bound;
  - `gptp_tables_wrap.sv:368-377`;
  - the table under test: `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:699-707` (`result_ram`, a write block this lane introduced).
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect"; "Positive, negative, and boundary behavior is covered".
- **Evidence:**
  - At the head the suite prints `results: 8446 compared, heads 0xff, 1 deep`. Every push therefore lands while the tail equals the head, or in an accept cycle.
  - The control `res_ns_r[res_tail_w]` -> `res_ns_r[res_head_r]` at `KL_gptp_txret.sv:701` stays green in `gptp_tables` (21/21), `gptp_shadow` (309/309) and `gptp_txts` (85/85).
  - The design admits several outstanding results. The capacity is `TXTS_CAP_N_P` = 8, and the conservation assertion is at `KL_gptp_txret.sv:686`.
  - The engine holds ready low while one result is pending. It pops that result only when its dispatch and serializer are idle (`KL_gptp_engine.sv:349, 551-552`).
  - The oracle is sound: with acceptance throttled, the queue reaches 3 deep, the head stays 21/21, and the same control fails `results lockstep`.
- **Impact:**
  - For one of the five converted tables, the evidence does not cover the write port's address or the queue's ordering with more than one entry, which is the case the queue exists for.
  - The suite's "filled" claim is not true for that table.
  - The product is not wrong at this head: `res_tail_w` is unchanged, and the throttled probe is equivalent at depth 3.
- **Required outcome:** one of these two.
  - Under lockstep, `gptp_tables` reaches at least two outstanding results, grades that as named coverage, and `mutants.py` carries a result-queue write-index control that fails `results lockstep`.
  - Or the executor publishes an argument that two outstanding results are unreachable in the plane, and narrows the claim at `sim_main.cpp:10-12` and in the README to match.
- **Verification:**
  - `make -C tb/verilator/gptp_tables` prints a results depth of at least 2, all checks pass, and the new control reports `caught by "results lockstep"`.
  - `receipts/results_depth_probe.log` shows the oracle side already works.

### R592-1-F2: RESIDUE (RTL, Docs). Three source comments misdescribe the FIFO output

- **Location:**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:238-239`: "count 0 is the all-clear tkeep an empty FIFO output presents";
  - `KL_gptp_shadow.sv:876-877`: "an empty FIFO's zero count presents the all-clear tkeep it always did";
  - `KL_gptp_shadow.sv:256-259`: explains `TXF_BEATS_C` through "DEPTH in OCTETS when KEEP_ENABLE is set", but both FIFOs now set KEEP_ENABLE to 0 and take DEPTH in beats.
- **Evidence:**
  - `axis_fifo.v:390-394` reloads the output stage from `mem[rd_ptr]` whenever the stage is empty. After traffic, the idle output carries a stale word.
  - `receipts/idle_keep_probe.log` shows `tx_tkeep_o` = 11111111 with tvalid low, and the old form shows the same value. Behaviour is identical: the `tx_fifo lockstep` compares tkeep in every cycle, and `lane_probe` proves the decode exact for every count.
  - The capacity value `TXF_BEATS_C` is still exact; only its explanation is stale.
- **Impact:** comment wording only. No logic, figure, test or generated artifact changes.
- **Exact fix:**
  - At :238-239, replace "and count 0 is the all-clear tkeep an empty FIFO output presents" with "and a never-written FIFO word holds count 0, which decodes to the all-clear tkeep; any other word decodes to exactly the mask the eight-bit FIFO stored".
  - At :876-877, replace "so an empty FIFO's zero count presents the all-clear tkeep it always did" with "so every stored word, including a stale one an idle FIFO presents, decodes to the mask the eight-bit FIFO held".
  - At :256-259, replace the octet sentence with "The pinned `axis_fifo` with KEEP_ENABLE=0 takes DEPTH in beats (`ADDR_WIDTH = $clog2(DEPTH)`) and rounds it up to a power of two, so this is the exact capacity and not an estimate."
- **Verification:** `gptp_tables` 21/21 and the lint ratchet are unchanged (a comment-only edit).

### R592-1-F3: RESIDUE (Docs). The plan's eligibility sentence is broader than its evidence

- **Location:** `docs/design/MARK_II_AREA_PLAN.md:690`, "The remaining tables read two ports at once, write two at once, or read in parallel."
- **Evidence:**
  - `scratch_r` is single-read and single-write. `KL_gptp_engine.sv:150-154` states this, and its reads are at :742 and :813, the latter simulation-only. Its exclusion reason is the bank's state-port merge.
  - `tsf_r` (`KL_gptp_shadow.sv:479, 541, 558`) is one write and one read. The executor's REVIEW READY offers it as an untaken decision.
  - The PR body (line 54) is accurate; the durable plan is not.
- **Impact:** wording only. A later lane reading the plan would not learn that `tsf_r` stays convertible.
- **Exact fix:** replace the sentence with "The remaining tables were not converted: `rf_r` reads three ports at once, `ann_ctx_r` is written with the bank, `scratch_r` would need the bank's output merge, `evq_pd_ctx_r` is read 144 bits whole, and `evq_r` and the TX slot already sit at their primitive's depth. `tsf_r` (32 x 64, one write, one read) could take the two freed RAMB18 for at most 44 LUTRAM sites, at the cost of a one-cycle lag on its debug output; that option is left to a manager decision."
- **Verification:** `check_doc_style.py`, `docs_check.py` and `check_em_dash.py --base e8454e27` rc 0.

### R592-1-F4: SUGGESTION (Tests). TX lane counts 1, 3, 5, 6 and 7 never leave the FIFO

- **Location:** `tb/verilator/gptp_tables/sim_main.cpp:464-465`, where coverage requires exactly 0x114.
- **Evidence:** a control that rounds odd counts down survives. The engine's frames end in 2, 4 or 8 lanes. The decode for every count is proven only by this round's exhaustive `lane_probe`.
- **Suggested outcome:** a small directed check of the decode for all counts 0..8, for example `lane_probe`'s TX half next to the suite, so that a microcode change that produces a new frame length is not the first test of those counts.

### R592-1-F5: RESIDUE (Docs, evidence wording). "40/40 engine mutants"

- **Location:** the REVIEW READY comment (6100339945), "gptp-processor `make tb` rc 0 (40/40 engine mutants)", and the published `HANDOFF.md` section 4.
- **Evidence:**
  - The engine campaign holds 33 `MUTATIONS` entries; `receipts/gp_engine_mutants.log` shows the control plus 33/33 caught.
  - Gaskets holds 4 and tsngen holds 3, so 40 is the donor total.
  - The figure is right; its label is wrong.
- **Exact fix:** "40/40 donor mutants (engine 33, gaskets 4, tsngen 3)".
- **Verification:** this round counted engine 33 by AST and ran it. The gaskets and tsngen counts are by AST only; those campaigns were not run here.

## Prior public review findings at this head (read after this round's verdict and ledger)

The only prior round is R593-1, the external review published at 17:59Z: POSITIVE, two RESIDUE items and three SUGGESTIONs.

| Prior item | Status at this head | Basis |
|---|---|---|
| R-01 RESIDUE, plan sentence at `MARK_II_AREA_PLAN.md:690` | Retained. It is the same defect as F3 | Reached independently; same evidence |
| R-02 RESIDUE, three FIFO-output comments | Retained. It is the same defect as F2 | Reached independently, with an idle-output probe confirming it |
| S-01 SUGGESTION, the ledger tag is single-valued | Retained | `receipts/tag_probe.log`: stuck-at-1 survives, stuck-at-0 is caught |
| S-02 SUGGESTION, no per-reset-segment coverage | Retained | Consistent with the executor's own statement of a pre-existing wedge after the second warm reset (HANDOFF section 8). Not re-measured per segment here |
| S-03 SUGGESTION, the guard admits 8- and 32-bit widths the classifier and gearbox cannot serve | Retained, pre-existing | `receipts/lane_guard_elab.log`: those widths elaborate with the guard silent. This round's lint suppressed SELRANGE |

R593-1 did not report F1. This round's verdict differs from R593-1's for that reason only.

## Lens results

- `[R592] PASS Conformance` - assignment 6097272538 scope and proof items against `KL_gptp_shadow.sv:233-272,316-324,431-470,834-884`, `KL_gptp_txret.sv:328-359,633-741`, `gptp-processor/hdl/common/KL_gptp_timer.sv:76-108`, `AREA_BUDGET.md:395-411`, `syn/ooc/pp_resource_baseline.json` (route-1x1), and `MARK_II_AREA_PLAN.md:672-717`.
  - Widths, depths and read latency are unchanged (lockstep, `yosys_map.log`). No register-map or wire file is in the diff. The timestamp path (`tsf_r`, `res_ns_w`) is unchanged.
  - The claimed route figures satisfy the gate's tolerances: WNS +0.122 against a +0.049 minimum, WHS +0.019 against 0, RAMB at most +0.
  - The record is unchanged (D7).
  - The below-range saving (plane -107 to -253 against 300-700) is stated plainly, and the image's -369 is not credited.
- `[R592] PASS RTL` - reset and X: every reader of the un-cleared RAM fields is gated by occupancy, validity or armed state (`KL_gptp_txret.sv:537-553,590-599,735-740`; `KL_gptp_engine.sv:349-350,484-489`; `KL_gptp_timer.sv:113-114`).
  - The `axis_fifo` parameters (`axis_fifo.v:137,223-240,290`) give an unchanged ADDR_WIDTH and a bit-0 bad-frame judgement.
  - The lane encode and decode are exhaustively equal for 1..8 lanes, and the guard fires at 9.
  - There is no CDC change. Lint ratchet 90/90. F2 is wording only.
- `[R592] PASS Robustness` - `gptp_tables` 29.1 M cycles with 0 mismatches across 33,528 overflow drops, 12,226 bad frames, corrupted and non-contiguous tkeep (the popcount control is caught), 11.2 M stalled TX cycles and two warm resets mid-traffic.
  - A 3-deep result queue under throttled acceptance shows 0 mismatches (`results_depth_probe.log`).
  - Non-default lane counts are handled by the guard and `lane_probe`. S-03 and S-02 are retained as suggestions.
- **Tests UNCLEAN (F1)** - examined:
  - the oracle form: `gptp_tables_wrap.sv:168-210` is the old FIFO configuration with real tkeep, `:235-292` is the old gearbox enables, and `:312-391` are reset-cleared register arrays. These are the previous storage forms, not copies of the new ones;
  - the 15 author controls re-applied (15/15) and six reviewer controls (two survivors);
  - `gptp_shadow`, `gptp_txts` and `gptp_plane`, and the donor engine bench with its 33/33 mutants.
- `[R592] PASS Docs` - `MARK_II_AREA_PLAN.md` and `AREA_BUDGET.md`: the arithmetic was checked against the route-1x1 record (-369, -1,193, -6, 0/-2, -0.177/-0.012; 87.5 -> 86.5 tiles).
  - The per-table primitive counts match the field widths.
  - Every pin link is at `18dd997b`. Donor `docs/MANAGER.md` (+24 memory LUTs, -256 registers) matches the timer RAM.
  - `TESTING.md`, the suite README, the generated matrix and README-tests are covered; 18 doc gates rc 0.
  - F3 and F5 are RESIDUE only.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6097272538 and D7; `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, donor `KL_gptp_timer.sv` at the lines above; `AREA_BUDGET.md:395-411`; `pp_resource_baseline.json` route-1x1; `MARK_II_AREA_PLAN.md:672-717`; `yosys_map.log` | R592-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| RTL | CLEAN (F2 RESIDUE carried) | the three RTL files; `axis_fifo.v:137,223-240,290,390-394`; `KL_gptp_engine.sv:349-350,484-489,551-552`; `lane_probe.log`; `lane_guard_elab.log`; `idle_keep_probe.log`; `parent_lint.log`; `gp_lint.log` | R592-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Robustness | CLEAN | `gptp_tables_head_run.log`; `results_depth_probe.log`; `extra_mut_rx_top_as_popcount.log`; warm-reset phases at `sim_main.cpp:107-116`; guard and lane probes | R592-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Tests | UNCLEAN (F1 open) | `tb/verilator/gptp_tables/*`; `gptp_tables_mutants_author15.log`; `gptp_tables_mutants_reviewer.log`; `suite_probe.log`; `tag_probe.log`; `gp_engine_tb.log`; `gp_engine_mutants.log` | R592-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |
| Docs | CLEAN (F3 and F5 RESIDUE carried) | `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, `TESTING.md`, suite README, `MODULE_MATRIX.md`, README-tests, donor `docs/MANAGER.md`, eight pin-link pages, `rom_digests.tsv`; `doc_gates.log`; `gp_docs.log` | R592-1 | `9d42762c555118e3ea86665bf7d8c6ef673698d3` |

## Real limits of this round

- **No Vivado run.** The routed and synthesised figures, Vivado's primitive mapping and timing were not reproduced. The route reports are not public; the hand-off lists only their digests. The tolerance check above is arithmetic on the claimed figures. Primitive structure is supported only by the open-tool mapping.
- **Suites not run:**
  - the full sweep, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, the Yosys portability bank, the builder, xvlog and act;
  - from the donor's `make tb`, only the engine bench and its mutants. The ucpu, parser, gaskets, tsngen and Arty benches were not run.
- **Reachability not proven.** This round did not prove whether two or more outstanding results occur in the shipping image; F1's second option leaves that to the executor.
- **Hosted runs not complete.** At 18:45Z, `rtl-full` and Verilator shard 2/5 were still in progress. This is not hosted acceptance.
- **No manager source bank** runs at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Close F1 by a re-review at the corrected head. A changed suite un-covers Tests only, plus Docs if the README changes.
- Hosted acceptance at the exact head: `rtl-full` and Verilator shard 2/5 were still in progress at 18:45Z.
- Publish donor PR #78 (`18dd997b`) before the parent. FPGA-gPTP#77 (issue #621) moves the pin before this lane merges, so a merge round follows.
- Build and validate the merge-turn candidate on live dev `f88df731c77ec3d876b74e41b0091c513370afe9` (builder and native banks), and link its receipts.
- Decide on the plan's outcomes:
  - whether to accept the below-range L10a saving (107-253 against 300-700);
  - whether the cumulative tables keep the 500-LUT planning figure until the week-4 re-measure;
  - the offered `tsf_r` option.
- File the pre-existing `KL_gptp_shadow` `tx_fifo` pop under the departure fence as its own issue (known context).
- Carry F2, F3 and F5 to the residue checklist.

R592-1 FINISHED
