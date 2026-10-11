[R592] POSITIVE - exact head 354f781828d8b4d73037129f297b072320a10f9c

# R592-3: internal review of PR #713 (issue #640, Mark II lane M7, plan L10a), round 3

Reviewer: [R592], internal cleared-context reviewer. Head `354f781828d8b4d73037129f297b072320a10f9c`, tree `27d0094ad4a11b5d2fe55091b6ae93d9f1f70237`. Source base `e8454e2751d05b02ee8e5a571857589ab358ab86`. Gitlinks: `gptp-processor` `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (from `5dce647a`), `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `2ad2f845`.

## Summary

- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs. All five are clean. No BLOCKER, MAJOR or MINOR is open.
- New this round: two RESIDUE wording items (R592-3-RES1, R592-3-RES2). Both are carried to the manager's residue checklist with exact texts.
- Every prior public finding that needed a change is resolved at this head. Two SUGGESTIONs are retained: R592-2-S1 (optional, not taken) and R593-1-S-03 (pre-existing, routed to #495 at merge).
- The lane's measured saving (107-253 LUTs) is below the assignment's target of about 500 (300-700). The lane reports this honestly, as the assignment's proof list requires. Accepting the shortfall is a manager decision; it is listed under pending manager duties, not as a defect.

## Reconstruction

- **Contract:** `AGENTS.md`, `CONTRIBUTING.md` sections 2-3 and `docs/README.md`.
- **Issue #640:** the body (NFR-RES-01, 38,040 LUTs, function unchanged, gate re-recorded only in the change that reaches the target). Read with it:
  - the owner and manager decisions D1-D9 and the block-RAM decision;
  - the lane M7 assignment ([6097272538](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538));
  - the TAKEN comment ([6097298086](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097298086));
  - the manager's round-2 and round-3 assignments ([6100980189](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100980189), [6104116064](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104116064)). Round 2 states the route is not repeated, because the record is not re-recorded (D7).
- **Scope derived from the assignment:**
  - Move eligible fabric gPTP plane tables into block RAM, or narrow their indices. Target about 500 LUTs (300-700).
  - BRAM growth only within the firmware BRAM ledger. A read-latency change needs deterministic bounds.
  - No change to gPTP behaviour, register map or timestamp path.
  - Proof: the named gPTP, timestamp and CDC suites. Per-table lockstep with planted wrong-depth, wrong-read-latency and index-alias defects, each failing a named check. The integrated route and resource gate through the M0s recipe. An honest saving report.
- **Diff and history:** `git diff e8454e27..354f7818` (37 files, 20 commits), and the submodule's `5dce647a..18dd997b`. The submodule changes `hdl/common/KL_gptp_timer.sv` and `docs/MANAGER.md` only; its intermediate commits `f61b90c6`/`4f9fb19b` are reverted by `861e8f80`.
- **Public evidence:**
  - the round-1 hand-off at `3e0f36b8:review-evidence/640-m7-r1` (`author/HANDOFF.md`, sha256 `30a4d784...`; `author/PR-BODY.md`);
  - the executor's REVIEW READY comments for rounds 1-3;
  - the PR body.
- **Hosted state:** no hosted run exists at this exact head. There are 0 check runs and 0 workflow runs; the combined status is pending with no contexts (`receipts/hosted_check_runs.tsv`).

## What the change does (verified against the RTL)

| Table | Change | Why function is preserved (evidence) |
|---|---|---|
| Tap frame FIFO (`KL_gptp_shadow.sv:321-326, 434-470`) | Stores the highest enabled lane (3 bits) in `tuser` beside the bad bit; `KEEP_ENABLE=0`; DEPTH in beats | The serializer only ever reduced `tkeep` to its highest set lane (old `ser_top_w` loop). Same reduction now happens before the FIFO, and the all-clear case gives lane 0 as before. `axis_fifo.v:137`: with `KEEP_ENABLE=0`, `ADDR_WIDTH=$clog2(DEPTH)`, equal to the old `$clog2(DEPTH/KEEP_WIDTH)`. The bad-frame test at `axis_fifo.v:292` masks with `USER_BAD_FRAME_MASK=(LANE_W_C+1)'(1)`, so only bit 0 judges a frame |
| Transmit frame FIFO (`:797-830, 834-886`) | Stores the beat's lane count (4 bits); `tx_tkeep_o` decoded as lanes below the count | The gearbox's old `gb_keep_r` accumulated contiguous bits from lane 0 to `gb_idx_r`, i.e. exactly `count = gb_idx_r+1`; count 0 (never-written word, BRAM init 0) decodes to the old all-clear |
| Egress ledger type/seq/tag (`KL_gptp_txret.sv:339-351, 637-645`) | Distributed RAM, write at tail outside reset, one named head read port | Every reader is gated by `have_entry_w` (`:537`, `:552-553`, `:573-574`), and every entry in `[head, head+n)` was written after the reset that zeroed `n_led_r`. Write condition `led_we_w` (`:637`) is the old one verbatim. `led_live_r` stays in flops |
| Egress result queue (`:353-357, 696-740`) | Distributed RAM, write at tail outside reset | The only consumer samples on `txts_accept_w` (`KL_gptp_engine.sv:349-350, 484-490`) and `txts_valid_o = n_res_r != 0` (`txret:735`) |
| Timer deadlines (`KL_gptp_timer.sv:80, 91-94, 106-118`) | Distributed RAM, written on `rst_n && arm_we_i` | `armed_r` is set only by the same arm write that stores the deadline, and the sweep reads `delta_w` only under `armed_r[sweep_r]` (`:113`) |

The read latency is unchanged everywhere (combinational read, synchronous write, as the flop arrays were). The width guard `g_refuse_lanes` (`KL_gptp_shadow.sv:271`) refuses lane counts outside 1..8 at elaboration. The only shipping instance (`milan_datapath.sv:7503`) uses `TDATA_WIDTH=64`.

## Independent executions at this head

All runs used the scoped Verilator 5.050: `receipts/tool_identity.txt` holds the wrapper's sha256 and `--version`. Each run had its own log and rc file, and none was piped. Concurrency stayed within 16 jobs, with one short exception: the `gptp_plane` and donor engine Makefiles hard-code `-j 0` for their roughly 6-second C++ compile.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/gptp_tables` (limits check, run, `mutants.py`) | table check current; 36/36 checks over 32,100,038 cycles; 26/26 controls each caught by its own named check | `gptp_tables_all.log`, `.rc` = 0 |
| `gptp_shadow` `make all` | 309/309, lifecycle PASS, 9/9 controls | `gptp_shadow_all.log`, rc 0 |
| `gptp_txts` `make all` | 85/85, 6/6 controls | `gptp_txts_all.log`, rc 0. Limit: `MILAN_LITEX_PYTHON=true`, so the converted-chain staleness check was not run (no LiteX environment here; the MAC model is not touched by this PR) |
| `gptp_plane` `make run` | 29/29 | `gptp_plane_run.log`, rc 0 |
| `ptp_ts`, `ptp_sync`, `ptp`, `clkvalid`, `cdc` default targets | all rc 0 (e.g. `ptp_sync` 15/0, `cdc` 16/0, `ptp_pps` 58/0, `clkvalid` 19/0 and 14/0, `ptp_ts` SVA campaign 62/0) | `*_default.log` |
| donor `tb/verilator/engine` `make run` (focused; not the donor bank) | 1613/1613 per leg | `gp_engine_run.log`, rc 0 |
| donor `make contract`, `make docs`, `make lint` | rc 0 each | `gp_contract.log`, `gp_docs.log`, `gp_lint.log` |
| `scripts/lint_rtl.py --check` | PASS, 90 <= 90 | `lint_rtl_check.log`, rc 0 |
| 22 doc and source gates (`gen_one_valued_table --check`, `check_gptp_docs` with and without the submodule, `gen_module_matrix --check`, `docs_check`, `check_em_dash --base e8454e27`, `check_doc_style`, `gen_toc --check`, `check_doc_paths`, `check_submodule_docs`, both diagram generators `--check`, `check_diagram_pngs`, `ci_scope --selftest`, the py/cpp/sv idiom checks, hygiene, test-evidence, naming, `check_rtl_source_lists`, `git diff --check e8454e27 HEAD`) | all rc 0 | `gate_*.log`, `gate_*.rc` |
| Reviewer fault probes, 16 defects in the changed RTL, independent of `mutants.py` (`scripts/probes.py`, `scripts/probes2.json`) | see below | `probes/probes.json`, `probes2/probes.json`, `probes_summary.tsv`, `probe_logs/` |
| RTL-equality of the author's sweep heads | `9c7ad7f4..354f7818` and `49e1ce48..354f7818` change only comments in `KL_gptp_shadow.sv`, test files, docs and the donor gitlink (`docs/MANAGER.md` only) | `git diff` in this report's reconstruction |

### Reviewer probes (each in a private copy of an exact-head extraction)

Caught by `gptp_tables` through the table's own lockstep or decode check:

| Probe | Lockstep or decode check that failed |
|---|---|
| `rx_lowest_lane` | `rx_fifo lockstep` |
| `rx_bad_mask_all_bits_sized` | `rx_fifo lockstep` |
| `tx_decode_le` | `tx_fifo lockstep`, `tx_fifo decode` |
| `tx_decode_count0_allones` | `tx_fifo lockstep`, `tx_fifo decode` (`gptp_shadow` misses this one) |
| `tx_count_no_plus1` | `tx_fifo lockstep` |
| `tx_fifo_user_disabled` | `tx_fifo lockstep` |
| `ledger_type_written_at_head` | `ledger lockstep`, `results lockstep` |
| `result_seq_from_ledger_tail` | `results lockstep` |
| `result_ns_low_bit_stuck` | `results lockstep` |
| `timer_written_at_sweep_slot` | `timer lockstep` |

Survivors, each explained:

| Probe | Why it survives |
|---|---|
| `ledger_tag_stuck_1` | Declared in `one_valued.tsv`. The stimulus has no untagged frame |
| `result_ok_stuck_1` | Declared; `gptp_shadow` catches it, 305/309 |
| `result_gen_stuck_1` | Declared, no consumer. `gptp_shadow` 309/309, as the declaration states |
| `ledger_write_ungated_when_full` | Equivalent by design: an allocation into a full ledger is an asserted invariant violation (`KL_gptp_txret.sv:684`). This is R592-2-S1's class |
| `timer_deadline_drops_delta_msb` | Equivalent under reachable arm deltas, which are below 2^31 ms |
| `rx_bad_mask_all_bits` | Invalid probe: `axis_fifo`'s `USER_BAD_FRAME_MASK` is an untyped parameter, so `'1` became 1'b1. Re-run sized as `rx_bad_mask_all_bits_sized` above, which is caught |

## Findings

### R592-3-RES1: RESIDUE (Tests, Docs). The lockstep's independence claim is broader than the results reference's inputs

- **Location:** `tb/verilator/gptp_tables/README.md:9-10` and `tb/verilator/gptp_tables/gptp_tables_wrap.sv:14-15`. Both say every reference is written "from signals the change did not touch".
- **Evidence:**
  - The result-queue reference takes its write strobe and its `ok` bit from the plane's `push_res_w` and `res_ok_w` (`gptp_tables_wrap.sv:410, 414`).
  - Both now read the converted ledger port: `tag_ok_w` at `KL_gptp_txret.sv:539-541`, `resolve_w` at `:552`, `res_ok_w` at `:590` and `push_res_w` at `:604`.
  - The test power is intact. The ledger lockstep compares that port in every cycle the ledger holds an entry (`gptp_tables_wrap.sv:424-428`), and every resolution requires `have_entry_w`. Probe `ledger_type_written_at_head` fails both `ledger lockstep` and `results lockstep`.
- **Impact:** wording only. No measurement, figure, verdict, test behaviour, code behaviour or clause claim changes.
- **Exact fix:** at both places, after "from signals the change did not touch", add: "except that the result queue's write strobe and `ok` bit come from the plane's resolution logic, which reads the ledger's converted head port; the ledger lockstep grades that port in every cycle the ledger holds an entry, which includes every resolution".
- **Verification:** `make -C tb/verilator/gptp_tables` is unchanged at 36/36 and 26/26; `check_doc_style.py` rc 0.

### R592-3-RES2: RESIDUE (Docs). The plan says the tables' widths are unchanged, next to a table that narrows two of them

- **Location:** `docs/design/MARK_II_AREA_PLAN.md:675`, "Their function, widths, depths and read latency are unchanged." The table directly below it (`:679-680`) narrows the FIFO words from 74 and 73 bits to 69.
- **Impact:** wording only. No figure or claim about function changes.
- **Exact fix:** "Their function, depths and read latency are unchanged; only the two frame FIFOs' stored byte-enable fields narrow, as the table shows."
- **Verification:** `check_doc_style.py`, `docs_check.py` and `check_em_dash.py --base e8454e27` rc 0.

## Prior public review findings at this head (read after this round's own pass)

| Finding | Status at `354f7818` | Evidence |
|---|---|---|
| R592-1-F1 MINOR (Tests): result queue never held two results | Resolved | `results: 11377 compared, heads 0xff, 3 deep, 110 written behind a waiting result`; check `results coverage: two or more results outstanding` passes; control `results_write_index` caught by `results lockstep` (`gptp_tables_all.log`) |
| R592-1-F2 = R593-1-R-02 RESIDUE: three FIFO-output comments | Resolved | `KL_gptp_shadow.sv:236-242`, `:258-261`, `:878-880` carry the exact texts |
| R592-1-F3 = R593-1-R-01 RESIDUE: plan eligibility sentence | Resolved | `MARK_II_AREA_PLAN.md:690-691`, including the `tsf_r` option |
| R592-1-F4 SUGGESTION: odd TX lane counts | Resolved | `tx_fifo decode: counts 0 to 8 presented enables 00 01 03 07 0f 1f 3f 7f ff, 0 decoded wrong`; control `tx_fifo_decode_odd_counts` caught; probes `tx_decode_le` and `tx_decode_count0_allones` caught |
| R592-1-F5 RESIDUE: "40/40 engine mutants" label | Resolved going forward | The round-2 REVIEW READY on #640 carries "40/40 donor mutants (engine 33, gaskets 4, tsngen 3)". The round-1 hand-off is unedited history |
| R593-1-S-01 SUGGESTION: tag one-valued | Resolved | Declared in `one_valued.tsv`; `ledger values: tag: 1 distinct: 0x1, declared 0x1` |
| R593-1-S-02 SUGGESTION: per-segment coverage | Resolved as documented | `README.md` cites #714 and defers per-segment coverage to its fix |
| R593-1-S-03 SUGGESTION: lane guard admits widths the classifier and gearbox cannot serve | Retained, pre-existing | `KL_gptp_shadow.sv:271`; routed to #495 at merge by the round-2 assignment |
| R593-2-F1 MINOR (Tests, Docs): `ok` and `gen` one-valued, undeclared | Resolved | A value census of all 11 columns, with one named check each. `ok` and `gen` are declared with their reasons and coverage. The README's limits table is generated, and `make` checks it first. My probes: `result_ok_stuck_1` is caught by `gptp_shadow` (305/309); `result_gen_stuck_1` survives both suites, exactly as declared. Stuck-column and list controls are caught |
| R593-2-R-01 RESIDUE: PR body checkout command | Resolved | The PR body reads `git switch --detach origin/640-m7` |
| R593-2-S-01 SUGGESTION: tautological decode coverage | Resolved | The line is dropped; the run prints the enables the plane presented |
| R592-2-S1 SUGGESTION: full-ledger write guard never exercised | Retained, optional | Not taken. Probe `ledger_write_ungated_when_full` survives both suites. Unreachable by design (`KL_gptp_txret.sv:684` asserts it) |
| R592-2-RES1 RESIDUE: PR body called the PR a draft | Resolved | The PR body reads "Marked ready for review; merge waits for both reviews to be positive."; `isDraft` is false |

## Lens results

- **Conformance:** PASS.
  - Artifacts examined:
    - the assignment 6097272538 and rounds 6100980189/6104116064;
    - `KL_gptp_shadow.sv:243-273, 321-326, 434-470, 797-886`, `KL_gptp_txret.sv:339-357, 537-604, 637-740` and `KL_gptp_timer.sv:76-128`;
    - `axis_fifo.v:137, 180-185, 223-240, 284-300`.
  - These were checked against "no change to gPTP behaviour, its register map or its timestamp path" and "a read-latency change needs deterministic bounds". No port, register or timestamp arithmetic changed, and no read latency changed.
  - BRAM fell by 2 RAMB18. The block-RAM ledger debits nothing (`MARK_II_AREA_PLAN.md:852-853`, `AREA_BUDGET.md:268`).
  - The per-table controls exist and pass (26/26).
  - The route figures are author-attested and internally consistent: 50,267-369=49,898; 54,413-1,193=53,220; WNS fall 0.177; WHS fall 0.012 (`MARK_II_AREA_PLAN.md:695-700`). They were not re-executed here.
  - The saving shortfall is reported honestly (`MARK_II_AREA_PLAN.md:714-716`), as the proof list requires.
- **RTL:** PASS.
  - Artifacts examined: the same RTL lines; `axis_fifo.v:292` (the bad-frame mask); `KL_gptp_engine.sv:349-350, 484-490, 513-519`; `lint_rtl_check.log` (90 <= 90); `gp_lint.log`.
  - Widths: `LANE_W_C=3` holds lanes 0-7 and `CNT_W_C=4` holds counts 0-8. The decode loop is bounded by `KEEP_W_C`.
  - Equivalence: the FIFO depth arithmetic is equal and the write enables are verbatim. A write and a read in the same cycle behave as the flop arrays did.
  - Reset: gating is unchanged in effect, and every reader is guarded.
  - No CDC or clocking change.
- **Robustness:** PASS.
  - Artifacts examined: reset during activity; malformed, runt, oversize and corrupted-`tkeep` input; overflow; and stalls. Each table's readers are gated by occupancy or the armed state after reset (`txret:537, 735`; `timer:113`). Warm resets run in traffic (`sim_main.cpp:147-170, 539-547`) and the lockstep stays at zero across them (`gptp_tables_all.log`).
  - Full-ledger allocation is an asserted invariant (`txret:684`).
  - The width guard is at `KL_gptp_shadow.sv:271`.
  - Probes: `rx_bad_mask_all_bits_sized` and `tx_fifo_user_disabled` are caught.
- **Tests:** PASS. R592-3-RES1 is wording only and carried.
  - Artifacts examined: `tb/verilator/gptp_tables/{gptp_tables_wrap.sv, sim_main.cpp, mutants.py, one_valued.tsv, Makefile, README.md, waivers.vlt}`, `scripts/gen_one_valued_table.py`, and the logs `gptp_tables_all.log`, `probes_summary.tsv`, `gptp_shadow_all.log`, `gptp_txts_all.log` and `gptp_plane_run.log`.
  - Every table's references are independent old-form models, apart from the strobe noted in RES1.
  - Every author control can fail and does. The census closes the one-valued-column class, and 10 of the 10 non-equivalent, non-declared reviewer probes are caught by the table's own lockstep or decode check.
- **Docs:** PASS. R592-3-RES1 and R592-3-RES2 are wording only and carried.
  - Artifacts examined: `MARK_II_AREA_PLAN.md:558-560, 672-718, 850-853`; `AREA_BUDGET.md:197-200, 267-268`; `TESTING.md:150, 409, 601`; the suite README; `MODULE_MATRIX.md`; three `README-tests.md`; eight pin-link pages; `rom_digests.tsv` (three rows, all at the unchanged image digest `c496ed8a`); and the donor `docs/MANAGER.md`, whose figures are consistent with 24 LUTRAM for 8x32 and 256 fewer registers.
  - The 22 doc and source gates all return rc 0.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment and round rulings on #640; the three changed RTL files and `axis_fifo.v` at the cited lines; route/gate figures in `MARK_II_AREA_PLAN.md:695-716`; `gptp_tables_all.log` | R592-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| RTL | CLEAN | `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, `KL_gptp_timer.sv`, `axis_fifo.v`, `KL_gptp_engine.sv` at the cited lines; `lint_rtl_check.log`; `gp_lint.log`; `probes_summary.tsv` | R592-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Robustness | CLEAN | Reset/occupancy gating at `txret:537,637-645,684,735`, `timer:91-118`; `KL_gptp_shadow.sv:271`; warm-reset phases in `sim_main.cpp`; `gptp_tables_all.log`; probes `rx_bad_mask_all_bits_sized`, `ledger_write_ungated_when_full`, `tx_fifo_user_disabled` | R592-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Tests | CLEAN (RES1 carried) | `tb/verilator/gptp_tables/*`; `scripts/gen_one_valued_table.py`; `gptp_tables_all.log` (36/36, 26/26); `probes/`, `probes2/`, `probe_logs/`; `gptp_shadow_all.log`, `gptp_txts_all.log`, `gptp_plane_run.log`, `*_default.log`, `gp_engine_run.log` | R592-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Docs | CLEAN (RES1, RES2 carried) | `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, `TESTING.md`, suite README, `MODULE_MATRIX.md`, README-tests, pin-link pages, `rom_digests.tsv`, donor `docs/MANAGER.md`, PR body; `gate_*.log` | R592-3 | `354f781828d8b4d73037129f297b072320a10f9c` |

## Real limits of this round

- No integrated route, no Vivado run and no resource-gate `check` were run here. The route figures and the gate PASS are the executor's attested receipts, listed by sha256 prefix in `HANDOFF.md` section 10. Those receipts are not published; this round checked only their arithmetic.
- No full sweep, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, Yosys portability, xvlog, builder or full donor `make tb` (out of this review's permissions). The executor ran them at heads whose compiled RTL equals this head; this round verified that equality by diff.
- `gptp_txts` ran with the LiteX model staleness check bypassed (`MILAN_LITEX_PYTHON=true`). The suite's simulation and controls ran in full.
- The author's unpublished differential hash (`5de6fe9546553c22`) was not relied on or reproduced.
- No hosted run exists at this head. No act or local CI replica was run (not permitted).
- Physical calibration NOT RUN. Field skips are not hardware proof; the #117 bench evidence comes after merge.
- Receipts had the local Verilator image path and home path redacted to `<PINNED_VERILATOR_IMAGE>` and `<HOME>`.
- R593-3 was in flight while this round ran and was not read.

## Pending manager duties

- Decide whether the below-range saving (107-253 LUTs against 500, range 300-700) is accepted for lane M7. Also decide the offered `tsf_r` option.
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link the receipts. Hosted `rtl-fast` and the ready-head exhaustive contexts are needed at the exact head; none exist now.
- Decide whether the route and gate receipts (`HANDOFF.md` section 10) should be published, or the gate re-checked at merge. D7 keeps the record unchanged.
- Carry R592-3-RES1 and R592-3-RES2 to the residue checklist.
- Route R593-1-S-03 to #495 at merge. R592-2-S1 remains optional.
- Publish the donor branch `640-m7` (`18dd997b`) on FPGA-gPTP before the parent; the remote branch already resolves to `18dd997b`. Handle donor PR FPGA-gPTP #78.
- If #621 lands in dev before merge, apply round 2's item-4 merge.
- After merge, run containment and close or move #640 per its umbrella acceptance (this lane does not reach 38,040 LUTs).

## Clone integrity after probes

`receipts/clone_integrity.txt`:

- HEAD and tree are as stated above. The index equals HEAD and the working tree equals the index.
- No entry is marked assume-unchanged or skip-worktree. Nothing is untracked or ignored.
- All 1,279 tracked blobs hash to HEAD's object ids, and their modes match.
- Gitlinks: `gptp-processor` `18dd997b`, `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e`. Each is checked out at its gitlink with no changes.

R592-3 FINISHED
