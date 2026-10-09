[A531]

## Contents

- **[Status](#status)** — Current head, verification, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2g](#round-2g-default-suite-wall-clock)** -- Default-suite split, measured headroom and campaign ownership.
- **[Round 2f](#round-2f-merge-result-resource-re-baseline)** -- Merge-result resource records and repeated verification.
- **[Round 2e](#round-2e)** -- Merge, current validation and disposition.
- **[Round 2d](#round-2d)** — R474-2's finding, its fix, the new case and controls, and the wording fixes.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOP at `1e79ebdc06528edff74c0a7f530f20f99e3326a2` pending manager publication and a
passing exact-head hosted `verilator-suites` result. Both cold defaults
meet the assigned scaled limit; the moved campaigns and assigned command
checks pass. The builder's historical gate 11 remains explicitly uncovered.
REVIEW READY follows the required hosted result and independent re-review.

Round 2f was REVIEW READY at `4640d995913cb93653a47e73856e8bd7dfe7c428`. It merges dev
`6aa25dec` and records all three resource endpoints on that merge result,
with unchanged policy. Route WNS/WHS are +0.299/+0.031 ns. Assigned final
verification commands passed; the unrelated historical calibration arm
without its placed report remains explicitly uncovered. The Round 2f
section gives the current results and remaining integration obligations.

Previous round-2e status: REVIEW READY at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`, including the
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
git switch --detach 4640d995913cb93653a47e73856e8bd7dfe7c428
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/lwSRP
for dependency in protocol-processor gptp-processor third_party/verilog-axis third_party/lwSRP; do
    test "$(git -C "$dependency" rev-parse --show-toplevel)" = "$PWD/$dependency" || exit 1
    git -C "$dependency" rev-parse HEAD
done
# Expected pins are listed under Round 2f below.
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
`2525eae9`. Current merged-head evidence is reported under Round 2f below.

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


## Round 2f: merge-result resource re-baseline

[Assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6061613334), following the [composition review](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6061607463).

Status: REVIEW READY.
Public handoff: [A531 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6066156323).
Final head: `4640d995913cb93653a47e73856e8bd7dfe7c428`.
Records commit: `Re-baseline merged listener settle resource records`.
Measurement head: `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
It merges requested dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246` into
round-2e head `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` with `--no-ff`.
The merge had no conflicts. Its tree, `47e1e22d511016d3772c33419afc84ca88930f55`,
is exactly the composition review's candidate tree.
Required dependencies were initialized; each root was verified before its
repository commands. Pins: processor `2ad2f845`, time-sync processor
`5dce647a`, streaming library `48ff7a7e`, reservation library `9197193e`.
`resource-receipts/merge-admission.json` records full identities.

### Measurements and policy

The preceding records describe #686's inputs at `e519e31f`.
All three comparisons against those records exited 0 before any record
was replaced. Every `record --write` also exited 0.

| Endpoint | LUT (delta) | FF (delta) | Slices (delta) | RAMB36 / RAMB18 | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|
| route-1x1 | 50,267 (-124) | 54,413 (+150) | 15,779 (-9) | 74 / 27 | 14 | +0.299 / +0.031 |
| ooc-1x1 | 23,179 (0) | 19,779 (0) | - | 16 / 3 | 8 | -3.562 / +0.159 |
| ooc-8x8 | 30,135 (0) | 27,380 (0) | - | 21 / 5 | 8 | -2.278 / +0.159 |

Every RAMB36, RAMB18 and DSP delta is zero. Route CARRY4 changes by +30;
standalone CARRY4 is unchanged. The route leaves 71 slices free.
WNS improved by 0.058 ns and exceeds the +0.030 ns floor by 0.269 ns.
WHS improved by 0.002 ns and exceeds its zero floor by 0.031 ns.
There are no unrouted nets or routing errors; the full IOB check passes.
Slow corners at 0 and 85 C have WNS/WHS +0.299/+0.063 ns; fast corners
have +1.434/+0.031 ns. The critical setup path has 14 levels and 9.294 ns
data delay, including 7.331 ns of routing.
Standalone timing has no I/O constraints and does not establish an 8x8 route.

All measurement identities match the preceding baseline. Both integrated
runs and both standalone runs use one synthesis worker; the route keeps
the recipe's `ExtraPostPlacementOpt` placement and 32 general workers.
The 8x8 integrated run supplies bound parameters, and the standalone
clock is the shipping 20 ns. The four processes ran serially under the
shared lock, with no heavy functional build overlapping them.
Peak sampled service memory during measurement: 13,151,162,368 bytes, below 17 GB.

Policy is unchanged. Its canonical SHA-256 before and after is
`f0e6babaeeff50eb098f3ea2e55ca8cd76ee746f83134f44c6c958f85a581158`.
Every stored record equals the measured record. The budget still records
the unmet 60% LUT target: this route is 12,227 LUTs over it. At the new
WNS record, the unchanged 0.25 ns fall rule requires a comparable candidate
to retain at least +0.049 ns; the absolute floor remains +0.030 ns.

### Reproduction and receipts

The standing recipe is `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
`resource-receipts/measure-commands.json` contains every executed argument
vector, working directory, rc, elapsed time and sampled memory peak.
`ax7101-argv.json` and `ax8x8-argv.json` retain the shipping elaboration
arguments from the builder dry runs; only the external output destination
and omission of `--build` separate elaboration from the recipe steps.
Use those arguments at the measurement head with the same patched build
environment. The recipe helper was given `--single-thread-synthesis`;
standalone exports additionally received `--integrated-clock` and their
completed integrated log. Executed Tcl is retained for all four runs.

`baseline-before.json` preserves the preceding records;
`commands/check-*.log` and `.rc` preserve the three comparisons;
`record-commands.json` and `commands/record-*.log` preserve the writes.
`policy-audit.json`, `measurement-summary.json` and `input-audit.json`
record policy equality, deltas, and source/header/memory-image rehashes.
Each measurement has six memory images; no source or image changed during
measurement, and no completed log reports a missing memory image.
The input SHA-256 values are:

| Endpoint | Input SHA-256 |
|---|---|
| route-1x1 | `95a6cc95786fa743da28e2aa603d3a6af08200c86bf4bb7c452aeba7ec072c4c` |
| ooc-1x1 | `2dd522bd12b3480a8817cf2bb3dd969ac7be6f3d80be70d13fe32ce5576011a5` |
| ooc-8x8 | `5604984543f875b19f344900a8b183adf81281c02ba42517ff894502f7a07f0c` |

`resource-receipts/inventory.json` records the original SHA-256 and byte
size of every retained or inventoried artifact. Executed Tcl, input
manifests, utilization, route status, timing, IOB results and gate output
are retained in full when within 200 KB. Larger artifacts remain outside
this packet, with size/hash receipts and clearly labelled text excerpts.

### Verification

The full builder command exited 0. Gate 23h reproduced the five-patch
series byte for byte across four installed files, and all five missing-patch
controls were rejected. No elaboration arm was skipped for a toolchain
reason. Historical gate 11 calibration did not run because its mf48 placed
report is absent; this verdict does not cover that unrelated calibration.
Portability passed all 58 tops and its structural checks. Firmware,
MAAP, capture ring, the standing follow-ring suite, default render and the
corrected datapath suite all exited 0. The render pull-in campaign passed
18/18 phases, 558 checks, zero failures and no ungradable windows.
The main physical-rate integration scenario also passed: 143 checks over
16.992556520 simulated seconds, 6,517,392 payload comparisons, 814,672
sample-order comparisons and 135,935 packet-sequence comparisons. Both
observed recentres completed on the wire. All 54 failure-control checks
passed: setup abort 6, no-TX accounting 20, no-Pdelay accounting 14, and
recentre controls 14. The complete suite exited 0. Traffic in this physical-rate test uses the diagnostic AAF bypass;
licensed streaming is not its claim.
All 39 source, documentation, policy and negative-control checks completed
with rc 0. The extra hierarchy ranking command also completed with rc 0.
The resource self-test passed 260 arms and 500 generated cases; its mutation
campaign rejected 174 of 174 defects. Recipe self-tests and mutants passed.

Two invocation failures are retained: the ranking formatter was first given
an unsupported `--selftest` option (rc 2), then invoked with its actual
report/root arguments (rc 0); the datapath pool rejected `SIM_JOBS=8`
(rc 2), then passed with rc 0 using the documented ceiling of 2. Neither
failure changed RTL, tests, expectations or policy. Final command receipts
are under `round2f-verification/`.

Final execution commands are recorded per job in `round2f-verification/jobs/`
and `checks/`. The suite builds used external build directories whose
tracked bench inputs were checked byte for byte against the lane. The
following commands describe the repeated scope; `$BENCH` is that staged
bench directory and `$PHYSICAL` is its separate physical-rate build directory:

```sh
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$WORK/firmware"
make -C "$BENCH/follow_ring" -j16 SWEEP_JOBS=8
make -C "$BENCH/maap" -j16
make -C "$BENCH/chmap_capture" -j16 run netcheck
make -C "$BENCH/milan_dp" -j16 SIM_JOBS=2
make -C "$BENCH/milan_dp_render" -j16
make -C "$BENCH/milan_dp_render" -j16 tdm8render-pullin PULLIN_JOBS=16
make -C "$PHYSICAL/milan_dp_gptp" -j16
bash syn/yosys/run.sh --results "$WORK/portability"
python3 -B syn/ooc/pp_resource_gate.py check-baseline
python3 -B syn/ooc/pp_resource_gate.py --selftest
```

`source-gate-spec.json` gives the exact source/documentation and recipe
control invocations. Two compile slots, each with four compiler workers,
bounded memory without changing model parameters. Independent groups ran
concurrently; each long job had its own detached process, log and rc file,
with bounded foreground waits.

### Final admission

The 50 effective verification commands all exited 0. Their retained initial
supervisor exited 1 because it includes the two rejected invocations;
`final-verification.json` explicitly maps each to its successful corrected
receipt. No test, assertion or policy was changed to obtain a pass.
Five post-commit checks also exited 0: punctuation against dev, resource
policy, the full PR diff, documentation and documentation paths after
removing the three temporary build links. The final audit binds the tested
file hashes to the committed bytes and confirms that exactly the baseline
JSON and two area documents changed after the measured merge.

Peak sampled verification memory: 11,493,605,376 bytes.
Peak sampled memory across measurement and verification: 13,151,162,368
bytes, below 17 GB. All jobs have ended. The worktree and all four
submodules are clean. Both first-parent commits have one-line subjects,
without bodies or trailers. The recorded measurement head remains distinct
from the final records/documentation head.

### Classification, scope and recommendation

This round updates measurement records and authoritative area documentation;
it adds no protocol-visible behavior. The prior diagnosis, option analysis,
settle action, residual recovery limitation and protocol test plan remain
in the earlier sections. The prior +113 LUT/+78 FF own-area result is
historical evidence accepted by the composition review. Whole-image mapping
changes in this round are not an isolated cost estimate of the settle logic.

Recommend independent review of the new records and documentation.
All assigned final verification commands passed. The assigned three-endpoint resource comparison
passes without changing policy. This round does not repeat the earlier
three-directive timing sweep or the full arrival-envelope campaign.
Broader merge-bank, hosted-context, independent review and physical bench
obligations remain with the integration handoff. Desk and physical-rate
simulation results do not discharge hardware acceptance. Earlier rounds
and their fix options remain above.


## Round 2g: default-suite wall clock

Public STOP: issue #645 comment 6074038320.
Candidate head: `1e79ebdc06528edff74c0a7f530f20f99e3326a2`.
Parent: `4640d995913cb93653a47e73856e8bd7dfe7c428`.
Assignment: issue #645 comment 6073617515.
Review addressed: PR #672 comment 6073609394, R474-4-F1 and R474-4-R1.
Status: STOP pending manager publication and exact-head hosted evidence.

### Change and classification

The review's failure was default-suite wall clock: both suites hit the
1,800-second hosted guard. The retained hosted receipt compares the dev-class
runner with the faster earlier candidate run. This round changes scheduling
inside existing targets, with no RTL, interface, protocol, source-list,
suite-list or timeout change. R474-4's Tests and Docs finding still needs
independent re-review; these are author verification results.

- `follow_ring` defaults to its four existing legs: `b8`, `pullin`,
  `small-pullin` and `settle-control`. Its twelve rebuilt defects remain
  executable through `make mutants`.
- The render default keeps both shapes, all eighteen LAW phases, and the
  five leg-side positive/negative controls. `--with-pullin` preserves the
  former standing pull-in at its original position after serial/CRF/LAW.
  The existing `tdm8render-pullin` target runs that history plus eighteen
  fresh-boot phases. No grading function, wait bound or stimulus duration
  changed. `scope-audit.json` binds the unchanged phase implementations.
- TESTING.md declares both explicit campaigns and the manager merge bank
  as owner. Its second test-plan link now lands on `#simulation`, which
  contains the controls column; the settle-recentre link remains. The
  existing-source-recentre locator now names `g_src_recentre`.
- The old 152.6 ms fresh-boot comment was stale. The measured standalone
  case takes 1,246.8 ms of simulated time after the hold; its corrected
  comment keeps the existing two-second guard.

### Cold default wall clock

| Default command | Measured seconds | At 1.58x | Limit | Result |
|---|---:|---:|---:|---|
| `make -j16` in `follow_ring` | 354.107 | 559.489 | 1440 | rc 0 |
| `make -j16` in `milan_dp_render` | 733.249 | 1158.533 | 1440 | rc 0 |

Both satisfy the assigned ceiling, 80% of the unchanged 1,800-second guard.
The committed page and Makefile headers round these figures to one decimal.
Both object trees started empty. The suites ran concurrently with the builder;
the later controls overlapped the render default's tail. Outer make used
`-j16`; a two-slot compile wrapper limited each elaboration to four compiler
workers. Elapsed time includes compilation, simulation, controls and queueing,
measured monotonically with a one-second completion poll. No gate output was
piped. Each background job had its own log and exit-code receipt and was
waited to completion.

A standalone, fully graded one-case render smoke (`--pullin`) passed all 33
checks in 591.216 s. Adding it to the measured default gives 1,324.465 s,
or 2,092.655 s at 1.58x, beyond the assigned limit. It remains explicit.
No shorter settling wait or weaker grading is substituted. The four-leg
`follow_ring` default still retains its INTERNAL pull-in and fine-pull cases.

### Reproduction and receipts

Set `LANE` to this candidate, `WORK` to an empty external build directory,
`SIM` to the pinned 5.050 executable, `RV32_SDK` to the existing compiler
installation, and `LITEX_PYTHON` to the interpreter with the required patches.
The retained helper recipes describe the isolated bench input copy, compiler
limit, environment, and detached job launcher. This build directory contains
no Git checkout. `bench-inputs.json` records every staged bench file by hash;
source directories reference the verified candidate. Neither generated files
nor build outputs belong in the repository or this evidence packet.

The commands, run from the corresponding staged suite directory, were:

```sh
make -j16
make -j16 mutants SWEEP_JOBS=4
make -j16 tdm8render-pullin PULLIN_JOBS=6
./obj_tdm8r/Vmilan_dp_tdm8r --pullin
python3 -B "$WORK/check_pullin_control.py"
```

The first command was run once per cold default. The second belongs to
`follow_ring`; the remaining commands belong to `milan_dp_render`. The
render campaign started with six children; ten GNU xargs parallelism
increments were requested after the ring controls completed. The request
and observed child count are retained in `campaign-parallelism.json`.
Using `PULLIN_JOBS=16` reproduces the same nineteen independent cases.

The focused negative uses the existing `tdm8_render_mutants.py` plant,
build, run and verdict functions for its named no-settle mutation, on a
scratch copy only. Its raw negative exit is 1 as expected; the control
runner exits 0 only when the named law check fails. The positive binary
must pass beside it. This does not claim a repeat of the unrelated full
render mutation campaign or erase the earlier #657 exception.

Source and documentation gates run from the candidate:

```sh
python3 -B scripts/measure_test_evidence.py --check
python3 -B scripts/measure_test_evidence.py --selftest
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
```

`jobs/gate-*.command.json` retains all 32 source/documentation command
vectors, including the pinned Markdown interpreter. Their matching `.rc`
and `.result.json` files record success. The final comment-only edit was
followed by repeated C++ idiom, wording and diff checks, also rc 0. The
scheduling checker and 105-check self-test both pass. Suite/target discovery
is unchanged, so `run_all_suites.sh`, the evidence pins and CI_WORKFLOWS.md
remain byte-identical to the parent.

| Evidence | Result |
|---|---|
| Cold follow_ring | b8 48/0; pullin 18/0; fine pulls 10/10; controller at four rates; rc 0 |
| Cold render default | shipping 258/0; second shape 71/0; leg-side controls 5/5; rc 0 |
| Explicit ring defects | 12/12 caught by their named checks; rc 0 |
| Explicit render campaign | rc 0; 19/19 legs, 830 checks, zero failures; includes the preserved history |
| Standalone pull-in | 33/0, 591.216 s; rc 0 |
| Missing-recentre control | named first-event law check fails; raw rc 1; control runner rc 0 |
| Source/documentation | 32 commands plus three final repeats, all rc 0 |
| Evidence contract | check rc 0; self-test 105/105, rc 0 |
| Builder | rc 0; no elaboration arm skipped for a toolchain reason; historical gate 11 uncovered |

The builder's gate 11 requires a placed utilization report that is absent.
Its calibration claim remains uncovered, as recorded in Round 2f. This
round does not claim a new hardware, placement or area measurement.

The standalone trace recentres after 124,683,570 axis cycles (1,246.8 ms),
then grades fill 14 and first-event delay 8.733..8.734 media ticks, with zero
loopback slips after the recentre. The preserved history recentres after
132,771,070 cycles (1,327.7 ms) and passes all 272 checks with zero later
loopback slips. The negative trace, phase logs and command receipts are in
this round's packet. `receipts.json` records raw and retained hashes/sizes;
home and build roots in retained text are replaced by variables. Files over
200 KB are represented by hashes, sizes and bounded excerpts.

`measured-source-binding.json` records both measured and committed hashes.
Only full-line comments changed after the cold runs: measured times and
the stale settling-time note. The non-comment text is identical.

### Area, protocol effect and recommendation

The selected split has zero RTL delta: no LUT, register, memory, timing,
wire-field or stream-behavior change is introduced by this round. The
Round 2f resource records and their stated limits remain applicable.
Earlier diagnosis, fix options, area comparisons and physical acceptance
obligations remain in the preceding rounds.

Retain the split and the declared manager-owned campaigns. Publish this
candidate, run the required replication and obtain a passing hosted
`verilator-suites` result on this exact head, then seek independent re-review
and post REVIEW READY. Hosted success is not established by these timings.
No merge or further RTL work is authorized by this handoff.
