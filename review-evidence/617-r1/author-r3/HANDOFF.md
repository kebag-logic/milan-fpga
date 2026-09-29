# [A431] Round 3 handoff: issue #617 / PR #618

Status: REVIEW READY at `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b` (local branch, not pushed; this lane may not push). All 85 assigned local gates rc 0 at that head; 13 suites, 52,285 checks, 0 failures.

- Repository: kebag-logic/milan-fpga, origin `https://github.com/kebag-logic/milan-fpga.git` (confirmed).
- Lane: `$LANES/617-capture-frame-atomic`, branch `617-capture-frame-atomic`.
- Round-3 start: `377d1ac3658feb8d544e6ed1005b186b67127f35` (confirmed HEAD). Branch base: dev `ce550952e47fbd92367f0d9b099345100f7f4215`.
- Head: `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b`, four round-3 commits on `377d1ac3` (ten on dev):
  - `abe78678f` Keep the media grid to one tick per period whatever cycle a trim update lands on (NCO RTL + media_nco check 10).
  - `112c0cb88` Sweep the sub-cycle NCO race, bind the datapath's keep-off and grade the settled lock past the envelope (capture_coherence, chmap_capture [Q], mutants).
  - `c5e44378a` State the capture crossing's envelope as relative rate and the media grid's terminal guarantee (docs, comments).
  - `ddb077477` Spell the media_nco terminal-compare mutation row without an em dash (the first gate run at `c5e44378` failed `check_em_dash --base`; the gates were stopped and all re-run at `ddb07747`).
- Work directory (scratch, outside the tree and this output directory): `$VALIDATION_STORAGE/617-a431-work` (logs/, gates-ddb0774/, the probe trees).
- Simulator: Verilator 5.050 (`$VALIDATION_TOOLS/verilator-v5.050/bin` first on PATH) for every run. Synthesis: Yosys 0.66, sv2v v0.0.13 (CI pins v0.0.12).
- Assignment: issue #617 comment 5879911799 (round 3).
- Reviews answered: R394-2 (PR #618 comment 5879806778) and R395-2 (PR #618 comment 5879904352).
- Roles: executor [A431]; internal reviewer [R394]; external reviewer [R395].
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5879964310
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5881204511

## 1. NCO race reproduction at 377d1ac3

Method: R395-2's packaged probe (`scripts/probe_crossing/probe_fine.cpp` + `probe_bench.hpp`, their sha256 in R395-2's MANIFEST), built with their recorded command (`ncofix-build-cmd.txt`) in a `git archive` tree of `377d1ac3`, Verilator 5.050; per-phase commands exactly `run_fine.sh`'s (16-way parallel instead of 4; the concatenated log is the same bytes).

| Run | RTL | Result | Log sha256 |
|---|---|---|---|
| `-50 -1 2` | `377d1ac3` | 9 failures, 3 placements: P-50/34+1.1, 35+0.1, 36+0.1 (1 repeat, 2 skips each) | `8086192922b7...` = R395-2 `receipts/probe-fine-m50.log`, byte-identical |
| `-60 -1 2` | `377d1ac3` | 98 failures, 92 placements | `0ab19e671ba4...` = R395-2 `receipts/probe-fine-m60.log`, byte-identical |
| `-50 -1 2` | `377d1ac3` + only the NCO compare `>=` | 0 failures | `444864382bfa...` = R395-2 `receipts/probe-ncofix-fine-m50.log`, byte-identical |
| `-60 -1 2` | `377d1ac3` + only the NCO compare `>=` | the SAME 98 failures, 92 placements | `0ab19e671ba4...`: byte-identical to the unfixed run |

Finding (published, it changes one ruling-1 expectation): **the -60 ppm failures are not the NCO race.** With the NCO fixed the -60 ppm log does not change by one byte. Every one of the 92 placements is a single net-zero repeat/skip (1,1) of an on-crossing engagement whose departure is slow (64 - 60 = 4 ppm net), last slip at columns 76 to 181; 6 of them fall in the 300-column probe's second half. That is the 64-column window law being wrong beyond +/-50 ppm (ruling 3, `kEngageColumns`), and it is answered there (section 6).

The race itself, at 50 MHz (the direct test, section 3): the trim lowers the end from 1041 to 1040 on the cycle the count sits at 1041; `==` misses, the count runs to 2047, wraps, and the period is 3,089 cycles (R395-2's trace).

## 2. NCO fix (file:line)

`hdl/ieee1722/crf/KL_media_nco.sv` (line numbers at the round-3 head):

- The terminal compare is monotone: `else if (32'(cnt_r) >= end_w) begin` (was `==`), in `media_grid` at `:241`.
- The TERMINAL COMPARE contract comment above it (`:213-234`) states what the NCO now guarantees, whatever cycle a trim lands on:
  - one tick per period, never lost, never doubled; the count never passes `DIV_C`, so it never wraps;
  - an update lowering the end below the count ends the period on that cycle: no longer than the old trim set it, one cycle past the new end (two only for a step of more than `DEN_C` LSB, beyond the servo's +/-200 ppm authority); the accumulator books the new trim, so the grid runs that cycle behind its account: a one-time phase step, never a lost sample or a rate change;
  - at a steady trim the grid is bit-for-bit the `==` grid (media_nco checks 1-9, INTERNAL unchanged).
- The trim-register comment (`:187-192`) no longer claims the trim "moves at most once per servo tick": it says a producer may move it on any cycle, names the #74 aligner as the in-tree producer that does, and points at the terminal compare. The shared-predicate comment (`:199-202`) names the one bounded exception.
- No port, parameter or interface change. Mechanism chosen: the monotone compare (the ruling's first option), because it keeps the trim latency exactly as it was and the `==` restore stays a meaningful mutant; a latched end would make `==` an equivalent mutant.

## 3. Direct NCO test

`tb/verilator/media_nco/sim_main.cpp` check 10, `test_terminal_race()`, both shapes (A 100 MHz, B 50 MHz). For every move of the period's end one trim step can make (lent/nominal/borrowed, up and down, by one and by two; the borrow moves are unreachable at 50 MHz, where the clamp cannot take the sum below zero, and the test says so), it holds one trim from the period start and moves it so the new trim first reaches `trim_r` on each cycle from three before the old terminal count to the next period's first (`kLandFirst`..`kLandLast` = -3..+1). Trims are chosen from the phase read at the period start, at the sum boundaries, so each move is the least step that moves the end. Three checks per trial, stated as what a grid owes, not how the RTL does it: one tick in a period the old or the new trim sets; the count never past the higher end (no wrap); the accumulator books the trim in force on the period's last cycle (closed form, as check 2's phase oracle). Plus a vacuity check that an update landed with the count already past the new end.

`tb/verilator/media_nco/Makefile`: `build` target, `NCO_SRC`/`MDIR` overridable (for the mutation arm).

| NCO | media_nco result | Log sha256 |
|---|---|---|
| round-3 head (`>=`) | 410 checks, 410 PASS, 0 FAIL | `ea92fae342d5...` (`logs/nco-fix.log`, working tree before commit; the gate run at the head is section 10) |
| `377d1ac3` (`==`, via `NCO_SRC`) | 410 checks, 400 PASS, 10 FAIL, rc 1: exactly the 5 trials whose update lands past the new end x 2 checks (period 6,178/6,179 at 100 MHz, 3,089 at 50 MHz; top count 4,095 / 2,047) | `e3ed70256217...` |

## 4. Sub-cycle sweep tables (-50 / -60 / +50 ppm)

Committed: `capture_coherence` `CRF-fine-50` (`--fine` alone; also in the full run): -50 ppm, offsets -1..+1 cycle of the crossing, 4 quarter-cycle holds x 64 sub-step phases each (the TDM accumulator preloaded to k/64, calibrated per phase as R395-2's probe does), 300 columns, 768 engagements.

| Run | NCO | Checks | Failures | Slipping engagements | Max last slip col |
|---|---|---:|---:|---|---:|
| `CRF-fine-50` | round-3 head | 15,425 | 0 | 141, all 1 repeat + 1 skip | 57 |
| `CRF-fine-50` | `377d1ac3` (`NCO_SRC`) | 15,425 | 27 (9 placements x `[C] CRF slips net zero`, `... only inside the engagement's first columns`, `slips while the CRF lock held`) | 127 x (1,1) and 9 x (1 repeat, 2 skips) | - |

R395-2's `scripts/probe_crossing/run_fine.sh`, their probe re-derived from the round-3 harness by their own `make_probe.py` + `make_probe_fine.py` (anchors intact) and built with their `ncofix-build-cmd.txt` plus the one addition the new wrapper needs (the extracted keep-off include and `+incdir+obj_fine`); run with their script, 4-way:

| Run | Result | Slipping | Max last slip col |
|---|---|---|---:|
| `run_fine.sh -50 -1 2` | 64 runs, 20,544 checks, **0 failures** | 162, all (1,1) | 57 |
| `run_fine.sh -60 -1 2` | 64 runs, 20,544 checks, **0 failures** | 115, all (1,1) | 181 (window 224, section 6) |

(Final numbers at the committed head: section 10.)

+50 ppm and the rate map (recorded, R395-2's packaged probe with only the NCO fixed, offsets -2..+2, 1,280 placements, 300 columns; head grading, so window failures past 64 columns are counted):

| Rate | Slipping | Kinds | Max last slip col |
|---|---|---|---:|
| true plan (-10.64) | 105 | (1,1) | 19 |
| -25 | 153 | (1,1) | 23 |
| -40 | 97 | (1,1) | 31 |
| -55 | 153 | (1,1) | 87 |
| -62 | 180 | (1,1) | 294 |
| -63 | 219 | 129 (1,1), 90 (1,0): carried across | 294 |
| -64 | 218 | 44 (1,1), 174 (1,0) | 279 |
| +50 | 25 | (1,1) | 8 |
| +60 | 63 | (1,1) | 8 |
| +65 | 64 | (1,1) | 8 |
| +66 | 52 | (1,1) | 8 |
| +68 | 151 | 21 (1,1), 130 (0,1): carried across | 302 |
| +70 | 318 | 43 (1,1), 275 (0,1) | 302 |

## 5. Settled-lock table (+/-80, +/-100 ppm)

Committed (`capture_coherence` full run, `CRF-settle-80/+80/-100/+100`, 30,000 columns, tail = second half), round-3 working tree:

| Scenario | Engaged | Acquisition slips | Last slip col | Tail slips | Tail spread (cycles) |
|---|---:|---|---:|---:|---:|
| -80, -256 | -257 | 0 | - | 0 | 126 |
| -80, 0 | -1 | 1 repeat, 1 skip | 6,284 | 0 | 109 |
| +80, +8 | +7 | 1, 1 | 6,056 | 0 | 110 |
| +80, +264 | +263 | 0 | - | 0 | 126 |
| -100, -256 | -257 | 1, 1 (transient crosses) | 13,065 | 0 | 159 |
| -100, 0 | -2 | 1, 1 | 11,036 | 0 | 142 |
| +100, +8 | +8 | 1, 1 | 10,963 | 0 | 141 |
| +100, +264 | +265 | 1, 1 (transient crosses) | 12,374 | 0 | 159 |

Every check passes, including `[V] the CRF lock held its phase` and `[C] slips while the CRF lock held` = 0, and the per-walk `SLIP_TDM` check (each repeat and skip counted). The spreads show the close still converging on its 256-cycle target in the tail (the integrator's time constant); the recorded long runs show where it goes.

Recorded (R395-2's packaged probe, NCO fixed, 13 placements across the whole frame (-512..+512) x 4 rates, 60,000 columns each, tail = columns 30,000-60,000): 52 runs, **0 tail slips**, every acquisition slip a (1,1) pair, last at column 13,065; tail spreads 41-84 cycles, the close >= 198 cycles from the crossing throughout the tail and converging on 256. Logs in the work directory (`logs/settle/`).

Verdict: the settled lock is guarded to +/-100 ppm relative rate. No STOP.

## 6. Envelope as measured

Relative rate at the aligner = the TDM frame against the local axis clock (TIME_SYNC.md assumes the local oscillator within +/-100 ppm, so a +/-50 ppm Milan source does not bound it).

| Term | Value | Evidence |
|---|---|---|
| Pull on a raced engagement | 64 ppm: u = 256 << KP_LOG2_P(2) = 1024 in 1/16 ppm | derived; the junction wrapper exports it (`engage_u_o`) |
| Pulled-engagement margin | 256 - 4 x rate: 56 at 50 ppm, 16 at 60, 0 at 64 | derived (R394-2 S3) |
| On-crossing engagement limit | about 63 ppm below nominal, 67 above (net zero at -62 / +66; carried across at -63 / +68) | recorded, section 4 |
| Unpulled transient peak | ~3 cycles/ppm: 149 (50), 238 (80), 250 (84), 257 (86), 263 (88), 269 (90), 299 (100) | committed CRF-50/+50 and CRF-settle; recorded 20,000-column runs at +/-84..90 |
| Transient limit | about 86 ppm: no crossing at 86; crossing at -88 and +90 | recorded |
| Settled lock | no slip, measured to +/-100 ppm | section 5 |

Behaviour by band (TIME_SYNC.md "The guarded crossing" tables it):

| Relative rate | Engagement on the crossing | Unpulled engagement | Settled lock |
|---|---|---|---|
| within +/-50 | 1 repeat + 1 skip, net zero, by column 57 (every sub-cycle phase at -50: CRF-fine-50; R395-2 -50 probe) | transient <= 149, 107 cycles clear | no slip |
| 50 to the on-crossing limit | 1 + 1, net zero, by column 87 (55), 181 (60), 294 (62) | under the keep-off | no slip |
| on-crossing limit to ~86 | carried across and back: 1 + 1 by column 6,300 (80) | under the keep-off | no slip |
| beyond ~86 | carried across and back, by column 11,100 (100) | transient crosses and returns: 1 + 1 by column 13,100 (100) | no slip, to +/-100 measured |

The engagement window law (`coherence_bench.hpp`): `kEngageColumns` = 64 stays the window within the Milan +/-50 ppm bound, now derived correctly (R395-2 F3, R394-2): net departure at the bound (64 - 50) ppm x 1e-6 x 1041.7 = 0.0146 cycles/frame, one cycle of jitter in 68 frames, first column about four frames after the engagement: 64 columns; measured 57. Below the bound the departure is faster (19/23/31 at -10.64/-25/-40). `engage_columns(ppm, pull)` stretches it beyond the bound by (pull - 50)/(pull - |rate|) (100 at 55, 224 at 60, 448 at 62) and is unbounded at or past the pull. `tail_start()`: a CRF run's lock tail is its second half and never starts inside its engagement window (identical to "the second half" for every committed CRF scenario, whose windows are <= 64 columns against tails from column 150 up: `CRF-fine-50`'s 300-column runs start the tail at 150 > 64). This is what makes R395-2's 300-column -60 ppm probe pass: its window is 224 columns, so its tail starts at 224; the 6 slips at columns 166-181 are acquisition, net zero. Stated for review: that is a change to the grading, justified by ruling 3's instruction to correct the derivation; within the Milan bound the law is unchanged (64 columns, tail = second half).

## 7. Mutant table

`tb/verilator/capture_coherence/mutants.py` (the suite's `make mutants`), 8 legs, each with a clean control; 19 mutants. Working-tree run before the commit (identical sources): `27 checks: 27 PASS, 0 FAIL`, 862 s sequential (`explore/arm_seq_wt.log`); the gate run at the head is section 10.

| # | Leg (mode) | Mutant | Named check that must fail | New in round 3 |
|---|---|---|---|---|
| C1-C8 | junction `--quick`, band `--band`, band50 `--band50`, fine `--fine`, dp `--quick`, dp-band `--band`, chmap, nco | clean controls | none | band50, fine, nco legs |
| M1-M8 | junction | the round-1/2 crossbar mutants (per-pair law of `ce550952`, no snapshot, first-pair close, late publish, unwritten stage, coincidence law ignored, round-1 snapshot instant, round-1 counter law) | as round 2 | - |
| M9 | band | the round-1 aligner binding (slot-0 marker, tick itself, default keep-off) | `[C] slips while the CRF lock held` | pattern updated: the wrapper binds `MGA_KEEPOFF_CYC_C` |
| M10 | band | keep-off back to the 1/128-sample default | `[C] slips while the CRF lock held` | pattern updated |
| M11 | band | the aligner sees the tick itself | `[C] CRF slips net zero` | - |
| M12 | dp | `milan_datapath` tells the crossbar a one-pair frame | `[A] AAF columns mixing two TDM frames` | - |
| M13 | dp-band | `milan_datapath`'s round-1 aligner binding | `[C] slips while the CRF lock held` | - |
| M14 | chmap | RM1: close on the bucket's last pair whatever the frame length | `F1: col 0 carries its own pair-0 frame (L)` | - |
| M15 | chmap | **RM7**: a queued tick takes no snapshot when its walk starts (`tdm_snap_w = IDLE && !tick_pend_r && tick_i`) | `Q: col 2 pair 0 L is frame 4` (9 failures in a standalone run: col 2 repeats frame 2, and the skip counter reads 2) | yes |
| M16 | chmap | **RM8**: a queued tick snapshots at the tick (`tdm_snap_w = tick_i`), reloading the running walk | `Q: col 1 pair 2 L is frame 2` and `Q: col 2 pair 0 L is frame 4` (12 failures: col 1 torn on pairs 2-3, col 2 frame 3) | yes |
| M17 | band50 | **RM5**: `milan_datapath`'s `MGA_KEEPOFF_CYC_C` cap 256 -> 128 (R395-2's `rm5-keepoff128.diff`, the same line) | `[C] slips while the CRF lock held` | yes |
| M18 | nco | **the `==` terminal compare restored** (`377d1ac3`'s grid) | `update landing at old end +0: one tick, in a period the old or the new trim sets` | yes |
| M19 | fine | **the `==` terminal compare restored**, under the -50 ppm sub-cycle sweep | `[C] CRF slips net zero` | yes |

## 8. Resource comparison

`KL_media_nco` alone, the `ooc.sh` recipe replayed (the NCO is a `run.sh` top, not in `ooc.sh`'s AREA list): `sv2v --top=KL_media_nco`, then `yosys: read_verilog; chparam -set CLK_FREQ_HZ_P <clk> -set TRIMW_P 18 KL_media_nco; synth_xilinx -family xc7 -top KL_media_nco -flatten; stat`. Yosys 0.66, sv2v v0.0.13 (CI pins v0.0.12). `TRIMW_P 18` as `milan_datapath` binds it. Stat files: `evidence/ooc-KL_media_nco-*.txt`.

| Clock | Version | LUT | FF | CARRY4 | MUXF7/F8 | DSP48E1 | BRAM |
|---|---|---:|---:|---:|---:|---:|---:|
| 50 MHz (shipping 1x1 TDM8) | `377d1ac3` (`==`) | 101 | 46 | 35 | 3/1 | 1 | 0 |
| 50 MHz | round-3 head (`>=`) | 106 | 46 | 37 | 0/0 | 1 | 0 |
| 100 MHz | `377d1ac3` | 103 | 47 | 35 | 5/2 | 1 | 0 |
| 100 MHz | round-3 head | 104 | 47 | 37 | 2/0 | 1 | 0 |
| 50 MHz, `-nodsp` | `377d1ac3` / head | 147 / 146 | 46 / 46 | 41 / 43 | 7/2 / 0/0 | 0 | 0 |
| 100 MHz, `-nodsp` | `377d1ac3` / head | 153 / 150 | 47 / 47 | 41 / 43 | 14/6 / 2/0 | 0 | 0 |

The change is the compare: an equality over 11/12 bits becomes a magnitude compare (two more CARRY4), LUT +5 / +1, FF unchanged, and the MUXF7/F8 of the equality decode go away. `KL_chan_map_capture` and `milan_datapath` RTL are unchanged in logic this round (comments only), so their round-2 figures stand (1x1 TDM8 `KL_chan_map_capture` LUT 1265, FF 1384, BRAM 0; the gate run re-measures it, section 10).

## 9. Latency effect

None this round.

- The NCO: at a steady trim the count meets the end exactly, so every tick lands where the `==` grid put it (media_nco check 1, bit-exact against the legacy divider, and checks 2-4 unchanged). Under a moving trim the only difference is the race case: a period that `==` lengthened to 3,089 cycles (a two-tick hole) is now one cycle past its new end. The walk's read point, the frame age and the per-pair table are unchanged.
- The keep-off value is unchanged (256 at 50 and 100 MHz); the wrapper now derives it.
- The per-pair latency table in `TIME_SYNC.md` is re-scoped, not changed: the 1x1 TDM8 shape at 50 MHz with TDM pairs 0-3 on talker slots 0-3; at 100 MHz a pair period is 520.8 cycles, and a pair feeding talker t's slots read 104 x t cycles later at `ce550952`, so its change is 104 x t cycles less (R394-2 S3).

## 10. Gate table

All at head `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b`; the tree was clean before and after (`git status --porcelain` empty), suite build directories cleaned first; every gate from the physical path `$LANES/617-capture-frame-atomic`, unpiped, log + rc per gate, four detached streams waited for in the foreground; Markdown gates in `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`; `GIT_CONFIG_*` core.commitGraph=false (this worktree's git warns on stderr). Full list with each command and seconds: `evidence/gate-summary-ddb0774.txt` (85 entries, all rc 0). The round-2 gate set (79) plus the ruling-1 NCO suites (`media_nco`, `crf_rx`, `crf_tx`, `mmcm_servo`, `mmcm_servo_autorepair`) and `run.sh --top KL_media_nco`.

| Gate | Command | rc | Result |
|---|---|---:|---|
| Builder bank | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local Arty mf48 build report, absent here), 692 s |
| Lint ratchet | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 violations <= ratchet 90; 17 waived, 0 justified lint_off |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet; 0 in `hdl/`, 4 in the pinned processor; 139 s |
| Yosys | `syn/yosys/run.sh --top milan_datapath` / `KL_chan_map_capture` / `KL_media_nco` | 0 | 339 / 10 / 2 s |
| OOC | `OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture` | 0 | LUT 1265, LUTRAM 32, FF 1384, BRAM 0, CARRY4 34 (unchanged from round 2) |
| `capture_coherence` | `make -C tb/verilator/capture_coherence` | 0 | junction 20,832 / 0; datapath 332 / 0; mutation arm 27 / 27; 1,236 s |
| `chmap_capture` | `make -C tb/verilator/chmap_capture` | 0 | 371 / 0 + netlist 20 / 0 |
| `media_nco` | `make -C tb/verilator/media_nco` | 0 | 410 / 0 |
| `media_grid_align` | `make -C tb/verilator/media_grid_align` | 0 | 45 / 0; negative controls MGA_MUT_U_SIGN, MGA_MUT_NO_KEEPOFF, MGA_MUT_COIN red as required |
| `crf_rx`, `crf_tx`, `mmcm_servo`, `mmcm_servo_autorepair` | `make -C tb/verilator/<suite>` | 0 | 16,116 / 127 / 311 / 47 checks, 0 failures |
| `tdm`, `pair_fill`, `pp_shadow` | `make -C tb/verilator/<suite>` | 0 | 58 / 41 / 2,120 checks, 0 failures |
| `milan_dp_render` | `make -C tb/verilator/milan_dp_render` | 0 | 222 / 0 |
| `milan_dp` | `make -C tb/verilator/milan_dp` | 0 | 11,206 / 0, 1,384 s |
| Suite tally | `scripts/suite_tally.py` over the 13 suite logs, and `--verdict` per log | 0 | 52,285 checks, 0 in-suite failures (`evidence/suite-tally-ddb0774.txt`) |
| Markdown | `docs_check`, `check_em_dash --base ce550952...` and `--selftest`, `gen_toc --check/--verify-anchors/--selftest`, `check_doc_style` and `--selftest`, `check_doc_paths`, `check_feature_status` and `--self-test`, `gen_module_matrix --check`, gptp/solution/submodule docs, `DOC_MAP.gen --check`, `check_archive` | 0 | PASS |
| Code quality | sv/cpp/py/sh idiom, hygiene, naming, port contracts, fail-fast, test evidence, TODO ownership, cohesion/control-flow self-tests, each with its `--selftest` | 0 | PASS |
| Source lists and scope | rtl source lists, SoC sources, `pp_srcs`, wire accountability, CI events, ci_scope self-test, bare-metal, NVM record space, diagrams | 0 | PASS |
| HDL reference | `gen_hdl_reference.py --output <work>/hdlref-out` and `--selftest` (pyslang 11.0.0 venv) | 0 | built |

Recorded (not gates), at the committed head: R395-2's `run_fine.sh -50 -1 2` and `-60 -1 2` with their probe re-derived by their scripts from a `git archive` of `ddb07747` (`make_probe.py`, `make_probe_fine.py`; probe_fine.cpp sha256 `286e93fb...`, probe_bench.hpp `a34332f2...`): 0 / 20,544 each, logs sha256 `e6b3d525...` (-50) and `b2e6138c...` (-60), listed in `evidence/large-logs-sha256.txt`. The same probe at +/-50 ppm over -4..+4 cycles (2,304 placements each): 0 failures, last slip column 57 (-50) and 8 (+50).

Not run: the whole-tree sweep `scripts/run_all_suites.sh` (the affected suites were assigned), the act replica and hosted CI (nothing pushed), bench acceptance 4.

## 11. Round-3 finding disposition

| Finding / ruling | Disposition | Where |
|---|---|---|
| R395-2 F1 (MAJOR), ruling 1: lost media ticks | FIXED in `KL_media_nco` (monotone terminal compare), contract comment rewritten; no port change | sections 1-3; mutants M18, M19 |
| | direct test (media_nco check 10) fails at `377d1ac3` (10), passes at the head | section 3 |
| | committed sub-cycle capture sweep `CRF-fine-50` fails at `377d1ac3` (27), passes at the head | section 4 |
| | R395-2 `run_fine.sh -50 -1 2`: 0 failures; `-60 -1 2`: 0 failures (probe re-derived from the head by R395-2's scripts) | section 4 |
| | NOT the NCO race: the -60 ppm failures (published with byte-identical logs) - they were the window law, answered under ruling 3 | section 1 |
| | NCO area reported; every NCO-instantiating suite re-run | sections 8, 10 |
| R395-2 F2 = R394-2 S2, ruling 2: keep-off constant | TAKEN: the wrapper binds the datapath's own declaration (`mga_keepoff.py`, derived, no literal); `band50` arm leg runs the placed +/-50 ppm bands; RM5 killed by `[C] slips while the CRF lock held` | `coherence_wrap.sv`, `Makefile`, `mutants.py`; M17 |
| R394-2 F2 = R395-2 F3, ruling 3: envelope | STATED AS MEASURED, relative rate at the aligner: on-crossing limit ~63/67 ppm (binding constraint 4 x rate < keep-off; margin 256 - 4 x rate), transient limit ~86 ppm, behaviour beyond each; settled lock measured to +/-100 ppm (committed `CRF-settle`, recorded 52 x 60,000 columns): guarded, no STOP | sections 5-6; TIME_SYNC.md, REGISTER_MAP.md, crossbar banner, datapath comment, CHANGELOG, PR body |
| | `kEngageColumns` derivation corrected (net departure at the bound); rate-derived window beyond; lock tail never inside the window | `coherence_bench.hpp` |
| | R394-2 S3 taken: the pulled-engagement margin stated; the latency table scoped to 1x1 TDM8 at 50 MHz with its slot mapping, other clocks and mappings stated | TIME_SYNC.md |
| R394-2 F1 vs R395-2 S1, ruling 4: aligner banner | comment only: settle-band sentence scoped to the module default; pointer to the datapath binding (256 cycles, one-cycle-late tick, #386 recentre up to its 32,768-tick ceiling) | `KL_media_grid_align.sv:80-87` |
| R394-2 S1, ruling 5: queued-tick snapshot | TAKEN: `chmap_capture` `[Q]` (tick mid-walk, closes before and after it); RM7 and RM8 killed | M15, M16 |
| Ruling 6: documents | TIME_SYNC.md, REGISTER_MAP.md `SLIP_TDM`, `KL_chan_map_capture.sv` ONE CROSSING, CHANGELOG.md, TESTING.md, media_nco README, PR body; the 64-column claim re-measured at every sub-cycle phase at +/-50 ppm (57 / 8), now stated for +/-50 ppm only | section 6 |

## 12. Open risks

- **Suite time.** `capture_coherence` grows from about 15 to about 21 minutes locally (section 10 has the exact seconds): the junction leg adds `CRF-fine-50` and `CRF-settle` (168 -> about 240 s), the mutation arm adds three legs and five mutants (sequential, 862 s). That is inside `run_all_suites.sh`'s 1,800 s per-suite guard locally, with less margin than before; the hosted duration of shard 1/5 is unobserved (nothing pushed). If it matters, the arm's legs are independent and could run in parallel (a follow-up; not done, to keep this change small).
- **The -60 ppm premise.** Ruling 1 expected the NCO fix to clear R395-2's -60 ppm run. It does not by itself (byte-identical logs, section 1); the -60 ppm run passes because ruling 3's corrected window admits its 181-column net-zero acquisition and the lock tail no longer starts inside that window. R395-2's packaged probe binary still embeds `377d1ac3`'s grading (64 columns, tail at column 150) and still reports those 98 window failures with the NCO fixed; re-derived from this head by R395-2's own scripts it reports 0. The reviewers should judge the grading change (section 6) on its own.
- **The one-cycle phase step.** The monotone compare trades a two-tick hole for a one-cycle phase step when an update lands past a lowered end (two cycles only for a step beyond the servo's authority). Exactness at a steady trim is untouched; the aligner absorbs the step. A latched end would be exact but adds a period of trim latency and makes the `==` mutant equivalent.
- **Envelope limits are recorded, not committed**, except +/-50 ppm (committed sweeps) and +/-80/+/-100 ppm (committed `CRF-settle`). The on-crossing limit (63/67 ppm) and the transient limit (86-90 ppm) come from recorded probe runs in the work directory; their logs are listed by sha256 in section 10's evidence table.
- **Engagement cost unchanged**: a raced engagement is still pulled up to 256 cycles, and the #386 recentre waits up to its 32,768-tick ceiling (682.7 ms, round 2's probe).
- **Not run**: the whole-tree sweep, the act replica and hosted CI (nothing pushed; this lane may not push), bench acceptance 4. Local sv2v is v0.0.13; CI pins v0.0.12.

## 13. Log (2026-09-29, CEST)

- 00:31: confirmed origin and HEAD `377d1ac3`. Read #617 in full, the round-3 assignment and R394-2 / R395-2.
- 00:35: posted TAKEN (https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5879964310).
- 00:45-00:50: rebuilt R395-2's packaged fine probe at `377d1ac3`: -50 ppm 9 failures / 3 placements (P-50/34+1.1, 35+0.1, 36+0.1), -60 ppm 98 / 92, both exactly R395-2's. With only the NCO compare changed: -50 ppm 0 failures; -60 ppm the SAME 98 / 92 - every one a single net-zero repeat/skip clearing slowly (last slip at column 76-181), no lost tick. So the -60 ppm failures are the 64-column window law (ruling 3), not the NCO race (ruling 1).
- 00:55: rate map of on-crossing engagements with the fix (packaged probe, -2..+2 cycles, 1,280 placements each): true plan max last slip col 19; -25: 23; -40: 31; -55: 87; -62: 294 (all net zero); -64 and beyond carried across (a repeat without its skip inside 300 columns); +50/+60/+65: col 8; +70 carried across.
- 01:00: settled lock at +/-80 and +/-100 ppm, 52 placements x 60,000 columns: 0 tail slips, acquisition slips net zero and ended by column 13,065. Guarded: no STOP.
- 01:05: NCO fix (`>=`), media_nco check 10 (410/0; 10 failures with the 377d1ac3 NCO), NCO OOC area.
- 01:10: capture_coherence: derived keep-off (mga_keepoff.py), rate-derived engagement window, CRF-fine-50 (15,425/0; 27 failures / 9 placements with the 377d1ac3 NCO), settle sweeps; full junction 20,832/0 in 241 s. R395-2's run_fine.sh re-derived from this tree by R395-2's own scripts: -50 ppm 0 failures, -60 ppm 0 failures.
- 01:15-01:25: chmap_capture [Q] (371/0; RM7 9 failures, RM8 12); datapath leg 332/0; mutants.py new legs (band50, fine, nco) and mutants (RM5, RM7, RM8, `==` x2): 27/27, 862 s sequential. Transient and on-crossing limits pinned (84-90 ppm; -63/+68).
- 01:25-01:35: docs (TIME_SYNC.md, REGISTER_MAP.md, CHANGELOG.md, TESTING.md, media_nco README), comments (aligner banner, datapath binding, crossbar banner, NCO contract); static gates on the working tree. Committed `abe78678`, `112c0cb8`, `c5e44378`.
- 01:38: gate run at `c5e44378`: `check_em_dash --base` failed on one added README table row (an em dash; the gate reads only committed lines, so the pre-commit run had passed). Stopped the streams; fixed in `ddb07747`.
- 01:40-02:16: full gate run at `ddb07747`: 85 of 85 rc 0; suite tally 52,285 checks, 0 failures. R395-2's run_fine.sh at the committed head: -50 and -60 ppm, 0 failures each.
- 02:20: evidence assembled; PR-BODY.md Round 3 section written.
- 02:25: posted REVIEW READY (https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5881204511). Stopped: no push, no PR edit, no other comment.
