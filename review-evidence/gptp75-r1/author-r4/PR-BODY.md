[A281]

Closes #75

The PHC interface exports `phc_slew_active_o`, a registered level covering the policy's transient offset correction. Correction starts outside ±100 ns when the pair does not step, and completes after two consecutive consumed pairs inside that band. The level rises before the affected addend and clears with the replacement addend. Ordinary PI tracking continues, including nonzero frequency trims.

Missing Sync and lost asCapable retain the level while the correction remains applied. Reset clears it; a replacement step clears it with its integral-only rate; becoming grandmaster explicitly retires the active correction. The integration guide defines these edges and the consumer's rate alignment and overlapping-window responsibilities.

The generator publishes the policy verdict, with all four tracked ROM images regenerated. Step thresholds, PI arithmetic, the rate clamp, ROM depth and dispatch entries retain their prior behavior. The image uses 1,008 of 1,024 words, leaving 16 words spread across packing gaps. Shared legs may occupy the formerly reserved addresses 0..15: dispatch starts at 16 and reset does not fetch. The manager guide records these invariants and the requirement that each leg fit an available gap.

## Round 2

- Added inactive-direction checks for an idle Sync receipt timeout, a grandmaster identity change followed by in-band pairs, and an in-band first pair after returning from grandmaster duty. The checks use public wire inputs and verify consumed offsets, rate writes, and every level edge.
- Added named controls for an idle lapse incorrectly arming qualification and mastership incorrectly retaining qualification. Each must fail its own check. Both unchanged reviewer probe drivers catch both corresponding defects, with passing positive controls.
- Refreshed the source-evidence anchors and added bindings for the slew port, PHC words 2 and 3, and the policy leg. The documentation gate now checks every local line anchor against its claimed source construct: 20 exact anchors, plus seven checker controls.
- Documented the publication-flags lapse hook, current ROM headroom, and prefix-packing policy. Recorded the asCapable-only mutation's reachability limitation.

Round 2 changes tests and documentation; RTL, the generator, and ROM bytes are unchanged from the first review head.

## Round 3

- Added the inactive asCapable-loss and recovery check requested by R304-2 F3 and R305-2 F1. Bad Pdelay responses drop capability through wire inputs, the harness holds it lost, good exchanges restore it, and the first two consumed pairs have offsets of 0 ns and +100 ns. The checks require a low level throughout, no edge, no rate write during the lapse or recovery, and exactly one PI rate write per consumed pair.
- Added `slew idle asCapable loss arms qualification`, with the same pattern and replacement as X01. The control must fail `slew: in-band pair after asCapable recovery stays inactive`.
- Re-ran `probe_mutants_r2.py` unchanged against the shipped harness. X01 fails the new named check; the positive control passes 1,613 checks. X02, X04 and X05 are also caught. X03 survives as documented in the review; its equivalent one-pair arming never raises the level on an in-band pair.
- Re-ran the unchanged `make_gap_tree_r2.py` and its Probe C: the positive control passes 1,631 checks and X01 fails the probe's named recovery check.
- The second unchanged round-2 reviewer driver also catches R21, the X01 equivalent, at the new named check, and catches R22.
- Refreshed the manager guide to the PR's measured engine figures: 4,853 LUTs, 3,652 registers and +1.773 ns WNS, with the measurement date, baseline comparison and report link.

Round 3 changes only the engine harness, its mutation controls, and the manager guide. RTL, the generator, and ROM bytes are unchanged.

## Round 4

- Split `exercise_the_slew_level_contract()` into eight named phases. The coordinator is 10 lines; the phases are 13–30 lines. Expanding their bodies in call order reproduces every original statement, with no changes to checks, stimuli or expected values.
- Annotated `check`, `selftest` and `main` in `scripts/check_source_evidence.py`, and added the `main` docstring. The ledger still reports 20 exact anchors and 0 findings; its seven-arm self-test and all output bytes are unchanged.
- Recorded the complete engine check list before and after: 1,613 checks on each of three images, with all 4,839 names and their order byte-identical. Both complete mutation runs catch all 33 mutants on the same checks. Their verdict tables, return codes and full ordered failure lists are identical, including all six required slew checks.
- `make -j8` and the separate `make -C tb/verilator/engine mutants` return 0. All repository suites execute, with no skips.
- Fetched local candidate `6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf` into the parent consumer and committed only its gitlink as `d2d89eb677d835c4b888b042833cf274290a3e30`. The consumer is based on `dev` `573f0052` plus the supplied local pin commit. All six assigned checks return 0: C++ idioms, Python idioms, source parsing, source lists, builder, and the shadow suite with its mutation controls. The builder reports one calibration arm not run because its expected utilization report is absent; that arm is not covered by this result.

Round 4 changes only the two assigned source files. RTL, microcode, ROM images, mutation definitions and documentation claims are unchanged. The candidate and consumer pin are local; the parent connection work remains with #545.

Validation: the repository's default gate set and all six assigned parent consumer gates return 0. The repository suite bank has no skipped suites. The engine passes 1,613 checks on each of three images. All 33 engine mutants are caught, including all six slew controls on their named checks. Arithmetic, parser, adapter, independent packet-generator, timestamp-tag, lint, contract, documentation, and diagram gates also pass. The source-evidence check reports 20 exact anchors and passes all seven negative controls.

The prior synthesis comparison measured 4,773 → 4,853 LUTs (+80, 1.68%) and 3,646 → 3,652 registers (+6). Memory LUTs remain 466, block RAM tiles 1.5, and DSPs 4. WNS moved from +2.249 ns to +1.773 ns, with timing met. A fresh round-3 synthesis run reproduces these candidate figures and the standalone microCPU figures; both timing checks pass.

The existing loop has no 0.5 s maximum. With a master 140 ppm fast, the closed-loop ±90 µs traces keep the level asserted for 3.069413 s and 1.916689 s, then resume ordinary tracking. Completion uses measured settling, without an expiry timer. Loss of trustworthy measurements can hold the level indefinitely while the correction remains applied; steady-state field behavior is not established by simulation.

Parent #545 must connect `KL_gptp_shadow.u_engine` through the datapath to the CRF servo, validate the mastership retirement addend, and run its consumer gates. The manager must settle acceptance of the ±100 ns/two-pair tolerance and reconcile the measured duration with the parent's 0.5 s premise. Parent changes and hardware validation remain with that work.
