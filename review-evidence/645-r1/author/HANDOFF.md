[A531]

# Stage 2e handoff

Status: **REVIEW READY under the stage-2e ruling**.
Head `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`, branch `645-ring-slip`.

Public handoff: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6001987003.

The [stage-2e ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994641859)
requires the three-directive measurement at dev `fa450d30`, the stale-depth
comment correction with mutation planting, and another dev merge if it moved.
The baseline misses the +0.030 ns setup-margin requirement on AltSpreadLogic_high.
That satisfies the ruling's timing condition for REVIEW READY. Current-head
functional, parser and own-area acceptance is complete, and all fresh timing
reports have been inspected. Failed margin grades remain failed; no threshold
was weakened.

Takeover: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994663339.
Executor [A531]; internal reviewer [R474]; external reviewer [R475]. No push,
PR publication, hardware operation or merge into dev was performed.

## Branch and source binding

Recorded scratch roots are `$VALIDATION_STORAGE/645-a531-s2e-work` for the
fa450d30 baseline and its `merged/` subdirectory for the current candidate.
`$WORK` in current receipts denotes that `merged/` directory. Generated
products and oversized originals live there, outside the evidence directory.
The completed measurement runner is `merged/run_measurements.py`; its exact
sequence is recorded in `measurement-driver.log`, per-step logs and `.rc` files.
The aggregate measurement and functional return codes are both zero. These
paths locate the recorded run, while the reproduction recipe permits a new
external scratch location. Timing margin grades are separate and retain the
recorded failures.

Origin is `https://github.com/kebag-logic/milan-fpga.git`. Resume head was
`b2c81239f686592b224510c9d4f196a6c7aa7f25`. Stage 2e adds:

- `e80dd7ad43574b109b51d4f586efad776d547553`: `Correct loopback queue depth in capture summary`.
  The sole edit says sixteen instead of eight at `KL_chan_map_capture.sv:360`.
- `f325c3ab4a9faa0e2b7784e796728ebe6acf3fd3`: `Merge dev 510fae60 into ring-slip lane`.
  Required clean no-fast-forward merge, parents e80dd7ad and
  `510fae60b26bef1db138de5cf2ac72b17b5011a5`.

- `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`: `Merge dev 28f9666f into ring-slip lane`.
  Required clean no-fast-forward merge after dev advanced again. It extends only
  `docs/findings/653_DISCONNECT_ORDER_BENCH.md`; no executable input changes.
  The 132 export inputs and all OOC source bytes match their preceding receipts.
  Current simulations remain bound through the explicit documentation-merge proof.

All three subjects are one line, without body or trailers; no rebase or amendment.
No author logic, port, register-map or parameter edit is made in this stage.
The explicit dev merge imports the processor adoption and its upstream changes.
Processor pin is now `ead8036035affd53ef4b29979190f2f4f67084c0`;
gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; AXIS
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
Submodule top-level directories were verified before further Git commands inside them.

Before the correction, exact old-line searches covered every tracked
`tb/**/*.patch` and the mutation tables. No context dependency was found;
there are no tracked patch files in that set. All five follow-ring and twenty
capture-coherence arms plant after the correction, also rechecked after the merge.
Planting is distinct from simulation execution. Current source/documentation
checks are 26/26 at rc 0. See `stage2e/merged/` for current evidence and
`stage2e/source/` for the earlier comment-only checks.

The original assignment, issues #645/#647/#629/#643, PR #648, requirements,
media-clock and time-sync designs, and #629 bench findings were read in full.
Earlier option-C, own-area/#657, depth/envelope and ordering rulings remain in force.
Prior HANDOFF_STAGE1.md through HANDOFF_STAGE2D.md are historical snapshots.

## Timing comparison

Base is measured afresh in the authorized detached scratch worktree at
`fa450d301805881ad713b67521477bf042ddadfd`; the lane checkout was never switched.
All three implementation processes and rejected-constraint checks return 0,
with no critical warnings and all TNS/THS zero. Margin grading remains separate:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Margin grade |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.244 / +0.102 | +1.638 / +0.036 | PASS (0) |
| AltSpreadLogic_high | +0.026 / +0.049 | +1.478 / +0.014 | FAIL (1) |
| ExtraTimingOpt | +0.056 / +0.049 | +1.478 / +0.017 | PASS (0) |

The premerge candidate table below comes from completed stage-2d reports at
b2c81239 and applies to the comment-only e80dd7ad inputs. It is historical
at the merged head, whose changed processor inputs require fresh implementation:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Margin grade |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.120 / +0.053 | +1.633 / +0.019 | PASS (0) |
| AltSpreadLogic_high | +0.142 / +0.065 | +1.483 / +0.026 | PASS (0) |
| ExtraTimingOpt | +0.001 / +0.001 | +1.476 / +0.012 | FAIL (1) |

Fresh current-head table:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Margin grade |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.151 / +0.099 | +1.552 / +0.036 | PASS (0) |
| AltSpreadLogic_high | +0.101 / +0.097 | +1.385 / +0.033 | PASS (0) |
| ExtraTimingOpt | -0.209 / +0.062 | +1.420 / +0.030 | FAIL (1); stage-2e disposition |

All three fresh implementation processes and constraint checks return 0, with
the full critical-warning census retained. Detailed worst-five extracts and timing grades are
retained for every directive.

The base's failing path is SDRAM zqcs_timer_count1_reg[26] to
bankmachine0_level_reg[1], 16 levels and 9.699 ns. The former candidate minimum
is the processor receive-validator hdr_src_mac_r_reg[0] to transmit-arbiter
FSM, 39 levels and 19.728 ns. These are different cones. The ruling accepts a
base miss on any directive; the measurements do not establish the same failing
processor path at base. Both original worst-five path extracts are retained.

The fresh ExtraTimingOpt result has Slow TNS -0.294 ns at two failing setup
endpoints, THS zero, and Fast TNS/THS zero. All other current TNS/THS
entries are zero as well. Its implementation and rejected-
constraint check return 0, while its margin grade remains 1. The critical-warning
census contains one `Route 35-39` timing diagnostic; the first two directives
have none. Current worst-five extracts are retained for all three directives.
The baseline-miss disposition permits review readiness; this is not timing
closure or proof that the same path failed at the requested baseline.

The current minimum is the notification write-index register to the transmit
arbiter slot register, 42 logic levels and 20.130 ns data-path delay. It differs
from both the requested baseline minimum and the former candidate minimum.
For the manager-owned timing follow-up, the current worst five are below;
paths are relative to `milan_datapath/pp_shadow/u_pp/`.

| Source | Destination | Slack (ns) | Levels | Data delay (ns) |
|---|---|---:|---:|---:|
| `u_notify/wr_ix_r_reg[0]_replica_4/C` | `u_tx_arbiter/slot_r_reg[0]/D` | -0.209 | 42 | 20.130 |
| `u_notify/wr_ix_r_reg[0]_replica_4/C` | `u_tx_arbiter/slot_r_reg[1]/D` | -0.085 | 42 | 20.005 |
| `u_notify/wr_ix_r_reg[0]_replica_4/C` | `u_tx_arbiter/slot_r_reg[2]/D` | +0.073 | 42 | 19.847 |
| `u_notify/wr_ix_r_reg[0]_replica_4/C` | `u_tx_arbiter/owner_r_reg[0]/D` | +0.229 | 41 | 19.627 |
| `u_aecp/u_ucpu/uop_e_r_reg[imm][0]/C` | `u_aecp/u_d3/taint_r_reg/D` | +0.265 | 35 | 19.705 |

All implementations use identical shipping 1x1 arguments, xc7a100t-fgg484-2,
AreaOptimized_high synthesis, ExploreArea optimization, the named placement,
AggressiveExplore physical optimization/routing, 32 threads and default seed.
Each design's alternates reuse its own fresh synthesis checkpoint. Runs are
sequential under the shared lock and do not overlap another heavy build in this
lane. No bitstream is generated. WNS must be >= +0.030 ns and WHS >= 0.
Slow and Fast timing models are each reported at 0 and 85 C power conditions;
those repeated temperatures are not four independent timing models.

`stage2e/TIMING-RECIPE.md` documents the original comparison. `stage2e/merged/`
contains the new source inventory, fresh export and implementation recipe.
The earlier 134-input comparison is premerge evidence only. Large reports and
checkpoints stay outside this directory, with SHA-256 and size receipts.

## Reproduction and classification

The historical diagnosis classifies #645 as a ring location left near an
edge after frequency pull-in, with no later loopback recentre. The servo
locks frequency, not absolute phase. At the measured 5.92 ppm INTERNAL-to-peer
offset, acquisition walks about 1.43 media ticks before LOCKED and 0.03
afterwards. The retained #386 render-only recentre fires about 43 ms after
selection, before that walk. A late packet can therefore cause a ring slip
well after lock. #647 is a separate trigger gap: an INTERNAL aligner pull-in
moves the running render stream without the former source-change arm, so
its render latency remains displaced. This evidence does not support a
persistent frequency mismatch after lock.

The selected implementation retains #386 and adds a later action on both
rings: eight consecutive 512 ms LOCKED windows while following; 2048 in-band
ticks at INTERNAL; a 2^20-tick ceiling; a subsequent excursion beyond four
settle bands rearms it. Loopback depth is sixteen, the class-A PDU-end target
is eleven, and the retained-event target is five. All pairs act together.
Below target the next walks hold the missing number of pops, at most five;
above target one oldest event is dropped. Both slip counters stay unchanged
for this declared action. Startup lock and reset reacquisition include it.
The diagnostic loopback adds three ticks (62.5 us) over target eight; the
AAF presentation path and latency-equals-presentation-offset law are unchanged.

The prior stage's physical trace records the bounded startup action:

```text
TRACE SETTLE t=0.755754160 fill=2 dup=0 skip=0 source=0 err=14
TRACE ORDER t=0.755882000 last=36275 index=36275 step=0 fill=5 dup=0 skip=0
```

The ORDER line occurred four times in one output PDU with unchanged
counters. That run had 139 checks / 2 failures; its separate accounting
controls had 40 / 0. Those are historical diagnosis results, before the
required merge, and do not clear the new checker. Earlier traces and all
historical evidence remain in HANDOFF_STAGE1.md through HANDOFF_STAGE2C.md.


## Fix options and area

The original A/B prototype estimates are vendor OOC synthesis using
Vivado 2026.1, xc7a100tfgg484-2, 20 ns and the shipping 1x1 parameters.
They are area probes, not simulated implementations. Option A's number includes
the meter phase export but excludes an additional 32-bit reference mux.
Original diffs and reports remain in `area/`; the selected C implementation has
separate later evidence and is remeasured below.

| Option | Area evidence at 1x1 | Protocol-visible effect | Validation |
|---|---|---|---|
| A: servo phase feedback | Historical prototype +169 LUT / +129 FF, plus mux | Changes loop dynamics; does not remove accumulated pre-lock phase or restore INTERNAL latency | Offsets, arrival and phase sweeps; zero-gain control; full servo/meter/integration |
| B: aligner-band/excursion recentre | Historical prototype +9 LUT / +1 FF | Bounded render action after INTERNAL pull-in; leaves loopback slip | Both pull-in directions and all phases; remove excursion arming |
| C: later recentre of both rings | Fresh OOC +80 LUT / +73 FF; routed bound 112 LUT / 73 FF | Declared bounded startup/reset/switch action; loopback adds 62.5 us; AAF presentation law unchanged | Four arrival envelopes, INTERNAL phases, five controls, exact physical ordering and two controls, integration, area and timing |
| D: document former behavior | 0 | Leaves untimed slips and persistent render shift | Explicit changed specification and offset/phase sweep; does not fix either issue |

Option C is the ruled implementation. Own-logic limit is 120 LUT / 120 FF.
| Measured scope | Base LUT / FF | Head LUT / FF | Delta LUT / FF |
|---|---:|---:|---:|
| Recentre blocks | 41 / 51 | 67 / 92 | +26 / +41 |
| Complete capture module | 1076 / 1336 | 1130 / 1368 | +54 / +32 |

The conservative routed own-logic bound is **112 LUT / 73 FF**, within the
120/120 limit. The routed count is 80 fan-in LUTs minus one capture LUT
counted in its module delta, six identical direct functions and ten exhaustively
proved shared band functions, plus the capture delta of 49: 112 LUTs. The
41 new settle FFs plus 32 capture FFs total 73. OOC capture retains one
block RAM tile; recentre uses none. The bound excludes only identical
functions with recorded proof. The shared
band proof covers all 65,536 signed-error assignments and catches its planted
control. Whole-design resource movement includes the processor adoption and
is not charged to this lane. Fresh OOC, routed cell lists, proof and return
codes are retained in `stage2e/merged/area-ooc/` and `area-route/`.

All heavy builds completed before vendor implementation. Only existing-binary
boundary simulations overlapped it after their binaries and the remaining
run-only driver path were verified. The completed boundary verdict is zero.
See `render-boundary-builds.json`.

## Current functional acceptance

All refreshed functional commands return 0. The full datapath passes
11,877 checks; render passes 259 shipping and 65 multistream checks plus five
stimulus controls; media-clock passes 55, 32 and 50 positive checks plus 31
control checks; processor integration passes 646, 606, 606 and 311 checks.
Capture-coherence passes 332 datapath, 20,832 core and 30 control checks.
Physical, accounting and ordering controls pass 143 + 40 + 14 = 197 checks.

The eighteen-phase pull-in campaign has zero loopback slips during and after
pull-in. Seventeen phases have gradable render windows; +1042 is explicitly
NOT GRADABLE after settle because a PDU end is four cycles from the boundary.
All eighteen record a new settle 152.625 ms after the hold. No ungradable
window earns render-law evidence.

Boundary passes 81/81 over 564 windows: 123 positive, 246 correctly rejected
control windows and 195 NOT GRADABLE. Its maximum observed walk is three
cycles; the five-cycle allowance and nine-cycle ambiguity remain unchanged.
These counts were read from the fresh completed logs, not transferred from
prior results.

Portability passes 55/55 tops. Builder returns 0 with the required compiler
and elaboration; its historical Arty area-calibration arm remains NOT RUN
because the reference report is absent. Both additional source-list and wire
truth self-tests return 0. All 26 source/documentation gates at the final
documentation merge return 0, with RTL lint 90 within budget 90.
The vendor parser returns 0: 125 files analysed, with two existing processor
diagnostics matching its ratchet and none in hdl/. It reports use before
declaration for `cancel_hit_w` in `KL_pp_originator.sv:194` and `vd_push_w`
in `KL_pp_rx_validator.sv:383`. Parser analysis does not establish elaboration.
Fresh OOC and routed attribution pass the own-area limit; every measurement
process and source-input verification returns 0.

The standalone follow-ring campaigns remain applicable: all twenty declared
inputs are byte-identical to b2c81239 except the normalized depth comment.
The standalone model does not instantiate the protocol processor. See
`stage2e/merged/follow-ring-source-identity.json` for the comparison and
`HANDOFF_STAGE2D.md` for exact commands and prior run receipts.

| Arrival envelope | Runs / decisions | Post-decision slips | Min empty / full margin (ticks) |
|---|---:|---:|---:|
| None | 16 / 48 | 0 | 4.984320 / 5.076480 |
| Uniform 0..5 us | 16 / 48 | 0 | 4.899840 / 4.907520 |
| Uniform 0..2 us, probability 1e-4 of 0..24 us tail | 16 / 48 | 0 | 3.893760 / 5.091840 |
| Uniform 0..60 us | 16 / 48 | 0 | 2.565120 / 2.234880 |
| INTERNAL holds 52 and 56 us | 32 / 32 | 0 | 4.984320 / 5.091840 |

Phases k/16, seeds 645+k, 40 s INTERNAL-to-AAF then 20 s each AAF-to-CRF
and CRF-to-AAF, peer/Internal offsets -11.02/-5.10 ppm, uncompressed 512 ms
windows. All margins exceed one tick. Counters grade from the decision PDU
end without a grace interval. Late-arrival runs establish slips and margins,
not the render law. No-lateness has 45 on-law and three ungradable observations;
INTERNAL has 27 fully gradable pairs, two BEFORE and three AFTER NOT GRADABLE.
Five controls are caught: NO-SETTLE, RENDER-ONLY, EARLY, W1 and OVERSHOOT17.

The physical checker independently derives the declared action from fill,
PDU boundaries, capture walks and packetizer slots, then grades its exact wire
step. Other samples must advance by one. One control inserts an undeclared
repeat outside the declared PDU; the other understates the declared step by
one. All original physical assertions remain. The fresh normal run passes
143 checks with zero failures; accounting passes 40 and the two ordering
controls pass 14. The complete physical suite is 197 checks with zero failures.

## Current physical trace observations

The completed normal leg passes 143 checks, accounting passes 40 and ordering
controls pass 14, all with zero failures and command return code 0. The independent
declaration and observed wire step agree at startup and reset:

```text
RECENTRE decision=1 input_pdu=6047 cycle=37790215 fill=0 step_events=-5 dup=0 skip=0
RECENTRE output=1 input_pdu=6047 output_pdu=6047 step_events=-5 dup=0->0 skip=0->0
RECENTRE WIRE decision=1 output_pdu=6047 declared_step=-5 observed_step=-5 events dup=0 skip=0
RECENTRE decision=2 input_pdu=92221 cycle=576382035 fill=0 step_events=-5 dup=0 skip=0
RECENTRE output=2 input_pdu=92221 output_pdu=92220 step_events=-5 dup=0->0 skip=0->0
RECENTRE WIRE decision=2 output_pdu=92220 declared_step=-5 observed_step=-5 events dup=0 skip=0
```

The run covers 16.992556520 simulated seconds, 849,627,826 axis cycles, in
3768.79 wall-clock seconds. It performs 6,517,344 payload, 814,666 sample-order
and 135,936 packet-sequence comparisons. Both decisions complete; all plan,
span, payload, ordering, sequence and counter error totals are zero.
Licensed ACMP/SRP streaming, physical TDM render, CRF recovery,
multiple-responder cease, PHY/MAC calibration, CPU/DDR and physical compliance
remain NOT RUN. The original first-10-ms warm-up comparison exclusion remains.

## Reproduction commands

Reproduce from the candidate root, using external WORK and the pinned
simulator on PATH, with bytecode generation disabled:

```sh
make -j16 -C tb/verilator/follow_ring build MDIR="$WORK/model" VERILATOR_JOBS=4
python3 -B tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/no-lateness" --jobs 4 --jitter-us 0 --hold-s 40 \
  --switch-hold-s 20 --extra --dwell-s 1.0
python3 -B tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/uniform5" --jobs 4 --jitter-us 5 --hold-s 40 \
  --switch-hold-s 20 --extra --dwell-s 1.0
python3 -B tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/tail" --jobs 4 --jitter-us 2 --tail-us 24 --tail-p 1e-4 \
  --hold-s 40 --switch-hold-s 20 --extra --dwell-s 1.0
python3 -B tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/uniform60" --jobs 4 --jitter-us 60 --hold-s 40 \
  --switch-hold-s 20 --extra --dwell-s 1.0
python3 -B tb/verilator/follow_ring/sweep.py pullin --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/pullin" --jobs 4 --hold-us 52 56
MAKEFLAGS=-j16 VERILATOR_JOBS=4 python3 -B tb/verilator/follow_ring/mutants.py \
  --mdir "$WORK/mutants" --jobs 3
```

Keep independent jobs concurrent, with separate log and rc files and
foreground waits below ten minutes. Build products stay outside the tree
and evidence directory. Do not overlap a vendor run with another heavy build.

With BROAD, PHYSICAL and FOCUSED naming those external staging roots, and the
pinned simulator on PATH:

```sh
make -j16 -C "$BROAD/tb/verilator/milan_dp" VERILATOR_JOBS=2 SIM_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_render" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_mclk" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/pp_shadow" VERILATOR_JOBS=2
make -j16 -C "$PHYSICAL/tb/verilator/milan_dp" ax1x1gptp-build VERILATOR_JOBS=3
(cd "$PHYSICAL/tb/verilator/milan_dp" && ./obj_ax1x1gptp/Vmilan_dp_ax1x1gptp)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_abort.py)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_recentres.py --jobs 2)
make -j16 -C "$FOCUSED/tb/verilator/milan_dp_render" tdm8render-pullin PULLIN_JOBS=8 VERILATOR_JOBS=2
(cd "$FOCUSED/tb/verilator/milan_dp_render" && python3 -B tdm8_render_mutants.py --law-boundary --jobs 4)
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
bash syn/yosys/run.sh
python3 -B scripts/xvlog_gate.py --check
```

The vendor parser, area queries and implementation commands run under
`flock $VIVADO_LOCK`. Exact current launch arguments and return codes
are in `stage2e/merged/recipes/` and `stage2e/merged/integration/`.
Set BROAD, PHYSICAL and FOCUSED to separate external test staging directories;
tracked test files are copied and hash-checked against the candidate, while
source inputs resolve to the candidate. These are not additional Git checkouts.
The pinned simulator is `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`.
Use the verified compiler and shipping build environment.
No gate is piped. Independent jobs have their own log/return-code files and
run concurrently within the 12 GB limit. Waits remain in the foreground and
below ten minutes; do not stop while jobs are running. Keep generated products
outside the repository and evidence directory.

## Run setup and cleanup

The final source check verifies all 132 measured inputs unchanged. The three
run-owned links (`sw/builder/out`, `configs/generated/ltn_rom.hex` and
`configs/generated/ucode.hex`) were removed only after their targets matched
this run. The lane and all three initialized submodules are clean, including
ignored files; the optional external submodule remains uninitialized. The
fa450d30 scratch worktree is also clean. See `final-clean-state.json` and
`final-git-audit.json` under `stage2e/merged/`.

Setup attempts remain visible. The original baseline collector needed the
shipping interpreter rather than the system interpreter; the unchanged
collector then passed. The first fresh export refused generated ROM files left
by the builder; those files and the failure log were preserved externally,
and the unchanged export passed after its output paths were prepared. A
metadata check first expected the documentation merge to add a file, while Git
reported modification of the existing file; it stopped before writing and the
correct exact-file check passed. One source launcher used the wrong evidence
parent directory and stopped before any gate ran; the corrected launch passed
all 26 gates. Its first launcher return code was not captured, so it is not
reported as a successful gate. The corresponding setup receipts and original
logs are retained. No DUT, test or threshold was changed to clear these setup
issues.

The OOC reports estimate area only: their clock source is not bound for timing.
The routed cell queries emit no-input-pin diagnostics for constant primitives;
the equivalence proof handles those constants explicitly and refuses unknown
leaves. All four OOC invocations, both routed queries, the proof including its
planted control, own-area limit and final input verification return 0.

## Recommendation and limits

Retain option C. The measured fa450d30 baseline miss satisfies the stage-2e
timing disposition, without converting a failed grade into a pass. The refreshed
current-head acceptance is complete; hand the committed lane to independent
review with the prepared PR body.
The four historical full render-mutation failures stay with #657; bench items
remain with the manager. The original B8 INTERNAL slips within 1.94 s of
the binds were not reproduced by the clean-start diagnosis model and remain a
bench limitation. Talker-relative presentation-time phase work is not claimed
here; the original option-A assessment assigns it to #632. No independent review, hosted result, hardware release,
merge-result validation or containment is claimed. The prepared PR body is
not a published PR. Do not push.
