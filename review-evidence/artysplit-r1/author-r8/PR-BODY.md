[A829]

## Description

Adds the Arty split configuration with one AAF talker, one AAF listener and one CRF input.
The system bus and CPU run at exactly 80 MHz, with an 800 MHz VCO, 50 MHz datapath and exact output divisors.
The `(1,1,2)` scheduler point uses its own measured costs: a 1250 us slice and a 10 ms AECP pace.
MII advertises only 100BASE-TX full duplex and refuses to publish an incompatible link mode.
Optional writable timestamp corrections reset to the configured 1409/100 ns pair.
Existing scheduler rows and shared AX product images are unchanged. No Linux scheduling point is added.

The latency console accepts `lat IIIII EEEEE`, two five-digit decimal values in nanoseconds.
`lat 01409 00100` plus CR exactly fills the 16-byte receive FIFO.
Dropped digits, extra bytes and unequal field widths are refused before either correction is written.

The branch merges `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350` (PR #987) by a merge commit, `49b534fc9`, with conflicts resolved by meaning.

## The Arty row

The merged firmware raised the measured AECP, ACMP and MAAP costs at this point, so the 950 us / 9 ms row no longer met its own rule.
As the manager ruled, the row is the one the existing rules give, installed exactly as derived, in two steps:

1. `f7b90e3b7`: from the merged maxima of round 4's census and the merged firmware's first 132 cases.
   Slice 950 -> 1250 us, AECP pace 9 -> 10 ms, transmit bound 30 -> 35 ms (the tx row 34.59 ms, rounded up), retry cold 125 -> 130 us.
   Stated costs: AECP record 290, ACMP 245, MAAP 125, MAAP timer 160, TICK event 50, rebuild 255, aecp_long 385, long AECP record 1105, AS_PATH and AVB_INFO 30, SET_CONFIGURATION edit 325 us.
2. `74f942be5`: the complete 147-case campaign at step 1's row moved six statements, again by the rule.
   Poll base 225 -> 235, centisecond (`CTRL_LOOP_TICK_US`) 150 -> 160, LINK event 150 -> 190, MAAP event 160 -> 165, withdrawal 90 -> 95 us. The slice, pace and queued bound did not move.

At 1250 us the slice holds both MRPDU builds (1035 us), so `CTRL_LOOP_BUILD_MOST` is 2 at this point.
`CTRL_LOOP_TICK_US` is read by the service harness's model only, so step 2 changes no firmware byte.
At the installed statements two rows meet every rule and bound: this one and 950 us at a 130 ms queued bound. The derivation takes the first by pace, then queued bound, then slice.

The base's `srp-kept` and `srp-bound` groups apply #969's disposition (ruling of 2026-11-22, amended 2026-11-23): their registrations over the unit and statements are owed and never restate the row.
[#1022](https://github.com/kebag-logic/milan-fpga/issues/1022), blocked by #977, carries that cost at this point. Section 15 cites it.
`kept_grade.py` passes on this image: 0 findings, every kept record within its bound record, nothing over THE SHARE.
The derivation leaves out exactly those owed measurements: SRP record applies up to 495 us, and `srp-bound`'s build of one at 740 us, walk and polls base.
Every other measurement of the two groups counts.
The published control counts them too, and finds no qualifying row: all 52 candidates fail an owner bound, and the least last queued notice is 225.54 ms against 140.

## Round 8

Evidence, documentation and comments only. No firmware, RTL, row or image change.

- `bdbd7b7c4`: section 15 cites #1022, states the control's result, the derivation's choice of row and the ROM headroom (1404 bytes).
- `367c1dcdb`: `census_extract.py` writes a compact census extract. `receipt_regrade.py` reads the part limit an extract's `census.json` states, never above 15 MB.
- `9f15ecb30`: the service-budget README cites the installed row's [published qualification](https://github.com/kebag-logic/milan-fpga/blob/907764ebbc99dad85babf522da92c13d92ab20aa/review-evidence/artysplit-r1/author-r7/receipts/published-qualification.json) (`076e7cc7...`: PASS, 147 cases, its model `arty_grade.py`'s). It states that the earlier 145-case receipt qualified the superseded 950 us / 9 ms / 30 ms row, and cites #878's held-egress ruling by decision.
- `64a76076e`: wording residues. The `lat` command in the CHANGELOG; #878's held-egress ruling cited by decision in the builder guides; both VERSION values in CLOCK_DOMAINS; S25FL128S in the split configuration; its calibration comment without the workflow clause; the mutant fixtures' comments without lane labels.
- `011aaa6f0`: the extra blank line at the end of four Python helpers removed; `git diff --check` from the base is clean.

## Issue and roles

Relates to #878; its acceptance ruling keeps #878 open for the offset measurement under #1007 and lets this PR merge on its own gates.
Relates to #665, #818, #829, #894, #969, #977, #983 and #1022.
Target: `pf-arty-split-1` -> `dev-soft-core`.
Executor: `[A829]`. Independent reviewers: `[R927]` and `[R928]`; their reviews of `4adfa9dc` are negative on evidence and documentation, and review of this head is pending.

## Authoritative references

- [Issue #878 and owner rulings](https://github.com/kebag-logic/milan-fpga/issues/878); [#969's disposition](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252); [#1022](https://github.com/kebag-logic/milan-fpga/issues/1022).
- Milan v1.2 7.2.2/7.2.3 and 4.2.1; IEEE 802.1BA-2011 Table 6-1 and 6.5.
- `ctrl_loop.h`, THE SHAPES and THE SHARE; `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15; `tb/verilator/ctrl_service_budget/kept_grade.py`.

## Source and image

Head `011aaa6f080321e0a89f915720ebb3ee14807a16` (the PR head). The image and census are at `74f942be5`. Every later commit changes documentation, comments, end-of-file bytes, the receipt regrader or the new extractor only.
Selected implementation: `AltSpreadLogic_high`. It is the same placed design as `ExtraTimingOpt` (one image manifest), so the two tie on every report.

| Directive | Slow 0/85 C WNS / WHS ns | Fast 0/85 C WNS / WHS ns | Floors |
|---|---|---|---|
| ExtraTimingOpt | 0.433 / 0.138 | 1.606 / 0.050 | PASS |
| AltSpreadLogic_high | 0.433 / 0.138 | 1.606 / 0.050 | PASS |
| ExtraPostPlacementOpt | 0.064 / 0.126 | 1.606 / 0.050 | PASS |

Zero failing setup or hold endpoints in every report.
Post-route utilization, from the retained routed checkpoints (Design State `Physopt postRoute`): 33015 LUTs, 40369 registers, 13791 slices and 78 BRAM tiles.
These equal round 6's routed totals from its retained routed checkpoint, so the routed-total LUT delta is 0, inside the ~50-LUT band.
Bitstream SHA256 `24a782c505c1ae4aea61d2abf1b1dd2e2cf0e5aa08e12a717e10cfddb37a871e` (3270263 bytes); routed checkpoint `1bbc99779c5de6ae18f6f8fd0c3a610e34eca148c7b9a44c2a584a1f5ca9233e`.
Firmware ELF SHA256 `b6cfb9a4e051e865101ceb220a3dfe4f7c487938c97d3e764c0f7407085038d2`: 159620 bytes, 44.5/56 RAMB36, the same sections as the memory ledger states.
Layout `cec51feba98b59282db1125e5778fcf3988f82efb2ebdce0dbc3a16f55263fc4`, manifest `1730c43f993f0fbbd8cdfed6d3164b6e077d7743dcfafd8990750cbcda324d4f`; the image identity and offline flash-pair input checks pass.

## Validation

At `74f942be5` (unchanged for these gates since):

- All four firmware shards with RV32 coverage; Arty native boot (0 findings), native controls 6/6, region self-test.
- Service-budget self-test, 8 partitions: 297/297 mutants caught, 0 failures.
- Console and MII host arms; 15/15 focused plants caught.

At `011aaa6f0`:

- Documentation, inventory, style, paths, gPTP docs, Python/C++ idiom, em-dash and TOC checks pass.
- `rows_tiers` 1033/1033, `load_grade` 28/28, `egress_ledger` 21 mutants, `record_classes`, `arty_grade` and `kept_grade` self-tests pass. `arty_grade.py` passes, with load 0.5004771140.
- The mutant fixtures' values are identical across their comment change. The split configuration's generated outputs are unchanged by its comment edits.

**Service qualification: PASS**, over 147 native cases across eight image variants. All six checks pass: owner model, share, record classes, retry costs, transmit costs and held-egress ledger.

| Owner bound | Value | Limit |
|---|---:|---:|
| Load | 0.5004771140 | 0.70 |
| ACMP | 29.77 ms | 30 ms |
| txL | 48.82 ms | 49 ms |
| Last queued notice | 117.47 ms | 140 ms |
| Longest whole pass | 142775 cycles, 1.7846875 ms | 2 ms |

The seven held-egress misses remain within their ledger; each measured below its figure.
The two steps share one set of traces. Every native executable, firmware ELF and all 147 stimuli are identical between the steps; no variant builds a flash image (the native builds are not XIP).
The receipts pair each step's hashes side by side. The build inputs differ only in generation dates, each compared with the date removed, so step 2's census regrades step 1's traces at the step-2 row.

## Reproduce and inspect

The compact census extract (`receipts/census-extract/` in this round's packet) holds every case manifest, scenario, stimulus, original grade and journal byte for byte.
It also holds the observation lines a grader reads: round 7's extract less the SPAN and CALL lines of traced functions no grader reads (`census_extract.READ_LABELS`).
`census-extract/FILES.json` maps every file to the round-7 packet files it comes from, with the SHA256 the round-7 `FILES.tsv` lists.

```sh
python3 tb/verilator/ctrl_service_budget/receipt_regrade.py census-extract
```

On the extract it reproduces all 147 grades and passes the cross-case step, line for line as on the full census (the full run's timing lines aside).
A copy without `srp-bound` is refused as the full census's was, the disposition naming its own breach.
The extract is 762 files and 1,434,762,896 bytes, largest file 13,999,999 bytes. No smaller extract of original lines regrades: the grades count every pass's polls, rounds and slices.
The twelve timing reports regrade from the round-7 packet with `--timing-only`.

## Open work and limitations

Independent reviews of this head, reviewer-owned lens coverage, the hosted checks and local replica, merge-candidate validation, maintainer authorization and post-merge containment remain pending.
No board operation was performed for this revision. ACMP, txL and the longest pass sit within 0.25 ms of their bounds (0.23, 0.18 and 0.215 ms).
#1022 tracks the owed registration cost at this point.

## Definition of done

- [x] `dev-soft-core` merged by a merge commit; conflicts resolved by meaning.
- [x] Arty row re-derived by the rule, installed and qualified by a complete census at it.
- [x] Image routed, timing-qualified at every corner and graded; post-route utilization compared with round 6's.
- [x] Owed registration cost has an owner (#1022) and a published control.
- [x] A regradable census extract and the paired step identity are in the evidence packet.
- [ ] Independent reviews and reviewer-owned clean-lens ledger complete.
- [ ] Required hosted checks, local replica and merge-candidate validation pass.
- [ ] Maintainer merge authorization and post-merge containment complete.
