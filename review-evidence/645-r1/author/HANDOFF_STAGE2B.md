# #645 / #647 implementation lane (stage 2b): [A531] handoff

Status: **STOP** (see section 8). The second ruling's fixed
8-event loopback target is implemented, tested and documented. One ruled
acceptance does not hold: at 5 us of uniform arrival lateness the loopback
ring drops one event right after the settle recentre at 2 of 16 set phases
(4 of 48 settle recentres). The rare 26 us tail, the pull-ins and every
run without lateness pass.

- Branch: `645-ring-slip`, head `332833afa6cd396b99ac6f0e7ab48757459d0e56`, on stage 2's head
  `ff6b28b0f56656271a61c7b3a075046922441366` (stage 1 `6ca6d668`, dev
  `fea346e76c2a57ed5cd131af8fc68dfeff57f877`, processor pin `631eeb34`)
- Rulings: stage 2 https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394,
  stage 2b https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985974804
- Earlier handoffs: `HANDOFF_STAGE1.md` (diagnosis), `HANDOFF_STAGE2.md`
  (option C with the 7-event target; its PR body and STOP are in `stage2/`)
- Executor [A531]; reviewers [R474] (internal), [R475] (external)
- Local and not pushed.

## Contents

1. What the ruling asks, and how this lane reads it
2. The RTL change
3. Tests, and a grading gap closed
4. Results
5. Area
6. Documentation
7. Gates
8. The finding, its options and the recommendation
9. Reproduction commands and evidence

## 1. What the ruling asks, and how this lane reads it

1. **A fixed 8-event loopback target**, not the adaptive 7-or-8. Read as:
   `LB_TARGET_C` = `LB_QDEPTH_C` = 8 events at a class-A PDU end, so two
   events of the previous PDU are left when the next PDU lands, whatever
   the phase. The bar: 0 slips after the settle recentre across the 16
   switch phases with the lateness tail, the switch runs and the pull-in
   runs, and the minimum margin at the worst phase stated.
2. **Area on the change's own logic**: the out-of-context delta and the
   change's own cells in the route, both reported, its flip-flops named.
3. **The 4 mutation-campaign failures belong to #657**: cited, not fixed.

"The switch runs" is read as stage 2's set-and-switch campaign, `make
sweep-b8`: 16 set phases at no lateness and at 0 to 5 us uniform, each run
an INTERNAL-to-AAF set and two stream-to-stream switches. That is where the
bar does not hold.

## 2. The RTL change

Commit `78eeba22f`, `hdl/ieee1722/aaf/KL_chan_map_capture.sv` only:

| Term | Stage 2 (7 events) | Stage 2b (8 events) |
|---|---|---|
| `LB_TARGET_C` | `LB_QDEPTH_C - 1` = 7 | `LB_QDEPTH_C` = 8 |
| `LB_LEFT_C` (left of the previous PDU at the next PDU start) | 1 | 2 |
| None left | hold one pop | hold two pops, one per walk |
| One left | nothing | hold one pop |
| Two left | drop the oldest | nothing |
| Three left | drop the oldest | drop the oldest |
| `rc_hold_r` per stream, `act_hold_r` per pair | 1 bit | `LB_HOLDW_C` = 2 bits: pops still to hold |

A walk start hands a stream's fresh decision to its pairs; a hold left from
the last decision carries on, one pop per walk, so every pair of the stream
holds in the same walks and stays in lockstep. A drop still acts in the
first walk only. A flush clears both. Neither slip counter moves for a held
or dropped pop. No port, register field or parameter changes; the
datapath is unchanged since stage 2.

## 3. Tests, and a grading gap closed

- **`tb/verilator/chmap_capture` `[LRC]`** (`558c97a94`): an unprimed
  stream ignores the pulse; none left holds two pops (e6 repeats twice) and
  no third (the next PDU follows in order); one left holds one (e5 repeats)
  and acts once; three left drops the oldest on both pairs (e4 never plays,
  the PDU after the pulse carries three events so nothing overruns the
  depth first) and acts once; two left moves nothing; a flush cancels; a
  pulse on a PDU's first beat acts at the next PDU, with two holds. Both
  pairs carry one event per tick throughout, and neither counter moves.
- **`tb/verilator/follow_ring`**: the centring check is (2, 3] ticks
  (`e54d81404`).
- **A grading gap in my own stage-2 harness, closed** (`681ad6aa2`). The
  harness split slips into "before" and "after" the settle recentre at the
  pulse plus 1 ms. A drop that the recentre itself causes lands within a
  PDU or a few of the pulse, so it was counted as part of the declared
  transient: at 5 us, phase 0.6875, `[B8]` passed with "slips set-to-settle
  3 (declared bound 3)", and only the switches' "no ring slip across the
  switch" caught the same drop there. The split is now the end of the
  stream's first PDU after the pulse (`kPduEndS`), the PDU the loopback ring
  decides on; any slip after it is the recentre's own. Stage 2's own
  campaign logs have no slip in that window, so its figures stand.
- **OVERSHOOT**, a planted control for that split (`1a99cab54`): the loopback
  target one past the depth (`LB_LEFT_C` = 3), planted in a copy of the
  capture crossbar through a new `CMAP_SRC` Makefile variable. On the
  standing B8 leg it holds three pops, the next PDU finds the queue full and
  drops an event 0.3 ms after the pulse, and the ring then sits inside
  (2, 3] ticks again, so centring passes. Built against the old harness it
  survives (8 checks, 0 failures); against the new it fails "[B8] no
  loopback slip after the settle recentre" (`stage2b/overshoot/`).
  `scripts/measure_test_evidence.py` records the copy (`11eafd84d`).

## 4. Results

Campaigns completed before the interruption, retained after checking their logs
and return-code files. The two failing seeds were rebuilt from current sources
and reproduced during this resume. RTL is identical to `78eeba22f`; the slip
split is `681ad6aa2`. Evidence: `stage2b/sweeps/` and `stage2b/resume/`.

| Campaign | Runs | Recentres | Slips after the decision PDU | Result |
|---|---:|---:|---:|---|
| No arrival lateness, 16 phases, INTERNAL to AAF then AAF to CRF and back | 16 | 48 | 0 | 16/16 pass |
| Uniform 0 to 5 us, same three transitions | 16 | 48 | **4** | **14/16 pass** |
| Uniform 0 to 2 us plus probability 1e-4 of another 0 to 24 us | 16 | 48 | 0 | 16/16 pass |
| INTERNAL pull-in: 52 us hold, 16 feed phases | 16 | 16 | 0 | 16/16 pass |
| INTERNAL pull-in: 56 us hold, 16 feed phases | 16 | 16 | 0 | 16/16 pass |

The four drops are one after the initial set at phase 0.625 (seed 655), and
one after each of the three transitions at phase 0.6875 (seed 656). Each is
one event per active channel pair, hence two increments of `SLIP_LB.SKIP`
for the four-channel stream. The shortened, freshly built reproductions of
the initial set both return 1 at the named no-post-settle-slip assertion.
This is a functional failure, independent of the earlier external interruption.

Before settling, at most two slips occur without the rare tail, or three
with it, at the planted 5.92 ppm offset. Stream-to-stream switches have zero
slips before settling. The 52 us hold has none during its pull; the 56 us
hold slips once at three phases before settling. These are the declared
transients, separate from the four disallowed drops above.

**Measured margins.** From each PDU's first committed event to its pop:

| Arrival model | Smallest post-settle margin | Largest | Phase of smallest |
|---|---:|---:|---|
| No lateness | 1.989 ticks (41.44 us) | 2.995 ticks | 0.5625, CRF to AAF |
| Rare tail | 0.891 ticks (18.56 us) | 2.988 ticks | 0.2500, AAF to CRF |
| Uniform 5 us, including the failed runs | 1.843 ticks | 3.080 ticks | 0.6875, initial set |

The nominal fixed-target lower margin is two ticks, 41.67 us; the sampled
no-lateness minimum is slightly below it because decision and queue commit
are different axis cycles. The rare-tail minimum is the remaining margin
of an already late PDU, not a new guaranteed arrival allowance. The ideal
three-tick total headroom leaves only 0.005 tick (0.10 us), plus serialization,
on the early side at the largest no-lateness margin. No positive lower
earliness bound follows from the fixed 8-event target alone.

For render timing with no lateness, all 45 gradable post-settle windows are
on the law; three windows are not gradable under #643's boundary rule.
Arrival-lateness campaigns do not grade the render law. In the INTERNAL
sweep, 27 of 32 cases have both before and after windows gradable and on the
law; two have only the before window ungradable, and three have the after
window ungradable. No ungradable window is counted as proof of the law.
The full integration pull-in campaign passed all 18 feed-phase legs.

**Exact cycle trace, phase 0.625 / seed 655.** `stage2b/resume/cycle_p10.log`
observes the existing model without changing inputs or RTL:

| Time (s) | Event |
|---:|---|
| 17.415138800 | settle pulse; pair 0 still has one event |
| 17.415138960 | that ordinary pop finishes; queue empty; recentre armed |
| 17.415140240 | PDU 134518 first payload beat; decision requests two held pops |
| 17.415142000 | its last beat; six events in pair 0 |
| 17.415262640 | next PDU's final pair-0 push finds the eight-entry queue full; SKIP becomes 1 |
| 17.415262800 | pair 1 makes the same drop; SKIP becomes 2 |
| 17.415264080 | next ordinary pair-0 pop, too late to free space for that push |

PDU 134518 arrived at 17.4151401 s, 4.83 us late, and had a 2.9338-tick
margin. PDU 134519 arrived at 17.4152607 s, only 0.43 us late. Its last
pair-0 push precedes the freeing pop by 1.44 us. That directly identifies
queue overflow, rather than an inferred missing event or a masked counter.
The prior trace excerpts used the render execution time as their relative
reference; their column is corrected to `from_render_execution_s`. It is
not the earlier settle pulse. The sweep margin summary is also corrected
to sum the switch drops as well as initial-set drops: four, not two.

## 5. Area

**No completed fixed-8-event integrated route is claimed.** The prior routed
pair is for stage 2's 7-event target, as recorded in `HANDOFF_STAGE2.md`.
The fixed-8 OOC attempt waited for the shared lock and timed out after
570 s without starting a synthesis process (rc 124). No other run was
interrupted. A separate Yosys estimate was then made for the changed blocks.

Yosys 0.66, sv2v lowering, `synth_xilinx -family xc7 -noiopad`, the same
1x1 capture parameters as the previous OOC comparison (4 slots, TDM8,
one 8-channel loopback stream). All five lowerings and synthesis runs
returned 0. `stage2b/resume/*_stat.txt` holds the mapped cell counts;
`input_hashes.txt` records full logs by size and SHA-256. `cmc_head8.sv`
was checked equal to the current capture RTL except its module name.
LUT here means the sum of mapped LUT1 through LUT6 cells, excluding
RAM32M and inverter pseudo-cells; FF means FDRE plus FDSE.

| Block | Base LUT / FF | Fixed 8 LUT / FF | Delta |
|---|---:|---:|---:|
| #386 plus settle trigger | 73 / 51 | 134 / 92 | +61 / +41 |
| Capture crossbar | 1,265 / 1,384 | 1,356 / 1,399 | +91 / +15 |
| **Sum** | | | **+152 LUT / +56 FF** |

This estimate exceeds 120 LUT. It is a STOP estimate, not evidence that
the fixed-8 implementation meets the area bar. Yosys maps the queue to
eight RAM32M cells in both versions; this differs from the earlier vendor
mapping and these totals must not be mixed across tools.

The unchanged trigger's prior Vivado OOC delta is +26 LUT / +41 FF.
Stage 2's full 7-event option was +36 LUT / +49 FF OOC. Its old integrated
route was +52 LUT / +164 FF in total, with **48 attributable added FF**:
41 settle registers and seven capture registers. The other 116 FF came
from differently retained unchanged logic, per the stage-2 register lists.
The second ruling excludes that unrelated variance from the limit. Those
old routed figures do not establish fixed-8 compliance. The fixed-8
route, its own-cell LUT attribution and its own FF names remain required
if the functional STOP is resolved.

## 6. Documentation

Commit `d12ce007c`:

- `docs/design/MEDIA_CLOCK_FOLLOWING.md`: the second ruling cited; the
  loopback-target row (8 events, the hold and drop rules); "The loopback
  lane's latency": two events, 41.7 us, over the empty edge, one event
  (20.8 us) more than the 7-event target, on the diagnostic loopback lane
  only, the declared AAF presentation path and latency = pto unaffected;
  the declared-transient paragraph names the PDU-end split; the open case
  rewritten (section 8); the follow_ring test-plan row (the split, (2, 3],
  OVERSHOOT, red at 2 of 16 phases at 5 us).
- `docs/design/TIME_SYNC.md`: the settle-recentre row says 8 events.
- `docs/reference/REGISTER_MAP.md` `SLIP_LB`: held pops (plural).
- `docs/testing/TESTING.md`: the follow_ring row (the split, OVERSHOOT, the
  red 5 us case); the render mutation row cites #657 for its four failures.
- In the RTL: `KL_chan_map_capture`'s RECENTRE banner and comments.

## 7. Gates

The required all-green bar is **not met**. No REVIEW READY is claimed.
Completed evidence is retained with its revision; interrupted or old evidence
is not promoted to a pass at the new head.

| Evidence | Revision / scope | Result |
|---|---|---|
| Fresh follow_ring build and both short failing seeds | Current RTL and harness | Build rc 0; both runs rc 1, the expected reproduction of the open defect |
| follow_ring standing B8 and pull-in | `681ad6aa2` harness, current RTL | rc 0; 26 and 6 checks respectively |
| follow_ring five planted controls | Final harness | rc 0; all five caught by their named check |
| chmap_capture default and netlist legs, including revised LRC | Fixed-8 RTL | rc 0 |
| milan_dp, milan_dp_mclk, media_grid_align, pp_shadow defaults | `e54d81404`; their RTL/tests unchanged since | Each rc 0 |
| milan_dp_render default, T30 and LAW included | `e54d81404`; render code unchanged since | rc 0 |
| milan_dp_render 18-phase pull-in campaign | Same | rc 0 |
| Static/style/documentation gates | Final changes | All 26 gates pass after the mutation-runner correction; initial failure retained below |
| Five small OOC mapping estimates | Current/frozen prototype inputs | Each lowering and synthesis rc 0 |
| Capture coherence and render LAW-boundary reruns | Stage 2b | Interrupted before an rc; **not a pass** |
| Complete portability sweep, vendor parser gate, builder gate | Stage 2b | Not completed; earlier stage-2 receipts remain historical only |
| Fixed-8 integrated route and own-cell attribution | Stage 2b | Not run |

Static receipts: `stage2b/resume/static_first_rcs.txt` has the initial
Python parameter-count failure introduced by the expanded mutation runner.
The final runner accepts one typed mutation record, so the rule's count
returns to its allowed seven. The budget and all five named failure
assertions are unchanged. Its corrected gate receipt is recorded separately.
The LRC documentation row is corrected from the old 7-event actions to the
actual none/one/two/three-left cases of the fixed-8 tests.

The full render mutation campaign previously had 30/34 checks passing;
four failures were identical at the base. The second ruling assigns them
to #657. This lane neither changes them nor calls that campaign green.
The earlier LAW-boundary campaign passed at stage 2; its stage-2b rerun
was interrupted, so it is explicitly unfinished here.

No push, hosted run, local hosted-workflow replica, PR, independent review,
merge validation or hardware action was performed. The STOP ends work at
the failed acceptance; it does not waive any remaining gate for a future
review-ready head.

## 8. The finding, its options and the recommendation

**Original classification, retained.** #645 is the frequency-only servo's
residual phase walk plus an uncentred loopback ring: E8's 4.1 s measurement
latency and PI acquisition move phase about 1.43 ticks at a 5.92 ppm offset,
then about 0.03 tick after LOCKED. #386 fires near 43 ms and only reaches
render; it cannot centre the loopback ring. A late PDU then slips a ring
left near empty. Thus assignment classification (a) applies to #645;
(b), too-early recentre, applies to render at the same source switch.
For #647 an INTERNAL aligner pull-in also moves render, without a source
change or re-engagement to request a new recentre. Stage 1 reproduced the
permanent shift in 7/13 gradable 52 us pull-ins and 4/14 gradable 56 us
pull-ins. These conclusions and the original traces remain in
`HANDOFF_STAGE1.md`; the second-stage trigger addresses that timing gap.

**The remaining fixed-8 failure is a headroom conflict.** An eight-event
queue receiving six-event PDUs has three tick intervals in total between
its empty and overflow edges, before accounting for serialized beats.
Putting the first-event latency in (2, 3] ticks buys the requested late-side
margin, but leaves an early-side margin that tends to zero with phase.
A decision referenced to one late PDU can therefore make a following less
late PDU overflow it. The exact trace in section 4 demonstrates this;
neither a longer wait for frequency LOCKED nor the unchanged render law
provides that missing early-side space. Four drops violate the second
ruling's zero-post-settle-slip requirement. They are not moved into the
pre-settle allowance, and the rejected adaptive target is not restored.

**Options for a further ruling; none applied to the candidate:**

| Option | Area evidence | Protocol-visible effect | Test plan / limitation |
|---|---|---|---|
| Keep fixed 8 and explicitly allow these post-settle drops | No added logic beyond current; Yosys total +152 LUT / +56 FF vs base | One additional dropped loopback audio event at the affected transition; render law unchanged | Keep both seeded failures and grade against a newly ruled bound; this reverses the current zero-slip bar, so not recommended |
| Keep fixed 8, choose a reference over 64 PDU starts (prepared option E) | Yosys capture 1,362 LUT / 1,409 FF, +6 / +10 over current; with trigger +158 / +66 vs base | Loopback action about 8 ms later than render, still a fixed target; requires a changed settle/action contract | Two exploratory short failing-seed runs passed; no complete campaign or adversarial proof. Must test all 16 phases, all-late training followed by an early PDU, loss, reset and flush; a finite sample window cannot guarantee the next packet's arrival bound |
| Keep fixed target 8, add queue headroom | Not synthesized or implemented. For depth 16 at 1x1, raw storage increases by 8 events x 4 pairs x 48 bits = 1,536 bits; pointer/count widths add 12 bits before optimization. LUT/BRAM packing and route costs remain unmeasured | Fixed-8 loopback latency stays +41.7 us over the old empty-edge placement; no declared render-latency or wire-format change | Requalify full/empty, wrap, same-cycle push/pop, reset/flush, all LRC actions, both failing seeds, all phase/tail/pull-in campaigns and the integrated route; changing a depth constant is outside this authorization |
| Revisit the phase-dependent 7/8 target | Prior prototype OOC total +68 LUT / +80 FF in Vivado; two edge cases remained | Diagnostic loopback latency depends on phase; render law unchanged | Requires explicit reversal of the second ruling and new boundary tests; not proposed as an authorized implementation |

**Recommendation:** retain the fixed-8 latency decision and ask for an
explicit queue-headroom ruling, including the accepted arrival envelope and
area measurement method, before changing any depth constant. Additional
storage separates late tolerance from early tolerance; selecting a lucky
arrival over a finite window does not prove the required bound. First
measure the chosen queue shape against the 120/120 own-logic limit; STOP
again if it cannot fit. The current estimate and unfinished routed evidence
must also be resolved. This is a recommendation for the next decision,
not a claim that an unbuilt deeper queue already passes.

The original alternatives remain documented, with measurements and tests,
in stage 1: servo phase feedback (+169 LUT / +129 FF, changes lock/phase
behaviour and does not centre the ring); band-only recentre (+9 / +1,
addresses INTERNAL render but not the frequency-acquisition walk); later
recentre to both rings (chosen C); or declare the original bounded
transient (zero area, leaves delayed slips). C's initial estimate was
+55 / +33 and its completed 7-event implementation +36 / +49; neither is
an area result for the current 8-event implementation.

## 9. Reproduction commands and evidence

Use the same local branch; no checkout, push or hardware is needed. The
compiler path below is the pinned executable supplied for this lane.
Build and campaign outputs stay outside the repository.

```sh
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export PYTHONDONTWRITEBYTECODE=1
WORK=$(mktemp -d /tmp/ring-slip-repro.XXXXXX)
make -j16 -C tb/verilator/follow_ring build MDIR="$WORK/model" VERILATOR_JOBS=16
"$WORK/model/Vfollow_ring" --case b8 --dwell-s 1.0 --set-phase 0.625 \
  --jitter-us 5 --hold-s 12 --seed 655 --allow-ungradable
"$WORK/model/Vfollow_ring" --case b8 --dwell-s 1.0 --set-phase 0.6875 \
  --jitter-us 5 --hold-s 12 --seed 656 --allow-ungradable
```

Expected on this head: build rc 0; each execution rc 1, exactly the B8
no-loopback-slip-after-settle check fails with got=1 / exp=0. `--allow-ungradable`
only permits render boundary windows; it does not relax the slip check.
The full sweep uses the standing seeds 645 through 660:

```sh
python3 tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/switches" --jobs 8 --jitter-us 0 5 --hold-s 40 \
  --switch-hold-s 20 --extra --dwell-s 1.0
python3 tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/tail" --jobs 8 --jitter-us 2 --tail-us 24 --tail-p 1e-4 \
  --hold-s 40 --switch-hold-s 20 --extra --dwell-s 1.0
python3 tb/verilator/follow_ring/sweep.py pullin --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/pullin" --jobs 8 --hold-us 52 56
MAKEFLAGS=-j16 VERILATOR_JOBS=4 python3 tb/verilator/follow_ring/mutants.py \
  --mdir "$WORK/mutants" --jobs 3
```

Expected campaign return codes: 1, 0, 0, 0 respectively. Execute independent
campaigns concurrently with separate log and rc files and a foreground wait;
each command must remain within the session's ten-minute command limit.
The saved completed sweeps avoid treating a time limit as a functional result.

For the small area estimate, lower the frozen source with sv2v, apply the
listed 1x1 parameters, then map with:

```text
read_verilog cmc_head8.v
chparam -set N_SLOTS_P 4 -set N_TDM_P 8 -set TDM_FRAME_PAIRS_P 4 -set N_LB_STREAMS_P 1 -set N_LB_CH_P 8 KL_chan_map_capture_head8
synth_xilinx -family xc7 -top KL_chan_map_capture_head8 -noiopad
stat
```

The same recipe applies to the base and prepared reference-window prototype;
settle wrappers have no capture parameters. Retained recipes and source
hashes identify their inputs. No tree export, build tree, package installation
or file larger than 200 KB is copied into this output directory.

Evidence index: `stage2b/sweeps/` (all campaign rows and margin summary),
`stage2b/traces/` (PDU excerpts), `stage2b/overshoot/` (old grace-period
control versus corrected split), `stage2b/resume/` (fresh failures, cycle
trace, static receipts, synthesis statistics and SHA-256/size inventory).
Earlier stage-specific evidence remains under `stage2/` and the two archived
handoffs. `PR-BODY.md` is a local, blocked draft only.
