[A829]

## Description

Adds the Arty split configuration with one AAF talker, one AAF listener and one CRF input.
The system bus and CPU run at exactly 80 MHz, with an 800 MHz VCO, 50 MHz datapath and exact output divisors.
The `(1,1,2)` scheduler point uses its own measured costs, now a 1250 us slice and 10 ms AECP pace.
MII advertises only 100BASE-TX full duplex and refuses to publish an incompatible link mode.
Optional writable timestamp corrections reset to the configured 1409/100 ns pair.
Existing scheduler rows and shared AX product images are unchanged. No Linux scheduling point is added.

The latency console accepts `lat IIIII EEEEE`, two five-digit decimal values in nanoseconds.
`lat 01409 00100` plus CR exactly fills the 16-byte receive FIFO.
Dropped digits, extra bytes and unequal field widths are refused before either correction is written.

The branch merges `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350` (PR #987) by a merge commit, `49b534fc9`, with conflicts resolved by meaning.

## The Arty row, re-derived for the merged firmware

The merged firmware raised the measured AECP, ACMP and MAAP costs at this point, so the 950 us / 9 ms row no longer met its own rule.
As the manager ruled, the row is now the one the existing rules give, installed exactly as derived, in two steps:

1. `f7b90e3b7`: from the merged maxima of round 4's census and the merged firmware's first 132 cases.
   Slice 950 -> 1250 us, AECP pace 9 -> 10 ms, transmit bound 30 -> 35 ms (the tx row 34.59 ms, rounded up), retry cold 125 -> 130 us.
   Stated costs: AECP record 290, ACMP 245, MAAP 125, MAAP timer 160, TICK event 50, rebuild 255, aecp_long 385, long AECP record 1105, AS_PATH and AVB_INFO 30, SET_CONFIGURATION edit 325 us.
2. `74f942be5`: the complete 147-case campaign at step 1's row moved six statements, again by the rule.
   Poll base 225 -> 235, centisecond (`CTRL_LOOP_TICK_US`) 150 -> 160, LINK event 150 -> 190, MAAP event 160 -> 165, withdrawal 90 -> 95 us. The slice, pace and queued bound did not move.

At 1250 us the slice holds both MRPDU builds (1035 us), so `CTRL_LOOP_BUILD_MOST` is 2 at this point.
`CTRL_LOOP_TICK_US` is read by the service harness's model only, so step 2 changes no firmware byte.

The base's two new groups, `srp-kept` and `srp-bound`, apply #969's disposition (ruling of 2026-11-22, amended 2026-11-23).
Their registrations over the unit and statements are owed to #977 and never restate the row.
`kept_grade.py` passes on this image: 0 findings, every kept record within its bound record, nothing over THE SHARE.
The derivation leaves exactly those owed measurements out of the maxima. These are SRP record applies up to 495 us, and `srp-bound`'s build of one at 740 us, walk and polls base.
Every other measurement of the two groups counts; LINK 190 and withdrawal 95 come from `srp-kept`, and centisecond 160 from `srp-bound`.
Without that disposition the rule finds no row: the last queued notice is about 225 ms against its 140 ms owner bound.

## Issue and roles

Relates to #878; its acceptance ruling keeps #878 open for the offset measurement under #1007 and lets this PR merge on its own gates.
Relates to #665, #818, #829, #894, #969, #977 and #983.
Target: `pf-arty-split-1` -> `dev-soft-core`.
Executor: `[A829]`. Independent reviewers: `[R927]` and `[R928]`; their reviews of `248d85c1` are negative, and review of this head is pending.

## Authoritative references

- [Issue #878 and owner rulings](https://github.com/kebag-logic/milan-fpga/issues/878); [#969's disposition](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252).
- Milan v1.2 7.2.2/7.2.3 and 4.2.1; IEEE 802.1BA-2011 Table 6-1 and 6.5.
- `ctrl_loop.h`, THE SHAPES and THE SHARE; `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15; `tb/verilator/ctrl_service_budget/kept_grade.py`.

## Source and image

Local head `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1`. Not pushed. The image and census are at `74f942be5`; the two commits after it change `docs/` and the receipt regrader only.
Selected implementation: `AltSpreadLogic_high`, tied with `ExtraTimingOpt` on every report (the regrader's tie-break names `ExtraTimingOpt`).

| Directive | Slow 0/85 C WNS / WHS ns | Fast 0/85 C WNS / WHS ns | Floors |
|---|---|---|---|
| ExtraTimingOpt | 0.433 / 0.138 | 1.606 / 0.050 | PASS |
| AltSpreadLogic_high | 0.433 / 0.138 | 1.606 / 0.050 | PASS |
| ExtraPostPlacementOpt | 0.064 / 0.126 | 1.606 / 0.050 | PASS |

Zero failing setup or hold endpoints in every report.
Post-placement utilization (selected): 33015 LUTs, 40369 FFs, 78.0 BRAM tiles, 13791 slices. Those are the totals of the previous route (round 6); round 5's were 33411, 40479, 78.5 and 14119.
Bitstream SHA256 `24a782c505c1ae4aea61d2abf1b1dd2e2cf0e5aa08e12a717e10cfddb37a871e` (3270263 bytes).
Firmware ELF SHA256 `b6cfb9a4e051e865101ceb220a3dfe4f7c487938c97d3e764c0f7407085038d2`: 159620 bytes, 44.5/56 RAMB36, and the same sections as the memory ledger states.
Layout `cec51feba98b59282db1125e5778fcf3988f82efb2ebdce0dbc3a16f55263fc4`, manifest `1730c43f993f0fbbd8cdfed6d3164b6e077d7743dcfafd8990750cbcda324d4f`; the image identity and offline flash-pair input checks pass.

## Validation

At `74f942be5`, unchanged since then for these gates:

- All four firmware shards with RV32 coverage; Arty native boot (0 findings), native controls 6/6, region self-test.
- Service-budget self-test, 8 partitions: 297/297 mutants caught, 0 failures.
- `rows_tiers` 1033/1033, `load_grade` 28/28, `egress_ledger` 21 mutants, `record_classes` 9/9, `arty_grade --selftest`, `test_ctrl_memory`.
- `arty_grade.py`: PASS, its model equal to the derivation (load 0.5004771140).
- Console and MII host arms; 15/15 focused plants caught.

At `4adfa9dc8`: documentation, inventory, style, paths, gPTP docs, Python/C++ idiom, em-dash and TOC checks pass.

**Service qualification: PASS**, over 147 native cases across eight image variants. All six checks pass: owner model, share, record classes, retry costs, transmit costs and held-egress ledger.
The model derived from the complete campaign equals the installed row.

| Owner bound | Value | Limit |
|---|---:|---:|
| Load | 0.5004771140 | 0.70 |
| ACMP | 29.77 ms | 30 ms |
| txL | 48.82 ms | 49 ms |
| Last queued notice | 117.47 ms | 140 ms |
| Longest whole pass | 142775 cycles, 1.7846875 ms | 2 ms |

The seven held-egress misses remain within their ledger. Each measured below its figure, for example `backlog.owed.if0` 62.73210 against 62.94 ms.
The two steps share one set of traces. Step 2 changes no firmware byte: every native executable, firmware ELF, flash image and all 147 stimuli are identical.
Its build inputs differ only in generation dates (LiteX date lines, CSR file headers, archive member dates; each compared with the date removed). So step 2's census regrades step 1's traces at the step-2 row, as round 5 did.

## Reproduce and inspect

From a checkout of the head, run `python3 tb/verilator/ctrl_service_budget/receipt_regrade.py <packet>` over the text receipt packet.
It checks every part and whole hash, reproduces all 147 case grades from the extracts, and reapplies the cross-case checks, owner model and timing floors.
This revision's regrader applies `run.py`'s #969 disposition in its cross-case step (`4adfa9dc8`).
Before that change it refused the five owed lines. A control packet without `srp-bound` is refused, the disposition naming its own breach.

## Open work and limitations

Independent reviews of this head, reviewer-owned lens coverage, the hosted checks and local replica, merge-candidate validation,
maintainer authorization and post-merge containment remain pending. No board operation was performed for this revision.
ACMP, txL and the longest pass each sit within 0.25 ms of their bounds (0.23, 0.18 and 0.215 ms).

## Definition of done

- [x] `dev-soft-core` merged by a merge commit; conflicts resolved by meaning.
- [x] The standalone `rows_tiers.py --selftest` failure is resolved and rechecked.
- [x] Arty row re-derived for the merged firmware by the rule, installed, and qualified by a complete census at that row.
- [x] Image routed, timing-qualified at every corner and graded.
- [ ] Independent reviews and reviewer-owned clean-lens ledger complete.
- [ ] Required hosted checks, local replica and merge-candidate validation pass.
- [ ] Maintainer merge authorization and post-merge containment complete.
