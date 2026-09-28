# [A425] Round 2 handoff: processor #131 / PR #132

Status: **all six round-2 items committed in the assigned order; no STOP.** Head
`2b38d68e704e8a62fbeae8171c9195ca93728488` on branch `131-d3-core-scalars` (round-1 head
`e1ae468f`, base `c951a9ff`). Not pushed; the PR is not edited (PR-BODY.md carries the text).

At the head: every processor suite (33 suites, 1,016,000 checks, 0 failing) and every
processor entry point returns rc 0, the in-tree D3 campaign kills 62 of 62 mutants with all
goldens passing, and nine of the eleven parent consumer commands return rc 0. The other two
are the round-1 pin state and one parent disposition this round's item 5 requires (see
"Suites and gates"): `pp_shadow` rc 2 on exactly the five declared round-1 ports, and the
evidence classifier rc 1 on the new `tb/pp_top/d3_mutants.py` (plus `retry_mutants.py`,
unexplained at this parent pin already). Both belong to the pin-adoption lane.

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5873696947 ·
TAKEN 5873705834 · REVIEW READY https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5875971493 · AECP hold-admission ruling 5873580386 (#131) · DR3a/DR4 ratification
https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5873060660 · reviews R390-1
(PR #132, 5873569558) and R391-1 (5873689921) · bank note 5873371256.

## Commits (one-line subjects, assigned order)

| Item | Commit | Subject |
|---|---|---|
| 1 R390-1 F2 = R391-1 F1 | `380a3e4` | Enforce the ratified 1,000 ms DR3a aggregate restore deadline from the accepted restore start, derived from the product clock |
| 2 R390-1 F1 = R391-1 F2 | `83e708a` | Admit at most one AECP record to the shared ingress while the D3 writer holds AECP, drop and count the rest at the slot gate |
| 3 R390-1 F3 | `b06130d` | Grade the derived DR2c backoff, the backoff's freedom of dispatch, blank-then-whole disagreement and the two-cycle roll-back strobe |
| 4 R391-1 F3 | `85b2f6f` | Grade a drained pass-1 read, a silent format judge and the rate walk to its eight-entry bound |
| 5 R390-1 F4 | `2fbe792` | Commit the D3 mutation driver in tb/pp_top and record every negative control in the suite READMEs |
| 6 R391-1 F4 | `2b38d68` | Give the writer's state-bus answer ports their contracts and state the unit of the new boundary parameters |

`e1ae468..2b38d68`: 22 files, +1,335 / -118. Line numbers are at `2b38d68`. Each commit was
validated before it was made (pp_top full, the touched unit suites, lint, `make check`, Yosys
on a scratch copy); the complete gates ran once, at the head.

## Items: change and proof

**1. The DR3a aggregate restore deadline (enforced, 1,000 ms from accepted `PP_CTRL[1]`).**
- Writer `hdl/aecp/KL_aecp_nvm_writer.sv`: parameter `RS_AGG_CYC_P` (`:177`), input
  `rs_go_i` (`:195`), counter `aggregate_ff` (`:550`) counting from the first cycle
  `rs_go_i` reads 1 through the binding walk, both passes and the roll-back to a terminal.
  `agg_expire_w` (`:547`) fires once, in the first cycle at or after the bound whose wait has
  no event in hand (the per-wait deadline's own rule, so no granted READ is orphaned); it joins
  the per-wait expiry in `expire_w` (`:530`), so the abort takes the per-wait path in the
  state the walk is in: cause 3, a READ in hand abandoned to the drain (`m_abort_o`, `:1059`,
  text unchanged), CLOSED before the image is proven, DEFAULTS in pass 0, the roll-back in
  pass 1 (still bounded per wait), CLOSED during the roll-back. Banner "THE AGGREGATE
  DEADLINE".
- Top `hdl/top/protocol_processor_top.sv`: one conversion, one rounding rule (R391-1 S1,
  taken): t ms = ceil(`CLK_HZ_P` x t / 1000), written reduced. `NVM_RS_TMO_CYC_P` =
  ceil(`CLK_HZ_P` / 50) (`:136`, was a floor), new `NVM_RS_AGG_CYC_P` = `CLK_HZ_P` (`:144`),
  backoff unchanged (its text is a reviewer anchor). Engine pass-through and
  `.d3_rs_go_i (restore_go_i)` (`:3613`).
- Bench: the wrap runs the top at a nominal `CLK_HZ_P` of 1,000,001 Hz (`tb/pp_top/pp_top_wrap.sv:402`)
  and no longer overrides the NVM deadlines, so the suite times the top's own derivations
  (per-wait 20,001, aggregate 1,000,001, backoff 500,001 clocks); the C++ re-derives them from
  the ruled milliseconds (`tb/pp_top/sim_main.cpp:52-55`). The device model gains a "withhold
  every grant" knob (`nv_gnt_every`).
- Named control **D3R13** (`tb/pp_top/d3_phases.hpp:1570`): every device request, the binding
  walk's included, granted 200 cycles inside the per-wait deadline (longest wait graded under
  20,001). All records saved: DEFAULTS registered by exactly the 1,000,001st clock counting the
  one that took `restore_go_i`, cause 3, nothing applied, the READ in hand drained, and once the
  device ends it a later SET persists. Erased device: the bound falls in pass 1 and the walk
  rolls back to DEFAULTS within one per-wait deadline of it. Plus **D3R8 deadline** (the
  per-wait abort lands on exactly the 20,001st stalled cycle: a floor derivation misses by one).
- Mutants killed: `no_aggregate_deadline`, `aggregate_mirrored` (100,000,000 literal),
  `aggregate_from_the_walk` (counts from the release), `per_wait_floor`.
- Docs: 08 F08.1 `T-NVM-RS-AGGREGATE`, section 2 rows ratified and converted; 01 F01.5
  `P-NVM-RS-AGG-CYC`; 07 5.3 aggregate paragraph and terminal rows; integrator 2 (26 = 26 = 26)
  and 9; diagram 21 inventory (PNG re-rendered and inspected).

**2. The AECP hold admission (ruling 5873580386).**
- Validator `hdl/packet_engine/KL_pp_rx_validator.sv`: input `aecp_hold_i` (`:101`); an AECP
  frame (0xFB on the own or AVDECC DA) is dropped at its slot gate, the subtype byte, its slot
  returned by the abort (`held_fail_w`, `:281`), and counted in a new saturating
  `rx_aecp_held_count_o` (`:140`, `:601`). Other subtypes are untouched.
- Top: `aecp_rx_res_r` (`:2649`) counts AECP records resident in the shared ingress (a
  parsed-header beat the latch takes, routed as the dispatch routes, until the engine's or the
  optional external drain's slot free); `aecp_rx_hold_w = !d3_done_w && (resident || one
  arriving)` (`:2655`): from reset to COMPLETE/DEFAULTS and for ever in CLOSED at most one AECP
  record occupies an RX slot and the AECP queue; `RX_SLOTS_P` - 1 stay ACMP's, ADP's, MAAP's.
  The counter is snapshot word 37 (`:4502`).
- Named controls: **D3O5** (`d3_phases.hpp:212`) CLOSED with `RX_SLOTS_P` + 2 = 6 AECP
  commands: a GET_RX_STATE after each answered in exactly 168 cycles, the idle latency; one held,
  five dropped and counted (side-port read of word 37), none answered; still 168 cycles after
  2,000 ms. **D3O6** (`:251`) a restore slowed 15,000 cycles on its next grant with 6 AECP
  commands queued after the release: GET_RX_STATE in the idle latency before the D3 terminal;
  the held command answered byte-exact at the terminal, five dropped and counted, never
  answered; a command after the terminal served with no drop. Unit level: `tb/rx_validator`
  F28 (`sim_main.cpp:719`). The unbounded-gating mutant `aecp_hold_unbounded` fails all six
  D3O5/D3O6 checks; `held_drop_uncounted` and `validator_admits_held_aecp` are killed too.
- The three documentation corrections: `docs/guides/integrator.md` (the "listener is
  unaffected" line and the CLOSED paragraph), `docs/architecture/07_memory_maps.md` (the CLOSED
  row, "the listener stays released", now states the admission; 5.5 lists word 37),
  `docs/architecture/03_packet_engine.md` rule (d) rewritten to the ruling, with rule (e)'s
  boot-hold exception (R390-1 S2), F03.2's held drop and a V10 row. Also 05 5.1 and the operator
  guide's word 37.

**3. R390-1 F3.** **D3S10** (`d3_phases.hpp:702`) now runs on the top's derived backoff
(500,001 clocks, no override) and grades each retry after the backoff and within one relatch
(`D3S10 timing`: 14 cycles here); `D3S10 backoff`: the writer owns in no backoff cycle and a
READ_DESCRIPTOR sent 1,000 cycles in is answered byte-exact 2,364 cycles later, before the
retry. **D3R4b** (`:1283`) blank in pass 0, whole in pass 1 aborts (cause 5) and rolls back;
**D3R4 strobe** (`:1249`) the roll-back strobe lasts two cycles with no debt owed. Killed:
`backoff_derivation` (`CLK_HZ_P / 200`), `backoff_holds_dispatch`, `disagree_one_direction`,
`rollback_one_cycle`, each with the reviewer's own anchor text.

**4. R391-1 F3.** **D3R5b** (`:1358`) pass 1's header READ never answered: deadline, cause 3,
roll-back to DEFAULTS, the READ drained; once the device ends it a later SET persists with
nothing unflushed. **D3R8b** (`:1779`) a silent format judge ends DEFAULTS by the per-wait
deadline, not the aggregate (within twice the deadline of the release). **D3R3b** (`:1194`)
over the suite's image re-packed with a ten-rate AUDIO_UNIT list (`d3_image_with_rates`,
`:813`): the eighth entry, read from the fourth lane, is restored; the ninth, listed but past
the eight-entry bound, is refused. Killed: `pass1_read_not_drained`, `judge_wait_unwatched`,
`rate_walk_stuck_on_first_lane`, `rate_walk_unbounded` (reviewer anchors).

**5. R390-1 F4.** `tb/pp_top/d3_mutants.py` (in the style of `gsi_mutants.py`): 62 mutants,
each in its own extract of `hdl/`, `tb/common/` and its suite; KILLED only on a completed run
with its tally, a non-zero exit and every named check failing; goldens first. Mutation-record
rows: `tb/pp_top/README.md` (58 rows), `tb/acmp_nvm/README.md` (3), `tb/rx_validator/README.md`
(M4); 09 8.2 points at the driver. Passes the parent's Python idiom gate (no host clock, no
process deadline). From the committed tree at the head: 62 of 62 KILLED, goldens PASS
([MUTANTS.md](MUTANTS.md)).

**6. R391-1 F4.** `sb_rvalid_i`, `sb_rdata_i`, `sb_err_i` carry `//!` contracts
(`KL_aecp_nvm_writer.sv:222-224`): the parent port-contract gate is at 111 <= 111. Naming:
`NVM_RS_TMO_CYC_P`'s comment states "clock cycles" (item 1); the engine's
`NVM_RETRY_BACKOFF_CYC_P` comment says "in clock cycles"; the writer's `DEB_TICKS_P` is renamed
`DEB_MS_P` (`:163`), T-NVM-DEBOUNCE in ms counted on the 1 ms tick. `_CYC_P` already counts as a
unit token in the parent gate (`NAME_UNIT` matches `_CYC_`); the two `_CYC_P` findings were
comments that documented ms without naming cycles, so no parent gate change is needed. The
naming gate passes (96 candidates, all recorded).

## Section 15.2 table and sweep

All 37 rows remain applied; [TABLE-15.2.md](TABLE-15.2.md) adds a round-2 column: 19 rows
unchanged, 18 updated by this round (08, 01, 07, 03, 05, 09, the integrator and operator guides,
diagram 21, the top, the engine, the suite READMEs), each saying what changed.

Named sweep at the head (`rg -n -U -i` of the contract's pattern over `docs hdl tb`), by
`sweep_reconcile.py` (the round-1 script, unchanged): **658 matching lines, 311 rewritten or
added by this lane (by blame), 347 with a location-specific scope reason, 0 unreviewed**
([SWEEP.md](SWEEP.md), 125,294 bytes). The context form (`-C 2 --sort path`): 2,990 lines,
1,389,010 bytes, SHA-256 `303b9cc63fcaaba1cec42a791e94c52998864c609e923558920a108f81d047c2`
(kept in scratch).

## Negative controls

[MUTANTS.md](MUTANTS.md) lists all 62 with their named assertions, failing-check counts and
first failing message. The round-2 additions:

| Control | Mutant | Named assertion(s) that fail |
|---|---|---|
| aggregate removed | `no_aggregate_deadline` | `D3R13 pass 0: DEFAULTS at clock`, `D3R13 pass 1` |
| aggregate mirrored, not derived | `aggregate_mirrored` | `D3R13 pass 0: DEFAULTS at clock` |
| aggregate counted from the release | `aggregate_from_the_walk` | `D3R13 pass 0: DEFAULTS at clock` |
| per-wait derivation floored | `per_wait_floor` | `D3R8 deadline` |
| unbounded AECP gating (the ruling's mutant) | `aecp_hold_unbounded` | `D3O5: in CLOSED each GET_RX_STATE`, `D3O6: during the slowed walk` |
| held drop not counted | `held_drop_uncounted` | `D3O5: one AECP command held`, `D3O6: at the terminal` |
| validator admits held AECP | `validator_admits_held_aecp` | `F28 held AECP`, `F28 rx_aecp_held counts both` |
| product backoff derivation | `backoff_derivation` | `D3S10 timing` |
| BACKOFF holds bus/dispatch | `backoff_holds_dispatch` | `D3S10 backoff` |
| blank-then-whole agreement | `disagree_one_direction` | `D3R4b` |
| one-cycle roll-back strobe | `rollback_one_cycle` | `D3R4 strobe` |
| pass-1 read not drained | `pass1_read_not_drained` | `D3R5b: once the device ends the drained pass-1 READ` |
| judge wait unwatched | `judge_wait_unwatched` | `D3R8b` |
| rate walk stuck on the first lane | `rate_walk_stuck_on_first_lane` | `D3R3b entry 7` |
| rate walk unbounded | `rate_walk_unbounded` | `D3R3b entry 8` |

The 47 round-1 controls keep their named assertions (`no_restore_watchdog` now plants on
`wait_expire_w` and names `D3R8: a READ granted` and `D3R8b`; `passes_may_disagree` also names
`D3R4b`). The reviewers' own scripts, rerun at the head, agree
([REVIEWER-RERUNS.md](REVIEWER-RERUNS.md)): R391-1's P1/P2 answer every GET_RX_STATE in 168
cycles, P5 ends at the aggregate, P3/P4 behave; all seven R391-1 mutants and R390-1's four are
KILLED; R390-1's probes answer every GET_RX_STATE in CLOSED and before the slowed terminal.

## DR3a measurements (ratified values, now enforced)

`./obj_dir/Vpp_top_sim --dr3a` at the head ([dr3a-2b38d68.txt](dr3a-2b38d68.txt), SHA-256
`27e26213c22bace00dcc22256ad71db9fe297ceac95ce18636124908a5fe72e8`): clk_i cycles from
`restore_go_i`; NVM model grants at once and streams a byte a cycle unless stated; bench image;
the wrap's clock is nominally 1,000,001 Hz, so RS_TMO = 20,001 and AGG = 1,000,001.
Conversions to the product: 50 MHz (20 ns/cycle) and 100 MHz (10 ns).

| Path | Terminal | go to release | go to terminal (cycles) | 50 MHz | 100 MHz |
|---|---|---:|---:|---:|---:|
| erased device, DRAM 31 | COMPLETE | 122 | 1,286 | 25.7 µs | 12.9 µs |
| nine records, DRAM 31 | COMPLETE | 122 | 1,989 | 39.8 µs | 19.9 µs |
| erased device, DRAM 143 | COMPLETE | 122 | 1,734 | 34.7 µs | 17.3 µs |
| nine records, DRAM 143 | COMPLETE | 122 | 2,661 | 53.2 µs | 26.6 µs |
| pass 0 DEVICE error | DEFAULTS (2) | 122 | 813 | 16.3 µs | 8.1 µs |
| pass 1 rule fetch error, roll-back | DEFAULTS (6) | 122 | 1,554 | 31.1 µs | 15.5 µs |
| pass 1 fetch 16,000 late, roll-back on debt | DEFAULTS (6) | 122 | 17,539 | 350.8 µs | 175.4 µs |
| NVM silent from its first read | DEFAULTS (3) | 20,003 | 40,006 = 2 x RS_TMO + 4 | 2 x 20 ms | 2 x 20 ms |
| image refused (magic) | CLOSED (7) | 122 | 164 | 3.3 µs | 1.6 µs |
| descriptor memory silent | CLOSED (7) | 122 | 8,188 | 163.8 µs | 81.9 µs |
| **every grant 200 inside the per-wait deadline, all records saved** | **DEFAULTS (3)** | 158,530 | **1,000,001 = AGG** (clock 1,000,001 from the accepted start) | **1,000 ms** | **1,000 ms** |

Longest waits: healthy D3 405/853 cycles (DRAM 31/143), binding 12; the slow device's longest
wait 19,812 of 20,001 (no per-wait deadline fires; the binding walk alone takes 158,530).
DR2a producer share unchanged: 50,028 bench cycles = the 500-tick window + 28 cycles.

Ratified constants at the product clocks, one conversion ceil(`CLK_HZ_P` x t / 1000): per-wait
20 ms = 1,000,000 (50 MHz) / 2,000,000 (100 MHz); aggregate 1,000 ms = 50,000,000 / 100,000,000;
backoff 500 ms = 25,000,000 / 50,000,000. Terminal after the bound: at once before the image is
proven (CLOSED) or in pass 0 (DEFAULTS); in pass 1 after the roll-back, whose debt wait and
re-LOCATE are each bounded by the per-wait deadline (worst 1,000 ms + 2 x 20 ms + 2 cycles;
R391-1's P5 rerun, the bound falling in pass 1: 542 cycles after it); during the roll-back at
once (CLOSED). The fire may wait for a cycle without an event, at most one record's byte stream
(none in the measured paths).

## DR4 scalar-stage contribution

Vivado 2026.1 (SW build 6511674) out-of-context synthesis, `syn/ooc/protocol_processor_ooc.tcl`,
part `xc7a100tfgg484-2`, 10 ns constraint, all six runs in this session on the same instrument
(reports in scratch):

| Shape | Base `c951a9f` LUT / FF / BRAM / DSP | Round 1 `e1ae468` | Round 2 head `2b38d68` | Lane 1 (head - base) | Round-2 increment | Writer `u_d3` LUT / FF |
|---|---|---|---|---|---|---|
| 1x1 (shipping) | 21,675 / 23,710 / 16.5 / 4 | 22,648 / 24,150 | 22,696 / 24,270 | **+1,021 LUT / +560 FF / 0 BRAM / 0 DSP** | +48 / +120 | 783 / 479 |
| 8x8 (diagnostic) | 29,059 / 31,164 / 24 / 4 | 30,115 / 31,703 | 29,854 / 31,619 | +795 / +455 / 0 / 0 | -261 / -84 | 1,111 / 527 |

Against the ruled scalar-core ceiling for lanes 1-2 (2,500 LUT / 1,400 FF / 0 BRAM / 0 DSP),
lane 1 uses 1,021 / 560 at 1x1, leaving 1,479 / 840 for lane 2. The validator grows +66 LUT /
+18 FF (the held drop and its counter). Synthesis WNS at 10 ns: -5.970 / -4.910 / -5.165 ns
(1x1 base / round 1 / head), -7.886 / -8.961 / -8.127 ns (8x8): synthesis estimates only.
Note: the round-1 packet's absolute totals for the same recipe and build (base 1x1 23,489 /
24,408) are about 1.8k LUT / 0.7k FF higher than this session's; I could not find the cause
(same tool build, same Tcl, same shape arguments), so only same-session deltas compare. Its
round-1 delta was +1,076 / +614; this session's round-1 delta is +973 / +440. Post-place and the
8x8 post-place obligation stay lane 2's (open, not waived).

## Parent-visible changes (for the pin-adoption lane)

- New top parameter `NVM_RS_AGG_CYC_P`, default `CLK_HZ_P` (1,000 ms; F01.5
  `P-NVM-RS-AGG-CYC`, F08.1 `T-NVM-RS-AGGREGATE`). **No new top port** this round.
- `NVM_RS_TMO_CYC_P` default is now ceil(`CLK_HZ_P` / 50) (was a floor: identical at 50 and
  100 MHz and at any clock divisible by 50 Hz).
- New side-port snapshot word 37 (host word address 0x20025): [15:0] the saturating count of
  AECP frames dropped at the slot gate while the D3 writer held AECP with one AECP record
  resident; [31:16] reads 0. Read through the existing bridge; the parent's register map and
  operator notes should list it.
- The AECP hold admission: from reset to COMPLETE/DEFAULTS, and for ever in CLOSED, one AECP
  command is held (answered at the release, never in CLOSED); every further AECP frame is
  dropped, counted and unanswered (the controller retries). ACMP, ADP and MAAP keep their slots
  and latency.
- The restore can now end on the aggregate: `rs_cause_o` 3 with DEFAULTS (pass 0, or pass 1
  rolled back) or CLOSED (before the image is proven, e.g. a binding walk that alone outlasts
  1,000 ms, or during the roll-back). Firmware's bounded wait for the restore should allow for
  1,000 ms plus a roll-back.
- R390-1 S1, named explicitly: the binding manager's alarm now follows at least 2 x
  `NVM_RETRY_BACKOFF_CYC_P` (about 1 s) of backoff after the first failure; the side port's
  control word 1 reads busy 0, done 0, fail 1 in CLOSED; `NVM_RS_TMO_CYC_P` bounds every D3 wait
  (the roll-back's debt wait and re-LOCATE included), not only the binding walk's reads.
- Parent evidence classifier: `DUT_READER_DISPOSITIONS["protocol-processor/tb/pp_top/d3_mutants.py"]`
  = "mutation campaign; it plants one D3 saved-state defect from its own table into an isolated
  copy and requires every named check to fail in a completed run; no expected value is read
  from the text" (proof in GATES.md).
- Not parent-visible: the writer's `DEB_TICKS_P` is now `DEB_MS_P` (module-internal; never in
  the parent's naming budget); new internal ports `rs_go_i`/`d3_rs_go_i`, `aecp_hold_i`,
  `rx_aecp_held_count_o` sit inside the top.

## Suites and gates

[SUITES.md](SUITES.md) (per suite) and [GATES.md](GATES.md) (per command, rc, seconds, log
SHA-256) at the head, run by [gates.py](gates.py) with the pinned Verilator 5.050 wrapper:

| Tree | Entry point | rc |
|---|---|---:|
| processor | `./scripts/run_suites.sh` (33 suites, 1,016,000 checks, 0 failing; pp_top 7,859, rx_validator 437) | 0 |
| processor | `./scripts/lint_hdl.sh` | 0 |
| processor | `make check` (params 26/26/26, links, matrices, WaveDrom, export freshness) | 0 |
| processor | `python3 scripts/gen_matrix.py --check` | 0 |
| processor | `./syn/yosys/run.sh` | 0 |
| processor | `make -C tb/nvm_port figures` | 2, then **0** (see below) |
| processor | `python3 tb/pp_top/d3_mutants.py` (62 of 62 KILLED, goldens PASS) | 0 |
| processor | `make -C tb/srp_top mutants` (64 checks, coverage 49/49) | 0 |
| parent | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 |
| parent | `xvlog_gate.py --check` (4 findings == ratchet, none in lane files) | 0 |
| parent | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 |
| parent | `sw/builder/test_builder.py` | 0 |
| parent | `make -C tb/verilator/pp_shadow -j8` | **2** |
| parent | `check_port_contracts.py` (111 <= 111) | 0 |
| parent | `measure_naming.py --check` (PASS, 96 recorded) | 0 |
| parent | `measure_test_evidence.py --check` | **1** |
| parent | `docs_check.py` | 0 |

- `figures`: the first run failed because my clone of the lane lacked the history the script
  reconstructs its matrix injection from (`dc354be~1`, `62d96d6~1`, on the processor's PR #13
  head); after fetching the pull-request heads into that scratch clone (read-only) it returned
  rc 0 with every figure agreeing.
- `pp_shadow` rc 2: the same 20 `PINMISSING` warnings as the manager's round-1 receipt, for
  the five declared round-1 ports; no new pin this round.
- Evidence classifier rc 1: `retry_mutants.py` (unexplained at this parent pin since before
  this lane) and the new `d3_mutants.py`; with both dispositions added in a scratch copy, rc 0
  and nothing else (GATES.md).
- The scratch parent is a clone of the read-only checkout at `7a7582f0` (the manager's bank
  uses its dev pin `ce550952`, where `retry_mutants.py` is already explained).

## Notes for review

1. Before the image is proven the aggregate ends CLOSED: that is the writer's existing abort
   path in that state (an unproven image cannot be judged against), which I read as "CLOSED as
   the state requires". It is reachable only when the binding walk or the image proof alone
   outlasts 1,000 ms.
2. The bench's clock is nominal (1,000,001 Hz) and separate from its compressed timebase; the
   odd hertz makes ceil differ from floor and from a count of 1 ms ticks by one clock, which is
   what D3R8 and D3R13 grade. BW3 and D3R8 now use the derived 20,001 (their tolerances are
   unchanged).
3. Parent contract section 5.1 names the writer's debounce `DEB_TICKS_P`; item 6 preferred a
   rename, so the writer's is `DEB_MS_P` (the binding manager keeps `DEB_TICKS_P`); F01.5 and 08
   map both.
4. Outside the ruling, unchanged: with the hold released and the engine serving, four
   READ_DESCRIPTORs in flight can still fill the four-slot pool (R390-1's COMPLETE-case probe
   gives the same three misses at `e1ae468` and here). Whether service time wants a share is
   the manager's call.

## Packet

HANDOFF.md, PR-BODY.md (Round 2 section), TABLE-15.2.md, SWEEP.md and `sweep_reconcile.py`,
MUTANTS.md, SUITES.md, GATES.md and `gates-results.jsonl`, REVIEWER-RERUNS.md,
`dr3a-2b38d68.txt`, `gates.py` and `parent_at.sh` (the scratch runners). Logs, synthesis reports
and scratch trees stay under `$VALIDATION_STORAGE/a425` (not copied: sizes and hashes above).
