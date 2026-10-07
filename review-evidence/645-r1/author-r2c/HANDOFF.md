[A531]

# Round 2 handoff (#645, #647): quiet-band arm, recovery qualification and symmetric settle action

Head: `886e16201654ba0fd0c60c41c228ea4c75b2f6d3` (branch `645-ring-slip`, target `dev`).
Live `dev`: `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`, merged with `--no-ff`
at the head. Origin: `https://github.com/kebag-logic/milan-fpga.git`.
Executor `[A531]`; reviewers `[R474]` (internal) and `[R475]` (external).
Nothing pushed. No port, register-map or parameter change beyond the ruled
localparams. Status: **every local gate complete; REVIEW READY posted with this head.**

## Authority

- [Original assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5981976917).
- [Round 2 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884),
  amended by the [two-PDU span ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440)
  and the [quiet-band and recovery ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115).
- [Timing bar: best of the three-directive sweep](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009790232),
  as `docs/integration/BUILDING.md` section 5 defines it.
- `REQUIREMENTS.md`, `docs/design/MEDIA_CLOCK_FOLLOWING.md`,
  `docs/design/TIME_SYNC.md`, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`.

The takeover comment for this round is 6010644995; it was not repeated.
Nothing here is a review verdict or a lens ledger: the negative findings
of R474-1 and R475-1 await independent re-review at this head.

## Commits this round (on top of `583f93a3`)

| Commit | Content |
|---|---|
| `639814a1` | Two-axis-cycle quiet-band arm, recovery qualification (one state bit, the existing dwell counter), recovery watch, fine-pull and paired-pull cases, three planted controls, controller regression at four clock rates, quiet-distribution reader |
| `4bddd95e` | Measured recovery windows and the declared residual in `MEDIA_CLOCK_FOLLOWING.md` |
| `31538f4b` | Quiet-band settling text; render harness comment on its focused coverage |
| `132d79e7` | `--no-ff` merge of dev `30e3c018` (#658, #670): reader-disposition table moved into `scripts/measure_test_evidence_readers.py`, `milan_dp/Makefile` resolved keeping both target sets |
| `5afae068` | `--no-ff` merge of dev `bd884631` (#676): adds only `docs/findings/667_TALKER_START_BENCH.md` |
| `b00df050` | States the measured 128-phase quiet distribution behind the arm |
| `33c951fc` | Corrects the 56 us pull-in slip count (4 phases, not 3) and widens the declared-transient measurement scope to both offset signs and the 0 to 60 us envelope |
| `9e529b20` | `--no-ff` merge of dev `6714181d` (#674, #675): docs, firmware unit tests, CI scope scripts and the `mbx` harness header; no file conflicts and no file of this lane touched |
| `f6bd415f` | `--no-ff` merge of dev `6a05347d` (#680): AAF packetizer startup admission (`KL_aaf_packetizer.sv`, +8 lines), its `aaf` startup suite and text; `TIME_SYNC.md` and the reader table auto-merged with this lane's edits |
| `4951c471` | `--no-ff` merge of dev `79b086d4`: per-suite default time limits in `run_all_suites.sh`, test-evidence scripts and documentation; `TESTING.md` and the milan_dp README auto-merged |
| `0a196192` | `--no-ff` merge of dev `910f338d`: firmware RV32 test tooling, `ci_events.py` and documentation; no HDL, testbench, harness or build input |
| `886e1620` | `--no-ff` merge of dev `09f1841b` (#665 FC): mailbox RTL and its `mbx` suite, mailbox generator, control-plane firmware and documentation; the mailbox is not in the AX7101 shipping file list |

`b00df050` and `33c951fc` change documentation only
(`round2c/resume/final-doc-identity-k.json`). The `9e529b20` merge changes no
HDL, synthesis, constraint or configuration file
(`round2c/resume/dev-merge-identity-m.json`). The `f6bd415f` merge changes the
AAF packetizer, so every gate that elaborates it was rerun at `f6bd415f`
(`round2c/resume/dev-merge-identity-f.json`). This lane's own sources
(`milan_datapath.sv`, `KL_chan_map_capture.sv`) and the follow_ring and
chmap_capture harnesses are byte-identical from `132d79e7` to the head. The
source exports used for the functional gates match `f6bd415f` blob for blob,
submodules included (`round2c/resume/export-identity-f6bd415f.json`). The
`4951c471` merge changes no HDL, harness, constraint or build input
(`round2c/resume/dev-merge-identity-g.json`). Its runner change only moves
default per-suite time limits, and every sweep here ran under an explicit
`SUITE_TIMEOUT` override, so the `f6bd415f` functional and timing evidence
covers the head. The source and docs gates and the changed evidence selftest
were rerun at `4951c471`. The `0a196192` merge changes only firmware test
tooling, `ci_events.py` and documentation (`round2c/resume/dev-merge-identity-h.json`);
the source and docs gates and dev's firmware-unit job were rerun at it. The
`886e1620` merge changes the mailbox RTL, which the shipping AX7101 image does
not elaborate, its `mbx` suite and the control-plane firmware
(`round2c/resume/dev-merge-identity-j.json`). The `mbx` suite, portability,
the vendor parser, the firmware-unit job and the source and docs gates were
rerun at `886e1620` (`round2c/gates-j/`, `round2c/vendor-j/`).

## Response to the negative reviews

This maps findings to changes and evidence. Classifications stay the reviewers'.

| Finding | Change | Evidence at this head |
|---|---|---|
| R474-1 F1: full-side asymmetry | From the full side the action drops exactly the excess above the target in every pair, in lockstep, counters unchanged; reversed offset sign added to the campaigns | `[LRC]` ten-left case and its SINGLE-DROP control; fast-sign campaigns (ring at the full edge at the switch) 64/64 |
| R475-1 F1: output-PDU span | Ruled rule: the action's repeats or drops are consecutive events within at most two consecutive output PDUs of each output, exact count, nothing outside, no grace | Six-phase capture span check, two-talker fanout, enable offsets 0 to 5, three span controls (non-consecutive, third PDU, extra repeat); physical wire check |
| R474-1 F2: sub-arm INTERNAL pull | Arm on any excursion past the two-cycle quiet band; arm disabled after an action until 2,048 quiet ticks; declared residual for a second pull inside that recovery | Full quiet distributions; fine pulls at 1/64-sample quanta; paired inside/outside pulls; NO-RECOVERY, HIGH-ARM and QUIET-ARM controls |
| R474-1 F3 / R475-1 F3: traceability | The generator credits only compiled sources; `follow_ring`'s text-copied datapath glue is marked, not credited | `gen_module_matrix.py --check` in the 28 source gates |
| R474-1 F4 / R475-1 F2: disengaged timing | `MEDIA_CLOCK_FOLLOWING.md` states the same 2,048-tick run, engaged or disengaged | Controller regression, disengaged leg, four rates |

## Classification (unchanged) and repair

#645 is the servo's pull-in phase walk accumulated in the diagnostic
listener loopback ring, outside the #386 at-switch render recentre: about
1.43 samples of walk, 0.03 sample left after LOCKED. #647 is a render-law
shift left when the INTERNAL aligner moves the grid under a running stream,
which armed no recentre. The stage-1 reproduction, traces and
classification evidence are in `HANDOFF_STAGE1.md` and `traces/`; they are
historical, not acceptance for this head.

Repair (option C as ruled): one settle recentre per transient, after the
servo reads LOCKED for 8 windows under following, or after the aligner
rests in its settle and quiet bands for 2,048 ticks at INTERNAL. A 2^20-tick
ceiling still applies. It reaches the render stage and every loopback pair.
The loopback queue is 16 deep with the derived target 11. Fewer than five
events left holds the missing pops; more than five drops exactly the excess,
in every pair together. The slip counters do not move; the render stage
counts it as a recentre.

Round 2's arm: the absolute aligner error strictly above two axis cycles
(320 ns at 6.25 MHz, 80 ns at 25 MHz, 40 ns on the shipping 50 MHz shapes,
20 ns at 100 MHz), outside recovery. After every action the arm stays off
until the engaged aligner spends 2,048 consecutive ticks inside the band;
source changes and re-engagement still arm at once.

## Quiet distributions (ruling 6010634115, item 1)

| Campaign | Cases | Windows | Samples | Quiet error | Band check |
|---|---:|---:|---:|---|---|
| Candidate (this implementation) | 128/128 rc 0 | 512 | 320,462,699 | -1..+1 axis cycle | band 2 = 2 x 1: PASS |
| Baseline (preserved four-band arm) | 128/128 rc 0 | 512 | 320,462,699 | -1..+1, identical histograms | PASS |

Phases are 16 set phases x {slow -11.02 ppm, fast +0.82 ppm against INTERNAL
-5.1 ppm} x {no lateness, 0 to 5 us uniform, 2 us plus a 1e-4 tail to 24 us,
0 to 60 us uniform}. Quiet windows are selected by stimulus time. Each run's
`[STEADY]` checks (no settle pulse, no excursion arm and no pending settle in a
quiet window) are counted in its tally; all 128 candidate runs report zero
failures. Every candidate run has exactly one settle recentre and one render
recentre per transient (384 windows), with zero loopback slips after it. The
histograms are identical sample for sample because the arm does not feed the
aligner. Of the baseline cases, 56 rest on
`round2c/resume/baseline-recovered-receipts.json`: the original driver's rc
line, plus log and binary SHA-256 values re-verified against the graded logs.

Arrival margins after the settle recentre, candidate, minimum per envelope (ticks; bar 1):

| Envelope | Empty side, slow / fast | Full side, slow / fast | Pre-settle slips max, slow / fast (bound 3) |
|---|---|---|---|
| none | 4.984 / 5.030 | 5.084 / 5.023 | 2 / 2 |
| 0 to 5 us | 4.846 / 4.854 | 4.908 / 4.908 | 2 / 2 |
| 2 us + 24 us tail | 3.848 / 3.802 | 5.100 / 5.030 | 3 / 2 |
| 0 to 60 us | 2.173 / 2.665 | 2.235 / 2.327 | 2 / 2 |

Stream-to-stream switches slipped nothing in any envelope. Late-arrival runs
report rather than grade the render law where #643's ambiguity window makes
it ungradable; the fine-pull and INTERNAL campaigns grade the law.
Receipts: `round2c/campaigns/summary.json` and per-group margins and inventories.

## Recovery and the declared residual (items 2 to 4)

All seven nonzero fine holds (25 MHz, 1/64-sample quanta) give exactly one
action. The one-quantum hold peaks at +9 axis cycles and arms. Every
completed recovery holds exactly 2,048 quiet ticks. The worst isolated
recovery window observed is 0.551148640 s (56 us hold at 6.25 MHz); the
longest fine-hold window is 0.538336080 s. Further disturbances can extend
the window without bound; the design document says so.

A second hold starting 0.10 s after an action, inside the measured
0.409918800 s recovery, gets no second action and keeps its render shift, as
declared and graded. The same hold at 1.50 s gets one new action and the law
back. The stimulus is checked against the actual recovery state.

Controls, each failing its named check (follow_ring `mutants.py`, 10/10):
NO-RECOVERY (two actions for one hold), HIGH-ARM (misses the +9 pull),
QUIET-ARM (arms in quiet), plus NO-SETTLE, SINGLE-DROP, EARLY, RENDER-ONLY,
OVERSHOOT, W1 and NO-ARM.

INTERNAL pull-in campaign (`make sweep-pullin`, 16 feed phases x 52 and
56 us holds) at `b00df050`, executable-identical to this head: 32/32 rc 0.
Every phase gets one settle recentre, 0.854 s and 0.190 s after the hold, and
no loopback slip after it. At 56 us, feed phases 0 to 3 slip once before the
settle (the declared transient). Four windows fall in #643's ambiguity window
and are reported. Table: `round2c/final-pullin/pullin.md`.

## Evidence status

| Evidence | Tree | Result |
|---|---|---|
| Source and docs gates (28 commands, including the module matrix check and the evidence selftest) | `886e1620` (also `0a196192`, `4951c471`, `f6bd415f`, `9e529b20`, `33c951fc`) | 28/28 rc 0; `measure_test_evidence_selftest.py` rc 0 at `4951c471` |
| `mbx` suite (the only suite reading the mailbox or the changed firmware sources), with the runner's verdict | `886e1620` | Wishbone 316, AXI4-Lite 361 and host model 316 checks, 0 failures; mutants 5/5 caught; verdict rc 0 |
| Default sweep shard 0/2 (60 suites, including aaf with dev's new startup sweep, follow_ring with its fine pulls, controller and ten controls, chmap_capture with the span checks, render, mclk, mbx and pp_shadow) | `f6bd415f` | 60/60 suites, 2,171,991 checks, 0 failures, rc 0 (four declared tsn_fuzz skips: generator absent) |
| Default sweep shard 1/2 (`milan_dp`, all legs) | `f6bd415f` | 12,064 checks, 0 failures, rc 0 |
| Default sweep total | `f6bd415f` | 61 suites, 2,184,055 checks, 0 failures |
| Physical (`--physical-gptp`) | `f6bd415f` | 197 checks, 0 failures, rc 0; 16.993 s simulated; two recentres on the wire, step -5 exact, inside the two-PDU span; recentre controls 14/0 |
| Render pull-in (`tdm8render-pullin`, 18 phases) | `f6bd415f` | 18/18 runs, 31 checks each, 0 failures; one settle recentre 1246.8 ms after the hold, no loopback slip; rc 0 |
| LAW boundary (`tdm8render-law-boundary`) | `f6bd415f` | 81/81 PASS over 564 windows, largest walk 3 cycles (stated 5); rc 0 |
| Builder (`--require-rv32 --require-elaboration`) | `f6bd415f` | rc 0, all gates pass; one arm NOT RUN for a recorded reason (gate 11 needs an Arty build tree absent from this host), as in earlier rounds |
| Source-list and wire-truth selftests | `f6bd415f` | rc 0, rc 0 |
| Portability (`syn/yosys/run.sh`) | `886e1620` (also `f6bd415f`) | 58 modules PASS including `KL_mbx`, tap purity PASS, rc 0 |
| Vendor parser (`xvlog_gate.py --check`, lane tree, shared lock) | `886e1620` (also `f6bd415f`) | PASS, rc 0: 0 findings in `hdl/`, 2 in the pinned processor equal to the ratchet |
| Dev's firmware-unit job (tally and RV32 selftests, control-plane and saved-state suites with the RV32 builds, coverage selftest and ratchet) | `886e1620` (also `0a196192`) | 7/7 rc 0: 18/18 and 28/28 planted cases, RV32 selftest 17 checks, control-plane PASS, 434 saved-state tests over 5 shapes, coverage PASS |
| Quiet distributions and arrival campaigns | models whose inputs are byte-identical at the head | 256/256 runs, readers rc 0 |
| INTERNAL pull-in campaign | `b00df050`, inputs byte-identical at the head | 32/32, rc 0 |
| Timing, three directives (best qualified image graded) | `f6bd415f` gateware; no gateware input changed through the head | ExtraPostPlacementOpt +0.368 ns WNS, minimum WHS +0.034 ns: PASS (at `132d79e7`: AltSpreadLogic_high +0.261 / +0.036) |
| Own area (OOC, own-logic rule) | `132d79e7`; own sources byte-identical at the head | OOC +119 LUT / +82 FF; routed bound +92 LUT / +80 FF at `132d79e7` (limit 120 / 120) |

Timing at the head's gateware (`f6bd415f` content, re-elaborated and
rebuilt), all corners at 0 and 85 C (setup WNS / hold WHS, ns). The shipping
1x1 TDM8 recipe was used: synthesis with one synthesis thread to a saved checkpoint,
then a fresh 32-thread implementation per placement directive, the
timing-grade hook, bitstream, rejected-constraint check and flash manifest.

| Directive | Slow | Fast | Critical warnings | |
|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.368 / +0.062 | +1.633 / +0.034 | 0 | selected |
| AltSpreadLogic_high | +0.039 / +0.102 | +1.434 / +0.019 | 1 (`Route 35-39`) | meets the margin |
| ExtraTimingOpt | +0.017 / +0.102 | +1.536 / +0.036 | 1 (`Route 35-39`) | below +0.030, recorded, not selected |

TNS, THS and failing endpoints are zero everywhere; speed file `-2 PRODUCTION
1.23`. All three runs produced bitstreams and manifests, with no rejected
constraint (`12-4739`, `20-1307`, `12-5201` absent). `Route 35-39` is the
intermediate route-slack warning that post-route optimisation clears. The
re-elaborated project equals the earlier one apart from dates, a comment's
order and the flash manifest (`round2c/timing-f6bd415f/elaboration/elaboration-compare.json`).
Receipts: `round2c/timing-f6bd415f/timing-current/` (per-directive corner
tables, CDC, exceptions, clock interaction, DRC, critical-warning census,
artifact hashes) and `sweep-grade.json` (rc 0). For reference, the dev
`28f9666f` manager table read +0.032, +0.345 and +0.164 ns, and this lane at
`132d79e7` read +0.129, +0.261 and +0.013 ns (`round2c/timing-current/`).
Placement in a sweep is noise-dominated; the gate grades the best image.

Area: OOC own logic +119 LUT / +82 FF (limit 120 / 120) at `132d79e7`, whose
own sources are byte-identical at the head; routed own-logic bound +92 LUT /
+80 FF in that image. Receipts: `round2c/area-ooc/`, `round2c/area-route/`.

## Reproduction

Use scratch outside the tree. Pins: processor `ead80360`, time processor
`5dce647a`, AXIS `48ff7a7e`; verify each dependency's repository root before
running Git inside it. `PACKET` is this handoff's directory.

```sh
REPO=$LANES/645-ring-slip
SCRATCH=$VALIDATION_STORAGE/645-a531/reproduce
SIM=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
cd "$REPO/tb/verilator/follow_ring"
make VERILATOR="$SIM" VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR="$SCRATCH/fr"
make sweep-pullin VERILATOR="$SIM" VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR="$SCRATCH/pullin"
make build VERILATOR="$SIM" VERILATOR_JOBS=2 MDIR="$SCRATCH/model"
python3 -B "$PACKET/round2c/campaign.py" --repo "$REPO" \
  --exe "$SCRATCH/model/Vfollow_ring" --out "$SCRATCH/campaign" --jobs 4
python3 -B quiet_distributions.py "$SCRATCH/campaign" --band 2 \
  --out "$SCRATCH/quiet.json"
cd "$REPO"
bash scripts/run_all_suites.sh "$SCRATCH/sweep"
bash scripts/run_all_suites.sh "$SCRATCH/physical" --physical-gptp
```

Expected: every command rc 0; campaign 128/128; `quiet distributions: 128
phases, 512 windows, peak 1 axis cycles; band 2: PASS`; the default `make`
ends `small pulls: 10/10 passed` and `follow_ring mutants: 10/10 caught`;
pull-in `32/32 runs passed`. `round2c/campaign.py` is scratch tooling, not
committed.

## Options and recommendation

| Option | Area | Protocol-visible effect | Test plan |
|---|---|---|---|
| A: servo phase feedback | historical OOC prototype +169 LUT / +129 FF | changes loop dynamics; does not restore an INTERNAL render phase | offset, arrival and phase sweeps; zero-gain control; integration |
| B: render-only correction | historical OOC prototype +9 LUT / +1 FF | fixes the render shift, leaves the loopback slip | both directions, fine boundaries, exact law, missing-arm control |
| C (implemented): both rings, quiet-band arm, qualified recovery | OOC +119 LUT / +82 FF; routed bound +92 / +80 | one exact consecutive action inside two output PDUs per output; counters and AAF presentation law unchanged; diagnostic loopback target 11 (+62.5 us over 8) | quiet and arrival distributions, fine and paired pulls, span and fanout controls, integration, area and timing |
| D: keep the behaviour or widen the residual | none | leaves a shift or slip outside the ruled residual | needs a new public decision |

Recommendation: C as implemented. The one declared residual is a second
INTERNAL pull starting inside the previous action's recovery window.

## Operational notes (not results)

- Dev moved four times during this resume. Each move was merged with
  `--no-ff`, and every gate whose inputs changed was rerun at the new head.
- The first vendor synthesis at `f6bd415f` content was stopped by this lane's
  own memory guard (rc -15, service peak 8.816 GB) after the reclaim threshold
  had been lowered mid-run. It was rerun with the earlier recipe's 8.75 GB
  threshold and an 8.95 GB guard (under the 9 GB ceiling); the synthesis then
  peaked at about 8.75 GB. Two driver mistakes (a path assertion and the wrong
  interpreter for the constraint checker) stopped the driver between vendor
  steps without affecting any vendor run. Receipts in
  `round2c/timing-f6bd415f/run/`; nothing from the stopped attempt is credited.

- A previous session ended on a service capacity error mid-run; its
  interrupted shard 0/2 and campaign cases were rerun, never credited.
- On resuming, overlapping launches briefly ran up to three writers per case
  log for under two minutes. All were stopped and every affected case was
  rerun by one driver (`round2c/resume/duplicate-start-a531k.json`).
- One gate relaunch ignored SIGHUP in its children, so the sweep's own
  hard-HUP cancellation control timed out in preflight (rc 2). It was
  relaunched without that; nothing from it is credited
  (`round2c/resume/gate-launch-nohup-abort.json`).
- Earlier resource interruptions, vendor scheduling, the memory guards
  and their receipts are described in `HANDOFF_ROUND2C_INTERIM.md`.

Large logs, checkpoints and executables remain in
`$VALIDATION_STORAGE/645-a531/round2c/`; this packet keeps text receipts under
200 KB, with size and SHA-256 for the rest. Hardware, flashing, push and PR
edits were not performed.
