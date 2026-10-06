[A531]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

REVIEW READY under the stage-2e ruling; `645-ring-slip` -> `dev`.
Head `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`.

Public handoff: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6001987003.
This is a prepared body, not a published PR.

The required fa450d30 baseline misses the +0.030 ns setup-margin bar on
AltSpreadLogic_high. The stage-2e ruling permits review readiness on that
condition. Current-head functional, parser and own-area acceptance is complete,
and all fresh timing reports have been inspected.
Timing failures remain failed grades; the threshold is unchanged.

## Linked Issue / roles

Closes #645
Closes #647
Relates to #657

The closure lines cover implementation; bench items remain with the manager.
Executor: [A531]
Internal cleared-context reviewer: [R474]
External reviewer: [R475]

## Description

Frequency pull-in can leave the listener ring near an edge, causing a later
slip after lock. An INTERNAL aligner pull-in can also leave a running render
stream with a persistent latency displacement. The existing at-switch render
recentre remains, and a later settle action recentres both rings. Loopback
depth is sixteen, with the class-A PDU-end target of eleven events. The declared
action holds at most five pops or drops one oldest event, without incrementing
slip counters; the AAF presentation law remains unchanged.

The physical checker grades the independently derived exact step in the declared
output PDU. Controls inject an undeclared repeat and a larger-than-declared step.
Startup/reset bounds and steady-state coverage are documented. Stage 2e corrects
the stale depth summary after exact mutation-context searches and successful
planting of all 25 arms. The required no-fast-forward dev merge at 510fae60
adopts processor pin ead80360; affected full-system acceptance is rerun.

## Authoritative references

- [Stage-2e ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994641859)
- [Stage-2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410)
- [Queue/envelope ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987852678)
- [Own-area and #657 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985974804)
- [Option C ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394)
- REQUIREMENTS.md; docs/design/MEDIA_CLOCK_FOLLOWING.md;
  docs/design/TIME_SYNC.md; docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md.

## How to get into the same state

```sh
git switch 645-ring-slip
git rev-parse HEAD
git log -3 --format='%H %P %s'
```

Expected head 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f, descending from the
required clean merges of dev 510fae60b26bef1db138de5cf2ac72b17b5011a5
and documentation-only 28f9666feab2b2ba287643c63ed3a16b1e0bb863.
Processor pin ead8036035affd53ef4b29979190f2f4f67084c0. Before further Git
commands inside any submodule, verify its top-level directory. Use the pinned
simulator, verified SDK and shipping build dependencies. HANDOFF.md records
exact source binding, dependency pins and artifact receipts.

## How to validate

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

Timing comparison and current-head measurements:

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


Completed functional evidence:

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

Expected result: functional and source gates return 0; both planted ordering
controls are caught; post-settle slips are zero with margins above one tick;
own area is at most 120 LUT / 120 FF. Timing grades keep WNS >= +0.030 ns and
WHS >= 0 at both fixed corners. A baseline margin miss is disposed by the
stage-2e ruling, not changed into a timing pass. Current-head functional, parser
and own-area acceptance is complete.

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


## Known limitations / out of scope

- Late-arrival campaigns grade slips/margins. Ungradable render windows earn no law evidence.
- Four historical full render-mutation failures remain assigned to #657.
- Bench, physical compliance, external I/O timing and release-bitstream acceptance are not established here.
- No unrelated processor logic change is made by the author; upstream changes arrive through the required merge.
- No independent review, hosted gate, merge-result validation or containment is claimed.
- No push or PR publication was performed.

The stage-2e author acceptance is complete under the explicit rulings. The
unchecked items below remain the full Issue/PR merge bar, including bench work,
review and hosted evidence; this preparation does not claim that bar is closed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
