[A265]

Closes #75

The PHC interface now exports `phc_slew_active_o`, a registered level covering the policy's transient offset correction. The policy starts correction outside ±100 ns when the pair does not step, and completes after two consecutive consumed pairs inside that band. The level rises before the affected addend and clears with the replacement addend. Ordinary PI tracking continues, including nonzero frequency trims.

Missing Sync and lost asCapable retain the level while the correction remains applied. Reset clears it; a replacement step clears it with its integral-only rate; becoming grandmaster explicitly retires the active correction. The integration guide defines these edges and the consumer's rate alignment and overlapping-window responsibilities.

The generator publishes the policy verdict, with all four tracked ROM images regenerated. The existing step thresholds, PI arithmetic, rate clamp, ROM depth and dispatch entries are unchanged.

Validation: the complete required gate returns 0, with no skipped suites. Three engine images pass 1,532 checks each. All 30 engine mutants are caught; the tied-low, first-pair-clear and pre-rate-clear controls fail their named checks. Arithmetic, parser, adapter, independent packet-generator, timestamp-tag, lint, documentation and diagram checks also pass.

OOC area against the base: 4,773 → 4,853 LUTs (+80, 1.68%); 3,646 → 3,652 registers (+6). Memory LUTs remain 466, block RAM tiles 1.5, and DSPs 4.

The existing loop has no 0.5 s maximum. With a master 140 ppm fast, the closed-loop ±90 us traces keep the level asserted for 3.069413 s and 1.916689 s, then resume ordinary tracking. Completion uses measured settling, without an expiry timer.

Parent #545 must connect the new named output in `KL_gptp_shadow.u_engine`, then carry it through the datapath to the CRF servo. The parent checkout is unchanged; its consumer validation remains with #545.
