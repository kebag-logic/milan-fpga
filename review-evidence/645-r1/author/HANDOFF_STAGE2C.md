# #645 / #647 stage-2c handoff [A531]

Status: **STOP: blocked by the physical gPTP integration gate**.
The ruled arrival/margin campaigns and both vendor area checks pass.
The physical gPTP suite returns 2 (139 checks / 2 failures). All area work
and the separately run accounting controls have finished; this head is
not REVIEW READY.

- Branch `645-ring-slip`, local head `535a710d3be73764fd0c951953565f462812bce8`.
- Resumed at `332833afa6cd396b99ac6f0e7ab48757459d0e56`.
- Dev base `fea346e76c2a57ed5cd131af8fc68dfeff57f877`.
- Origin verified as `https://github.com/kebag-logic/milan-fpga.git`.
- Processor `631eeb342ca1e3fa80e734077a56a943aee76ff1`; gPTP
  `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; AXIS
  `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
- Executor [A531]; internal reviewer [R474]; external reviewer [R475].
- No push, PR publication, independent review, merge or bench action.

## Authority and implementation

The [third ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987852678)
authorizes depth 16 and target `(depth + 6) / 2 = 11`, five retained events.
It retains the [option C ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394)
and the [own-area and #657 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985974804).
The [assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5981976917),
#645, #647, #629, #643, PR #648, REQUIREMENTS, CONTRIBUTING and the three
requested design/bench documents were read. TAKEOVER:
https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987861206.

The queue's two local constants are the only behavioural RTL changes in
stage 2c. Pointer, fill-count and held-pop widths derive from them. The
existing settle trigger still waits eight consecutive 512 ms LOCKED
windows under following, or 2048 in-band ticks at INTERNAL, with the
2^20-tick ceiling. The original #386 at-switch render recentre remains.
All pairs of each stream act together on the next PDU. Below target they
hold the missing number of pops; above target they drop one oldest event
toward it. No port, register-map or module parameter changed in this stage.

The diagnostic loopback adds three ticks (62.5 us) over target eight.
The declared AAF presentation path and latency = presentation-offset law
are unchanged. Queue storage is 64 x 48 bits at 1x1 and 512 x 48 at 8x8;
the latter fits one RAMB36. Actual memory mapping belongs to the synthesis
report, rather than an assumed LUTRAM implementation.

Local commits, all one-line subjects without bodies or trailers:

- `ee513ab9a`: depth/target, standing tests, margin observer and documentation.
- `344fbbc47`: document the wide default sweep and one-event drop precisely.
- `535a710d3`: state storage geometry independently of the inferred primitive.

The latter two change only comments/documentation. Executable RTL and test
behaviour are unchanged from the simulation builds. Vendor sources are
refreshed at the final head; `stage2c/source-hashes.json` binds that head.

## Functional evidence

All campaigns below returned 0. Each switch run sets INTERNAL -> AAF,
holds 40 s, then AAF -> CRF and CRF -> AAF for 20 s each. Set phases are
k/16 with seeds 645+k. These are real simulated seconds: the 6.25 MHz axis
clock scales the aligner's gains but does not compress the servo's 512 ms
windows. The peer is -11.02 ppm and INTERNAL -5.10 ppm against gPTP.

| Arrival campaign | Runs / decisions | Slips after decision PDU | Minimum empty margin, phase and transition | Minimum full margin, phase and transition |
|---|---:|---:|---|---|
| No lateness | 16 / 48 | 0 | 4.984320 ticks, 9/16, CRF -> AAF | 5.076480 ticks, 9/16, initial set |
| Uniform 0..5 us | 16 / 48 | 0 | 4.899840 ticks, 10/16, AAF -> CRF | 4.907520 ticks, 10/16, initial set |
| Uniform 0..2 us + probability 1e-4 of 0..24 us tail | 16 / 48 | 0 | 3.893760 ticks, 4/16, AAF -> CRF | 5.091840 ticks, 2/16, AAF -> CRF |
| Uniform 0..60 us | 16 / 48 | 0 | 2.565120 ticks, 0/16, CRF -> AAF | 2.234880 ticks, 9/16, AAF -> CRF |
| INTERNAL, 52 and 56 us holds | 32 / 32 | 0 | 4.984320 ticks, 56 us at 0/16 | 5.091840 ticks, 52 us at 14/16 |

The minima exceed the ruled one-tick floor. Before settling the maximum is
two slipped frames in each uniform campaign, three with the rare tail,
and one during an INTERNAL pull-in. The declared bound was not relaxed.
All stream-to-stream switches have zero slips before settling as well.
`stage2c/campaign-summary.json` names each extremal log and transition;
individual logs and campaign tables are retained beside it.

Empty margin is the first event's observed push-to-pop interval. Full
margin is the smallest interval from freeing a queue slot to reusing it,
over every push in the PDU. The observer follows the new four-bit pointers,
handles a drop followed by a pop, and observes pop before push in a shared
cycle. Both minima are executable checks. Slip grading starts at the
end of the PDU which made the recentre decision, with no 1 ms grace.

The loopback unit suite passes 408 checks. It pushes eighteen events into
the sixteen-entry queue, requires exactly two oldest drops, checks all
survivors in order and exactly two tail repeats. The recentre cases cover
five held pops and no sixth, one held pop, one oldest drop, no-op, unprimed,
flush and a pulse coincident with the first beat. Both pairs stay together
and declared recentres do not move either counter. The synthesized-netlist
leg also returned 0.

All five planted controls are caught by their named assertions:
NO-SETTLE, RENDER-ONLY, EARLY, W1 and OVERSHOOT. The last now plants target
seventeen, one beyond the depth, and fails the post-decision slip check.

The render law is asserted only with on-time arrivals and outside #643's
ambiguity window. The no-lateness switch campaign has 45/48 windows on the
law and three explicitly ungradable; the small INTERNAL campaign has
29/32 on the law and three ungradable. Every gradable on-time window passes.
The arrival-jitter campaigns prove slips and margins, not that separate
on-time law: their informational render summaries include 23 OFF THE LAW
tail windows and 48 ungradable wide-jitter windows. Lateness changes a PDU's
own fill/delay, so those summaries are not counted as law passes or failures.
`stage2c/render-law-gradability.json` preserves this distinction.
The sampled arrival models and offsets above do not claim arbitrary
network-delay or oscillator-offset coverage.

## Reproduction and traces

Use the pinned simulator and external scratch. Commands are from the
repository root unless a suite directory is stated.

```sh
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export PYTHONDONTWRITEBYTECODE=1
WORK=$(mktemp -d /tmp/ring-slip-review.XXXXXX)
make -j16 -C tb/verilator/follow_ring build MDIR="$WORK/model" VERILATOR_JOBS=16
python3 tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/switches" --jobs 8 --jitter-us 0 5 60 --hold-s 40 \
  --switch-hold-s 20 --extra --dwell-s 1.0
python3 tb/verilator/follow_ring/sweep.py b8 --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/tail" --jobs 8 --jitter-us 2 --tail-us 24 --tail-p 1e-4 \
  --hold-s 40 --switch-hold-s 20 --extra --dwell-s 1.0
python3 tb/verilator/follow_ring/sweep.py pullin --exe "$WORK/model/Vfollow_ring" \
  --out "$WORK/pullin" --jobs 8 --hold-us 52 56
MAKEFLAGS=-j16 VERILATOR_JOBS=4 python3 tb/verilator/follow_ring/mutants.py \
  --mdir "$WORK/mutants" --jobs 3
make -j16 -C tb/verilator/chmap_capture build MDIR="$WORK/chmap"
"$WORK/chmap/Vchmap_wrap"
```

The actual four arrival invocations ran independently and concurrently,
with one jitter value per output directory and separate log/rc files.
Builds used make -j16; compiler worker counts were bounded to fit 12 GB.
Independent suite groups also ran concurrently. Foreground status waits
were below ten minutes; all processes must finish before ending the session.

Current representative traces:

```sh
"$WORK/model/Vfollow_ring" --case b8 --dwell-s 1.0 --set-phase 0 \
  --seed 645 --jitter-us 60 --hold-s 16 --switch-hold-s 15 \
  --allow-ungradable --trace "$WORK/b8_trace.csv" \
  --servo-trace "$WORK/b8_servo.csv" --grid-trace "$WORK/b8_grid.csv"
"$WORK/model/Vfollow_ring" --case pullin --peer-ppm -5.10 --hold-us 52 \
  --latency-us 210.42 --after-s 2 --allow-ungradable \
  --trace "$WORK/pullin_trace.csv" --grid-trace "$WORK/pullin_grid.csv"
```

Both return 0 (29 and 8 checks). The wide-arrival trace has one pre-settle
slip and no later slip; minima 4.538880 empty / 2.641920 full ticks. Its
hold lengths differ from the campaign above, so its extrema are reported
separately. The INTERNAL trace restores fill fourteen and has no slips;
its margins are 5.337600 / 5.721600 ticks. `stage2c/traces/` contains logs,
servo history, PDU/grid excerpts and raw-file hashes. Grid samples are
1 ms apart; excerpt centres are sampled pending falls and locate the
pulse within that resolution. Files over 200 KB remain in scratch.

## Integration and gates

Completed:

- Capture coherence: rc 0, 20,832 junction checks, 332 complete-datapath
  checks and 30/30 mutation-runner checks. This rerun is complete.
- Default render: rc 0, 259 shipping-leg checks, 65 two-stream checks,
  and 5/5 no-rebuild controls.
- Portability: `bash syn/yosys/run.sh`, rc 0, including structural checks.
- Builder: `python3 sw/builder/test_builder.py --require-rv32
  --require-elaboration`, rc 0. Every elaboration arm ran. One historical
  Arty area-calibration arm is explicitly NOT RUN because its old placed
  report is absent; that arm is not counted as a pass.
- Source/doc gates: rc 0 for lint (90 violations within budget 90), source
  lists, interface contracts, idiom, naming, fail-fast, hygiene, test
  evidence, bare-metal scope, documentation style/paths/privacy, anchors,
  TOC and the added-line punctuation gate.

Complete datapath: rc 0 across its default configurations and controls.
The full render pull-in campaign also returned 0 across eighteen feed
phases, with zero post-settle loopback slips in all eighteen. Seventeen
phases grade the render law; +1042 is explicitly NOT GRADABLE because its
PDU end is four cycles from a pop, inside the nine-cycle ambiguity window.

Media-clock integration: rc 0, 31/31 control-runner checks.
Processor-shadow: rc 0, 311 checks with zero failures.

Aligner: rc 0, 45 checks and all three negative controls caught.

Vendor parser and all four OOC runs: rc 0; combined delta +80 LUT / +73 FF.

Physical gPTP: **rc 2**, 139 checks / 2 failures, 16.992510280 simulated
seconds (849,625,514 axis cycles), 3441.41 s wall clock. The reset-reacquisition
window reports four sample-order errors; the cumulative oracle reports
eight. Payload and AAF packet-sequence checks pass. The make target stops
at the failed physical leg. The accounting verifier was then run separately:
`python3 "$STAGE/tb/verilator/milan_dp_gptp/verify_abort.py"`, rc 0,
40 checks (6 setup-abort, 20 no-TX and 14 no-Pdelay) with zero failures.
This does not clear the failed physical leg. No test or acceptance criterion
has been weakened.

[#656](https://github.com/kebag-logic/milan-fpga/issues/656) already documents
139 / 3 at this lane's dev base `fea346e7`. Its
[separate diagnosis](https://github.com/kebag-logic/milan-fpga/issues/656#issuecomment-5986261146)
identifies the harness's exactly-48-kHz peer against the DUT's 47,999.49-Hz
INTERNAL grid and supplies a bench fix on another lane. This candidate's
139 / 2 with eight errors is **not a base-identical transcript**.

A print-only early-epoch probe reuses the positive run's DUT archive and
runs the existing bounded negative-control mode. That mode corrupts channel
3 and a peer timestamp at 1.2 s; the index oracle reads channel 0 and the
trace below precedes that timestamp. No RTL, checker or timing changes.

```text
TRACE SETTLE t=0.755754160 fill=2 dup=0 skip=0 source=0 err=14
TRACE ORDER t=0.755882000 last=36275 index=36275 step=0 fill=5 dup=0 skip=0
```

The ORDER line occurs four times in that outgoing PDU. Those repeats follow
the declared startup recentre and leave both slip counters at zero. This
locates four of the full gate's eight errors. The other four are in the
reset-reacquisition window and were not individually traced by this short
probe. #656's base trace instead shows one-sample gaps with `lb_skip`
advancing. The current failure therefore needs the declared-recentre
oracle reconciled with #656's clock-model correction, not a claim that
this is a base-identical run.

`stage2c/gptp-probe/` retains the observation patch, complete log, build
receipt, reproduction recipe and hashes of the reused DUT archive and
executables. The existing negative mode exits 1 (30 checks / 4 failures);
the trace collector's rc 0 only says it captured the requested evidence.
It is not a passing physical-gPTP verdict. Neither the #657 exception nor
the published #656 result waives the red positive gate. No other lane was
edited and no commits were imported.

LAW-boundary: **rc 0, 81/81 checks**, covering 564 windows across ascending,
descending and isolated-phase histories on the clean design and both
setpoint controls. The largest measured nearest-pop walk is three cycles,
within the harness's declared five. Ungradable windows remain ungraded;
the control must fail the named law checks wherever it is gradable.

Final-head route attribution is complete and within the ruled limit.
The physical gPTP failure prevents review readiness. Exact completed receipts and summarized large logs
are under `stage2c/`. The four base-identical render mutation failures
remain assigned to #657 by ruling; this lane does not change their tests.
The historical full campaign is 30/34 on this branch (28/32 at the dev
base); it is not reported as green or as a fresh stage-2c run.

Suites without external build-directory support run from an external copy
of tracked `tb/` files, with source/configuration directories linked to the
candidate. This is test staging, with no second checkout or branch.
Commands there use make -j16, VERILATOR_JOBS=4 and the suite's normal target;
render explicit targets run from inside `tb/verilator/milan_dp_render`:
`tdm8render-pullin PULLIN_JOBS=8` and
`tdm8render-law-boundary LAW_BOUNDARY_JOBS=4`.

## Area

The bar is the vendor OOC delta and the change's own routed cells, each
at most 120 LUT / 120 FF. Unrelated route variance is reported separately.
The vendor work waits on `$VIVADO_LOCK` without a lock timeout,
and starts after this lane's heavy builds finish.

OOC setup: shipping 1x1 capture parameters `N_SLOTS_P=4 N_TDM_P=8
TDM_FRAME_PAIRS_P=4 N_LB_STREAMS_P=1 N_LB_CH_P=8`, part
`xc7a100tfgg484-2`, 20 ns axis clock. The settle wrappers contain the
complete ordered #386 and added settle blocks. Their statements were
checked against the actual base/head datapath; historical routed base
RTL is byte-identical to dev. `stage2c/area-input-verification.txt` records
those checks. Preparation is reproducible with `stage2c/AREA-SOURCES.py`
and its accompanying `ooc.tcl`, writing sources to external scratch.

```sh
python3 "$OUT/stage2c/AREA-SOURCES.py" "$WORK/area"
cd "$WORK/area"
for tag in settle_base settle_head cmc_base cmc_head; do
  ONLY=$tag flock $VIVADO_LOCK "$VIVADO_BIN/vivado" \
    -mode batch -source ooc.tcl -nojournal -log "$tag.vendor.log" \
    > "$tag.vendor.out" 2>&1
  echo $? > "$tag.vendor.rc"
done
```

The shipping route uses `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`,
the AX7101 1x1 dry-run command, fresh firmware images and shipping constraints.
Recipe: `xc7a100tfgg484-2`, AreaOptimized_high synthesis, ExploreArea
optimization, ExtraPostPlacementOpt placement, AggressiveExplore physical
optimization/routing, 32 threads and the default seed. No bitstream is built.
The final checkpoint reports 107,006 routable nets, all fully routed, with
zero routing errors. Setup WNS is +0.004 ns, hold WHS +0.033 ns, TNS/THS zero,
and no setup/hold failing endpoints. These are single-recipe measurements;
the complete three-directive timing signoff remains outside this STOP handoff.

All four vendor OOC runs return 0:

| Block | Base LUT / FF | Head LUT / FF | Delta |
|---|---:|---:|---:|
| Settle | 41 / 51 | 67 / 92 | +26 / +41 |
| Capture | 1076 / 1336 | 1130 / 1368 | +54 / +32 |
| Sum | | | **+80 LUT / +73 FF** |

Both capture OOC designs infer one RAMB36 and zero LUTRAM, so the block-RAM
delta is zero. The storage geometry does not mandate a particular primitive.
This clears the OOC 120/120 bar.

The routed attribution also clears the bar: **at most 112 additional LUTs
and +73 FF attributable to the change**. This is a conservative LUT upper
bound, not an assertion that every counted LUT is newly added:

- The complete LUT fan-in of the 41 new settle registers, plus the pulse's
  combinational fan-out, contains 80 LUTs. One is inside capture and is
  counted in that module's delta. Six others have unchanged base functions
  and connections, after normalizing input ordering.
- Ten more are the pre-existing band-detector LUTs
  `media_grid_align/src_band_ticks_r[0]_i_6` through `_i_15`. Synthesis
  renamed their carry chain. An exhaustive comparison follows the actual
  LUT INITs and CARRY4 connections for all 65,536 values of registered
  `err_r[15:0]`: all ten functions are identical. An inverted-LUT control is
  caught. The primitive equations were checked against the installed
  library; only its source hashes and sizes are retained.
- Count every remaining cone LUT as added: 80 - 1 - 6 - 10 = 63.
  The whole capture module changes 1079 -> 1128 LUTs, a further +49.
  The conservative combined bound is therefore 63 + 49 = **112 LUTs**.
- New settle FFs are `settle_ceil_ticks_r_reg[20:0]` (21),
  `settle_run_ticks_r_reg[17:0]` (18), `settle_pend_r_reg` and
  `settle_recentre_p_r_reg` (one each). Capture adds 32 named FFs and removes
  none. Combined: 41 + 32 = **73 FF**. The cell lists retain every name.

Hierarchy names alone do not establish ownership: synthesis places some
new settle logic inside existing child hierarchies. The connection-based
cone above includes it. Raw route totals and variance are reported separately:

| Scope | Base LUT / FF | Head LUT / FF | Raw delta |
|---|---:|---:|---:|
| Whole design | 50,767 / 59,634 | 50,908 / 59,790 | +141 / +156 |
| Datapath own hierarchy | 563 / 2,805 | 572 / 2,957 | +9 / +152 |
| Capture | 1079 / 1321 | 1128 / 1353 | +49 / +32 |

The datapath's raw +152 FF includes the 41 new settle FFs and 111 retained
FFs in unchanged logic: 64 `gsi_gm_q`, 21 each `amap_edit_iclaim_expect`
and `amap_edit_iclaim_word`, two `amap_edit_remove` replicas, and one each
`aaf_follow_idx`, `tdmr_wr_en` and `gsiq_sel` replica. Other scopes net -28 FF.
The whole-design increase outside the attributed +73 is +83 FF. The
hierarchy-delta table reports the LUT and FF variance in every affected
scope. RAMB36, RAMB18, distributed RAM, SRL and DSP totals are unchanged.

The first full-route invocation returned 1 only after it had written the
routed checkpoint and all main reports: the final attribution query named
a net which optimization had removed. The corrected query follows the
actual settle-register connections and returns 0. It also regenerates
route status and timing from that checkpoint, reproducing the figures above.
Both checkpoint queries, the exhaustive comparison and the final area
comparison return 0. The original nonzero receipt is retained; it is not
relabeled as a clean full invocation. No DUT source changed for recovery.

`stage2c/vendor/` and `stage2c/route/` contain small reports, named cells,
proof results and reproducible recipes. Large checkpoints, netlists and
reports remain outside the evidence directory and have SHA-256/byte records.
To repeat attribution, set `BASE_REPORTS` and `HEAD_REPORTS` to the external
baseline/candidate report directories and run from the latter:

```sh
cd "$HEAD_REPORTS"
flock $VIVADO_LOCK "$VIVADO_BIN/vivado" -mode batch \
  -source "$OUT/stage2c/route/ownership.tcl" -nojournal \
  -tclargs "$HEAD_REPORTS/alinx_ax7101_route.dcp" \
  "$BASE_REPORTS/alinx_ax7101_route.dcp"
flock $VIVADO_LOCK "$VIVADO_BIN/vivado" -mode batch \
  -source "$OUT/stage2c/route/shared-logic.tcl" -nojournal \
  -tclargs "$HEAD_REPORTS/alinx_ax7101_route.dcp" \
  "$BASE_REPORTS/alinx_ax7101_route.dcp"
python3 "$OUT/stage2c/route/prove_shared.py" "$HEAD_REPORTS" "$HEAD_REPORTS"
python3 "$OUT/stage2c/route/compare.py" "$REPO" "$BASE_REPORTS" "$HEAD_REPORTS"
```

The parser passes at its unchanged ratchet: zero parent findings and four
existing findings in the pinned processor population.

The separate open-synthesis estimate maps through sv2v and
`synth_xilinx -family xc7 -noiopad`, all four lowering/mapping runs rc 0:

| Block | Base logic LUT / FF | Head logic LUT / FF | Delta |
|---|---:|---:|---:|
| Settle | 73 / 51 | 134 / 92 | +61 / +41 |
| Capture | 1265 / 1384 | 1240 / 1416 | -25 / +32 |
| Sum | | | +36 logic LUT / +73 FF |

Distributed memory changes from eight RAM32M to sixteen RAM64M. The raw
logic-LUT totals above exclude that memory and are not the vendor bar.

## Classification and options

Classification retained from the reproduced diagnosis: the servo locks
frequency only. At the measured 5.92 ppm INTERNAL-to-peer offset its
acquisition walks about 1.43 media ticks, with about 0.03 tick left after
LOCKED. The original #386 pulse occurs about 43 ms after the source change,
before that walk, and reaches only render. The old loopback queue therefore
remains near an edge, while a running render stream retains the phase
shift. An INTERNAL serial-clock hold moves that same grid without the old
source-change arm. These are missing post-transient recentres, not a
persistent frequency mismatch after lock. Stage-1 traces and controls are
in HANDOFF_STAGE1.md; the exact four target-eight overflow traces are in
HANDOFF_STAGE2B.md and stage2b/resume/.

Options from the diagnosis (historical prototype area, not current cost):

| Option | Area at 1x1 | Protocol-visible effect | Discriminating test |
|---|---|---|---|
| A: phase term in servo | +169 LUT / +129 FF, plus reference mux | changes media phase and loop/lock behaviour; does not repair the ring location or INTERNAL render shift | phase sweep plus servo/meter controls; zero phase gain restores the tail |
| B: aligner-band recentre | +9 LUT / +1 FF | one render discontinuity after INTERNAL pull-in; following acquisition still walks afterwards | both pull-in fold directions; removing the excursion arm retains the shift |
| C: later recentre to both rings | first prototype +55 LUT / +33 FF; current cost measured separately above | one declared settle action; diagnostic loopback delay grows; AAF latency law unchanged | four arrival campaigns, two INTERNAL hold sweeps, five planted controls, integration LAW and boundary tests |
| D: declare existing behaviour | 0 | leaves a later slip unbounded in time and retains shifted render latency | offset/phase sweep against an explicitly changed specification |


## Recommendation and limitations

The ruled option C is functionally supported by all four arrival campaigns
and both INTERNAL hold directions. Its implementation retains #386 and
adds the later action to both rings. The 64-PDU reference window remains
rejected: about 8 ms extra action delay with no arrival-bound proof.
The functional and vendor-area results support the ruled implementation, but
the physical gPTP gate prevents REVIEW READY. Its changed failure pattern
must be reconciled with #656. The vendor-area and one-tick-margin STOP conditions were checked and did
not fire.
The recommended next decision is to coordinate the physical gPTP bench
with #656: use its peer-clock correction and explicitly grade the declared
recentre separately from later ordering. A harness-only change costs zero
DUT LUT/FF and changes no protocol behavior. Its test plan must cover both
initial acquisition and reset reacquisition, require the declared action
to occur once with its bounded hold/drop, preserve zero errors outside that
action, and plant an extra unannounced repeat/gap which still fails. A
blanket extension of the warm-up exclusion would not supply that proof.
No such acceptance/checker change was made privately in this lane.

Physical bench confirmation belongs to the manager. Review, hosted gates,
merge-result validation and containment are not discharged by these desk
results.

## Execution notes and artifact policy

One first sweep launch put driver options after `--extra`; those four
attempts did not execute a simulation. Corrected launches completed all
runs above. The default interpreter lacked the pinned Markdown renderer;
those checks were rerun successfully with the installed renderer.
Export inventory initially failed after its external-output link had been
removed too early. Restoring the link completed preparation; generated
processor ROMs match byte for byte. No DUT source changed for these setup
corrections. Known generated links and bytecode directories were removed
from the source tree after routing; build data remains in external scratch.

The output directory contains prose, small logs, excerpts, recipes and
hash/size records. Toolchains, packages, build trees, tree exports and
files over 200 KB stay outside it. Historical stages remain in
`HANDOFF_STAGE1.md`, `HANDOFF_STAGE2.md`, `HANDOFF_STAGE2B.md`, `stage2/`
and `stage2b/`; historical evidence is labelled rather than presented as a
current pass.

Final workspace check: parent and all three pinned submodules are clean,
including ignored build output. Every manually inspected submodule root was
verified before its Git commands. All owned jobs have completed. The three
stage-2c commits have one-line subjects and empty bodies. Nothing was pushed.
