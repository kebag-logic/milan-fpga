[A835]

## Contents

- **[Status](#status)** — Gate tally, both release routes, the platform regression, and `994-gptp-pin-1213ac5b` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, dependency and environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN — `994-gptp-pin-1213ac5b` -> `dev-soft-core`, head `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21`. The branch merges `dev-soft-core` at `2509db68` (the #988 train's merge; its tree equals the old base `300da99b`'s, so the merge `3a8bdbf0` changes no file). Against `dev-soft-core` the branch carries this lane's six commits and that merge.

- **The platform regression (round 2).** `tb/verilator/gptp_shadow` now grades both adopted behaviours through the slice's transport and the real PHC: 408/408 at the head (326 before). Its mutation campaign plants both donor defects, and each fails its own named check: 11 of 11 controls caught. R916-1's two disposable probes, re-run at the head, each turn four new checks red.
- Both release routes fit and meet the #818 floor at every corner: 8x8/1if 46,246 LUT (-375 against the base), 1x1/1if 32,639 LUT (-41). BRAM and DSP equal at both shapes. No synthesis input changed after the routed commit `973f2f20`, and the 24 firmware image digests at the head equal round 1's.
- The gPTP consumers at the head: `gptp_shadow` (run, lifecycle, campaign), `gptp_plane` 31/31 and `phc-step` 62 checks with its 8 arms, `gptp_tables` 36 checks and 26/26 controls, `gptp_txts` 13/13 controls, `tsn_fuzz` with its field campaigns (gPTP 675 pass, AAF/AVTP 164 pass, equal to the tracked results). milan_dp `gptp` and `gptp-lat` 212/212 each, `[CA]` 0x22 and 0xFE on the wire.
- Round 1's full sweep (65 suites, 2,715,829 checks, 0 in-suite failures, at `8c5a51e1`), its physical `milan_dp_gptp` pass and its builder legs stand for every input this round does not touch. Round 2 changes `tb/verilator/gptp_shadow` and Markdown only. Every suite that reads a changed file was re-run, and the builder reads none.
- Every `run:` step of the docs workflow at the head, except the two builder legs and the compiler-absent firmware controls (each beyond a ten-minute window; none reads a changed file): rc 0, apart from this host's RV32 SDK install-verify, which refuses as on the base (no provenance receipt).
- `plat_ledger` 0 findings at the head. The whole-tree RTL lint passes (89 <= ratchet 89).

## Linked Issue / roles

Closes #994

Executor: `[A835]`
Internal cleared-context reviewer: `[R915]` (round 1)
External reviewer: `[R916]` (round 1)

## Description

Moves the `gptp-processor` gitlink from `1616fc8f` to FPGA-gPTP main `1213ac5b9e09b8759ba76cc70c53652b5e108996`, the merge of FPGA-gPTP PR #108, carries the new pin to every pin site, and grades the adopted behaviour on the platform.

`1213ac5b`'s tree is `7b579e33`, the tree of PR #108's reviewed head `331e27de`, which both its reviews passed (R905-2 and R906-2, each `POSITIVE` at that exact head). It fast-forwards `1616fc8f` on the donor's `main` through three merges:

| Donor issue | Merged PR | Parent-visible result |
|---|---|---|
| #102 | #103 | Test infrastructure only: the engine mutation arm runs its mutants at once. No `hdl/` or `syn/` change |
| #104 | #105 | Test infrastructure only: the engine builds compile through ccache. No `hdl/` or `syn/` change |
| #106 | #108 | The handler that takes the grandmaster role sends the first Announce and arms the 1 s cadence from it (IEEE 802.1AS-2011 Figure 10-15). Before, it armed a 2 ms beat, and an Announce at the receipt-timeout instant re-elected its grandmaster first, so the aged port's mastership never reached the wire. The role, asCapable and transmit-credit gates stay. The ROM shrinks by two words, to 1,013 of 1,024 |
| #107 | #108 | Taking the role always writes rate 0, so a mastership runs on this oscillator, the LocalClock (IEEE 802.1AS-2020 10.1.2.1). Before, the write applied only during a slew, so a mastership kept the slave's last trim, which a phase transient can wind to the +200 ppm rail. scaledLastGmFreqChange is the negated slave estimate, 0 when no slave rate was written since reset or since the last mastership (10.2.8.2.1 l), 11.4.4.3.9) |

No engine port, parameter or generator option changes, so no top-level port, parameter, register, builder or configuration change.

| Commit | Piece | Change |
|---|---|---|
| `973f2f20` | Gitlink | `1616fc8f` -> `1213ac5b`. The release routes ran at this commit; the six later commits change no synthesis input |
| `39e9c9d2` | Pin sites | The pin row in `docs/reference/SUBMODULES.md`; every engine-guide permalink (`GPTP_PLANE.md`, `TIME_SYNC.md`, the four `docs/guides/gptp/` pages, `docs/traceability/ieee8021as.md`, the SUBMODULES conflict list); both pin-bearing diagrams through `submodule_boundaries.gen.py` and `timesync_chain.gen.py`; the `gptp_ucode.hex` row of `syn/yosys/rom_digests.tsv` by `ooc.sh --record-rom-digests`, equal to the donor's tracked image (`4eb21cef...`) |
| `8c5a51e1` | Behaviour and records | `GPTP_PLANE.md` (the mastership's PHC write), `GM_LOSS_RECOVERY.md` (the first Announce at once and the mastership on this oscillator), `STRICTER_READINGS.md` (the Announce-at-the-instant row at `1213ac5b`), the #994 adoption record with the route figures in `SUBMODULES.md`, and the CHANGELOG |
| `bbfdb674` | Style | The same records within the audience style's ten-word sentence (the docs style gate's 18 findings at `8c5a51e1`) |
| `3a8bdbf0` | Merge | `dev-soft-core` at `2509db68`, the #988 train's merge. Its tree equals `bbfdb674`'s |
| `d616b1c6` | Platform regression | `tb/verilator/gptp_shadow`: phases 18 to 20 below, two observation taps in the bench wrapper, both donor defects in `mutants.py` and its lifecycle test |
| `f97e49fe` | Records | The `gptp_shadow` README and the gPTP test guide; the #994 record and the CHANGELOG name the regression and #997; the record states the release routes' selection rule as #818 does |

Historical measurement records that name `1616fc8f` (the CHANGELOG's earlier entries, the earlier SUBMODULES records, `AREA_BUDGET.md`, the #234 baseline finding, `pp_resource_baseline.json`'s `measured` strings, the `milan_dp` README's pre-#883 rows) stay as they are.

### The platform regression

`tb/verilator/gptp_shadow` runs the real engine inside `KL_gptp_shadow` (tap, frame FIFO, serializer, adjfine latch, gearbox, ticket and ledger) beside the real `timestamp_counter`, the real link guard and the launch observer. Three new phases run at the end of the run, each from a quiet master (unsealed, capable, no egress result owed):

| Phase | Graded |
|---|---|
| 18, #107 | Four masterships, each taken by the sync receipt timeout: from a slave settled on a grandmaster +100 ppm, one settled -100 ppm, the -100 ppm one again left while a slew corrects a 1,500 ns offset, and one elected and lost before any pair. Each takeover latches rate 0 into the real counter, retires the slew and steps no phase, and the counter then advances exactly 8 ns a clock. The Follow_Up TLV counts the mastership and carries the last slave offset. Its scaledLastGmFreqChange is rate 0 less the settled trim (within 5 %, both signs), present after the slewing slave, and 0 when no slave rate was written since the last mastership |
| 19, #106 | A grandmaster announcing at a 1 s interval stops announcing while its pairs continue, so the announce receipt timeout ages the port 3 s after its Announce. The first master Announce reaches the lane at once (285 clocks after the instant; the deferred beat would be 4,000), and two more follow 1 s apart. Then its next Announce is sent exactly 3.000 s after the elect, in the deadline's own millisecond: one master Announce reaches the lane, and that Announce then re-elects the grandmaster |
| 20, #106 | The transmit credit is withheld across a takeover by the ledger's seal (a refused record's barrier, the observer held in reset). No master Announce leaves while sealed, and the withheld one leaves one announce interval after the instant, with the cadence running on from it |

The bench wrapper exposes the slice's slew level and the counter's adjtime strobe, and the harness records every frame's last-beat clock and every published role change. The run now has 408 checks.

The campaign (`mutants.py`, the suite's default target) adds two controls, with the donor's own anchors:

| Control | File | Named check that fails |
|---|---|---|
| `first_master_announce_waits_for_a_beat`: SELF ends in END and BECOME arms a 2 ms Announce beat | `gptp-processor/hdl/ucode/gen_gptp_ucode.py` | `#106 race: one master Announce reaches the lane before the re-election` |
| `word3_applies_only_during_a_slew`: PHC word 3 applies only while a slew is active | `gptp-processor/hdl/top/KL_gptp_engine.sv` | `#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0` |

`mutants.py` now takes a control that edits two places, and the lifecycle test installs the real bytes of a dependency file a control plants in. R916-1's two disposable probes, re-run at the head, fail these checks:

| Probe (R916-1's patch) | Checks that fail at the head |
|---|---|
| `delayed-announce.patch` | the first master Announce leaves at once; the race's master Announce; both credit checks. 403 PASS of 407 |
| `retained-slave-rate.patch` | rate 0 and the 8 ns-a-clock advance, after the +100 ppm and the -100 ppm settled slaves. 404 PASS of 408 (the latched rate reads 13,402 and -13,434 units) |

Two harness changes come with it. The aged-head phase released its record hold with the enable still high, so the gate re-armed and held the next Pdelay_Req record for good. That was harmless while it was the last phase; it now drops the enable first, as every other hold does. And each new phase checks its quiet-master start, so a plane already broken by a mutant ends with a tally rather than at its own ledger-full simulation assertion.

### The release routes

The release recipe (the split image, one interface) at 1x1/1if and 8x8/1if, at most two routes at once, in the recipe's order, ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt. An image meeting the build floor (#818: WNS >= +0.030 ns and WHS >= 0 at every signoff corner) on the first directive ships from it; otherwise the best worst-corner WNS of the three ships. At 1x1 the first missed, as it does on the base, so all three were routed and ExtraTimingOpt is selected. The base is `300da99b`, whose image inputs were routed at `c2b2ba1a`: between the two only text and tests move, and the 24 firmware image digests equal the base's.

| Image, directive | WNS / WHS, worst corner | LUT | FF | Slice | BRAM tiles | DSP |
|---|---|---:|---:|---:|---:|---:|
| 8x8/1if base, ExtraPostPlacementOpt | +0.105 / +0.036 ns | 46,621 | 53,338 | 15,570 | 98.5 | 13 |
| 8x8/1if, ExtraPostPlacementOpt, selected | +0.066 / +0.036 ns | 46,246 | 53,381 | 15,622 | 98.5 | 13 |
| 1x1/1if base, ExtraTimingOpt | +0.384 / +0.036 ns | 32,680 | 42,805 | 14,297 | 80.5 | 13 |
| 1x1/1if, ExtraPostPlacementOpt, misses the floor | +0.007 / +0.036 ns | 32,555 | 42,803 | 13,598 | 80.5 | 13 |
| 1x1/1if, ExtraTimingOpt, selected | +0.170 / +0.024 ns | 32,639 | 42,805 | 14,147 | 80.5 | 13 |
| 1x1/1if, AltSpreadLogic_high | +0.072 / +0.024 ns | 32,633 | 42,803 | 14,142 | 80.5 | 13 |

| Figure | 8x8/1if change | 1x1/1if change |
|---|---:|---:|
| LUT | -375 | -41 |
| FF | +43 | 0 |
| Slice | +52 | -150 |
| BRAM tiles / DSP | 0 / 0 | 0 / 0 |
| WNS / WHS, worst corner | -0.039 / 0 ns | -0.214 / -0.012 ns |

The qualifying images at each signoff corner (WNS / WHS, ns):

| Image | Slow_85C | Slow_0C | Fast_85C | Fast_0C |
|---|---|---|---|---|
| 8x8/1if, ExtraPostPlacementOpt | +0.066 / +0.102 | +0.066 / +0.102 | +1.660 / +0.036 | +1.660 / +0.036 |
| 1x1/1if, ExtraTimingOpt | +0.170 / +0.102 | +0.170 / +0.102 | +1.636 / +0.024 | +1.636 / +0.024 |

- Every route completes with 0 failing endpoints and no routing error, and every image passes the split image identity gate.
- Both selected images meet the #818 floor at every corner.
- The 1x1 image's `signoff.txt` and `chain.log` print a second line, "ruling floors NOT met" with rc=1. That is the author tool's check of #870's lane-specific WHS >= +0.030 ns, not this issue's #818 floor (WHS >= 0), which the image meets. Its worst WHS fell 0.012 ns, to +0.024 ns.
- The worst setup paths are outside the gPTP plane: `KL_mbx` read data at 8x8 (16 levels), the SoC bus bridge into the UART FIFO at 1x1 (11 levels). The 1x1 image's worst hold path, +0.024 ns, is a zero-level `chan_map_render` register pair on `clkout1`.
- Where the LUTs move at 8x8, by the placed hierarchy: the gPTP plane is -294 LUT net (the engine cell +912, the wrapper's own logic -1,397, logic synthesis moved across that boundary), `KL_mbx_cdc` +627, `milan_datapath`'s `stream_table` -439 and `csr` -269.

**The owner's exception.** FPGA-gPTP PR #108 measured the 8x8/1if image at +455 LUT against a parent base with the older pin. The owner [accepted that growth as a recorded exception](https://github.com/Mister-M-alt/FPGA-gPTP/pull/108#issuecomment-7121892317) on 2026-11-24 and left fit and the #818 floor gating the image that carries this pin. On this base the growth does not appear: the 8x8/1if image is 375 LUTs smaller and the 1x1/1if image 41 smaller, and both meet the floor. Nothing in this PR recovers area; the difference is in synthesis mapping of the composed train.

## Authoritative references

- IEEE 802.1AS-2020 10.1.2.1 (LocalClock entity), 10.2.4.14, 10.2.8.2.1 l), 10.3 (BMCA and port state machines), 10.3.9.1 and 10.6.3 (announce receipt timeout), 10.3.11, 11.4.4.3 and 11.4.4.3.9, B.1.1
- IEEE 802.1AS-2011 Figures 10-13 (with Cor1) and 10-15
- Milan v1.2 4.2.6.2.3 and Table 4.2
- #994 scope and acceptance; FPGA-gPTP #106, #107 and its D1/D2/D3 ruling; FPGA-gPTP PR #108, its two `POSITIVE` reviews at `331e27de` and the [owner decision of 2026-11-24](https://github.com/Mister-M-alt/FPGA-gPTP/pull/108#issuecomment-7121892317)
- #818 (the build floor and the best of the three directives); `docs/integration/BUILDING.md` section 5
- `docs/design/GPTP_PLANE.md` (the integration contract), `docs/reference/SUBMODULES.md`, `tb/verilator/gptp_shadow/README.md`

## How to get into the same state

```sh
git fetch origin 994-gptp-pin-1213ac5b
git checkout --detach f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
git submodule status
```

`git submodule status` shows `gptp-processor` at `1213ac5b9e09b8759ba76cc70c53652b5e108996`.

## How to validate

```sh
export MAKEFLAGS=--no-print-directory
make -C tb/verilator/gptp_shadow
make -C tb/verilator/gptp_plane
make -C tb/verilator/gptp_tables
make -C tb/verilator/gptp_txts
make -C tb/verilator/tsn_fuzz
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$(mktemp -d)"
python3 scripts/check_doc_style.py
python3 scripts/check_gptp_docs.py
python3 scripts/check_submodule_docs.py
python3 scripts/docs_inventory.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
(cd syn/yosys && ./ooc.sh --record-rom-digests) && git diff --exit-code syn/yosys/rom_digests.tsv
git diff --check 2509db684b58b920e215b0d5d327b4a845bac3f4 HEAD
```

For the whole tree, as in round 1: `bash scripts/run_all_suites.sh "$(mktemp -d)" --wait --shard K/4` for K = 0 to 3, `--physical-gptp`, and `python3 sw/builder/test_builder.py --require-rv32`.

Expected result / pass criteria: every command exits 0. `gptp_shadow` ends `408 checks: 408 PASS, 0 FAIL`, `mutant lifecycle: PASS (... eleven named defects ...)` and `controls: 11   failures: 0`. Its two new controls print `caught by "#106 race: ..."` and `caught by "#107 settled +100 ppm: ..."`. The gptp leg prints `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A` and gptp-lat `... 0xF8FE436A`, each `212 checks: 212 PASS, 0 FAIL`. `plat_ledger` prints `plat_ledger: PASS (0 finding(s))`. `ooc.sh --record-rom-digests` leaves `rom_digests.tsv` unchanged. Run with `TSN_GEN_ROOT` set, so `tsn_fuzz` runs its field campaigns.

To see the regression go red, apply one of R916-1's patches (`delayed-announce.patch`, `retained-slave-rate.patch`) inside `gptp-processor` and run `make -C tb/verilator/gptp_shadow run`. The checks in the probe table above fail.

The routes follow the release recipe for each shape: `endstation_builder.py <config> --placement split`, the split boot's runtime, the platform image linked against a stand-in export's CSR map at one interface, then `milan_soc.py` with the builder's argv, `--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive <directive>` and `--build`. Each selected image is read at the four signoff corners and checked by `sw/litex/check_image_identity.py`.

## Known limitations / out of scope

- [#997](https://github.com/kebag-logic/milan-fpga/issues/997): after a grandmaster takeover at -100 ppm, a parent consumer run of FPGA-gPTP saw no AECP response for two GET_COUNTERS windows (FPGA-gPTP PR #108, R905-1-S3, retained by R906-2). It reproduces at `1616fc8f` too, so it is pre-existing parent behaviour that this adoption does not cause or fix. #997 owns the reproduction without retries and the fix.
- `gptp_shadow` runs about twice as long: on this loaded host its simulation took 94 s at the head against 47 s at `bbfdb674`, and the default target runs it twelve times (the run and eleven controls). `scripts/suite_shards.py` still registers the hosted window measured before this change (393 s). That figure needs a new hosted measurement once this head has run. It stays well inside the suite's 1,800 s `run_all_suites.sh` timeout.
- The existing `credit_never_withheld` control names a check, "credit: the engine is held off at the reserve", that the run does not have. It is caught by other checks, at this head and at `bbfdb674` alike. The name is left for its own change.
- Area recovery of the 8x8/1if image stays with the optimisation line (#994 out of scope; the owner's decision). On this base there is no growth to recover.
- The resource gate's endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`) are not re-measured. `route-1x1` measures the all-fabric image; this issue's acceptance names the release images, which are recorded above. The standalone tops, `KL_pp_shadow`, hold no gPTP logic.
- The firmware gate's four shards were not run: no firmware input moves. The 24 image digests (ELF, stripped and loadable, at the eight ledger points) equal the base's and round 1's.
- Nothing here measures the board: the bench runs after the merge.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
