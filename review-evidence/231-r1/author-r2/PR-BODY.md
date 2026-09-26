[A337]

Closes #231

Commit: `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4`

Establish the current protocol processor area and timing baseline for the shipping 1x1 and supported 8x8 product configurations. Add a reproducible recipe derived from the shipping build, complete wrapper parameters and image hashes, hierarchical resource tables, and mapping comparisons. No RTL or donor changes.

The shipping 1x1 route uses 48,618 LUTs, with 22,441 assigned to the reconstructed protocol-wrapper name (which includes relocated datapath logic), with final setup slack +0.013 ns and hold slack +0.014 ns under the existing constraints. Integrated 8x8 synthesis uses 68,136 LUTs against 63,400 available. The baseline distinguishes standalone estimates from integrated results and preserves the historical substitution provenance.

Validation: both full builder modes and every requested local gate returned rc 0. The compiler-backed run exercised 855 target compiler invocations. The historical mf48 calibration report was unavailable in both builder modes; the compiler-absent mode also deliberately skipped target compile evidence. Both documentation CI modes passed. Complete evidence and command records accompany the author handoff.

The existing clock-constraint warnings and I/O-delay omissions remain documented limitations. The three placement runs all pass their final setup and hold checks; the best measured setup slack is +0.123 ns. The complete reports retain the exact shipping result separately.

## Round 2

All five items in the round-two assignment are addressed. Default-flow whole-design totals remain the fit baseline. A separate integrated run preserves the protocol-wrapper boundary with `KEEP_HIERARCHY TRUE`; its results are labelled attribution-only. No RTL, donor, geometry, image, clock or synthesis-directive change accompanies that constraint.

| Endpoint | Whole LUT, default / attribution | Wrapper-name LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|---:|
| 1x1 synthesis | 51,125 / 52,210 | 23,272 / 22,314 | 6,639 / 4,678 | 1,296 / 111 |
| 1x1 route | 48,618 / 48,825 | 22,441 / 20,655 | 6,428 / 4,504 | 1,299 / 111 |
| 8x8 synthesis | 68,136 / 70,206 | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |

The public boundary and load probes ran unchanged on all three attribution checkpoints. At 8x8 synthesis, the dynamic-state scope drops from 8,817 to 607 raw LUT cells and from 5,922 to zero cells with only external loads. The default load names include datapath audio-map registers. Attribution dynamic-state load histograms are empty at all three endpoints. Remaining wrapper-level external loads include exported signals; the probe does not measure reverse relocation. Raw LUT cells differ from combined utilization LUTs.

The attribution 1x1 route finishes with setup slack +0.041 ns, hold slack +0.015 ns and zero failing setup, hold or pulse-width endpoints. Preserving the boundary changes mapping and sharing: the 8x8 attribution wrapper has eight DSPs, versus five under the default reconstructed name, with the three additional DSPs in `u_nvm`. Attribution counts cannot be subtracted from default whole-design totals.

Complete rankings now cover every reported direct processor and wrapper child, plus own logic, at a zero threshold. LUT and FF ranks are independent. All eight endpoints include parent totals and explicit LUT-sharing reconciliation; the timing tables are labelled subsets. The complete 328-row ranking is in `docs/findings/PP_SHADOW_BASELINE_RANKING.tsv`.

Equivalent-geometry hierarchical Yosys runs locate the largest raw logic-count differences in SRP, processor own logic and notification logic. Complete disjoint contributions plus the measured flattening residual reconcile the original raw gaps exactly: 16,317 LUTs at 1x1 and 33,374 at 8x8. The residual is not assigned speculatively to individual modules. The full accounting is in `docs/findings/PP_SHADOW_BASELINE_MAPPING.tsv`.

The preparation self-test now exercises real script emission, inventory and CLI refusal with synthetic exports. The positive control passes, and all ten enforcement-removal mutants fail, including ROM-error promotion, readmemh inventory equality, empty SRAM, parameter ROM geometry, output containment and attribution constraints. The original public mutant driver also passes its control and kills all five mutants. Fast CI runs the maintained self-tests and mutant checks.

The dangling builder-output citation now denotes a directory. The path gate passes on a clean export with builder output absent. Every requested local gate returns rc 0, including both full builder modes, both documentation CI modes, the event-contract check and self-test, HDL and language gates, traceability, naming, test evidence, Behave and whitespace. The compiler-backed run records 855 target invocations. The historical calibration arm remains unavailable in both modes; compiler-absent mode additionally skips the target compiled CSR census. These skips are recorded as limits rather than evidence.

All 20 wrapper parameters and all six input-image hashes match for each product shape. The two 118-source exports retain source order and commands after work-root normalization; generated Verilog differs only in comments and work-root strings. Attribution synthesis logs contain zero missing-ROM diagnostics. Raw reports, checkpoint receipts and gate logs are retained separately from the compact handoff. The local commit is unpushed and awaits independent re-review; this prepared body has not been applied to the PR.
