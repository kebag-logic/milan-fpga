# [A432] Round 4 handoff: processor #131 / PR #132

Status: **all four round-4 items done in the assigned order; no STOP** (item 1 needed no
port change). Head `84572585ea76214c9f15f199590b8fc91f8c7edc` on branch
`131-d3-core-scalars` (round-3 head `cbbb5acc`, base `c951a9ff`). Not pushed; the PR is not
edited (PR-BODY.md carries a Round 4 section). Items 1, 2 and 4 are one commit each; item 3
is the PR body only, as R390-3 F3 states.

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5880658258 ·
TAKEN https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5880668649 ·
REVIEW READY https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5882491224 ·
reviews R390-3 (PR #132, 5880652244) and R391-3 (5880412380) · bank note 5880274287 ·
parent #70 scope record 5880276193.

## Commits (one-line subjects, assigned order)

| Item | Commit | Subject |
|---|---|---|
| 1 R390-3 F1 | `014e679` | Drain a READ abandoned in the arbiter's issue cycle for either manager: an abort presented with its strobe arms the drain there, graded by D3R18 and N10 |
| 2 R390-3 F2 + R391-3 F2 | `8610ab3` | Grade every pre-proof variant of the aggregate: the image proven by the writer's LOCATE after the bound or around it, a proof on the bound's own clock, a binding byte in hand at the expiry |
| 3 R390-3 F3 = R391-3 F1 | (PR body) | the consolidated parent-visible list, PR-BODY.md "Round 4" |
| 4 R391-3 S1-S3 | `8457258` | State the firmware's restore wait as 1,000 ms plus two per-wait deadlines plus a few clocks, the terminal tables' two wording points, and the binding manager's clock derivation for direct instantiators |

`cbbb5ac..8457258`: 16 files, +672 / -46. Line numbers below are at `8457258`. Each commit was
validated before it was made: for items 1 and 2 the full `tb/pp_top` (both builds),
`tb/acmp_nvm`, the documentation checks and the full D3 campaign, whose counts fill the
README column; item 1 also `make check` and Yosys on a clone; item 4 lint and the
documentation checks. The complete gates ran once, at the head.

## Items: change and proof

**1. An abort presented in the arbiter's issue cycle (R390-3 F1).**
- The defect: the binding walk's READ strobe `nvm_req_o` is registered
  (`hdl/acmp/KL_acmp_nvm_shadow.sv:762`), so it is out in the walk's first `H_RS_STREAM`
  clock, which never has a byte in hand; when `rs_agg_i` first reads 1 there, `rs_tmo_w`
  (`:566`) raises `nvm_abort_o` (`:576`) in the very cycle the arbiter issues the READ,
  while `own_r` is still `O_NONE`. The head's arbiter armed the drain only for an owned
  READ, so the abort was lost and the port waited in `S_RHFWD` for ever.
- The fix, in the arbiter only (`hdl/packet_engine/KL_pp_nvm_mgr_arb.sv`): `arm0_w`
  (`:157`) and `arm1_w` (`:159`) also arm the drain on `iss0_w && !m0_we_i && m0_abort_i`
  and `iss1_w && !m1_we_i && m1_abort_i`; `drain_ff` (`:167`). Banner paragraph "THE ISSUE
  CYCLE TOO" (`:56`); the two abort port comments (`:87`, `:103`) say "the READ it owns or
  strobes now". **No port change**, so the STOP condition does not apply.
- Manager 1 (the D3 writer) **cannot** present an abort with its own strobe:
  `m_req_o = done_r ? (ss_r == S_REQ) : (ws_r == W_RQ)` (`hdl/aecp/KL_aecp_nvm_writer.sv:1089`)
  and `m_abort_o = expire_w && (ws_r == W_RD)` (`:1095`). Before the terminal the two need
  different states; after it `ws_r` is `W_DONE` (every `done_r <= 1` goes with
  `ws_r <= W_DONE`, and `W_DONE` has no exit), so `m_abort_o` is 0 whenever the service
  requests. A timed-out `W_RQ` wait is by definition an ungranted one (`stall_w = !m_gnt_i`),
  so nothing is issued there. The arbiter covers manager 1 anyway (`arm1_w`), and
  `tb/acmp_nvm` **N10** (`tb/acmp_nvm/sim_main.cpp:2513`) drives manager 1 through the
  case: a READ presented with its abort (`:634`), then no byte accepted. The drain reads 1
  from the clock after the issue, moves the read's bytes, ends with it, nothing reaches
  manager 1, and the port then serves the walk and manager 1's next READ.
- Named cycle-exact check **D3R18** (`tb/pp_top/d3_phases.hpp:2084`): every binding and
  record saved, headers at once, each payload byte 12,350 clocks apart, and the fourth
  record's payload done held (`nv_rd_done_at`, `tb/pp_top/sim_main.cpp:747`, `:1532`) to
  the clock computed from the done-to-strobe lag measured in the same boot (4 clocks), so
  the fifth strobe lands on `agg_o`'s first clock. Graded: that clock carries the strobe,
  the abort and owner 0 (taps `dbg_bind_req_o`, `dbg_bind_abort_o`, `dbg_nvm_own_o`,
  `dbg_nvm_busy_o`, `tb/pp_top/pp_top_wrap.sv:398-401`, `:730-733`); the drain from the
  next clock with owner 1; the walk failed whole (cause 3) and DEFAULTS (cause 3); then,
  the device fast, the port idle (drain 0, busy 0, owner 0), a later SET persisting (1
  WRITE of 0x50, byte-exact), the port busy 26 of 100,000 clocks, nothing unflushed.
- Under the head's arbiter (`drain_misses_issue_cycle`): D3R18 "drained from the next
  clock (0, owner 1)" and "port idle (0) ... 0 WRITEs, the port busy 100000 of 100000
  clocks, unflushed 1" fail; N10 (`drain_misses_issue_cycle_m1`) "draining from -1, moved
  0 bytes" and "the walk is not done, or failed" fail.
- Comments and docs: `KL_acmp_nvm_shadow.sv:161-166` (`rs_agg_i`: the first waiting clock
  may be the issue clock, which the arbiter drains), `:553-558` (the deadline paragraph);
  `docs/architecture/07_memory_maps.md:615` (the binding-walk table's aggregate row);
  `docs/architecture/02_interfaces.md:596` (8.2's drain row); 09 section 8.2 row.
- R390-3's own E1 probe (`run_probe_r3.sh`), unmodified, at `8457258`
  (`receipts/probe-e1e2-at-8457258.txt`): ALIGNED on clock 1,000,000; afterwards
  "27 of 100000 cycles with the port not idle, 2 device ops, 1 WRITEs of 0x50, record
  persisted 1, d3_unflushed 0, owner 0, port state 0"; the one-clock-before and after arms
  the same. (At `cbbb5acc` the aligned arm showed the port never idle and 0 WRITEs.)

**2. Every pre-proof variant (R390-3 F2, R391-3 F2).** Harness: `pre_proof_power_up`
(`d3_phases.hpp:2182`, late image = none at reset, loaded before `PP_CTRL[1]`),
`pre_proof_boot` (`:2222`, the binding walk's last done placed from the bound),
`proof_lags` (`:2267`, the done-to-proof lags from two short fast boots: W_IMG and the
late image's LOCATE, 542 clocks), the byte-placement knob `nv_byte_at`
(`sim_main.cpp:750`, `:1517`), taps `dbg_bind_rvalid_o`, `dbg_d3_proof_o`
(`pp_top_wrap.sv:405-406`, `:734-735`). Values at the head (`receipts/d3r18-d3r21-values-8457258.txt`):
- **D3R19 past the bound** (`:2321`): D3R14's per-byte device, image late; the binding
  walk fails whole at the bound, the release 3 clocks later, the LOCATE proves the image
  542 clocks after it: DEFAULTS, cause 3, **546 clocks after the bound**, image valid,
  AECP released, 0 D3 record READs.
- **D3R19 inside the LOCATE**: the LOCATE starts 271 clocks before the bound and proves
  the image 271 after it: DEFAULTS, cause 3, 272 clocks after the bound, 0 READs.
- **D3R20 W_IMG** (`:2385`) and **W_IMGLOC**: the proof on exactly the bound's clock (image
  valid at the start, resp. loaded late with the LOCATE's answer in hand): DEFAULTS one
  clock after the bound, 0 record READs.
- **D3R21** (`:2414`): a payload byte placed at the device one clock before the bound (lag
  1) is in the binding manager's hand on the bound's clock and none on the next: cause 3
  registered two clocks after the bound (the walk failed on its next waiting clock),
  DEFAULTS 5 clocks after the bound.
- Every premise is graded by its own check. Mutants (`tb/pp_top/d3_mutants.py:356-383`), each
  KILLED from the tree by its named checks; see the table below. R391-3's
  `bind_agg_ignores_byte_in_hand` stays equivalent in effect, as that reviewer judged.

**3. The parent-visible list (R390-3 F3 = R391-3 F1).** PR-BODY.md "Round 4" consolidates
rounds 1-4 and states the measured attribution; the scratch parent demonstration is under
Suites and gates. Found this round and added to the list, each measured and applied in
scratch by [parent_edits.py](parent_edits.py):
- the `pp_shadow` phases K, K10, K12 (no walk before the enable), M2 (no walk after the memory
  handover) and P3 (blank with fail). The sim runs only once the round-1 ports are connected;
  without the edits these phases fail 80 of 590 checks per build;
- the `milan_dp` pool legs, which run only once `gmstep`/`gptp` pass. The image-less legs
  (main, nolpf, ax1x1, aclk) must accept the CLOSED terminal. The `sim_nxn.cpp` legs (notify,
  nxn, nxndv, nxn8, nxn4c) served AECP with no image, and they must start the walk once the
  descriptor memory answers. Without the edits notify fails 210 of 310, and the four nxn legs
  fail hundreds of checks and crash (rc 139);
- the `milan_dp_render` T8 REMOVE phase sensitivity (+272 axis cycles from the D3 walk);
- `cosim_top.sv`'s `RS_TMO_CYC_P` floor against the top's ceil.

**4. Suggestions (R391-3 S1-S3).** S1: `docs/guides/integrator.md:434-441` (1,000 ms plus
two per-wait deadlines plus a few clocks; 1,060 ms a stated margin; the wait decides
nothing), and the same bound stated in 07 `:656-659`, 08 `:45` and the writer banner
(`KL_aecp_nvm_writer.sv:78-82`). S2: the `NVM_RS_AGG_CYC_P` row (`integrator.md:91`) and
07's new row for the image proof's own per-wait deadline (`:669`), with the
misconfiguration-only CLOSED in `integrator.md:412` and `operator.md:255`. S3: the banner
paragraph "A DIRECT INSTANTIATOR DERIVES ITS CLOCK" (`KL_acmp_nvm_shadow.sv:38`) and the
`RETRY_BACKOFF_CYC_P` comment (`:146`); comment only.

## Section 15.2 table and sweep

All 37 rows remain applied. [TABLE-15.2.md](TABLE-15.2.md) adds a round-4 column: 11 rows
updated (07 5.3, 02 8.2, 08, 09, the integrator guide's sections 2 and 9, the operator
guide, the binding manager, the arbiter banner, the acmp_nvm and pp_top READMEs), 26
unchanged. Named sweep at the head (the round-1 `sweep_reconcile.py`, unchanged):
**703 matching lines, 356 rewritten or added by this lane, 347 with a location-specific
scope reason, 0 unreviewed** ([SWEEP.md](SWEEP.md)). `check-integrator-params.py` 26 = 26 = 26.

## Negative controls

[MUTANTS.md](MUTANTS.md) lists all 76 with suite, named assertions, failing-check count, first
failing message and the README equality. The round-4 additions:

| Control | Mutant | Named assertion(s) that fail | Failing checks |
|---|---|---|---:|
| the head's arbiter, binding walk (R390-3 F1) | `drain_misses_issue_cycle` | `D3R18: the READ abandoned in its issue cycle`, `D3R18: once the device ends` | 2 |
| the head's arbiter, manager 1 (R390-3 F1) | `drain_misses_issue_cycle_m1` | `N10 a manager-1 READ abandoned in its issue cycle` | 2 |
| the aggregate aborts in the proof's LOCATE (R390-3's edit) | `agg_closes_during_proof` | `D3R19 inside the LOCATE: DEFAULTS` | 2 |
| the proof keyed on the fired level (R390-3's edit) | `proof_past_needs_fire` | `D3R20 W_IMG: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 2 |
| the proof's DEFAULTS only from W_IMG (R391-3's edit) | `proof_default_only_from_img` | `D3R19 past the bound: DEFAULTS`, `D3R19 inside the LOCATE: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 3 |
| `agg_past_w` the fired level (R391-3's edit) | `proof_past_bound_needs_fired` | `D3R20 W_IMG: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 2 |
| `agg_o` a one-clock pulse (R391-3's edit) | `agg_o_pulse` | `D3R21: the binding walk fails whole` | 3 |

The 69 earlier controls keep their named assertions; 9 of them now also fail one or more of
the new checks, and their README counts are updated: `TRG_ptof`, `quarantine_released_by_time`,
`done_without_d3`, `no_aggregate_deadline`, `aggregate_mirrored`, `aggregate_from_the_walk`,
`agg_closes_before_proof`, `binding_walk_ignores_aggregate`, `proof_reads_records_past_bound`.

Reviewer scripts at the head (receipts):
- R390-3 `r390_3_mutants.py` (HEAD constant set to the round-4 head in a scratch copy;
  `receipts/r390-3-mutants-at-8610ab3.txt`): 16 KILLED on the D3 section, among them both
  round-3 survivors (`agg_closes_during_proof`: 2 checks; `proof_past_needs_fire`: 2);
  `hold_after_release` passes the D3 section (the full suite killed it in rounds 2-3; not
  rerun this round) and
  `held_gate_ignores_da` has no effect, both as R390-2 judged.
- R391-3 `run_r391_3.sh ... d3 <mutant>` for all 20 (`receipts/r391-3-d3-at-8610ab3.txt`):
  19 fail the D3 section, among them all three F2 survivors (`agg_o_pulse` 3,
  `proof_past_bound_needs_fired` 2, `proof_default_only_from_img` 3);
  `bind_agg_ignores_byte_in_hand` 0, equivalent in effect as that reviewer judged.
- R391-3 D1 at the head (`receipts/r391-3-d1-at-8457258.txt`): the five arms equal the
  reviewer's golden (+4, +545, +44, +4,105, +545).
- R390-3 E1/E2 at the head (`receipts/probe-e1e2-at-8457258.txt`): above; E2 at +271, 0 and
  -1 equals the reviewer's head readings.

## DR3a measurements (ratified values, enforced)

`./obj_dir/Vpp_top_sim --dr3a` at the head ([receipts/dr3a-8457258.txt](receipts/dr3a-8457258.txt)):
identical to round 3 on every path. clk_i cycles from `restore_go_i`; the wrap's clock is
nominally 1,000,001 Hz, so RS_TMO = 20,001 and AGG = 1,000,001 clocks; 50 MHz = 20 ns a
cycle, 100 MHz = 10 ns.

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
| every grant 200 inside the per-wait deadline | DEFAULTS (3) | 158,530 | 1,000,000 (= AGG) | 1,000 ms | 1,000 ms |
| every READ byte just inside the per-wait deadline | DEFAULTS (3) | 1,000,002 | 1,000,004 (AGG + 4) | 1,000 ms + 80 ns | 1,000 ms + 40 ns |

Round-4 paths, from the graded checks (clocks after the bound's own clock):

| Path | Terminal | after the bound | 50 MHz | 100 MHz |
|---|---|---:|---:|---:|
| D3R18: a binding READ abandoned in its issue clock, drained | DEFAULTS (3) | 4 (probe E1: done at c 1,000,004, `agg_o` at 1,000,000) | 80 ns | 40 ns |
| D3R19: late image proven by the LOCATE after the bound | DEFAULTS (3) | 546 | 10.9 µs | 5.5 µs |
| D3R19: the bound inside that LOCATE | DEFAULTS (3) | 272 | 5.4 µs | 2.7 µs |
| D3R20: the proof on the bound's clock (W_IMG, W_IMGLOC) | DEFAULTS (3) | 1 | 20 ns | 10 ns |
| D3R21: a binding byte in hand on the expiry clock | DEFAULTS (3) | 5 | 100 ns | 50 ns |

Longest waits unchanged: healthy D3 405/853 cycles (DRAM 31/143), binding 12; DR2a producer
share 50,028 bench cycles = the 500-tick window + 28. The terminal follows the bound within one
per-wait deadline plus a few clocks, or two after a roll-back (the integrator's wait:
1,000 ms plus two per-wait deadlines plus a few clocks; 1,060 ms a margin).

## DR4 scalar-stage contribution

Vivado 2026.1 out-of-context synthesis, the head's `syn/ooc/protocol_processor_ooc.tcl` over
three source trees (`git archive`), part `xc7a100tfgg484-2`, 10 ns constraint, all six runs
in this session on one instrument. This session reproduces round 3's absolute totals for
base and the round-3 head exactly.

| Shape | Base `c951a9f` LUT / FF / BRAM / DSP | Round 3 `cbbb5ac` | Head `8457258` | Lane 1 (head - base) | Round-4 increment | Writer `u_d3` LUT / FF | Binding `u_nvm_shadow` LUT / FF |
|---|---|---|---|---|---|---|---|
| 1x1 (shipping) | 21,675 / 23,710 / 16.5 / 4 | 22,705 / 24,269 | 22,706 / 24,269 | **+1,031 LUT / +559 FF / 0 BRAM / 0 DSP** | +1 / 0 | 790 / 479 | 689 / 1,268 |
| 8x8 (diagnostic) | 29,059 / 31,164 / 24 / 4 | 30,126 / 31,749 | 29,901 / 31,666 | +842 / +502 / 0 / 0 | -225 / -83 | 1,153 / 527 (was 1,144 / 527) | 791 / 1,004 (was 794 / 1,004) |

The arbiter is flattened into the top (no hierarchy row); its drain term is the +1 LUT. The 8x8
increment is synthesis variation outside the two changed modules (+9 / -3 LUT in them), as
R391-3 noted for earlier rounds; WNS at 8x8 -7.886 / -9.080 / -8.483 ns (base / round 3 / head).
Against the ruled scalar-core ceiling for lanes 1-2 (2,500 LUT / 1,400 FF / 0 BRAM / 0 DSP),
lane 1 uses 1,031 / 559 at 1x1, leaving 1,469 / 841 for lane 2. Synthesis WNS at 10 ns:
-5.970 / -5.165 / -5.165 ns (1x1 base / round 3 / head), synthesis estimates only.
Post-place and the 8x8 post-place obligation stay lane 2's (open, not waived).

## Parent-visible changes (for the pin-adoption lane)

The consolidated list is PR-BODY.md "Round 4"; the round-4 changes themselves are:
- **No top port or parameter** is added, removed or resized; no internal port changes.
- **Behaviour:** the arbiter drains a READ abandoned in its issue cycle (either manager).
  `nvm_cosim` instantiates `KL_pp_nvm_mgr_arb` directly with manager 1 tied off, so it sees
  no difference.
- **Documentation:** the firmware's bounded wait is 1,000 ms plus two per-wait deadlines
  plus a few clocks (1,060 ms a margin; the parent's `MILAN_NVM_RESTORE_TIMEOUT_MS` = 3,000
  covers it); the third, misconfiguration-only CLOSED; a direct instantiator of
  `KL_acmp_nvm_shadow` derives its two clock-referenced parameters.
- **Found this round in the parent (introduced by rounds 1-3's ruled behaviour, not by round
  4):** the `pp_shadow` K/M2/P3 phases, the `milan_dp` pool legs (image before `PP_CTRL[1]`;
  CLOSED for image-less benches), the `milan_dp_render` T8 phase sensitivity, and
  `cosim_top.sv`'s `RS_TMO_CYC_P` floor. Applied by `parent_edits.py` in scratch, they make
  the consumer set 15 of 15 rc 0.

## Suites and gates

[GATES.md](GATES.md) has every command with rc, seconds, log size and SHA-256, run by
[gates.py](gates.py) with the pinned Verilator 5.050 wrapper.

| Tree | Entry point | rc |
|---|---|---:|
| processor | `./scripts/run_suites.sh` (33 suites, 1,016,031 checks, 0 failing; pp_top 7,888, acmp_nvm 355) | 0 |
| processor | `./scripts/lint_hdl.sh` | 0 |
| processor | `make check` (lint, WaveDrom, links 968, matrices, params 26/26/26, stale) | 0 |
| processor | `python3 scripts/gen_matrix.py --check` | 0 |
| processor | `./syn/yosys/run.sh` | 0 |
| processor | `make -C tb/nvm_port figures` (PR #13 history fetched read-only first) | 0 |
| processor | `python3 tb/pp_top/d3_mutants.py` (76 of 76 KILLED, goldens PASS) | 0 |
| processor | `make -C tb/srp_top mutants` (64 checks, coverage 49/49) | 0 |

Parent consumer set (the manager's 15 commands, scratch parents at dev `b5c0f69d`, gitlink at
`8457258`):

| Command | gitlink only | declared edits applied |
|---|---:|---:|
| `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | 0, 0 |
| `xvlog_gate.py --check` (4 == ratchet) | 0 | 0 |
| `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 0, 0 |
| `sw/builder/test_builder.py` | 0 | 0 |
| `make -C tb/verilator/pp_shadow -j8` | **2** (20 PINMISSING) | 0 (4 builds, 0 failures) |
| `check_port_contracts.py` (processor 111 <= 111) | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 |
| `measure_test_evidence.py --check` | **1** (`d3_mutants.py`) | 0 |
| `docs_check.py` | 0 | 0 |
| `make -C tb/verilator/nvm_cosim lint` | 0 (2 PINMISSING) | 0 (0 PINMISSING) |
| `make -C tb/verilator/nvm_cosim quick` | **2** (308/315) | 0 (315/315) |
| `make -C tb/verilator/milan_dp -j8` | **2** (gmstep, gptp, gptp-lat; the pool never ran) | 0 (every leg and both mutation campaigns) |
| `make -C tb/verilator/milan_dp_render -j8` | **2** (T8 REMOVE, 2/151) | 0 (65/65, 152/152) |

**The declared list is sufficient, but only with the items this round adds.** Starting the
restore walk in `gmstep`, `gptp` and `gptp-lat` (the manager's list) does not make `milan_dp`
green. It lets `make` reach the pool legs for the first time, and five `sim_nxn.cpp` legs
and four image-less legs then fail on the ruled image-before-restore order. The
`pp_shadow` sim runs for the first time once the round-1 ports are connected, and its K, M2
and P3 phases fail. The render bench's T8 fails on a phase shift. Every one of these is a
parent test-harness change, applied by `parent_edits.py` and listed in PR-BODY.md. None is
a processor change.

`git status` of the lane is empty; the processor clone was clean after the gates.

## Notes for review

1. The render bench's T8 failure is not a processor defect: with the processor at
   `c951a9ff` and at the head the REMOVE's answer takes 370 axis cycles and the collection
   opens 639 after it in both; only the leg's arrival at T8 moves (+272 axis cycles, the D3
   walk in the boot restore the harness waits for). A frame committed before the removal
   reaches the pins up to one commit-to-pin bound later (T7 measures 30..2,113 axis
   cycles), so a collection opened 639 cycles after the removal can meet it. The fix is the
   harness's; measured with a debug copy (T8 239 frames, 238 silent at the head, 239 at
   base; 239 with the wait).
2. `cosim_top.sv`'s `RS_TMO_CYC_P (CLK_HZ_P / 32'd50)` is the floor the top used before
   round 2; the top derives the ceil. At the suite's 1 MHz both give 20,000, so no check moves;
   the list names it so the comment "derived the way it derives it" stays true.
3. The firmware persistence-disabled boot path (5880276193 item 2) is declared and not
   applied in the scratch demonstration: no consumer-set gate exercises it.
4. The assignment expected `milan_dp` green "once the harnesses start the restore walk".
   That premise held only for `gmstep`, `gptp` and `gptp-lat`. The manager's bank saw
   those three because `make` stops at the first failing target. The pool legs behind them
   need the image-before-restore order the contract states (§8.1; round 1's declared
   firmware obligation), which the `sim_nxn.cpp` legs did not follow. The edits are
   test-harness only, and the list names them; they are the pin-adoption lane's to make
   for real.
5. R390-3 S2 (a bound inside a healthy re-LOCATE ends CLOSED) was addressed to the manager
   and not assigned; the reading of round 3 stands and D3R15 pins it.

## Packet

HANDOFF.md, PR-BODY.md (Round 4 section), TABLE-15.2.md, SWEEP.md with `sweep_reconcile.py`,
MUTANTS.md with `mutants_table.py`, GATES.md with `gates.py` and `gates_table.py`,
`parent_edits.py` (the declared parent edits, applied to scratch parents only), and
`receipts/`:
- `parent-edits.diff` (the 12-file diff that script makes at dev `b5c0f69d`);
- the gate results (`gates-processor-results.jsonl`, `gates-parent-gitlink-only-results.jsonl`,
  `gates-parent-declared-edits-results.jsonl`) and `d3_mutants-results-8457258.json`;
- the reviewer reruns (`r390-3-mutants-at-8610ab3.txt`, `r391-3-d3-at-8610ab3.txt`,
  `r391-3-d1-at-8457258.txt`, `probe-e1e2-at-8457258.txt`, and `probe-e1e2-fix.txt` from the
  item-1 tree before its commit);
- `dr3a-8457258.txt`, `d3r18-d3r21-values-8457258.txt`, and the two `nvm_cosim` attribution
  variants.

Logs, synthesis reports, debug copies and scratch trees stay under `$VALIDATION_STORAGE/a432` (not
copied; log sizes and hashes in GATES.md). No file in the packet exceeds 200 KB.
