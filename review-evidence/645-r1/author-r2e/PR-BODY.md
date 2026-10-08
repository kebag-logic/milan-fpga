[A531]

## Contents

- **[Status](#status)** — Current head, verification, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2e](#round-2e)** -- Merge, current validation and disposition.
- **[Round 2d](#round-2d)** — R474-2's finding, its fix, the new case and controls, and the wording fixes.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`, including the
clean merge of dev `99e4eb6c`, the GMII capture fix and both requested wording
corrections. The sweep passed 61/61 with 2,185,760 checks; source/documentation
gates are 28/28. The known four #657 failures match dev.

The kept image, AltSpreadLogic_high, has +0.066 ns setup and +0.024 ns hold,
zero TNS/THS and a passing full IOB check. All three resource gates pass;
fresh own-area growth is +113 LUT / +78 FF against the 120 / 120 limit.
`645-ring-slip` -> `dev`. Independent reviews and the protected
publication/merge gates remain required. Earlier round results are historical.

## Linked Issue / roles

Closes #645
Closes #647
Relates to #629, #643, #657

Desk acceptance here does not discharge the issues' physical bench or release
obligations.

Executor: `[A531]`
Internal cleared-context reviewer: `[R474]`
External reviewer: `[R475]`

## Description

A late **settle recentre** fixes two residues of a media-clock transient:

- **#645.** The loopback ring keeps the servo's pull-in walk after a source
  locks, so it slips one frame 15 to 45 s later.
- **#647.** An INTERNAL aligner pull-in leaves a running stream's render
  latency shifted.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | Settle recentre armed by a CLOCK_SOURCE change, aligner re-engagement or an aligner excursion past a two-axis-cycle quiet band. It fires after 8 LOCKED servo windows (following) or 2,048 quiet ticks (INTERNAL), with a 2^20-tick ceiling. After an action, excursion arming waits for 2,048 consecutive quiet ticks (recovery qualification, one state bit, existing counter). |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | Loopback queue 16 deep, derived target 11. The settle action holds missing pops or drops exactly the excess, in lockstep across pairs. `SLIP_LB` does not count it. |
| `tb/verilator/follow_ring/` (new) | Real meter, CRF receiver, servo, NCO, aligner, loopback ring and render stage with the datapath's glue. Arrival campaigns (both offset signs, four envelopes, 16 phases), INTERNAL pull-in campaign, fine and paired pulls, controller regression at four clock rates, twelve planted controls, quiet-distribution reader. |
| `tb/verilator/chmap_capture/` | Symmetric action, a held walk before a pair's first commit counting no dup, the ruled two-PDU span check at six phases and on a two-talker fanout with offsets 0 to 5, and span controls. |
| `tb/verilator/milan_dp*/` | Physical wire check of each recentre's step and span; render pull-in leg; recentre controls. |
| Docs | `MEDIA_CLOCK_FOLLOWING.md` (contract, quiet band per clock rate, measured distribution, recovery window, declared residual), `TIME_SYNC.md`, `TESTING.md`, READMEs, regenerated module matrix (compiled sources only). |

No port or register-map change.

## Round 2d

[Round 2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032466525)
on [R474-2](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032462363).

- **R474-2-F1.** A held walk on a pair whose first commit of the PDU had not
  landed counted one `SLIP_LB` dup. `pop_dup_w` now excludes `pop_hold_w`.
  The action's pops, holds, drops and wire output are unchanged.
- **Standing case.** `[LRC]` drains a stream to zero left, pulses, drives
  only the decision beat, and walks before pair 1's first commit. It
  requires e6 five times, then e7, on both pairs, with zero dup and skip
  deltas. The same stimulus without the pulse must count exactly one dup,
  which proves the walk lands in that gap.
- **Controls.** HELD-DUP (every held pop counted) fails the new case, the
  `[LRC]` counter check and the span counter check. STARVED-HELD-DUP (the
  round-2c term) fails the new case and the `[LRC]` counter check, and no
  pre-existing check.
- **R474-2's probe P1** at this head: pulsed dup delta 0 (was +1).
- **Campaigns.** Quiet/arrival 128/128 with the reader PASS; INTERNAL
  pull-in 32/32. All 160 logs and the quiet-distribution JSON are
  byte-identical to round 2c, so the quiet distribution and the arrival grid
  are unchanged.
- **Area.** OOC own logic +113 LUT / +78 FF (limit 120 / 120). Only the
  capture head row changed; its 4 FF / 6 LUT drop from round 2c is synthesis
  replication variance, so +119 / +82 stays the conservative figure.
- **Timing gate: not met.** Synthesis now maps the LiteEth RX register
  `milansoc_phy_source_valid_reg`'s synchronous reset into a LUT in front of
  D (`eth0_rx_dv & ~eth_rx_rst`), so it cannot pack into the ILOGIC. Place
  30-722 follows, and the #475 check stops all three directives before
  routing. The remap is deterministic. Round 2c's inputs, re-synthesized
  today, still keep the reset on the pin. The only synthesized difference is
  this round's one term, so this is a latent fragility of the shipping
  build that the change happened to set off. The recommended fix is a
  separate Issue that makes the GMII RX IOB capture registers independent of
  control-set remapping; the handoff lists the options.
- **Wording.** `REGISTER_MAP.md` 0x8D4 reads "dropped events" verbatim.
  R474-2's `TIME_SYNC.md` sentence is 17 words, but the style gate allows
  10 per sentence in that file, so the same content is split into short
  sentences and line 492 is verbatim. The handoff shows both texts.

## Authoritative references

- [Round 2 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884),
  [two-PDU span ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440),
  [quiet-band and recovery ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115),
  [timing bar](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009790232).
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` (settle recentre), `docs/design/TIME_SYNC.md`,
  `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/integration/BUILDING.md` section 5,
  `REQUIREMENTS.md`.

## How to get into the same state

```sh
git fetch origin 645-ring-slip
git switch --detach 85db353400c6bf3965d279a9f5b5d47e08a0d1ed
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
for dependency in protocol-processor gptp-processor third_party/verilog-axis; do
    test "$(git -C "$dependency" rev-parse --show-toplevel)" = "$PWD/$dependency" || exit 1
    git -C "$dependency" rev-parse HEAD
done
# Expected pins are listed under Round 2e below.
```

Use Verilator 5.050.

## How to validate

```sh
S="$SCRATCH"                # set to an empty directory outside the tree
cd tb/verilator/follow_ring
make VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR=$S/fr
make sweep-pullin VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR=$S/pullin
cd ../../..
bash scripts/run_all_suites.sh $S/sweep
bash scripts/run_all_suites.sh $S/physical --physical-gptp
(cd tb/verilator/milan_dp_render && make tdm8render-pullin && make tdm8render-law-boundary)
python3 docs/traceability/gen_module_matrix.py --check
```

The full arrival campaign (128 runs) and its reader are in the handoff
packet; one run takes about 10 to 40 minutes.

Expected result / pass criteria: every command exits 0.

- `small pulls: 10/10 passed`, `follow_ring mutants: 12/12 caught`, and the
  settle controller PASS at 6.25, 25, 50 and 100 MHz.
- `follow_ring pullin campaign: 32/32 runs passed`.
- `quiet distributions: 128 phases, 512 windows, peak 1 axis cycles; band 2: PASS`.
- `chmap_capture`: `KL_chan_map_capture: 785 checks, 0 failures`.

The following table is historical Round 2d evidence, measured at `3eee12dc`
or Round 2d head `2525eae9`. Its intervening merges were `701b8332` and
`2525eae9`. Current merged-head evidence is reported under Round 2e below.

| Gate | Result |
|---|---|
| Arrival campaigns | 128/128 runs; quiet error within +/-1 axis cycle over 320,462,699 samples; one settle recentre per transient; no slip after it; minimum margins 2.17 (empty) and 2.24 (full) ticks; every log byte-identical to round 2c |
| INTERNAL pull-in | 32/32, byte-identical to round 2c |
| `chmap_capture` | 785 checks, 0 failures; netlist leg 20/0 |
| Default sweep | 61/61 suites, 2,185,420 checks, 0 failures; follow_ring controls 12/12 |
| Physical gPTP | 197 checks, 0 failures; two recentres on the wire at the exact step inside the span; counters unchanged; recentre controls 14/0 |
| Render pull-in, LAW boundary | 18/18 phases; 81/81 over 564 windows |
| Builder, selftests | rc 0 (builder's Arty calibration arm NOT RUN: build tree absent) |
| `mbx`, firmware unit job | at Round 2d head: 316, 361, 316 and 13 checks, 0 failures, mutants 5/5; 7/7 |
| Portability, vendor parser | 58 modules PASS; xvlog PASS at the ratchet, 0 findings in `hdl/` (Round 2d head) |
| Source and docs gates | 28/28 at Round 2d head |
| Timing | **FAIL**: synthesis rc 0; ExtraPostPlacementOpt, AltSpreadLogic_high and ExtraTimingOpt each stop at the IOB-pack check on `eth0_rx_dv` (Place 30-722); no bitstream, no WNS/WHS. Round 2c's `f6bd415f` gateware passed (+0.368 ns) |
| Own area | OOC +113 LUT / +78 FF (limit 120 / 120); round 2c's +119 / +82 is the conservative figure |

## Known limitations / out of scope

- **Declared residual.** A second INTERNAL pull that starts inside the
  previous action's recovery window gets no new recentre and may keep its
  render shift. The worst observed isolated window is 0.551 s. Continuing
  disturbances can extend it.
- **Loopback latency.** The diagnostic loopback target is 11 events, three
  ticks (62.5 us) later than 8. AAF presentation latency and the render law
  are unchanged.
- **#657.** Four render-mutation failures exist on `dev` as well; they are
  out of scope and the full mutation campaign is not claimed.
- **Not run here.** Hardware, flashing and the bench campaigns are outside
  this lane.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


## Round 2e

Assignment: [#645 comment 6050481968](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6050481968).
Starting head `2525eae9567865a8bc741901914bdf5a1caf2c26` was confirmed against
PR #672. Origin is `https://github.com/kebag-logic/milan-fpga.git`.

**Status: REVIEW READY**, head
`85db353400c6bf3965d279a9f5b5d47e08a0d1ed`.

Public handoff: [A531 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6056511818).

### Merge and wording corrections

| Commit | Change |
|---|---|
| `9a0d68e2016c0385171107277721aa187ce19674` | Merge dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` with `--no-ff`; clean automatic merge, no conflict resolutions |
| `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` | R474-3-R1: mutation-driver usage and four capture controls; R474-3-R2: TESTING.md links the complete twelve-control list |

Processor pin: `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
Time processor: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
AXIS: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
Each dependency's repository root was verified before its Git commands.
No RTL was authored in this round.

### Changed inputs and validation scope

| Merged input | Required evidence |
|---|---|
| Processor gitlink; mailbox RTL, generated contract and firmware | Full parent sweep, including datapath pool, loopback and render; physical-gPTP leg; firmware tests, RV32 build and coverage; source and protocol gates |
| Datapath NxN harness; simulation infrastructure and generated transmit chain | Full parent sweep; explicit render default, pull-in, LAW boundary and `tdm8render-mutants`; comparison with dev for #657 |
| Shared media-plane inputs and processor | follow_ring default and all twelve controls, 128 arrival cases and quiet reader, 32 INTERNAL pull-ins |
| GMII capture patch and build inputs | Builder including gate 23h; cycle fixture; shipping elaboration and full three-directive timing sweep with the complete IOB check |
| Resource baseline and measurement helper | `check` against the recorded route-1x1, ooc-1x1 and ooc-8x8 baselines; own logic compared with merged dev |
| Documentation and review wording | All 28 source/documentation gates |

### Functional results at the merged head

Shared infrastructure was treated as affecting the entire validation set.
`round2e/validation-scope.json` maps all 93 changed paths to their checks;
`round2e/merge-audit.json` records the automatic merge tree and zero conflict
resolutions. Credited commands returned 0 except the explicitly compared
#657 campaign below. Command vectors, working directories and return codes
are retained in `round2e/commands.json`, `round2e/jobs/` and
`round2e/source-gates/commands.json`.

| Gate | Result |
|---|---|
| Default sweep | 61/61 suites; 2,185,760 checks; zero failures, including datapath pool, loopback and render |
| Source/documentation gates | 28/28, rc 0 |
| follow_ring | Default suite, small pulls 10/10, all 12 mutation controls caught; settle controller at 6.25, 25, 50 and 100 MHz |
| Capture ring | 785 behavioral checks and 20 netlist checks, zero failures |
| Arrival campaign | 128/128; every log byte-identical to Round 2d; 384 post-settle windows with one settle pulse and render action, zero post-settle slip; minimum empty/full margins 2.17344 / 2.23488 ticks |
| Quiet reader | 128 phases, 512 windows; peak 1 axis cycle against band 2; statistics byte-identical to Round 2d |
| Standalone INTERNAL pull-in | 32/32, logs byte-identical to Round 2d; 28 on-law cases and four not gradable in the documented ambiguity band (two before, two after); one recentre and zero post-settle slip in every case |
| Full render pull-in | 18/18 phases, 558 checks, zero failures; all phases gradable; zero slip during the pull or after settling |
| Render LAW boundary | 81/81 checks over 564 windows; largest measured walk 3 cycles against the stated bound of 5 |
| Physical gPTP | 197 checks, zero failures: main 143, setup-abort 6, no-TX 20, no-Pdelay 14, recentre controls 14 |
| Firmware | Unit, NVM, RV32, tally, image and image controls rc 0; coverage gate passes all 20 files |
| Firmware mutations | 469/469 caught exactly once in four disjoint contiguous slices: 118 / 118 / 118 / 115; each command rc 0 |
| Specification suite | 14 features, 404 scenarios, 1,968 steps passed |
| Builder | rc 0, including gate 23h and all 5 missing-patch controls |
| Build-environment simulations | 5/5 simulations and 10/10 controls |
| GMII capture fixture | 1,036 cycle comparisons, nine direct pad registers, all 6 structure controls caught |
| Portability | 58/58 tops; tied-input check passes with two justified and zero unjustified ties; tap-purity check has zero violations |
| Vendor front-end | rc 0, zero findings across 81 owned RTL and 52 pinned processor files |

Four standalone 56-us pull-in cases, phases 0 to 3, each show one slip during
the pre-settle transient. This is unchanged from Round 2d; the claim is zero
slip **after** the settle. The full render campaign settles about 124,683,570
axis cycles (1,246.8 ms) after the hold. Detailed classifications and per-case
hashes are in `campaign-summary.json` and `render-summary.json` under
`round2e/`.

The physical trace independently observes both declared actions:

```text
RECENTRE WIRE decision=1 output_pdu=9822 declared_step=-5 observed_step=-5 events dup=0 skip=0
RECENTRE WIRE decision=2 output_pdu=95985 declared_step=-5 observed_step=-5 events dup=0 skip=0
```

See `round2e/physical/milan_dp_gptp.log` lines 518 and 689 and the retained
negative-control transcripts in `round2e/physical-controls/`.

### #657 comparison

| Revision | Result | Exit |
|---|---|---|
| Dev `99e4eb6c` | 28/32 passed; four known failures | 2 |
| Candidate `85db3534` | 30/34 passed; the same four failures | 2 |

All 32 shared outcomes match exactly, including the four failing lines:
the clean epoch leg, the acknowledgement-level and serial-reset arrival-skew
clean controls, and the surviving uncounted-repeat mutation. The candidate's
two additional checks pass: clean pull-in and the missing-settle mutation.
There is no observed merged-suite regression. This is the assignment's
accepted comparison, not a claim that the full mutation gate is clean.
Evidence: `round2e/mutation-comparison.json` and both campaign logs.

### Uncredited work and execution attempts

The optional external TSN field campaigns were skipped because their generator
is absent. Builder gate 11, the historical Arty calibration arm, was NOT RUN
because its report is absent. Neither is credited. Hardware, flashing and
bench campaigns remain outside this assignment.

Initial sweep preflights inherited ignored SIGHUP from their detached launcher
and failed their hard-HUP cancellation control before any suite ran. After
restoring the default signal disposition, both complete shards passed. The
initial specification-suite invocations used a missing executable and then an
incorrect working directory; the corrected complete invocation passed. The
first 8x8 elaboration used an incorrect configuration name and was corrected
before the successful elaboration. These attempts remain in the receipts.

The serial firmware mutation run was interrupted to partition it. Initial
interleaved `--mutation-shard INDEX 4` attempts trimmed the table before the
global named-test coverage check and reported uncovered tests; they were
interrupted and receive no validation credit. The documented
`--slice K/4 --jobs 4` invocations preserve that check and passed all 469
controls exactly once. The driver and coverage code are byte-identical to
dev `99e4eb6c`. See `round2e/firmware-sharding-comparison.json` and
`round2e/firmware-summary.json`.

### Three-directive shipping timing sweep

The sweep passes under the [#691 best-image ruling](https://github.com/kebag-logic/milan-fpga/issues/691#issuecomment-6045752839).
**Kept: AltSpreadLogic_high**, worst setup **+0.066 ns**, worst hold
**+0.024 ns**. Shipping synthesis and each implementation returned 0.
Every image passed constraint validation and manifest generation.

Values below are setup WNS / hold WHS in ns. The 0 C and 85 C reports give
the same values within each listed corner. TNS, THS and failing endpoints
are zero in all twelve reports; speed file is `-2 PRODUCTION 1.23`.

| Directive | Slow, 0 C and 85 C | Fast, 0 C and 85 C | Full IOB check | Margin grade |
|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.057 / +0.102 | +1.642 / +0.024 | 21 PASS, 1 INERT, 0 FAIL | Pass |
| AltSpreadLogic_high | +0.066 / +0.055 | +1.660 / +0.024 | 21 PASS, 1 INERT, 0 FAIL | Pass; kept |
| ExtraTimingOpt | +0.011 / +0.102 | +1.633 / +0.036 | 21 PASS, 1 INERT, 0 FAIL | Below +0.030 setup; not selected |

All nine GMII RX registers occupy ILOGIC sites in every row, including RX
valid at `ILOGIC_X0Y119`. The one INERT endpoint is `eth0_rx_er`: it
has no net and nothing drives or reads the pin, as the complete shipping
IOB checker verifies. There are zero critical warnings in synthesis and
each implementation. No rejected constraint was reported. The third row's
low positive setup result is recorded; it does not supply the kept image.

Evidence: `round2e/timing-summary.json`, per-directive corner reports and
critical-warning records, IOB reports, constraint return codes and manifests.
The kept bitstream is 3,825,992 bytes, SHA-256
`7b0c5eead7a68221c47e1f16077ec8ddbc3ca3631a033ff3e5e9235881c09977`.
Its manifest is 616 bytes, SHA-256
`76f092615a88014219ca74f234396a5680f040816e8202e66c93c22f2451859a`.
`round2e/kept-artifact.json` binds both to the candidate head.

### Resource checks and own-area limit

All three repository resource checks pass, rc 0, against the recorded
baseline. Each recipe identity matches. No baseline was changed.

| Endpoint | Baseline LUT / FF | Candidate LUT / FF | Delta LUT / FF | Candidate RAMB36 / RAMB18 | DSP | Result |
|---|---|---|---|---|---|---|
| route-1x1 | 49,957 / 54,274 | 49,913 / 54,309 | -44 / +35 | 74 / 27 | 14 | PASS |
| ooc-1x1 | 23,179 / 19,779 | 23,179 / 19,779 | +0 / +0 | 16 / 3 | 8 | PASS |
| ooc-8x8 | 30,135 / 27,380 | 30,135 / 27,380 | +0 / +0 | 21 / 5 | 8 | PASS |

The route is complete with no unrouted net or routing error. Its slice count
is 15,754 versus 15,734 (+20), with 87.5 BRAM tiles unchanged. The recorded
route recipe's WNS is +0.057 ns versus +0.124 (-0.067); WHS is +0.024 ns
versus +0.031 (-0.007). All are within the recorded policy. RAM and DSP
comparisons are retained in each endpoint report. OOC timing is characterization;
the shipping sign-off result is the kept image reported above.

The separate own-area comparison uses the exact dev and candidate capture
and settle logic, shipping 1x1 generics, and a 20 ns axis clock:

| Component | Dev LUT / FF | Candidate LUT / FF | Delta LUT / FF |
|---|---|---|---|
| Settle and existing source recentre | 41 / 51 | 74 / 93 | +33 / +42 |
| Capture ring | 1,076 / 1,336 | 1,156 / 1,372 | +80 / +36 |

**Own delta: +113 LUT / +78 FF; limit 120 / 120: PASS.**
The four separate synthesis commands and the area grade returned 0.
Evidence: `round2e/resource-summary.json`, the three resource-check logs,
`round2e/area-ooc/comparison.json`, and `round2e/area-source-audit.json`.
The GMII good/bad placement fixture also returned 0.

### Disposition and recommendation

**REVIEW READY at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`.** The assignment's merge, both wording
corrections and affected verification are complete, with the expressly
accepted #657 comparison. No STOP condition was triggered. This is an author
handoff; independent review and the protected publication/merge gates remain
required.

Recommendation remains option C, the implemented correction of both rings.
Its fresh own-area result is +113 LUT / +78 FF, and the
kept shipping image clears the timing and IOB bar. The classification,
protocol-visible effects, alternatives and test plans retained in
`HANDOFF.md` remain applicable. Alternative prototype area figures are historical, not
new measurements. The declared residual remains a second INTERNAL pull
starting during the previous action's recovery window. The diagnostic
loopback target remains 11 events; the AAF presentation law is unchanged.

The final tree and all three dependencies are clean at the recorded pins.
Both new first-parent commits have one-line subjects and no body or trailers.
Every job has ended. Peak service memory was
13.357 GB, below 17 GB. Vendor jobs
ran serially under the shared lock; the 8x8 OOC job waited behind another
service's run. No heavy functional build overlapped a vendor job in this
service. See `round2e/final-audit.json`, the command receipts and
`round2e/vendor.log`.
