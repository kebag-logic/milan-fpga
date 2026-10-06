[A531]

Public STOP: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994628555

# Stage 2d handoff

Status: **STOP -- required timing margin missed**. Head
`b2c81239f686592b224510c9d4f196a6c7aa7f25` on `645-ring-slip`.
ExtraTimingOpt slow WNS is +0.001 ns at both temperature settings, below the
required +0.030 ns. Slow WHS is +0.001 ns; fast WNS/WHS is +1.476/+0.012 ns.
The implementation command returns 0 but the required margin grade returns 1.
The [stage-2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410)
therefore requires STOP. No recovery change, threshold change or reroute follows.

All functional acceptance runs finish at rc 0. Physical is 143/0, accounting
40/0 and the new controls 14/0, totaling 197 checks with zero failures.
Datapath, render, media-clock, changed units, four arrival campaigns, INTERNAL,
five controls, boundary 81/0, builder, portability and source gates pass as
qualified below. The builder's historical Arty area-calibration arm is NOT RUN
because its reference report is absent; it earns no pass. Current routed own
area is bounded by 113 LUT / 73 FF, within 120/120. The other two required
timing directives pass. The tree and pinned submodules are clean; nothing was
pushed or published as a PR. HANDOFF.md and PR-BODY.md are complete for this STOP.

## Public contract and branch

The [stage-2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410)
requires the dev merge, exact decision-PDU ordering, two planted controls,
merged-head acceptance, build-defined timing signoff and startup/reset docs.
The earlier [option C](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394),
[own-area and #657](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985974804),
and [depth/envelope](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987852678)
rulings remain applicable. The original assignment, #645, #647, #629, #643,
PR #648, requirements and all three requested design/findings documents
were read. The takeover is
https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990664496.

Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
Stage 2d resumed at `535a710d3be73764fd0c951953565f462812bce8` and made:

- `be3ec6e57a9b22c76daef817c07cae5ade8ca012`: required no-fast-forward
  merge, parents `535a710d` and dev `fa450d30`, without conflicts.
- `fad3cf18633f424d0d52cfedbac2f705c4a024c1`: startup/reset discontinuity
  bounds and #396's steady-state scope in MEDIA_CLOCK_FOLLOWING.md.

- `b2c81239f686592b224510c9d4f196a6c7aa7f25`: exact physical wire ordering and two controls, read-only probes,
  build-only target and matching test documentation.

All subjects are one line with no body or trailers. Processor remains
`631eeb342ca1e3fa80e734077a56a943aee76ff1`, gPTP
`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Each submodule's top-level
directory was verified before running further Git commands within it.
Executor [A531]; internal reviewer [R474]; external reviewer [R475].
No push, PR publication, hardware operation or merge into dev is authorized.

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

| Option | Area at 1x1 | Protocol-visible effect | Discriminating validation |
|---|---|---|---|
| A: servo phase feedback | Historical prototype +169 LUT / +129 FF, plus reference mux | Changes loop dynamics, lock behavior and phase against the talker; does not remove pre-lock accumulated phase or restore INTERNAL latency | Sweep offsets/arrivals and phase; remove phase gain as a control; rerun servo, meter and integration. Exceeds the lane's area limit and does not solve both issues |
| B: aligner-band/excursion recentre | Historical prototype +9 LUT / +1 FF | Bounded render discontinuity after INTERNAL pull-in; no loopback correction during frequency acquisition | Both pull-in directions and all render phases; remove excursion arming as a control. Leaves #645 |
| C: later recentre of both rings | Stage-2c OOC +80 LUT / +73 FF; current routed own-logic bound <=113 LUT / +73 FF | Bounded declared startup/reset/switch action; loopback delay increases as above; AAF presentation law unchanged | Four arrival envelopes, INTERNAL phases, five controls, physical exact-step ordering plus two controls, full integration and timing. Ruled option |
| D: document the old behavior only | 0 | Leaves a late slip without a time bound and persistent render latency displacement | Offset/phase sweep against an explicitly changed specification. Does not fix either issue |

The stage-2c OOC measurements were settle 41/51 -> 67/92 LUT/FF and capture
1076/1336 -> 1130/1368, summing +80/+73. Both capture designs infer one
RAMB36. The own-area bar is 120 LUT / 120 FF. Historical routed attribution
counted a conservative 63 additional settle-cone LUTs plus capture's 49,
and 41 settle plus 32 capture FFs. It excluded demonstrably unchanged
functions using actual connections and exhaustive logic comparison. Its
whole-design +141 LUT / +156 FF was separately reported, not treated as
this change's own logic. Detailed cell lists, controls, recipes, parts,
clocks and source receipts remain in stage2c/vendor/ and stage2c/route/.

`stage2d/area-source-identity.json` shows the complete capture module and
repository settle block plus window constant are unchanged between the
submitted stage-2c head and the merged documentation head. It does not
compare the extracted OOC wrappers byte for byte. The area figures remain
historical evidence; historical routed ownership and whole-design totals
are not transferred to the new placement.

### Fresh routed ownership at the merged head

The default completed placement was queried afresh under the shared lock.
Its conservative own-logic bound is **113 LUT / 73 FF**, below both 120 limits.
The 80-LUT settle cone contains one capture LUT already counted in that
module's delta, six functions identical by complete input/output signature,
and ten shared band functions proved identical over all 65,536 signed-error
assignments. A planted truth-table change is caught. The remaining 63 LUTs
plus capture's 50-LUT delta give 113. All 41 settle flops and the 32 net added
capture flops are named in `stage2d/area-current/`; no added block RAM is claimed.

The whole design is 51,426 LUT / 59,787 FF versus the identified historical
pre-lane baseline's 50,767 / 59,634, a raw +659 / +153. This aggregate includes
changes outside the lane and implementation mapping effects; it is not an
isolated measurement of this change. The hierarchy-delta report retains those
differences rather than assigning them to the new logic. The baseline checkpoint
is the recorded stage-2c baseline, size 110,027,920 bytes and SHA-256
`922bb104490e8c35b51fb64306794ecd148cb149e3e05f9ab3770f1371a3d7f6`.
Current area queries, comparison and exhaustive proof all return 0. Full source
and artifact receipts permit regeneration of omitted oversized cell dumps.

## Current functional evidence

The merged-head ring model rebuilt at rc 0. Five independent campaigns ran
concurrently using that fresh binary, each with `--jobs 4`. The five unchanged
controls ran with `--jobs 3`. All return 0.

Each arrival run uses phases k/16, seeds 645+k, and INTERNAL -> AAF for 40 s,
then AAF -> CRF and CRF -> AAF for 20 s each. The peer and INTERNAL offsets
remain -11.02 and -5.10 ppm against gPTP. The 6.25 MHz axis clock does not
compress the 512 ms servo windows. Counters are graded from the decision
PDU end with no grace period.

| Arrival envelope | Runs / decisions | Post-decision slips | Min empty / full margin (ticks) | Max pre-settle slips |
|---|---:|---:|---:|---:|
| No lateness | 16 / 48 | 0 | 4.984320 / 5.076480 | 2 |
| Uniform 0..5 us | 16 / 48 | 0 | 4.899840 / 4.907520 | 2 |
| Uniform 0..2 us, probability 1e-4 of 0..24 us tail | 16 / 48 | 0 | 3.893760 / 5.091840 | 3 |
| Uniform 0..60 us | 16 / 48 | 0 | 2.565120 / 2.234880 | 2 |
| INTERNAL holds 52 and 56 us | 32 / 32 | 0 | 4.984320 / 5.091840 | 1 |

All margins exceed the one-tick floor. Late-arrival campaigns grade slips
and margins, not render-law coverage. Their raw render observations include
off-law and ungradable windows and are retained honestly. No-lateness has
45 on-law and three ungradable observations. INTERNAL has 27 fully gradable
before/after results, two BEFORE NOT GRADABLE and three AFTER NOT GRADABLE;
ungradable windows earn no render-law evidence.

The unchanged NO-SETTLE, RENDER-ONLY, EARLY, W1 and OVERSHOOT17 controls are
all caught. Capture-map passes 408 RTL plus 20 synthesized-netlist checks.
Aligner passes 45 checks plus three caught controls. Logs, exact arguments,
binary hashes, summaries and per-run receipts are in `stage2d/functional/`.

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

## Ordering harness

The committed checker uses read-only observations of pre-decision fill,
accepted PDU boundaries, capture walks and packetizer sample slots. It
calculates the declared step independently of the DUT's hold/drop controls
and audio values, then transports that exact slot plan to the MAC-wire oracle.
Everywhere else the sample index must advance by one. Every existing
assertion remains; four new assertions account for the plan, single-PDU
scope, completed decisions and unchanged counters. The normal physical tally is 143 checks, zero failures, up from 139 by exactly the four new assertions. The documentation test table now matches
the existing none/four/five/six retained-event cases and their target of eleven.

The unannounced-repeat control changes the first incoming sample after a
completed decision output PDU. Its verifier requires every ordering error
outside every declared PDU. The larger-step control leaves the actual
recentre intact but understates its declaration by one event; its real wire
step must exceed that allowance, and every error must be in the declared
PDU. The new verifier passes fourteen checks with zero failures, including
required PDU location, measured step, payload and sequence integrity, both
slip counters and absence of unrelated failures. Existing accounting controls
are unchanged. No DUT source changes in stage 2d.

The committed harness runs in an external physical-test staging directory so its
build does not share generated images with the broad datapath suite.
C++/Python idiom, whitespace and affected documentation checks pass; its compilation passes and both planted controls are caught. The normal
run has observed a five-repeat startup declaration matching the wire
exactly, in output PDU 6047, with both counters 0 -> 0. Reset reacquisition also declared exactly five repeats, output PDU 92215,
with both counters 0 -> 0. Both measured wire steps equal -5 events. The final
normal run passes 143 checks, with two decisions completed and no plan,
span, payload, ordering, packet-sequence or slip-counter error. It ran
16.992510280 simulated seconds (849,625,514 axis cycles) in 3501.68 seconds.
It performed 6,517,344 payload, 814,666 sample-order and 135,936 packet-sequence
comparisons. With unchanged accounting 40/0 and new controls 14/0, the suite
is 197 checks / zero failures. The original 139 physical assertions remain.

This is a modeled physical-clock gPTP integration leg. Licensed ACMP/SRP
streaming, physical TDM render, CRF recovery, multiple-responder cease,
PHY/MAC calibration, CPU/DDR and physical compliance are explicitly NOT RUN.
The original first-10-ms warm-up comparison exclusion remains declared.

## Integration reproduction

`stage2d/integration/pending-commands.json` records the exact argv and working
directory for each job. `test-source-identity.json` binds each external staging
copy of 369 tracked test files to the committed head. The physical and focused
render copies use distinct generated-image directories from the broad suites.
They share the same committed source inputs; no other checkout is used.

With BROAD, PHYSICAL and FOCUSED naming those external staging roots, and the
pinned simulator on PATH:

```sh
make -j16 -C "$BROAD/tb/verilator/milan_dp" VERILATOR_JOBS=2 SIM_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_render" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_mclk" VERILATOR_JOBS=2
make -j16 -C "$PHYSICAL/tb/verilator/milan_dp" ax1x1gptp-build VERILATOR_JOBS=4
(cd "$PHYSICAL/tb/verilator/milan_dp" && ./obj_ax1x1gptp/Vmilan_dp_ax1x1gptp)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_abort.py)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_recentres.py --jobs 2)
make -j16 -C "$FOCUSED/tb/verilator/milan_dp_render" tdm8render-pullin PULLIN_JOBS=8 VERILATOR_JOBS=2
(cd "$FOCUSED/tb/verilator/milan_dp_render" && python3 -B tdm8_render_mutants.py --law-boundary --jobs 4)
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
bash syn/yosys/run.sh
python3 -B scripts/xvlog_gate.py --check
```

The last vendor parser command, area queries and implementation run execute
sequentially under the shared lock; their full launch recipe is in
`stage2d/final-extra/`. Environment installation roots in copied recipes are
neutral placeholders to resolve locally. The parser and portability return 0.
The builder has the required compiler and elaboration environment; its one
historical area-calibration NOT RUN remains explicit. Additional unit commands
and all source gates are preserved as exact command receipts. Never pipe a gate.

## Timing signoff

Fresh shipping export uses the integrated endpoint in
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: part xc7a100t-fgg484-2,
AreaOptimized_high synthesis, ExploreArea optimization, the named placement,
AggressiveExplore physical optimization and routing, 32 threads, default
seed and initialized firmware. The alternate placements reuse this fresh
synthesis checkpoint and change only the placement directive. Runs are
sequential under `$VIVADO_LOCK`. No bitstream is requested.

Require WNS >= +0.030 ns and WHS >= 0 at both Slow/Fast timing models, each
reported at 0 and 85 C power conditions. Those temperatures repeat fixed
timing models; they are not four independent PVT models.

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Result |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.120 / +0.053 | +1.633 / +0.019 | PASS, rc 0; all TNS/THS zero |
| AltSpreadLogic_high | +0.142 / +0.065 | +1.483 / +0.026 | PASS, rc 0; all TNS/THS zero |
| ExtraTimingOpt | +0.001 / +0.001 | +1.476 / +0.012 | **FAIL required setup margin**, grade rc 1; run rc 0 |

All three completed directives have no critical warnings and pass the build's
rejected-constraint check. Speed file: -2 PRODUCTION 1.23, 2018-06-13.
No register/latch pins lack clocks, and no internal endpoints are
unconstrained. External coverage remains limited: 46 inputs have no input
delay and are false-pathed; 87 outputs lack output delay. CDC, interaction,
exception and unconstrained-path reports are retained without an external
I/O or hardware-compliance claim. This measurement does not qualify a
release bitstream.

`stage2d/TIMING-RECIPE.md` and `shipping-arguments.json` give the recipe.
`source-hashes.json` records 134 synthesis inputs, all rechecked unchanged
after the builder restored its temporary firmware links at the committed head. `stage2d/timing/` contains small reports and raw
SHA-256/size receipts for every retained or oversized artifact. Copies
replace home paths and host identity with neutral placeholders.

## Source gates and execution receipts

All 26 source/documentation checks now return 0 at the committed harness
head. Exact commands, results and hashes are in stage2d/source-final/.
RTL lint remains 90 within budget 90. Earlier documentation-head and draft
receipts remain retained separately. The final bare-metal check first used
the Markdown environment without YAML and returned 2; rerunning with the
normal interpreter and its required YAML dependency returned 0.

Initial Markdown anchor/contents/punctuation attempts returned 2 because
the pinned renderer dependencies were missing. Installing the documented
hash-pinned requirements in external scratch and rerunning returned 0.
Export itself returned 0; the first inventory wrapper returned 1 after its
temporary image links were restored too soon. Restoring those links and
repeating preparation returned 0. Original failed receipts remain retained.
The first alternate constraint-log check passed a string where its API
requires a Path and returned 1; the corrected invocation returned 0. Both
receipts are retained. No acceptance or DUT logic changed to recover these
setup errors.

All 134 implementation inputs matched their recorded hashes at the final
head before cleanup. The three temporary source-tree image links were removed;
no originals required restoration. Generated bytecode was moved to external
scratch. Final root and submodule status is clean, including ignored files. All output files are at most
200,000 bytes. Toolchains, installed packages, build trees, tree exports
and large artifacts remain outside the output directory.

Execution adjustment: the capture-coherence mutation driver sizes its pool
from CPU affinity and exposes no jobs flag. Its first invocation launched
enough concurrent compilations to reach the 12 GB service limit. No OOM or
process kill occurred before intervention. That incomplete campaign was
explicitly terminated and earns no verdict; its original log is preserved.
The retry uses a two-CPU affinity while retaining make -j16 and two compiler
workers. Other briefly paused build schedulers were resumed. No test or
DUT source changed.

The first datapath invocation returned 2 before the main simulation pool:
SIM_JOBS=6 exceeded that standing driver's explicit ceiling of two. All
models compiled; no failed DUT assertion was reported. The exact unchanged
make target passes with SIM_JOBS=2. The original command, log and
return code are retained. Accounting now passes all 40 checks, and the full
media-clock integration passes all 31 control-runner checks, both rc 0.

The complete render default now passes: 259 shipping checks, 65 multistream
checks and all five no-rebuild stimulus controls. The focused eighteen-phase
pull-in and LAW boundary campaigns run in separate test staging, so they
share no generated files with the default suite. Processor-shadow passes
all four legs (646, 606, 606 and 311 checks). Render-setpoint passes its
131-check positive runs and fifteen controls; repair passes 47 checks.
The full media-clock log contains positive legs of 55, 32 and 50 checks
plus the 31-check control runner, all with zero failures.

The focused INTERNAL render pull-in campaign passes all eighteen phases with
zero loopback slips during pull-in and after settle. Seventeen phases have
gradable render windows; phase +1042 remains NOT GRADABLE because its PDU end
is four cycles from the boundary, inside the nine-cycle ambiguity. All eighteen
record a fresh settle 152.625 ms after the hold. No ungradable window earns
render-law coverage. The boundary campaign passes 81/81 checks across 564 windows: 123 graded
positive windows, 246 correctly rejected windows in the two planted setpoint
controls, and 195 explicitly NOT GRADABLE windows. The largest observed walk
is three cycles, within the unchanged five-cycle walk allowance. The nine-cycle
ambiguity (five plus four) is unchanged; ungradable windows earn no law credit.

The completed meter suite passes 465 unit, six servo and 36 mutation checks.
The servo suite passes 109 unit, eight rail, 113 PHC and 90 slew checks.
The bounded capture-coherence retry passes 332 datapath, 20,832 core and
30 control-runner checks. Every completed acceptance command returns 0;
original failed or interrupted setup attempts remain separate receipts.

The vendor parser gate passes at the committed head. The full datapath default
passes 11,877 checks, including its render and GM-step mutation controls. The
unique completed integration-log tally is 37,130 checks with zero failures;
this parser tally excludes the meter mutation runner's separately reported
36/36 result and includes the completed physical and boundary campaigns.

A stale inline module summary at `hdl/ieee1722/aaf/KL_chan_map_capture.sv:360`
still says depth eight. The detailed contract, actual local constant, executable
cases and design documentation say sixteen. This documentation inconsistency
is recorded for review; stage 2d leaves DUT source unchanged as ruled. It does
not change the tested queue depth or the measured margin.

## Recommendation and remaining acceptance

Stop at the recorded head under ruling 4. Retain option C and the completed
physical checker/control evidence while requesting the maintainer's next
ruling on the failed required margin. No logic/area trade, alternate constraint,
threshold relaxation or extra placement attempt is authorized by this stage.
The two passing directives do not excuse the failed required directive.

The minimum setup path is in the 50 MHz processor domain, from
`milan_datapath/pp_shadow/u_pp/u_rx_validator/hdr_src_mac_r_reg[0]/C` to
`milan_datapath/pp_shadow/u_pp/u_tx_arbiter/FSM_onehot_arb_st_r_reg[0]/CE`
(and bits 1 and 2), with 39 logic levels and a 19.728 ns data path. Its location
does not waive the timing bar. Full corner reports and raw artifact receipts
are in `stage2d/timing/ExtraTimingOpt/`; the margin and constraint checks are
in `stage2d/final-extra/`.

The four historical full render-mutant failures belong to #657 and are neither
fixed here nor counted as passes. Bench items remain with the manager. No
independent review, hosted gate, hardware acceptance, release qualification,
merge-result validation or containment is claimed. The manager dispatches
the hosted physical job only after publication is authorized. Do not push.
