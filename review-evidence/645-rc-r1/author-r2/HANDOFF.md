# #645 design round: a bind at INTERNAL arms the settle recentre (lane A620)

Status: Round 2 DONE at `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c` (section "Round 2" at the end). REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6195691366 (text in `REVIEW-READY-R2.md`, read back in `REVIEW-READY-R2.readback.md`, equal but for one trailing newline). Round 1: REVIEW READY posted at `2639eecf3f94aa1a8be5c922058a05f0a48b1933`. Every gate and suite the change touches ran to rc 0 (section 6); open items in section 7.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187650593 (text in `TAKEN.md`)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6192046983 (text in `REVIEW-READY.md`, read back in `REVIEW-READY.readback.md`, equal but for one trailing newline)
- Branch: `645-bind-recentre` from dev `f62602531d415d6c1cae1374a3cc2938faf54049`, local, not pushed. Head and commits: section 8.
- Simulator: Verilator 5.050, the pinned wrapper first on `PATH` for every build and run. The host's own `verilator` is 5.052 and was never used.
- Builds and scratch lived in a scratch directory outside the tree and outside this packet. The in-tree suite builds are removed again at the end (section 6).
- Paths below such as `campaign/fix/` are in this packet.

## Contents

1. Reproduction, with its parameters derived from B17
2. The fix
3. Checks, planted controls and escapes
4. Area delta
5. Docs changes
6. Gates and suites
7. Open items for the manager
8. Commits and head
9. Packet layout

## 1. Reproduction (parameters derived from B17)

**Source.** B17's packet on PR #741's evidence branch `645-b17-review-evidence` at `35cc1ae4`, `review-evidence/645-b17-r1/author/summary/cNN.json`, read with `git show` (no checkout). Fields used: `tap.priming` (the first peer PDU after the CONNECT_RX command, and the arrival phase against the DUT's transmit grid), `tap.late_pdus` (every peer PDU over 10 us late, with its time from the bind) and `poll.slips` (each `SLIP_LB` step's interval). The scripts and their outputs are in `b17/`.

**Derived per cycle.** The first burst is the first run of consecutive PDUs over 10 us late; its time is from the first PDU.

| B17 cycle | First PDU after the bind, ms | First burst after the first PDU, s | Its peak, us | Largest later burst, us | B17's slip, s after the bind |
|---|---:|---:|---:|---:|---|
| 1 | 163.485 | 2.6534 | 28.833 | 28.691 | 2.56 to 3.14 |
| 2 | 93.536 | 1.4650 | 25.009 | 28.365 | 1.09 to 1.96 |
| 3 | 156.762 | 1.6719 | 26.326 | 28.713 | 1.07 to 1.95 |
| 4 | 52.750 | 3.1446 | 29.309 | 30.071 | 3.10 to 3.68 |
| 5 | 7.854 | 0.0938 | 24.565 | 30.260 | 0.07 to 0.64 |
| 6 | 131.486 | 3.4974 | 25.840 | 28.475 | 3.57 to 4.15 |
| 7 | 54.945 | 1.3014 | 24.968 | 29.140 | 1.06 to 1.94 |
| 8 | 28.539 | 1.3102 | 25.581 | 27.575 | 1.18 to 1.94 |
| 9 | 161.240 | 1.1185 | 25.128 | 29.528 | 1.04 to 1.95 |
| 10 | 101.128 | 5.3246 | 26.869 | 27.813 | 5.09 to 5.67 |

Every B17 slip interval holds its cycle's first burst and no other burst.

- **Burst shape.** Each first burst is 10 to 13 consecutive PDUs over 10 us late, spaced 122 to 126 us, falling linearly: least-squares slopes 1.468 to 1.664 us per PDU, mean 1.538. The harness makes PDU k of a burst `max(0, peak - 1.538 k)` us late.
- **Clocks.** delta_ppm stayed within +/-0.0017 ppm. The harness runs the peer on the DUT's own INTERNAL clock (`--case bind` defaults `--peer-ppm` to `--dut-ppm`, as `pullin` does).
- **Baseline lateness.** B17's lateness was p99 2.65 us and p99.9 4.4 to 6.1 us. The standing leg adds uniform 0 to 5 us; the campaign runs 0 and 0 to 5 us.
- **The primed-margin window.** The ring's margin is the time from a PDU's first event landing to the pop that takes it. B17 bounds it: no PDU over 10 us late slipped the ring before the first burst, so it was above 10 us; the smallest slipping burst peaked at 24.565 us (cycle 5), so it was below that; after the slip a 30.26 us burst passed, so margin + 20.833 > 30.26, above 9.43 us. Window: 10.0 to 24.565 us.
- **The priming phase.** B17 measured the peer's arrival phase against the DUT's transmit grid on the wire: 1.41 to 1.45 us after it, mod 125 us, the first PDU within -1.0 to +0.8 us of the steady phase. The DUT's transmit and receive pipeline latencies are not in B17's data, so that phase cannot be mapped to the media tick directly. The harness instead places the first PDU's arrival at a phase F of a media tick and measures the margin it primes. Without lateness the margin is about 20.88 - 20.5 F us up to F = 0.875 (20.80 us at 0, 10.40 us at 0.5, 2.56 us at 0.875) and 22.08 us at F = 0.9375. B17's window therefore holds F from 0 to 0.5, and 0.9375: 10 of 16 phases. The standing leg uses F = 0.125, whose primed margin with 0 to 5 us lateness is 13.3 to 18.4 us, mid-window.

**Reproduction without the fix.** Dev `f6260253`'s `milan_datapath.sv` (SHA-256 `553be35db215667953502e1f6284405da4f37babcf249b31ab3823f4b4350e11`) through the final harness (`DP_SRC` points the build at it). `make sweep-bind`'s recipe: all ten cycles at 16 first-PDU phases, without lateness and with 0 to 5 us, 320 binds (`campaign/base/`):

- Each of the 169 binds whose first PDU primed the ring inside B17's window slipped it exactly one frame (`SLIP_LB` +2 dups, 0 skips), within 10 ms of its first burst's start, and never again: B17's shape. `campaign/inside_check.txt` checks this per bind.
- The 151 binds outside the window slipped once (51) or twice (100). B17's single slip per bind and its 10 us bound exclude them.
- No arm, no settle recentre and no render recentre in any bind. All 32 runs fail their checks (rc 1), as a reproduction must.

The same shape, single cycles, from the first exploratory runs: B17 cycle 5 at F = 0.25 slipped +2 dups at the burst, 94 ms after the first PDU.

## 2. The fix

`hdl/milan/milan_datapath.sv`, inside the `g_settle_recentre` range that `follow_ring` copies verbatim (`dp_glue.py`) and `settle_control.py` compiles:

- `settle_bind_wait_r[s]`, one flop per loopback stream: set by the stream table's bind rise (`strtbl_bind_rise_w`), cleared by the stream's first accepted `tlast` beat on the LOOP tap (the beat that sets `KL_chan_map_capture`'s `q_primed_r`) and by its bind fall.
- `settle_bind_pdu_w[s]` is that beat while waiting. `settle_bind_arm_w = !follow_sel_r && |settle_bind_pdu_w` is ORed into `settle_arm_w` beside the source-change and re-engagement terms. The excursion term's line is unchanged, so the existing mutant plants still apply.
- Unchanged: the firing rule, the 2,048-tick INTERNAL dwell, the 2^20-tick ceiling, the pulse's fan-out to the render stage and every loopback stream, the counters. No port, register field, parameter or other module changes.
- Under following the beat clears the wait and arms nothing. Without the loopback lane (`LOOPBACK_P` = 0, the shipping 8x8 shape) the tap's valid is constant 0 and the arm prunes to nothing (section 4).
- The arm is the first PDU, not the bind's rise. B17's first PDUs came up to 163.5 ms after the command, and a recentre fired 42.7 ms after the rise finds the ring unprimed, which ignores it (control BIND-RISE).

## 3. Checks, planted controls and escapes

**`follow_ring` `bind` case** (`tb/verilator/follow_ring/sim_main.cpp`, `run_bind_cycle`). Per bind at INTERNAL:

| Check | Planted control that fails it | Escape (what it cannot see) |
|---|---|---|
| the bind primed the ring inside B17's window | none planted: it is the reproduction's premise, and the campaign reports where it fails (`--any-phase`) | the mapping from B17's wire phase to the media tick (section 1) |
| its first PDU armed the settle recentre once | NO-BIND-ARM (no arm); BIND-RISE (the arm 7.8 to 161 ms before the first PDU); `settle_control` plants no-arm and at-rise | an arm at a later beat of the first PDU's own frame (it lands within the 2.4 us window); `settle_control`'s any-beat plant covers it |
| one settle recentre, 2,048 media ticks after the arming | NO-BIND-ARM | a firing rule wrong only under following is out of this case's INTERNAL scope; `b8` covers following |
| the render stage counted one recentre | NO-BIND-ARM | the render stage's own snap: graded by `[PULLIN]` and the render suite, not here |
| no SLIP_LB change across the cycle | NO-BIND-ARM (cycles 5, 4, 9), BIND-RISE (cycles 4, 9) | a phase outside B17's window, whose slips before the ring acts are reported, not failed (section 7) |
| no loopback slip after the ring acts | NO-BIND-ARM (the expected action instant divides) | none at the graded phases; a burst beyond 0 to 5 us plus B17's peaks was not run |
| the ring centred after the recentre, margin in (5, 6] ticks plus lateness | NO-BIND-ARM | a target error inside (5, 6]: OVERSHOOT and `chmap_capture` `[LRC]` grade the target |
| empty-side and full-side margins at least one tick after it | NO-BIND-ARM | as above |

Under CRF following (`--follow-binds 1`): "the switch to CRF locked and settled before the binds", "the bind armed no settle recentre" and "no settle recentre from the bind to the next unbind". Control: FOLLOWING-ARM fails the first. Escape: the slip that still follows a bind under following is reported, not graded (section 7).

**The existing legs.** Their checks are unchanged. `follow_ring_wrap.sv` and `settle_control.py`'s header now declare the names the arm reads (the LOOP tap and the bind edges), because both compile the block verbatim. `b8` and `pullin` raise no bind rise: their stream stands for one bound long before, as at the bench, where at B8's 5.92 ppm offset the INTERNAL beat parks the ring at its empty edge within a few beats whatever a bind's recentre left (the wrapper says so).

**`settle_control.py`** (the controller, verbatim, at 6.25, 25, 50 and 100 MHz): a bind's first PDU arms at INTERNAL even during recovery; a PDU with no bind, the bind's own rise, a beat before the PDU's end, another stream's PDU, a later PDU, an unbound stream's PDU and a bind under following arm nothing. 8 actions at each rate (2 new). Eight scratch plants of the block, run through `settle_control.py`'s own harness, each end in its named `$fatal` (`controls/sc_plants/plants.log`, 8/8): no-wait ("a PDU without a bind armed"), any-stream, any-beat, keep-wait ("a later PDU armed again"), fall-ignored, ungated ("a bind under following armed"), at-rise and no-arm. These plants are evidence here, not tracked: `settle_control.py` reads the tracked datapath only.

**`mutants.py`**, `make mutants SWEEP_JOBS=4`: 15/15 caught, the twelve existing and NO-BIND-ARM, BIND-RISE and FOLLOWING-ARM (`suites/fr_mutants.log`).

**Campaign with the fix** (`campaign/fix/`, 32/32 runs rc 0):

- All 320 binds: one arm at the first PDU, one settle recentre 2,047.0 to 2,048.0 ticks after it, one counted render recentre.
- Nothing slipped after a ring acted, at any phase.
- The 169 in-window binds moved neither `SLIP_LB` counter.
- After the recentre: empty-side margin at least 3.48 ticks, full-side at least 4.88, centred margin up to 6.19 ticks with lateness.
- Six of the 151 out-of-window binds slipped once before the recentre acted (section 7).

**Standing leg** (`make -C tb/verilator/follow_ring`, `bind`): B17 cycles 5, 4 and 9 at F = 0.125 with 0 to 5 us: each one arm, one settle recentre 2,047.65 to 2,047.70 ticks later, one render recentre, `SLIP_LB` +0/+0, primed margin 13.28 to 18.40 us, margin after 4.28 to 5.88 ticks. Then cycle 5 under CRF following (LOCKED 2.56 s, the switch's settle 6.66 s after it): no arm, no recentre, and B17's burst slipped the ring one frame (reported).

## 4. Area delta

The change's own logic, out of context: the settle block (`SRC_SETTLE_ERR_C` to `end : g_settle_recentre`, as `settle_control.py` extracts it) as a top with its inputs as ports, at the shipping 50 MHz axis clock, base (dev `f6260253`) against head, re-measured at the final RTL. Vivado 2026.1, `synth_design -mode out_of_context -flatten_hierarchy full`, xc7a100tfgg484-2, 20 ns clock, run under the shared lock, 0 critical warnings; Yosys 0.66 `synth_xilinx -family xc7 -noiopad -flatten` beside it (`area/`).

| Shape | Loopback streams | Vivado LUT | Vivado FF | Yosys LUT | Yosys FF | WNS, ns |
|---|---:|---|---|---|---|---:|
| AX7101 1x1 TDM8 (shipping, `loopback_lane: true`) | 1 | 73 to 76 (+3) | 93 to 94 (+1) | 149 to 153 (+4) | 93 to 94 (+1) | +15.486 to +15.743 |
| AX7101 8x8 (shipping, `loopback_lane: false`) | 0 (tap tied 0) | 73 to 73 (0) | 93 to 93 (0) | 149 to 151 (+2) | 93 to 93 (0) | +15.486 |
| An 8x8 build with the loopback lane (not shipped) | 8 | 73 to 85 (+12) | 93 to 101 (+8) | 149 to 176 (+27) | 93 to 101 (+8) | +15.676 |

No block RAM, DSP or carry change in any row. Yosys's +2 LUT with the lane off is that estimator's; Vivado prunes the arm to the base netlist's counts.

**Against NFR-RES-01 and the #640 budget.** NFR-RES-01 asks for at most 38,040 LUT (60 % of 63,400). The recorded shipping route (`route-1x1`, `AREA_BUDGET.md`) is 50,267 LUT, 12,227 over; the Mark II plan's central estimate ends at 31,667, 6,373 under. The change adds 3 LUT and 1 FF on the shipping 1x1 shape and nothing on the 8x8: 0.02 % of the current gap and 0.05 % of the plan's margin, far inside each `pp_resource_gate.py` tolerance. The processor endpoints (`ooc-1x1`, `ooc-8x8`) do not contain this block and cannot move. No routed figure is claimed: at +3 LUT the route's own variance on unchanged RTL (`AREA_BUDGET.md` records 366 LUTs of growth outside the changed wrapper in one comparison) would swamp it.

| Input or report | SHA-256 |
|---|---|
| `area/base_n1.sv` | `d71e21b9be920b31376f3fb529c1f2774f4fab664d988bc13370243c0caddfb5` |
| `area/head_n1.sv` | `8182183f53cfa285b801908b61d39f3b66098f53217da45d97052815a97a7368` |
| `area/base_n8.sv` | `bcc4bac39215fdce42ebb10ed54ad4e5dc1248a430dd14be9192e0019df52071` |
| `area/head_n8.sv` | `27e12c4f7a0739d5572ddc684bfb64f9f39a8a09da573e4a2fcb99b8ef61c5d5` |
| `area/head_off.sv` | `1ba135a7d3c7d043c4e5e3f5a72ba39901d3f8a6da80c9fb2d40e1c4e75573e8` |
| `area/mk_ooc.py` | `aef2a340e54419ba18d7492b66529a24bd1e2b1b76ea51e6d8dabf032cf33ea4` |
| `area/ooc.tcl` | `8ac33d9020a68cfa61f9b9d55c66d783e3610894739f4b80cf3d7e4fde46ff5a` |
| `area/head_n1.vivado.util.txt` | `5605b89cf14e1fed3c696030d68b79d696967d7ce330b5717a7f120ed837b3c6` |

## 5. Docs changes

- `docs/design/MEDIA_CLOCK_FOLLOWING.md`: the settle-recentre table's "Armed by" row gains the bind arm; the loopback-latency paragraph now reads "A bind primes the ring where its first PDU lands; at INTERNAL the bind's settle recentre centres it"; a new subsection "A bind at INTERNAL" (B17's measurement and why, the arm, under following, every stream takes it, the follow_ring figures with the arming window); the test plan's `follow_ring` row (the `bind` leg, `sweep-bind`, three controls); the implementation notes.
- `docs/design/TIME_SYNC.md`: the settle-recentre row of the listener render-latency table, and two short lines under it (the page's 10-word sentence limit).
- `docs/reference/REGISTER_MAP.md`: the `SLIP_LB` row names the bind at INTERNAL among the declared discontinuities.
- `docs/testing/TESTING.md`: the `follow_ring` row and the explicit-campaign table (fifteen controls, the bind leg, `sweep-bind`), and the wall-clock record (section 6).
- `scripts/measure_test_evidence_readers.py`: the two `follow_ring` drivers' dispositions name the bind arm.

B17 is cited by its PR and report links. Its findings section is not on dev yet (PR #741 is in review), so no in-tree anchor is linked.

## 6. Gates and suites

Every command unpiped, logs and return codes in `gates/` and `suites/`.

**Source and docs gates at the head** (rc 0 each): `check_em_dash.py --base f6260253` (0 findings over 118 added lines, arms 339/339), `git diff --check f6260253 HEAD`, `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `docs/traceability/gen_module_matrix.py --check`, `check_feature_status.py`, `check_baremetal_only.py --check` (the pinned Markdown environment for the docs gates); `check_py_idiom.py`, `check_cpp_idiom.py`, `check_sv_idiom.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `check_todo_ownership.py`, `check_rtl_source_lists.py`, `check_port_contracts.py`, `measure_test_evidence.py --check` and `--selftest`, `measure_control_flow.py --selftest`; `lint_rtl.py --check` (90 <= 90); `xvlog_gate.py --check` under the lock (0 findings in `hdl/`). One earlier `check_cpp_idiom.py` run refused `std::atoi` in the new option parse; it was replaced by `std::strtol` before the commit.

**Suites, each `make -C tb/verilator/<suite>` with `MAKEFLAGS` unset** (`suites/`):

| Suite | rc | Checks | Wall, s |
|---|---:|---|---:|
| `follow_ring` default (five legs) | 0 | 96 tallied (b8 48, pullin 18, bind 30), small pulls 10/10, controller PASS at four rates | 876.9 |
| `follow_ring` `mutants SWEEP_JOBS=4` | 0 | 15/15 caught | 1297.3 |
| `milan_dp_mclk` | 0 | 55 + 32 + 50, controls 31/31 | 1533.4 |
| `milan_dp_render` default | 0 | 266 + 71 (the `[LAW]` phases, T30, T31), leg controls 5/5 | 2326.3 |
| `milan_dp_render` `tdm8render-pullin PULLIN_JOBS=4` | 0 | 19 legs, 838 checks, 0 failures; 0 loopback slips during and after each pull | 5055.1 |
| `milan_dp_render` `tdm8render-law-boundary` | 0 | 81/81 over 564 windows, largest walk 3 cycles against the stated 5 | 4305.3 |
| `capture_coherence` | 0 | 20,832 + 332, controls 30/30 | 1995.7 |
| `milan_dp_gm_steps` | 0 | 190, controls 6/6 | 2207.9 |
| `pp_shadow` | 0 | 609 + 609 + 649 + 317 | 1749.8 |
| `csr` | 0 | 1,815 tallied | 172.7 |
| `mbx` | 0 | 2,123 tallied | 64.0 |
| `avtp_parser` | 0 | 11,201 tallied | 28.7 |
| `chmap_capture` | 0 | 847 tallied | 159.3 |
| `milan_dp` default (`SIM_JOBS=2`) | 0 | 11,956 tallied over 15 tallies | 1897.3 |
| `milan_dp_gptp` (physical) | 0 | 143 + 6 + 20 + 14 + 14 = 197; two declared recentres (startup at input PDU 9,822 and reset reacquisition at 95,986), each step -5 on the wire with both counters 0 to 0 | 5728.0 |

`scripts/suite_tally.py` over the eleven default-sweep suite logs: 52,122 checks, 0 in-suite failures; with `--physical-gptp` 197, 0 failures; `--verdict` rc 0 on every log (`tally/`). Wall times are under heavy shared load (16 CPUs, load 20 to 67) and are not a timing claim.

One invocation mistake, retained: `milan_dp` with `SIM_JOBS=4` built every model and then `sim_pool.py` refused the job count ("--jobs must be 1 or 2 (the #517 ceiling)"), rc 2, before any simulation (`suites/milan_dp.simjobs4-refused.log`, hashed). It was re-run with `SIM_JOBS=2`.

**Wall clock of the five-leg default.** Cold, back to back, CPUs 0-3, independent jobs on the other CPUs: the five legs 857.6 s, the four earlier legs alone (`-j4 b8 pullin small-pullin settle-control`) 800.9 s (`wallclock/`). The bind leg costs 7.1 %. This host is slower than the round 2h replica host and does not reproduce its 437.2 s, so the projection scales the measured hosted window: 1114.2 s x 1.0709 = 1193.2 s, 66.8 s under 1260 s and 246.8 s under 1440 s. Recorded in `TESTING.md` and the suite's Makefile as a projection; hosted acceptance of the head is still owed.

**Synthesis and builder gates.** `syn/yosys/run.sh`: 58/58 tops, rc 0. `sw/builder/test_builder.py --require-rv32 --require-elaboration`: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11's historical Arty calibration arm, whose placed report is not on this host (as in the lanes before), with no elaboration arm skipped for a toolchain reason.

**The physical leg's recentres.** They are still exactly two, startup and reset reacquisition, each the declared -5 step on the wire with `SLIP_LB` unchanged, and every ordering check passes. They decide at input PDUs 9,822 and 95,986; PR #672's round-2e evidence recorded output PDUs 6,047 and 92,220. The later decision is consistent with the bind's arm restarting the pending dwell at the stream's first PDU (one pending flag), but no base run of this leg was made here, so that is an inference.

**Logs not kept.** The pull-in campaign's 19 per-leg logs and the mutation campaign's per-mutant run logs lived in the suites' in-tree build directories, removed in the final cleanup. Their totals (19 legs, 838 checks, 0 failures; 15/15 caught, with each new control's failing checks listed in section 3) were read before it, and the suite logs keep each leg's settle line and each control's verdict.

**The tree afterwards.** `git status --short --ignored` is empty in the superproject and in every initialised submodule: every build output, cache and generated image of these runs was removed (`git clean -fdX`, after checking the tree held no ignored file at the start, and in `protocol-processor` for one bytecode cache).

## 7. Open items for the manager

- **The arming window at phases B17 excludes.** For the 42.7 ms between a bind's first PDU and its recentre firing, the ring keeps its primed margin. In the campaign, 6 of the 151 binds whose first PDU primed the ring under 10 us (the two phases nearest the empty edge, 3.8 and 2.6 us without lateness, with 0 to 5 us of lateness) slipped once in that window, each within about 2 ms of the first PDU. B17's evidence puts the bench's margin above 10 us with no PDU over 10 us late before a burst, and none of the 169 in-window binds slipped. Stated in the design as a limit of the ruled firing rule, not declared. An option, not taken without a ruling: prime the ring at the target on the bind's first PDU (a `KL_chan_map_capture` change) instead of waiting for the dwell.
- **Under following a bind arms nothing**, as ruled. Such a ring still primes where its first PDU lands, and the standing leg shows B17's cycle-5 burst slipping it one frame under CRF following. Stated as a limit.
- **Every stream takes the recentre.** On a shape with several listener streams and the loopback lane, a bind at INTERNAL recentres the other running streams too; a ring at its target takes no step. The shipping 1x1 shape has one listener stream; the shipping 8x8 has no loopback lane.
- **Hosted wall clock.** The default `follow_ring` gains a leg; its hosted window at the head needs the exact-head `verilator-suites` run.
- **The bench repeat** of B17's ten binds on an image with this change is #645's acceptance, after the merge.
- **Shard timing.** `scripts/suite_shards.py` keeps `follow_ring` at 1158 hosted seconds; the fifth leg adds about 7 %. Its figure is a hosted measurement, so it is not edited here.
- **Packet privacy.** The suite logs and the scratch scripts (`run_chain.sh`, `assemble.sh`, `wallclock/wallclock.sh`) carry this host's paths. Redact before publishing the packet.

## 8. Commits and head

On dev `f62602531d415d6c1cae1374a3cc2938faf54049`, local, not pushed, no PR. One-line subjects, no body, no trailers.

| Commit | Subject | Files |
|---|---|---|
| `4e6b5398136680b32f2241a0eb0729f2c2e817ef` | Arm the settle recentre on a listener bind's first PDU at INTERNAL, with follow_ring's B17 bind replay and controls (#645) | `hdl/milan/milan_datapath.sv`, `tb/verilator/follow_ring/{Makefile,follow_ring_wrap.sv,mutants.py,settle_control.py,sim_main.cpp,sweep.py}`, `scripts/measure_test_evidence_readers.py` |
| `2639eecf3f94aa1a8be5c922058a05f0a48b1933` | Document the settle recentre's bind arm and its B17 evidence (#645) | `docs/design/MEDIA_CLOCK_FOLLOWING.md`, `docs/design/TIME_SYNC.md`, `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md` |

Head `2639eecf`, tree `c0bece4c6943bee323b9a72c4e677abdda840004`; 12 files, +625 / -41. Every simulation in sections 1, 3 and 6 ran on this RTL and harness; the only later edits were comments in the suite's Makefile and documentation.

## 9. Packet layout

| Path | What |
|---|---|
| `HANDOFF.md`, `PR-BODY.md`, `TAKEN.md` | This file, the PR body, the posted TAKEN text |
| `b17/` | `b17_derive.py` and `b17_burst.py` with their outputs: the per-cycle parameters and burst slopes read from B17's packet |
| `campaign/fix/`, `campaign/base/` | `sweep-bind`'s 32 runs each: command, log, rc, the driver's table `bind.md`; `summary-fix.md`, `summary-base.md` (`summ_bind.py`) and `inside_check.txt` (`inside_check.py`) |
| `suites/` | Each suite's log, rc and wall seconds; logs over 200 KB as an excerpt, with size and SHA-256 in `LARGE.sha256`; `chain.log` |
| `tally/` | `suite_tally.py` totals and `--verdict` outputs |
| `gates/` | Every gate's log and rc |
| `area/` | The OOC tops, `mk_ooc.py`, `ooc.tcl`, Vivado utilisation and timing reports, Yosys stats |
| `controls/sc_plants/` | The eight scratch plants of the bind arm through `settle_control.py`'s harness: script, run logs, `plants.log` (8/8) |
| `wallclock/` | The five-leg and four-leg cold replicas: script, logs, `result.txt` |
| `run_chain.sh`, `assemble.sh` | The scratch orchestration and this packet's assembly |
| `MANIFEST.sha256` | SHA-256 of every packet file except itself |


## Round 2 (PR #742: R635-1-F1 = R634-1-F1, R634-1-F2, R634-1-S1)

Assignment: [A10] "Round 2 for PR #742" on #645 ([comment 6193474559](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6193474559)), answering R635-1 ([6192392408](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6192392408)) and R634-1 ([6193454471](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6193454471); its receipts read from `origin/645-rc-review-evidence`, `review-evidence/645-rc-r1/reviews/R634-1/`). Started from `2639eecf3f94aa1a8be5c922058a05f0a48b1933` (confirmed equal to origin's `645-bind-recentre`). The RTL does not change. Round 2 receipts are under `r2/`. Not pushed; no PR edit.

### R2.1 Commits

| Commit | Subject | Files |
|---|---|---|
| `e0960932045bdae2ac0602b82d0021da18b525af` | Bound follow_ring's B17 bind window below by cycle 5's later burst, 9.427 us, not B17's 10 us listing threshold (#645) | `tb/verilator/follow_ring/sim_main.cpp` |
| `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c` | Document B17's supported primed-margin bound and the bind arm's pre-existing arming-window slips, #743 (#645) | `docs/design/MEDIA_CLOCK_FOLLOWING.md` |

`2639eecf..fb5dd3da`: 2 files, +62 / -30. Against dev `f6260253`: 12 files, unchanged RTL (`hdl/milan/milan_datapath.sv` is byte-equal to `2639eecf`'s). Every simulation below ran on the `sim_main.cpp` committed in `e0960932`; the only edit after them is one sentence of the design page.

### R2.2 F1: the lower bound B17 supports

`r2/b17_bound.py` reads the ten `review-evidence/645-b17-r1/author/summary/cNN.json` (evidence branch `bdb96b66`) and nothing else; `r2/b17_bound.txt` is its output. Per cycle: the first burst (the listed burst inside the slip interval) slipped the ring, so the margin was below its peak; every later burst met a ring one tick (20.833 us) further from its empty edge and slipped nothing, so the margin was above the largest later peak less one tick.

| Cycle | Lower bound, us | Upper bound, us |
|---|---:|---:|
| c05 | 30.260 - 20.833 = **9.427** | **24.565** |
| the other nine | 6.742 to 9.238 | 24.968 to 29.309 |

Cycle 5 alone gives both edges of the window, 9.427 to 24.565 us, so no cross-cycle assumption is needed for the window itself; every other cycle's interval contains it. The summaries hold no per-PDU lateness below B17's 10 us listing threshold (`late_pdus` keeps only PDUs over 10 us; the cycle's lateness percentiles are whole-cycle), and the raw captures are not in the packet, so the measured pre-burst maximum could not be extracted; the later-burst bound is the one used, as ruled. The 10 us threshold is printed and never used.

Changes: `sim_main.cpp` `kB17MarginLoUs = kB17[4].later_us - kTickUs` (9.4267 us) and `kB17MarginHiUs = kB17[4].burst_us` (24.565 us), derived in the source from cycle 5's replay row; the file comment and the constant's comment give the derivation and say the listing threshold bounds nothing. The design's "What B17 measured" and "Why" paragraphs say the same; "since nothing that late slipped it" and "At the bench that margin was above 10 us" are gone. `grep -rn "nothing that late"` over `docs/`, `tb/` and the PR body: no match (rc 1).

**The split moved, so `sweep-bind` was rerun** on both datapaths (`sweep.py bind --jitter-us 0 5 --extra --dwell-s 0.5`, the arguments of `make sweep-bind`, built out of tree; `r2/campaign/fix16/`, `base16/`):

| | Round 1 (10 us) | Round 2 (9.427 us) |
|---|---|---|
| Head: runs passing | 32 / 32 | 32 / 32 (rc 0) |
| Binds inside / outside | 169 / 151 | **177 / 143** |
| Head: inside binds with any `SLIP_LB` change | 0 | 0 |
| Head: one arm, one settle, one render recentre | 320 / 320 | 320 / 320, firing 2,047.02 to 2,048.02 ticks after the arm |
| Head: slips after the ring acts | 0 | 0 |
| Head: margin after the recentre | empty side >= 3.479, full side >= 4.884 ticks | the same |
| Dev's datapath on the head's inside binds | 169 of 169 one frame at the first burst | **177 of 177** one frame (+2 dups, one event) at the first burst, nothing else (`r2/base_on_head_window.py`) |
| Dev's datapath on the head's outside binds | 151: once 51, twice 100 (slip events) | 143: 43 one frame, 99 two frames, 1 a frame and a pair (+3 dups at the burst, `bind_j5_p12` cycle 1) |

The 8 binds that moved are the eight of `bind_j5_p05` (phase 0.3125, 0 to 5 us) whose lowest primed margin is 9.440 us; cycles 8 and 9 of that run stay outside. All 8 hold on the head. R634-1 expected no lower edge in [9.43, 10) on this grid; this run has one. Dev's datapath classes 171 of the 177 inside by its own measurement, because without the arm it measures the primed range up to the first burst rather than to the settle recentre and lateness takes six of them to 9.280 us; all 177 still slip exactly one frame at their burst, B17's signature.

### R2.3 F2: the arming-window residual

The arm stays as ruled. Grids run on both datapaths (`r2/campaign/`), every one at the 9.427 us bound:

| Grid | Command (per run, sweep.py) | Head runs | Inside: binds with a one-pair dup | Outside: binds that slipped before the burst |
|---|---|---|---|---|
| `sweep-bind`, 16 phases x {0, 0 to 5 us}, all ten cycles | `--jitter-us 0 5 --extra --dwell-s 0.5` | 32 / 32 pass | 0 of 177 | 6 of 143, phases 0.8125 and 0.875, 0.129 to 2.127 ms after the first PDU |
| 32 phases x 0 to 5 us, all ten cycles | `--phases 32 --jitter-us 5 --extra --dwell-s 0.5` | 31 / 32 (`bind_j5_p27` fails its cycle-7 no-change check) | **1 of 151**: cycle 7, phase 0.84375, +1 dup 0.127 ms after the first PDU (primed 19.04 to 24.16 us) | **19 of 169**, four phases 0.78125 to 0.875, up to **2.503 ms** after the first PDU |
| 128 phases x {0, 0 to 5 us}, cycle 7 | `--phases 128 --jitter-us 0 5 --extra --b17-cycles 7 --dwell-s 0.5` | 254 / 256 (`bind_j5_p114`, `bind_j5_p119`) | **2 of 140**: phases 0.890625 and 0.9296875 (0 to 5 us), +1 dup 0.127 and 0.252 ms after the first PDU (primed from 18.24 and 17.44 us) | 6 of 116, six phases 0.7734 to 0.8594, up to **2.877 ms** |

- **Pre-existing on dev, not removed by the arm.** `r2/early_slips.py` compares every slip before the first burst on the head and on dev's datapath, bind by bind: 6 / 6, 20 / 20 and 8 / 8 binds, each slip identical in kind and in time to the microsecond (`r2/early-16.txt`, `early-32.txt`, `early-dense.txt`). On dev the three in-window binds then also take the +2 frame at the burst (+3 dups).
- R634-1 measured the same three dups as 1 of 141 and 2 of 132 under the 10 us classification; the denominators moved with the bound, the dups did not.
- Every out-of-window bind that slipped early dipped to a primed margin of 3.52 us or less. The in-window dups came at 17.44 us and more.
- The one-pair dup's mechanism is #743's; it was not investigated here (no probe, no RTL read beyond round 1's).
- No slip after the ring acts in any of the 896 head binds (320 + 320 + 256) across the three grids.

**Where it is stated.** `MEDIA_CLOCK_FOLLOWING.md` "A bind at INTERNAL", the arming-window bullet: out of the window per grid (the 16-phase grid's "6 of 143" no longer the whole picture), in the window with incidence, phases and #743, both pre-existing on dev. The test plan's `follow_ring` row: the no-change criterion is for in-window binds at the leg's and `sweep-bind`'s phases, and finer grids find the pre-existing dup (#743). `sim_main.cpp`'s bind-case comment says the same. PR body: Round 2 and Known limitations.

**Checks, controls and escapes in round 2.**

| Check | Control (demonstrated detection) | Escape |
|---|---|---|
| In-window "no SLIP_LB change across the cycle" at the 9.427 us bound | It fails, rc 1, on the pre-existing one-pair dup at 32-phase `p27` and dense `p114`, `p119` (head and dev): the check sees a single dup | `sweep-bind`'s 16 phases and the default leg's phase 0.125 contain no dup phase, so the standing gate is green with the residual present; stated in the design and test plan, #743 owns it |
| The window classification itself | The 8 `bind_j5_p05` binds at 9.440 us cross from outside to inside and are graded; they hold | A margin between 9.427 and 9.440 us is not on any grid |
| NO-BIND-ARM, BIND-RISE, FOLLOWING-ARM and the other 12 | `make mutants`: 15/15 caught, each by its named check (`r2/suites/fr_mutants.log`) | as round 1 |

### R2.4 S1: area headline

The area claim in the PR body now cites the current headline, `AREA_BUDGET.md:124`: 50,013 LUT, 11,973 over NFR-RES-01's 38,040; +3 LUT is 0.025 % of that gap. Section 4's `route-1x1` row (50,267, 12,227 over) is the older comparison record, kept there as round 1 measured against it.

### R2.5 Gates and suites at `fb5dd3da`

Every command unpiped, output to a file, rc recorded (`r2/gates/`, `r2/suites/`). Verilator 5.050, the pinned wrapper first on `PATH`.

| Gate or suite | rc | Result |
|---|---:|---|
| `make -C tb/verilator/follow_ring` (five legs) | 0 | b8 48, pullin 18, bind 30 checks, 0 failures (`suite_tally.py`: 96 / 0, `--verdict` rc 0); small pulls 10/10; settle control PASS at 6.25, 25, 50 and 100 MHz; 570 s under shared load |
| `make -C tb/verilator/follow_ring mutants SWEEP_JOBS=8` | 0 | 15/15 caught; `--verdict` rc 0; 441 s |
| `sweep-bind` (head), 32 runs | 0 | 32/32, table above |
| `check_em_dash.py --base f62602531` | 0 | 0 findings over 144 added lines, arms 339/339 |
| `git diff --check f62602531 HEAD` | 0 | |
| `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_doc_paths.py`, `gen_module_matrix.py --check`, `check_feature_status.py`, `check_gptp_docs.py` | 0 each | the pinned Markdown environment |
| `check_baremetal_only.py --check` | 0 | system interpreter; the first attempt under the Markdown environment refused, rc 2 ("pyyaml is unavailable"), retained as `check_baremetal_only.mdvenv-refused.*` |
| `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `--selftest` (105/105) | 0 each | |

Not rerun, because nothing they read changed (RTL byte-equal, no other harness touched): the other ten default-sweep suites, the physical gPTP leg, `lint_rtl.py`, `xvlog_gate.py`, Yosys, the builder tests, the area synthesis and the wall-clock replica. Round 1's receipts for them stand, at `4e6b5398` / `2639eecf`. The wall-clock figure is unchanged in kind (the bind leg's work is the same; only a classification constant moved).

**The tree afterwards.** `git status --short --ignored` is empty in the superproject and every initialised submodule: the in-tree `follow_ring` build directories and one `scripts/__pycache__` were removed with `git clean -fdX` on those paths.

### R2.6 Packet additions

| Path | What |
|---|---|
| `r2/b17_bound.py`, `r2/b17_bound.txt` | The window's derivation from `cNN.json` |
| `r2/grid_summary.py`, `r2/summary-*.txt` | Per-grid summaries: window classes, `SLIP_LB`, slip timing |
| `r2/base_on_head_window.py`, `r2/window-dense.txt` | Dev's datapath on the head's in-window binds |
| `r2/early_slips.py`, `r2/early-{16,32,dense}.txt` | Every early slip, head against dev |
| `r2/campaign/{fix16,base16,fix32,base32,fixdense,basedense}/` | Every run's command, log, rc and the driver's `bind.md`; `<grid>.driver.log` and `<grid>.rc` beside (`fix16.rc` reads `rc=0`, the others the bare code; head grids `fix32` and `fixdense` exit 1 on the in-window dup, the base grids 1 on the reproduction) |
| `r2/campaign/dev_milan_datapath.sha256` | Dev `f6260253`'s `milan_datapath.sv`, extracted with `git show`, its SHA-256 and size |
| `r2/suites/` | The default and mutants logs, rc, wall seconds, tally and verdicts; both build logs |
| `r2/gates/` | Every gate's log and rc |
| `r2/scripts/launch.sh`, `suite.sh` | The scratch launchers: each campaign and suite ran detached (`setsid`), polled in the foreground, because one exceeds a single foreground command's limit |

The launchers and command files carry this host's scratch paths; redact before publishing the packet.
| `MANIFEST.sha256` | Round 2: SHA-256 of every packet file except itself and the per-grid files; each `r2/campaign/<grid>/MANIFEST.sha256` hashes its grid's files and is itself listed in the top manifest, so every file stays under 200 KB |
