[A272]

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

Validation: the complete required local gate returns 0 with no skipped suites. Three engine images pass 1,586 checks each. All 32 engine mutants are caught, including all five slew controls on their named checks. Arithmetic, parser, adapter, independent packet-generator, timestamp-tag, lint, contract, documentation, and diagram gates also pass.

The prior synthesis comparison remains applicable: 4,773 → 4,853 LUTs (+80, 1.68%) and 3,646 → 3,652 registers (+6). Memory LUTs remain 466, block RAM tiles 1.5, and DSPs 4. WNS moved from +2.249 ns to +1.773 ns, with timing met. Synthesis was not repeated for this tests-and-documentation revision.

The existing loop has no 0.5 s maximum. With a master 140 ppm fast, the closed-loop ±90 µs traces keep the level asserted for 3.069413 s and 1.916689 s, then resume ordinary tracking. Completion uses measured settling, without an expiry timer. Loss of trustworthy measurements can hold the level indefinitely while the correction remains applied; steady-state field behavior is not established by simulation.

Parent #545 must connect `KL_gptp_shadow.u_engine` through the datapath to the CRF servo, validate the mastership retirement addend, and run its consumer gates. The manager must settle acceptance of the ±100 ns/two-pair tolerance and reconcile the measured duration with the parent's 0.5 s premise. Parent changes and hardware validation remain with that work.
