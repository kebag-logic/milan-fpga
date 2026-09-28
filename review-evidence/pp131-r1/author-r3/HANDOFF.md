# [A429] Round 3 handoff: processor #131 / PR #132

Status: **all four round-3 items and the taken suggestion committed in the assigned order;
no STOP.** Head `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` on branch `131-d3-core-scalars`
(round-2 head `2b38d68e`, base `c951a9ff`). Not pushed; the PR is not edited (PR-BODY.md
carries a Round 3 section).

At the head: every processor suite (33 suites, 1,016,016 checks, 0 failing) and every
processor entry point returns rc 0; the in-tree D3 campaign kills 69 of 69 mutants with all
goldens passing; nine of the eleven parent consumer commands return rc 0, and the other two
are exactly the declared pin-adoption items of round 2 (`pp_shadow` on the five round-1
ports; the evidence classifier on `d3_mutants.py` and, at this parent pin, `retry_mutants.py`).
The reviewers' own scripts, rerun at the head, kill every mutant they reported surviving.

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5876934804 ·
TAKEN https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5876943921 ·
REVIEW READY https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5879510598 ·
aggregate clarification 5876655419 (#131) · reviews R390-2 (PR #132, 5876649455) and R391-2
(5876927371) · bank note 5876225160 · DR3a/DR4 ratification
https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5873060660.

## Commits (one-line subjects, assigned order)

| Item | Commit | Subject |
|---|---|---|
| 1 R390-2 F1 = R391-2 F2 | `f8d1a83` | Never close a provable image on the aggregate deadline: a binding walk still reading takes its own per-wait path, and the D3 walk proves the image and ends DEFAULTS |
| 2 R390-2 F2 | `9d66095` | State in both guides every terminal the aggregate deadline can take and both causes of CLOSED, as 07 section 5.3 lists them |
| 3 R390-2 F3 | `58c5fe9` | Grade the aggregate's span over the roll-back: a bound inside its debt wait or its re-LOCATE ends it CLOSED on the bound's own clock |
| 4 R391-2 F1 | `e94bea8` | Grade the aggregate's inertness after COMPLETE, DEFAULTS and CLOSED, and its wait for a clock without an event in hand |
| Taken: R391-2 S1 | `cbbb5ac` | Grade the admission's resident-count return: a record the external drain steals and returns in CLOSED frees the one-record AECP share |

`2b38d68..cbbb5ac`: 19 files, +801 / -103. Line numbers are at `cbbb5ac`. Each commit
was validated before it was made (full `tb/pp_top`, both builds; the full D3 campaign, whose
counts fill the README column; `make check`; for item 1 also `tb/acmp_nvm`, lint and Yosys);
the complete gates ran once, at the head.

## Items: change and proof

**1. The aggregate never closes a provable image (the clarification, 5876655419).**
- Writer `hdl/aecp/KL_aecp_nvm_writer.sv`: the aggregate joins the abort only once the image
  is proven (`expire_w`, `:544`); before it, it only sets `agg_fired_r`, and the new output
  `agg_o` (`:209`, `:567`) carries that level. At the proof (`proof_w`, `:602`: a validated
  image, or the LOCATE's hit) past the bound (`agg_past_w`, `:566`, the saturating count at
  the bound, so a proof landing on the bound's own clock counts too) the walk ends DEFAULTS,
  cause 3, with no record READ (`:810`). A LOCATE error still aborts, cause 7, CLOSED; after
  the proof and in the roll-back nothing changed. Banner "THE AGGREGATE DEADLINE" (`:58`).
- Binding manager `hdl/acmp/KL_acmp_nvm_shadow.sv`: input `rs_agg_i` (`:155`) joins its own
  per-wait expiry (`rs_tmo_w`, `:552-553`): at once in H_RS_REQ, where no read is issued, and
  in H_RS_STREAM only in a cycle without a byte, done or err, so the read it issued goes to the
  arbiter's drain exactly as at its own deadline; the walk fails whole, cause 3, and releases
  the listener. Banner refusal (a) names it (`:70-78`).
- Wiring: engine output `d3_agg_o` (`hdl/aecp/KL_aecp_engine.sv:582`, `:1851`); top
  `d3_agg_w` (`hdl/top/protocol_processor_top.sv:2555`) into `.rs_agg_i` (`:2566`) from
  `.d3_agg_o` (`:3625`). The `NVM_RS_AGG_CYC_P` comment (`:138-145`) and the port comments
  (`:458-490`) state the path and CLOSED's causes. `tb/acmp_nvm/acmp_nvm_wrap.sv` ties `rs_agg_i` to 0 (no D3 writer there).
- Bench: per-byte slow device knobs `nv_hdr_every` / `nv_byte_every` (header probe and
  payload apart, by the port's offset) and a one-shot grant on a chosen cycle `nv_gnt_at`
  (`tb/pp_top/sim_main.cpp:725-740`, `:1475`); aggregate taps `dbg_d3_agg_o`,
  `dbg_d3_agg_fired_o` (`tb/pp_top/pp_top_wrap.sv:398`, `:718`).
- Named control **D3R14** (`tb/pp_top/d3_phases.hpp:1702`), the reviewers' probe D1 device
  (each header byte `RS_TMO / 8 - 400` = 2,100 clocks apart, each payload byte
  `RS_TMO - 1000` = 19,001; every record and every sink's binding saved), two arms:
  - image valid: the binding walk's longest wait 19,002 of 20,001; it fails whole on the
    bound's clock 1,000,001 (`restore_cause_o` 3, no sink bound, its READ drained); the
    listener released by clock 1,000,003; **DEFAULTS registered by clock 1,000,005**,
    `rs_cause_o` 3, the D3 walk's longest wait 0 (no record READ requested), 0 D3 READs,
    image valid, rows cleared, AECP released (a READ_DESCRIPTOR answered byte-exact), the
    enable released to ADP (0 early enable cycles); once the device ends the drained READ a
    later SET persists (1 WRITE);
  - image refused (magic flipped): the same binding walk end, then **CLOSED, cause 7**,
    AECP owned, ADP not enabled.
- Mutants killed: `agg_closes_before_proof` (the ruling's pre-walk close: CLOSED cause 3 at
  the bound), `binding_walk_ignores_aggregate` (the binding walk reads on to about
  3.2 million clocks), `proof_reads_records_past_bound` (DEFAULTS only by the per-wait
  deadline, 20,005 clocks after the bound).
- Docs: 07 5.3 (the binding-walk table's aggregate row; the aggregate paragraph; the D3
  table's pre-proof row now DEFAULTS, CLOSED only if unprovable; the roll-back row's cause),
  08 section 2 T-NVM-RS-AGGREGATE, 01 F01.5, 03 rule (e), 09 section 8.2, `tb/pp_top/README.md`.
  The DR3a printout gains the path (below).

**2. Both guides (R390-2 F2).** `docs/guides/integrator.md`: the `NVM_RS_AGG_CYC_P` row lists
every terminal the aggregate can take; bring-up step 3 lists both causes of CLOSED
(`rs_cause_o` 7, the image; any other cause, a pass-1 roll-back that could not prove the image
again, `restore_rb_o` 0) and every aggregate terminal (binding walk still reading: it fails
whole, then DEFAULTS; pass 0: DEFAULTS; pass 1: roll-back to DEFAULTS; inside a roll-back
another fault started: CLOSED with that fault's cause), with the bounded wait at 1,000 ms plus
40 ms; section 4.1 no longer calls the writer's debt hold "deferred".
`docs/guides/operator.md`: the outcome table gains the aggregate rows and the roll-back CLOSED
row; the CLOSED paragraph and the section 9 troubleshooting row name both causes and say a slow
device alone ends on defaults. `docs/diagrams/23-bringup-decision.svg` step 3 names both causes
and the 1,000 ms bound; PNG re-rendered (`rsvg-convert -w 2040`) and inspected. All consistent
with 07 5.3 as item 1 adjusted it.

**3. The aggregate's span over the roll-back (R390-2 F3).** **D3R15**
(`d3_phases.hpp:1850`) uses a grant-steering helper (`Steer`, `:1799`): the device withholds
every grant and releases each so that a chosen command is granted on a chosen harness cycle,
every earlier one after an equal share of the time left (each wait stays inside the per-wait
deadline). Two arms, each graded on its premise (the fault's READ granted on its steered cycle;
at the bound the roll-back under way):
- debt wait: the rate rule's AUDIO_UNIT fetch answers 16,000 clocks late, pass 1 aborts
  (cause 6) about 5,800 clocks before the bound, the burst is still owed at the bound (strobe
  on, debt set): **CLOSED on the bound's own clock**, cause 6;
- re-LOCATE: a DEVICE error on pass 1's header READ of 0x02 100 clocks before the bound
  (cause 2); at the bound the strobe is off and the store is walking the image again:
  **CLOSED on the bound's own clock**, cause 2.
`agg_not_in_rollback` (R390-2's own edit) is KILLED by both (4 checks). R390-2's probe C2
shows the same at this head.

**4. Inertness after the terminal and no firing with an event in hand (R391-2 F1).**
**D3R16** (`:1929`): COMPLETE (every record saved), DEFAULTS rolled back (rule fetch error,
cause 6) and CLOSED after a roll-back (the re-LOCATE meets a silent memory, cause 2), each
followed by a SET where AECP runs and observed two per-wait deadlines past the bound: verdicts,
ownership (CLOSED owned every cycle) and rows (the SET value included) unchanged, 0 roll-back
strobe cycles after the terminal. **D3R17** (`:2007`): with every record saved, the device's
grants are steered so the writer's arbiter grant of 0x57's header READ lands on the bound's own
clock (graded: the count reads `AGG - 1` in the observation where the grant is in hand; the
latency from the previous payload READ's device grant, 9 clocks, is measured in the same
boot); the aggregate waits for the next clock without an event, **DEFAULTS 2 clocks later**,
cause 3, and that READ goes to the drain; once the device ends it a later SET persists with
nothing unflushed. Killed: `agg_not_stopped_at_terminal` (D3R16, 3 checks: COMPLETE rolled
back, DEFAULTS' rows reset, CLOSED turned into DEFAULTS), `agg_fires_with_event_in_hand`
(D3R17, 2 checks: no drain, the port wedged, the SET never written); both are R391-2's own
edits.

**Taken: R391-2 S1.** **D3O7** (`d3_phases.hpp:294`): in CLOSED the optional external drain
(`aecp_txn_ready_i`, then `aecp_rxs_free_i` with the head record's slot, which the wrap now
exposes: `pp_top_wrap.sv:82-84`, `:429`, `:494`; the harness drives them 0 everywhere else)
steals the held command; of the next two AECP commands the first is held and only the second
dropped and counted (word 37 +1). `resident_never_returned` (R391-2's edit) is KILLED.

## Section 15.2 table and sweep

All 37 rows remain applied; [TABLE-15.2.md](TABLE-15.2.md) adds a round-3 column: 22 rows
unchanged, 15 updated by this round (07 5.3, 08, 09, 01, the integrator guide's sections 2 and
9, the operator guide, diagram 23, the top's contracts and wiring, the binding manager, the
engine, the `acmp_nvm` wrap, the `pp_top` README, 03 rule (e)), each saying what changed; the
integrator guide's section 4.1 and the writer are changed outside the rows.

Named sweep at the head (`rg -n -U -i` of the contract's pattern over `docs hdl tb`), by
[`sweep_reconcile.py`](sweep_reconcile.py) (the round-1 script, unchanged): **681 matching
lines, 334 rewritten or added by this lane (by blame), 347 with a location-specific scope
reason, 0 unreviewed** ([SWEEP.md](SWEEP.md), 129,233 bytes). The context form
(`-C 2 --sort path`): 3,103 lines, 1,399,260 bytes, SHA-256
`2f2e7a75a3168023a4e2f79536efa3244bd03a9a656468e811b72969c26dcfa4` (kept in scratch).
`check-integrator-params.py`: 26 = 26 = 26.

## Negative controls

[MUTANTS.md](MUTANTS.md) lists all 69 with suite, named assertions, failing-check count and
first failing message; every count equals its README record. The round-3 additions:

| Control | Mutant | Named assertion(s) that fail | Failing checks |
|---|---|---|---:|
| the pre-walk close (the clarification's named mutant) | `agg_closes_before_proof` | `D3R14 image valid: DEFAULTS` | 3 |
| the binding walk not told of the aggregate | `binding_walk_ignores_aggregate` | `D3R14 image valid: the binding walk`, `D3R14 image refused: the binding walk` | 5 |
| the proof past the bound starts pass 0 | `proof_reads_records_past_bound` | `D3R14 image valid: DEFAULTS` | 1 |
| the count paused in the roll-back (R390-2 F3) | `agg_not_in_rollback` | `D3R15 debt wait: CLOSED`, `D3R15 re-LOCATE: CLOSED` | 4 |
| the count running past the terminal (R391-2 F1) | `agg_not_stopped_at_terminal` | `D3R16 COMPLETE`, `D3R16 DEFAULTS`, `D3R16 CLOSED` | 3 |
| firing with an event in hand (R391-2 F1) | `agg_fires_with_event_in_hand` | `D3R17: the writer's grant`, `D3R17: once the device ends` | 2 |
| the resident count never returned (R391-2 S1) | `resident_never_returned` | `D3O7: the returned slot frees the share` | 1 |

The 62 earlier controls keep their named assertions; 23 of them now also fail one or more of
the new checks (their README counts are updated). The reviewers' own scripts at the head agree
([REVIEWER-RERUNS.md](REVIEWER-RERUNS.md)): R390-2's `agg_not_in_rollback` and
`agg_ignores_in_hand` and R391-2's three survivors are KILLED; probe D1 and P8 case A now end
DEFAULTS at clock 1,000,005; P6 differs from its round-2 oracle in exactly the 452 pre-proof
expiries, each now DEFAULTS cause 3.

## DR3a measurements (ratified values, enforced)

`./obj_dir/Vpp_top_sim --dr3a` at the head ([dr3a-cbbb5ac.txt](dr3a-cbbb5ac.txt), SHA-256
`e55e3884c4de7d751df2c5f00a9810ec6c06c77fdd0dad96d4c2cbed7b860f44`): clk_i cycles from
`restore_go_i` (the "terminal" column is the observing loop index: the terminal is registered
by that clock + 1); the NVM model grants at once and streams a byte a cycle unless stated;
the bench image; the wrap's clock is nominally 1,000,001 Hz, so RS_TMO = 20,001 and
AGG = 1,000,001 clocks. Conversions: 50 MHz (20 ns a cycle) and 100 MHz (10 ns).

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
| every grant 200 inside the per-wait deadline, all records saved | DEFAULTS (3) | 158,530 | 1,000,000 (clock 1,000,001 = AGG) | 1,000 ms | 1,000 ms |
| **every READ byte just inside the per-wait deadline, all bindings saved (new)** | **DEFAULTS (3)** | **1,000,002** | **1,000,004 (clock 1,000,005 = AGG + 4)** | **1,000 ms + 80 ns** | **1,000 ms + 40 ns** |

Longest waits: healthy D3 405/853 cycles (DRAM 31/143), binding 12; the grant-slow device
19,812 of 20,001; the byte-slow device's binding walk 19,002 (it alone would run to about
3.2 million clocks) and D3 0. DR2a producer share unchanged: 50,028 bench cycles = the 500-tick
window + 28 cycles. Ratified constants at the product clocks, ceil(`CLK_HZ_P` x t / 1000):
per-wait 20 ms = 1,000,000 (50 MHz) / 2,000,000 (100 MHz); aggregate 1,000 ms = 50,000,000 /
100,000,000; backoff 500 ms = 25,000,000 / 50,000,000. After the bound the terminal follows:
before the proof, after the binding walk's own path (at its next stalled cycle), the release
and the proof (a LOCATE, if needed, bounded per wait): 4 clocks here; in pass 0 at the next
clock without an event (2 clocks in D3R17); in pass 1 after the roll-back, whose debt wait and
re-LOCATE are each bounded per wait (worst about 1,000 ms + 2 x 20 ms; D3R13 pass 1: 543 clocks);
inside a roll-back at once (CLOSED, D3R15).

## DR4 scalar-stage contribution

Vivado 2026.1 (SW build 6511674) out-of-context synthesis, `syn/ooc/protocol_processor_ooc.tcl`
(shape arguments `1 1` for the shipping 1x1; the top's default shape is 8x8), part
`xc7a100tfgg484-2`, 10 ns constraint, all six runs in this session on the same instrument
(reports in scratch). This session reproduces round 2's absolute totals for base and round-2
head exactly (21,675 / 23,710 and 22,696 / 24,270 at 1x1).

| Shape | Base `c951a9f` LUT / FF / BRAM / DSP | Round 2 `2b38d68` | Head `cbbb5ac` | Lane 1 (head - base) | Round-3 increment | Writer `u_d3` LUT / FF | Binding `u_nvm_shadow` LUT / FF |
|---|---|---|---|---|---|---|---|
| 1x1 (shipping) | 21,675 / 23,710 / 16.5 / 4 | 22,696 / 24,270 | 22,705 / 24,269 | **+1,030 LUT / +559 FF / 0 BRAM / 0 DSP** | +9 / -1 | 790 / 479 (was 783 / 479) | 688 / 1,268 (was 685 / 1,268) |
| 8x8 (diagnostic) | 29,059 / 31,164 / 24 / 4 | 29,854 / 31,619 | 30,126 / 31,749 | +1,067 / +585 / 0 / 0 | +272 / +130 | 1,144 / 527 (was 1,111 / 527) | 794 / 1,004 (was 783 / 1,004) |

Against the ruled scalar-core ceiling for lanes 1-2 (2,500 LUT / 1,400 FF / 0 BRAM / 0 DSP),
lane 1 uses 1,030 / 559 at 1x1, leaving 1,470 / 841 for lane 2. Synthesis WNS at 10 ns:
-5.970 / -5.165 / -5.165 ns (1x1 base / round 2 / head), -7.886 / -8.127 / -9.080 ns (8x8):
synthesis estimates only. The 8x8 increment is mostly placement-free synthesis variation
outside the two changed modules (+33 / +11 LUT in them). Post-place and the 8x8 post-place
obligation stay lane 2's (open, not waived).

## Parent-visible changes (for the pin-adoption lane)

- **No top port or parameter** is added, removed or resized this round.
- **Behaviour**: an aggregate expiry while the binding walk still reads now ends the binding
  walk failed (`restore_cause_o` 3, every binding at its default, nothing preloaded) and the D3
  walk DEFAULTS (`rs_cause_o` 3; done, fail, AECP and the enable released), where round 2 ended
  CLOSED. CLOSED now means an unprovable image (cause 7) or a pass-1 roll-back that could not
  prove it again (the pass-1 cause). Firmware's bounded wait: 1,000 ms plus 40 ms.
- **Internal port `rs_agg_i`** on `KL_acmp_nvm_shadow` (connected inside the top). The parent's
  `tb/verilator/nvm_cosim/cosim_top.sv:257` instantiates that module directly: its
  `make lint` stays rc 0 with one new `PINMISSING` warning (86 against 85 at `2b38d68`); the
  pin-adoption lane should tie `.rs_agg_i (1'b0)` there.
- **Found this round, introduced in round 1**: the parent's `nvm_cosim` quick loop
  (`make -C tb/verilator/nvm_cosim quick`, outside the consumer set) fails 7 of 315 checks
  (B1 to B4 `later_record_persists@end:0x21`, and `restores_last_verified` after the power
  cycles following B1, B2 and B4). It passes 315 of 315 with the processor at `c951a9ff` and at
  `505524e`, and fails identically from `f72a2d2` (DR2c for both producers: the binding
  manager's 500 ms backoff) through `2b38d68` to this head. The pin-adoption lane reconciles
  those cases with the ruled DR2c backoff.
- **Carried from rounds 1 and 2**: the five round-1 ports (`pp_shadow` PINMISSING, 20 warnings,
  unchanged); `NVM_RS_AGG_CYC_P`; the ceil per-wait default; snapshot word 37; the evidence
  classifier's `DUT_READER_DISPOSITIONS["protocol-processor/tb/pp_top/d3_mutants.py"]` = "mutation
  campaign; it plants one D3 saved-state defect from its own table into an isolated copy and
  requires every named check to fail in a completed run; no expected value is read from the
  text" (at this parent pin also `retry_mutants.py`'s line, which the dev pin has).
- Not parent-visible: the engine's `d3_agg_o`, the writer's `agg_o`, the bench wrap's new
  ports and taps.

## Suites and gates

[SUITES.md](SUITES.md) (per suite) and [GATES.md](GATES.md) (per command, rc, seconds, log
SHA-256) at the head, run by [gates.py](gates.py) with the pinned Verilator 5.050 wrapper:

| Tree | Entry point | rc |
|---|---|---:|
| processor | `./scripts/run_suites.sh` (33 suites, 1,016,016 checks, 0 failing; pp_top 7,875) | 0 |
| processor | `./scripts/lint_hdl.sh` | 0 |
| processor | `make check` (lint, WaveDrom, links 967, matrices, params 26/26/26, stale) | 0 |
| processor | `python3 scripts/gen_matrix.py --check` | 0 |
| processor | `./syn/yosys/run.sh` | 0 |
| processor | `make -C tb/nvm_port figures` (PR #13 history fetched read-only first) | 0 |
| processor | `python3 tb/pp_top/d3_mutants.py` (69 of 69 KILLED, goldens PASS) | 0 |
| processor | `make -C tb/srp_top mutants` (64 checks, coverage 49/49) | 0 |
| parent | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 |
| parent | `xvlog_gate.py --check` (4 findings == ratchet, none in lane files) | 0 |
| parent | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 |
| parent | `sw/builder/test_builder.py` | 0 |
| parent | `make -C tb/verilator/pp_shadow -j8` (the five round-1 ports, 20 PINMISSING) | **2** |
| parent | `check_port_contracts.py` (processor 111 <= 111) | 0 |
| parent | `measure_naming.py --check` (PASS, 96 recorded) | 0 |
| parent | `measure_test_evidence.py --check` (`retry_mutants.py`, `d3_mutants.py`; rc 0 with both lines) | **1** |
| parent | `docs_check.py` | 0 |

The scratch parent is a clone of the read-only checkout at `7a7582f0` (the manager's bank uses
its dev pin, where `retry_mutants.py` is already explained).

## Notes for review

1. **The roll-back at the bound is unchanged** (the clarification's third bullet, "as D3 §6.3
   states"): a bound falling in the roll-back's debt wait is a roll-back "whose debt outlasts
   the deadline", and one falling in its re-LOCATE a roll-back that has not validated the image
   by the deadline; both end CLOSED with the pass-1 cause, as round 2 did. D3R15 pins both, so
   a different ruling would change that check, not a silent behaviour.
2. **CLOSED after a pre-proof expiry carries cause 7**, not 3: the aggregate aborted nothing
   there, and the image's own failure ends the restore (cause 3 only if the proof's LOCATE
   outlasts the per-wait deadline, which the store's 4,096-clock watchdog normally precludes).
3. **"No further NVM record reads"**: the D3 walk requests none after a pre-proof expiry (D3R14:
   longest D3 wait 0, 0 D3 READs). The binding walk also stops issuing: in H_RS_REQ the aggregate
   ends it at once. That term is not graded by a named check: without it the walk would issue
   one more READ and abandon it to the drain a clock later, which the ruling's "its own per-wait
   path" also allows.
4. **Steering** (D3R15, D3R17) only times the model device's grants; every wait stays inside the
   per-wait deadline, the target command's region and offset and its grant cycle are graded as
   the premise, and the RTL is untouched. R390-2's C1 forces the device's grant, not the writer's
   arbiter grant, which is why it saw no difference; D3R17 lands the writer's own grant.
5. R390-2 S1 (an `RX_SLOTS_P >= 2` floor) was not assigned and is not taken.

## Packet

HANDOFF.md, PR-BODY.md (Round 3 section), REVIEW-READY-COMMENT.md, TABLE-15.2.md, SWEEP.md and `sweep_reconcile.py`,
MUTANTS.md, SUITES.md, GATES.md, REVIEWER-RERUNS.md with `receipts/` (the reviewers' reruns and
the two adapted runner copies), `dr3a-cbbb5ac.txt`, `gates.py`. Logs, synthesis reports and
scratch trees stay under `$VALIDATION_STORAGE/a429` (not copied: sizes and hashes above and in
GATES.md).
