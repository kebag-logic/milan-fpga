# [A418] D3 lane 1 handoff: processor core and scalar records

Status: **all six contract items implemented and committed in order.** Final head `e1ae468f7e237f321ce5fee19e59ae157da4b83d` (branch `131-d3-core-scalars`, base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`). At that head every processor suite and entry point returns rc 0; the parent xvlog, C++ and Python idiom gates return rc 0; the parent evidence classifier returns rc 1 with exactly the single pre-existing finding the base head already had (`tb/acmp_talker/retry_mutants.py`, not a lane file). The mutation campaign kills 47 of 47 mutants. DR3a numbers are submitted for the manager's ratification, not ratified here.

Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`. Read-only parent authority: `kebag-logic/milan-fpga` at `7a7582f03ce5ba7863a90ac342c21be18d90db0b`, `docs/design/SAVED_STATE_MATERIALIZATION.md` section 18.1, table 15.2, rulings DR1a-DR6 and the DR2c-carrier correction.
Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5868003073 · TAKEN: 5868015000 · earlier STOP: 5868697891 · REVIEW READY: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5873035418 · correction: https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5868716535 and disposition 5868716919.

## Commits (one-line subjects, in the assigned order)

| Group | Commit | Subject |
|---|---|---|
| 1 arbiter/ownership, AECP hold | `66267d9` | Hold AECP dispatch from reset in the D3 writer as arbiter manager 1 |
| 2 scalar records, command-side triggers | `4dd37c2` | Persist the scalar records from command-side change triggers in the D3 writer |
| 3 both passes, validation, combined restore | `5e1476d` | Restore the scalar records in two agreeing passes under the SET rules and combine the restore verdicts |
| 4 rollback and debt | `505524e` | Roll both stores back on a pass-1 abort, hold the roll-back while descriptor debt is owed, and re-prove the image |
| 5 DR2c for both producers | `f72a2d2` | Space both record producers' write attempts by the DR2c backoff and grade count, timing and alarm revocation |
| 6 table 15.2 and sweep | `39789f9` | Synchronize the section 15.2 contracts, guides, diagrams and suites with the D3 writer, and grade the volatile set and the DR3a spans |
| 6 (test tightening) | `81c8a5f` | Fail the one saved record on a device error in both passes and print the DR2a producer span |
| 6 (generated tally) | `e1ae468` | Record the dynamic-state suite's regenerated shape tally after its change-qualifier checks |

48 files changed from the base: 4,372 insertions, 513 deletions. Line references below are at `e1ae468` (unchanged since `81c8a5f`, which differs only in `tb/dyn_state/shape_tally.txt`, the tracked tally the dyn_state suite deletes and regenerates on every run; its committed copy had gone stale with the new H checks, so a suite run dirtied a clean checkout).

## Contract items: change and proof

**1. Arbiter/ownership and AECP hold.** New `hdl/aecp/KL_aecp_nvm_writer.sv` is manager 1 of the landed `KL_pp_nvm_mgr_arb` (top `:2615`); no second arbiter. `own_o` (`writer:983`) holds dispatch from reset to the terminal and for ever in CLOSED, and in service from ACQUIRE to the end of one latch; `bus_o` (`:984`) selects the state bus only from reset to the terminal and during the latch (a program the engine took before ACQUIRE keeps the bus: the deadlock found in group 2). Engine dispatch hold `!d3_own_w` at `engine:2426`, `:2463`, `:2586`; 2:1 state-bus selection and masked µCPU answers; prog_busy `:1824`. Image proof: `img_valid_i` or a LOCATE of ENTITY 0; error ends CLOSED cause 7 (`writer:516`). S1/S3/S4 and the S2 guard are reused unchanged. Proof: `tb/pp_top` D3O1-D3O4, D3S9, D3S11, D3R9; controls `hold_released_at_go`, `dispatch_not_held`, `own_taken_at_the_walk`, `image_unproven_continues`, `latch_ignores_program` killed.

**2. Scalar records and command-side triggers.** Records `0x00` cfg u16, `0x02+AU` rate u32, `0x0A+CD` clock source u16, `0x30+SI`/`0x40+SO` formats u64, `0x50+SO` offset u32, F07.8 framed (magic, layout 2, id, length, CCITT-FALSE crc16). Trigger: `KL_aecp_dyn_state.wr_chg_o` (`dyn_state:287`), an accepted write that changes `{value, valid}` for selectors 0-5 (DR2b), tapped `engine:1819` only while the µCPU drives the bus; IDENTIFY and restore writes excluded. Set/clear by group AND index, taint, change wins the done edge, first-dirty debounce, round-robin burst (`writer:805`, `:862-:873`). Proof: D3S1-D3S8 with real AECP SETs, byte-exact frames against an independent builder; `tb/dyn_state` H. Controls `TRG_cfg` ... `TRG_ptof`, `taint_ignored`, `clear_wins_same_edge`, `clear_by_group`, `clear_by_index`, `identify_is_a_change`, `unchanged_compare_ignores_validity` killed.

**3. Both passes, validation and combined restore.** Pass 0 whole/blank; pass 1 agreement (cause 5, `writer:507`), frame check, the SET programs' value rules (configurations_count, AU rate list at 144, clock_sources_count, the integrator's format judge kind 0 sel 15 bit 0, PTOF bit 31), apply with the valid flag (`:535`); UNFRAMED blank vs DEVICE abort; torn cause 1; deadline cause 3 with the granted read abandoned to the drain (`:496`); descriptor error cause 6, never a refusal. Top: `restore_done_o` = binding terminal AND release AND D3 done (`top:2584`), busy/fail/blank combined (`:2585-:2591`, blank excludes failure), `restore_closed_o`, `rs_cause_o`, `restore_cause_o`; ADP enable = `entity_enable_i && restore_done_o` (`:1680`); side port keeps the requested enable. Proof: D3R1 (all nine rows, first and last index, cleared-first value and valid, real GETs, volatile set gone), D3R2-D3R9; controls `RPL_*` x6, `rule_ignored`, `passes_may_disagree`, `device_error_reads_as_blank`, `unframed_reads_as_device_error`, `desc_error_is_a_refusal`, `no_restore_watchdog`, `restore_writes_are_changes`, `enable_not_released_by_restore`, `done_without_d3`, `blank_ignores_d3` killed.

**4. Rollback and debt.** A pass-1 abort raises `rb_rst_o` (`writer:1012`) resetting `KL_aecp_dyn_state` and `KL_aecp_desc_store` together (`engine:1528`) for at least two cycles and while `desc_debt_i` (`writer:701`); the guard keeps the hard reset only; the store's reset re-arms its watchdog and re-walks the image; the re-LOCATE proves it (DEFAULTS, `restore_rb_o`) or ends CLOSED (`:705`). The listener, its gate and the binding manager are untouched. Proof: D3R4, D3R7, D3R10 (4,000/5,000/16,000/30,000-cycle late bursts), D3R11 (restored binding kept), D3R12; controls `no_rollback`, `dyn_not_rolled_back`, `store_not_rolled_back`, `rollback_ignores_debt`, `closed_releases_the_entity` killed.

**5. DR2c for both producers.** Top parameter `NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 2) + (CLK_HZ_P % 2)` (`top:139`) bound to both producers. Writer: attempts start at the grant, three in all, BACKOFF from the error then a fresh latch, attempts never replenished, sticky alarm (`writer:863`, `:886`, `:967`). Binding manager: `H_FL_BACKOFF` before relatch (`shadow:894`, `:915`, `:924`). `nvm_alarm_o` = either producer's (`top:2595`). DR2c-carrier correction applied: only a producer's own exhaustion raises the alarm; the backend owns a record from its window done. Proof: D3S10 (count, timing, no fourth, revocation) and `tb/acmp_nvm` E8-E11; controls `no_backoff_d3`, `no_backoff_binding`, `fourth_attempt`, `fourth_attempt_binding`, `alarm_forgiven_by_success`, `alarm_forgiven_binding` killed.

**6. Table 15.2 and sweep.** All 37 rows applied: [TABLE-15.2.md](TABLE-15.2.md) gives the status and location of each. The 6.3 wording that follows 7.1 is reconciled in `docs/architecture/08_timing.md` ("One alarm"). Diagrams 20, 21, 23 and 24 edited, PNGs re-rendered with `rsvg-convert` and inspected; WaveDrom F02.8 re-rendered; `scripts/check-integrator-params.py` rc 0 (25/25/25); MODULE_MATRIX regenerated in group 1. The ROM generated by `gen_ucode.py` is byte-identical after its comment rewrites.

## Section 15.2 sweep

The exact named search (`rg -n -U -i -C 2 ... docs hdl tb`) at `e1ae468`: rc 0, 2,860 output lines, 1,376,047 bytes (kept in scratch, over the packet size limit). Its file order varies between runs, so the stable identity is the same search with `--sort path`: SHA-256 `a5a95acb4aa3bae8f9a8603d481d7ecf9b27694fd986a9604c0164678656c39d`, same size. Without context it returns 624 matching lines: 276 were rewritten or added by this lane (by blame) and state the D3 contract; each of the other 348 carries a location-specific scope reason; 0 unreviewed. The line-by-line table is [SWEEP.md](SWEEP.md), produced by `sweep_reconcile.py` in this packet (it fails on any unreviewed match).

## Negative controls (mutation campaign)

`d3_mutants.py` in this packet plants each mutation in a scratch copy, requires a clean golden build per suite, and counts a mutant killed only when the build succeeds, the simulation completes with its tally, and every named check fails. The campaign at `39789f9`: goldens PASS (pp_top, acmp_nvm); 46 of 47 mutants killed. The survivor, `device_error_reads_as_blank`, failed D3R5, D3R11 and D3R12 but not D3R6: its single injected device error hit pass 0 only, and pass 1's disagreement (cause 5) kept the restore failed, so the H8 property held by a second mechanism. `81c8a5f` makes D3R6 inject the error on every read of the record and require cause 2. Campaign at `81c8a5f`: 47 of 47 killed. **Final campaign at `e1ae468`: 47 of 47 killed, both goldens PASS, none survived or refused** ([MUTANTS.md](MUTANTS.md); summary SHA-256 `2fc7dfa3e3cd0277f207134aabcbdbc7ffa3021bf75a7898ca1788e780ac8ef8`, logs in scratch).

| Contract control | Mutant(s) | Named failing assertion |
|---|---|---|
| Delete each scalar trigger | `TRG_cfg`, `TRG_rate`, `TRG_clks`, `TRG_fmti`, `TRG_fmto`, `TRG_ptof` | `D3S1 <group>` |
| Delete each scalar replay | `RPL_cfg`, `RPL_rate`, `RPL_clks`, `RPL_fmti`, `RPL_fmto`, `RPL_ptof` | `D3R1 <group>` |
| Keep a store uncleared | `store_not_cleared` | `D3R1: every row at its reset value` |
| Ignore valid flags | `valid_not_cleared`; `unchanged_compare_ignores_validity` | `D3R1: every row at its reset value`; `D3S8 validity` |
| Clear by group or index alone | `clear_by_group`, `clear_by_index` | `D3S6 group`, `D3S6 index` |
| Drop taint / same-edge precedence | `taint_ignored`, `clear_wins_same_edge` | `D3S4 taint`, `D3S5 same edge` |
| Count restore writes as changes | `restore_writes_are_changes` | `D3R1: no restore write is a change` |
| Collapse DEVICE into blank (and the reverse) | `device_error_reads_as_blank`, `unframed_reads_as_device_error` | `D3R5 device error on the header`, `D3R6: the one saved record`; `D3R6: an erased device restores blank` |
| Omit descriptor rollback or debt hold | `no_rollback`, `dyn_not_rolled_back`, `store_not_rolled_back`, `rollback_ignores_debt` | `D3R4`, `D3R10 5000`, `D3R10 16000` |
| Release AECP/ADP early | `hold_released_at_go`, `dispatch_not_held`, `own_taken_at_the_walk`, `enable_not_released_by_restore`, `done_without_d3`, `closed_releases_the_entity` | `D3O1`, `D3R9: the held SET`, `D3R1: the enable requested from reset`, `D3R12` |
| Release quarantine by time alone | `quarantine_released_by_time` | `D3R5: once the device ends the drained read a later SET persists` |
| Zero, boundary, corrupt, refused, indefinite delay | `rule_ignored`, `no_restore_watchdog`, `passes_may_disagree`, `desc_error_is_a_refusal`, `image_unproven_continues` | `D3R2: COMPLETE`, `D3R8`, `D3R4`, `D3R7`, `D3O2`/`D3O3` (D3R3 grades zero/boundary acceptance, D3R8 the deadline boundary) |
| Remove backoff | `no_backoff_d3`, `no_backoff_binding` | `D3S10 timing`, `E9 DR2c timing` |
| Permit a fourth attempt | `fourth_attempt`, `fourth_attempt_binding` | `D3S10 count`, `E8 DR2c count` |
| Forgive an exhausted alarm | `alarm_forgiven_by_success`, `alarm_forgiven_binding` | `D3S10 revocation`, `E11 DR2c revocation` |
| Persist IDENTIFY / volatile state | `identify_is_a_change` | `D3S7` (plus D3R1 volatile checks: IDENTIFY 0, lock free, registry empty after the cycle) |
| Latch over a running program; blank ignoring D3 | `latch_ignores_program`, `blank_ignores_d3` | `D3S9`, `D3R1: COMPLETE` |

Existing controls reconciled (#18/#19/#21): those issues are `tb/nvm_port` limitations (no reset mid-commit; three port mechanisms without coverage; no handshake-misbehaving port model); this lane changes no port logic and closes none of them. `09_verification.md` 8.2 records that.

## DR3a measurements (submitted for ratification; not ratified here)

Measured with `./obj_dir/Vpp_top_sim --dr3a` (after `make gsi-build` in `tb/pp_top`; the suite run builds the same binary) at `e1ae468`, from a clean checkout; output SHA-256 `6041757f6e3df24ba349876324dde6088cd33270ddcfa69fe7e21cde015cbae8`, byte-identical at `81c8a5f`: clk_i cycles from `restore_go_i` (the processor's view of an accepted `PP_CTRL[1]`) to the terminal. Bench models: the NVM device grants at once and streams one byte per cycle; descriptor memory first-word latency 31 cycles (suite default) or 143 (the reference SoC's measured ~1,424 ns at 100 MHz); the bench image is the suite's small model; `RS_TMO_CYC_P` is 20,000 in the bench. Conversions: 50 MHz product clock (20 ns/cycle) and the 100 MHz processor default (10 ns).

| Path | Terminal | go to release | go to terminal (cycles) | at 50 MHz | at 100 MHz | Longest single wait: binding / D3 (cycles) | Longest D3 record op |
|---|---|---:|---:|---:|---:|---|---:|
| erased device, DRAM 31 | COMPLETE | 122 | 1,286 | 25.7 µs | 12.9 µs | 12 / 405 | 12 |
| nine records saved, DRAM 31 | COMPLETE | 122 | 1,989 | 39.8 µs | 19.9 µs | 12 / 405 | 31 |
| erased device, DRAM 143 | COMPLETE | 122 | 1,734 | 34.7 µs | 17.3 µs | 12 / 853 | 12 |
| nine records saved, DRAM 143 | COMPLETE | 122 | 2,661 | 53.2 µs | 26.6 µs | 12 / 853 | 31 |
| pass 0: DEVICE error on a header | DEFAULTS (2) | 122 | 813 | 16.3 µs | 8.1 µs | 12 / 405 | 25 |
| pass 1: rule fetch error, roll-back | DEFAULTS (6) | 122 | 1,554 | 31.1 µs | 15.5 µs | 12 / 540 | 27 |
| pass 1: fetch 16,000 cycles late, roll-back held on debt | DEFAULTS (6) | 122 | 17,539 | 350.8 µs | 175.4 µs | 12 / 11,920 | 27 |
| NVM device silent from its first read | DEFAULTS (3) | 20,002 | 40,004 = 2 x RS_TMO + 4 | 40.0 ms at the 20 ms candidate | 40.0 ms | 19,999 / 19,999 | - |
| descriptor image refused (magic) | CLOSED (7) | 122 | 164 | 3.3 µs | 1.6 µs | 12 / 39 | - |
| descriptor memory silent | CLOSED (7) | 122 | 8,188 = 2 x DESC_MEM_TMO_CYC_P | 163.8 µs | 81.9 µs | 12 / 8,063 | - |

Image walk from reset (header, index map, names): 199 cycles (DRAM 31), 535 (DRAM 143) for the bench image. The longest healthy wait (405/853) is the image proof: the D3 walk starts before the store finishes its boot walk and its LOCATE waits for it.

Per-wait candidate: 20 ms = `ceil(core_hz x 20 / 1000)` = 1,000,000 cycles at 50 MHz, 2,000,000 at 100 MHz. It exceeds every measured healthy wait (at most 853 cycles = 17.1 µs at 50 MHz) and the largest record transaction measured here (31 cycles for a 16-byte record) by more than three orders of magnitude. For the product's 8x8 image the names table (99 x 64 B = 792 beats in two bursts) and the index map dominate the image walk; with ~72 cycles of first-word latency per burst at 50 MHz that estimate is about 1,000-1,500 cycles (20-30 µs): an estimate, not a measurement. The largest future record (an 8x8 output map, 584 B framed) is a later stage's.

Aggregate candidate: 1,000 ms = 50,000,000 cycles at 50 MHz, 100,000,000 at 100 MHz. Every measured path ends far inside it; the longest is the silent device at 2 x the per-wait deadline (40 ms at the candidate). **Finding for the ratification:** this processor enforces no aggregate counter; only each wait is bounded. A device that answers every wait just inside the per-wait deadline could stretch a walk to (number of waits) x 20 ms: the D3 walk has about 2 passes x 27 records x (grant + 8 header bytes + up to 8 payload bytes + end) ~ 970 waits (~19 s), the binding walk 8 x (1 + 8 + 20 + 1) = 240 (~4.8 s). The manager should either accept per-wait enforcement with the aggregate as a measured budget, or rule an aggregate counter (processor or firmware reporting) before lane 2 implements. Both numbers remain initial candidates.

DR2a (this producer's share): one real `SET_STREAM_INFO` with no other traffic reads pending for 50,028 bench cycles from acceptance to the port's done of its WRITE: the 500-tick first-dirty window (bench ms = 100 cycles) plus 28 cycles of latch, frame and write, i.e. 500 ms + 0.56 µs at 50 MHz. The window-to-durable part (the integrator's 1,000 ms window, capture and flash) is lane 2's to measure.

## DR4 scalar-stage contribution

Vivado 2026.1 out-of-context synthesis of `protocol_processor_top`, part `xc7a100tfgg484-2`, `syn/ooc/protocol_processor_ooc.tcl` (10 ns constraint), matched heads: base `c951a9f`, candidate `f72a2d2` (the `hdl/` and `syn/` trees of group 6 differ from `f72a2d2` in comments only: the code-token diff is empty and the generated ROM is byte-identical).

| Shape | Base LUT / FF / BRAM / DSP | Candidate | Delta | Writer instance `u_d3` |
|---|---|---|---|---|
| 1x1 (shipping) | 23,489 / 24,408 / 16.5 / 4 | 24,565 / 25,022 / 16.5 / 4 | **+1,076 LUT (logic; LUTRAM +0) / +614 FF / 0 BRAM / 0 DSP** | 871 LUT / 459 FF |
| 8x8 (diagnostic) | 30,066 / 32,078 / 25.5 / 4 | 31,336 / 32,752 / 25.5 / 4 | +1,270 LUT / +674 FF / 0 / 0 | 1,104 LUT / 504 FF |

Against the ruled scalar-core ceiling for lanes 1-2 combined (2,500 LUT-equivalents / 1,400 FF / 0 BRAM / 0 DSP), lane 1 uses 1,076 / 614 at 1x1, leaving 1,424 / 786 for lane 2's parent glue. Synthesis WNS at the 10 ns constraint: base -5.619 ns, candidate -5.017 ns (1x1); -10.532 / -10.197 ns (8x8); both shapes' synthesis paths fit a 20 ns (50 MHz) period only as a synthesis estimate. Post-place, the corrected #607 constraints and firmware size (no firmware change here) are lane 2's; the 8x8 post-place obligation stays open and blocked, not waived. Reports stay in scratch (`util.rpt`, `util_hier.rpt`, `timing.rpt` per run).

## Parent-visible changes (for pin adoption)

- New top ports: `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`, `restore_cause_o[1:0]` (the binding walk's cause, newly exported), `d3_unflushed_o`.
- New top parameter: `NVM_RETRY_BACKOFF_CYC_P` (default `ceil(CLK_HZ_P / 2)`); `NVM_RS_TMO_CYC_P` now also bounds every D3 wait.
- Changed semantics: `restore_done_o`/`restore_busy_o`/`restore_fail_o`/`restore_blank_o` combine both walks (blank never with fail); `nvm_alarm_o` is either producer's; the ADP engine sees `entity_enable_i && restore_done_o` (the side port's lock keeps the requested enable); AECP dispatch is held from reset to the D3 terminal (for ever after CLOSED); manager 1 of the NVM arbiter now issues D3 record READs and WRITEs on the device face (record ids `0x00`, `0x02+`, `0x0A+`, `0x30+`, `0x40+`, `0x50+`); an unprovable descriptor image now ends CLOSED instead of serving BAD_ARGUMENTS.
- Parent glue per D3 5.2: `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`; `aecp_dyn_dirty_o` stays exported as a diagnostic only; `alarm_i` takes the combined `nvm_alarm_o`; restore status takes the combined verdicts. Firmware must load and CRC-check the AEM before `PP_CTRL[1]` (D3 5.3 change 1) or the restore ends CLOSED.
- Unchanged: the device face signals, the port's framing and causes, the side-port map (control word 1 now reads the combined verdicts; CLOSED reads busy 0, done 0, fail 1).

## Suites and gates

At `39789f9` (group 6 first commit): processor `./scripts/run_suites.sh` rc 0 (33 suites, 1,015,938 checks, 0 failing; pp_top 7,841), `lint_hdl.sh` rc 0, `make check` rc 0, `gen_matrix.py --check` rc 0, `syn/yosys/run.sh` rc 0; remaining rows recorded below when the runs end.

Final head `e1ae468f7e237f321ce5fee19e59ae157da4b83d`, run by `gates.py` (this packet) in scratch clones: the processor clone checked out at the head; the scratch parent copy (gPTP and `third_party/verilog-axis` initialised from the pin lane as the disposition shows) with its `protocol-processor` gitlink staged at the same head. Every command in the foreground; logs, sizes and SHA-256 in scratch `results.jsonl`.

| Tree | Entry point | rc | Seconds | Result |
|---|---|---:|---:|---|
| Processor | `./scripts/run_suites.sh` | 0 | 573.2 | 33 suites, 1,015,938 checks, 0 failing ([SUITES.md](SUITES.md)); pp_top 7,841, acmp_nvm 353, dyn_state 118 |
| Processor | `./scripts/lint_hdl.sh` | 0 | 12.2 | every top lints clean, `KL_aecp_nvm_writer` included |
| Processor | `make check` | 0 | 28.8 | diagram lint, WaveDrom freshness, links, compliance matrix, module matrix, parameters (25/25/25), export freshness |
| Processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 94 rows, 0 untested |
| Processor | `./syn/yosys/run.sh` | 0 | 79.3 | portability synthesis incl. `KL_aecp_nvm_writer` and the AECP memory mapping |
| Processor | `make -C tb/srp_top mutants` | 0 | 1239.7 | 64 checks, assertion coverage 49/49 |
| Processor | `make -C tb/nvm_port figures` | 0 | 243.7 | every measured figure and historical form agrees (port banner line count preserved) |
| Parent scratch | `python3 scripts/xvlog_gate.py --check` | 0 | 139.3 | PASS, 4 findings == ratchet (all pre-existing, none in lane files) |
| Parent scratch | `python3 scripts/measure_test_evidence.py --check` | **1** | 5.5 | exactly the base head's single finding: `protocol-processor/tb/acmp_talker/retry_mutants.py` UNEXPLAINED (#129's file; its disposition belongs to the parent). No lane file is a finding; the lane's mutation driver is out of tree for that reason. |
| Parent scratch | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | every ratchet at budget 0 (G3-G5 heads had one multi-declarator finding from an array initialiser; fixed in group 6) |
| Parent scratch | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | clean |

After the suite run the processor scratch clone is clean (`git status` empty). Earlier heads: G1 `66267d9`, G3 `5e1476d` and G6 `39789f9` gate runs are recorded in scratch (`gates-g1`, `gates-g3`, `gates-g6`); at `5e1476d` the C++ idiom gate returned rc 1 on the array initialiser noted above.

## Prior-session STOP evidence (resolved)

`run_probe.py`, `carrier_probe.sv`, `carrier_probe.cpp`, `probe-*.log`, `probe-results.json`, `ARTIFACTS.json`, `STOP-COMMENT.md`, `processor-*.log`, `processor-results.jsonl`, `gate-*.log`, `parent-nvm-backend.log` and `source-copy-verification.json` are the earlier STOP's evidence at the unchanged base, kept as history. `FINAL-STATE.json`, `EVIDENCE.json`, `SUITES.md`, `TABLE-15.2.md`, `SWEEP.md`, `MUTANTS.md` and the three scripts `gates.py`, `d3_mutants.py`, `sweep_reconcile.py` are this lane's. The owner resolved it (correction and disposition linked above); this lane implements the corrected contract.

## Remaining obligations (outside this lane)

Names and maps (lanes 3 and 4), parent glue, targeted physical scalar/PTOF proof, post-place area and the DR2a window-to-durable time (lane 2), the full fault campaign (lane 5), #15's reusable-service criterion (DR1a) and #20's reconciliation (DR1b). DR3a numbers await the manager's ratification or revision before lane 2 implements.
