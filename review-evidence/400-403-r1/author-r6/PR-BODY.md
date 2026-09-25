[A323] Make SRP and boot declarations describe the implemented behavior.

Closes #400
Closes #403

Every SRP declaration now identifies its live consumer, fixed-profile validation or legacy scratch role. Unsupported timer, VID and TSpec values refuse with a reason. The generated startup VID reaches the processor through the parent wrapper, while documented runtime diagnostics and Domain adoption remain available.

Every declared Stream Output, including CRF, receives the required 2 ms factory presentation offset. Legal runtime offsets affect only their addressed output and reach both readback and transmitted timestamps. The configuration explicitly names the existing promiscuous receive posture. AAF and MAAP reset disabled; generated firmware policy supplies their active values and allocates exactly the declared outputs.

The bundle incorporates dev 220cb5a3, retains its processor revision 990f9652 and ROM digests, and regenerates the submodule diagrams. Validation also corrected two stale test fixtures and documented the existing listener-offset refusal, with additional negative cases. Actual saved-state restoration remains assigned to #70 under the 2026-09-23 owner decision.

Validation passed: both complete builder modes with all-config elaboration, 26 declaration refusals and binding/header mutations, the 20-case CSR reset matrix, protocol-wrapper VID/adoption/RX/allocation checks, every entry in the default datapath sweep, 344 behavior scenarios, and the requested documentation and source gates. The historical placed-utilization calibration report was unavailable. Area comparisons for all three changed RTL modules show zero delta at the measured default shape.

## Round 2

The firmware host-test header omitted four generated boot constants. It now derives the complete set from each shape's generated overlay and SRP table through the shared boot-policy function. The builder compiler fixture uses that function too. The builder gate now includes the saved-state firmware self-test for every shipped shape.

Round 2 validation passed at `7463ab0889da9a95fce7c921e386d6035d69778e`: all 48 manager bank commands, both complete builder modes, the firmware self-test across five shapes with all four planted defects detected, declaration checks, the CSR and protocol-wrapper suites, every chunk of the default datapath sweep including its mutation campaigns, all 344 behavior scenarios, and the requested documentation and source gates. The area comparison again reports zero delta for all three changed RTL modules at the default shape. The compiler-absent run explicitly leaves compiler-dependent checks unmeasured; the historical placed-utilization calibration report remains unavailable.

## Round 3

The saved-state co-simulation header now uses the shared boot-policy derivation. Default protocol-wrapper and register suites generate committed fixtures for a distinct startup VID, a declared CRF output, and nonzero admission reset bits. Headers come from the builder. Reset, allocation, pruning, presentation-row and declaration-count text now matches the implemented contracts.

Local validation at `e122f3302cf8a8e89de960233a8638b9dd1387dc` passed: all 48 manager-bank entries, both complete builder modes, all 55 default suites in five chunks, all 33 explicit datapath recipe commands, quick and full co-simulation, documentation and source gates, and 344 behavior scenarios. Full co-simulation killed all 39 named mutants. Review mutants 41, 43 and 35 fail the default targets with three, three and two checks respectively; restored targets pass.

Clean default-target wall clocks changed from 18.502 to 52.735 seconds for the protocol-wrapper suite and from 30.480 to 35.146 seconds for the register suite. Both remain below their unchanged 1,800-second budgets. The repository area recipe reports zero change in every measured counter for all three changed RTL modules at the default shape.

Compiler-dependent arms are explicitly unmeasured in the compiler-absent mode and covered by the separate SDK run. The historical placed-utilization report and field-campaign generator remain unavailable; no hardware or field result is claimed. Hosted exact-head validation and independent re-review remain required.

## Round 4

Builder comments now state the supported MAAP and promiscuous RX contracts. The unread RX posture constant and allocation-policy normalization are removed. Regenerating all five shipped configurations before and after produces 61 byte-identical artifact files, including the generated header copies and sweep fragments.

The declaration fixture rejects invalid emitter VIDs explicitly, including under optimized Python. Both suite banners and READMEs now describe their current default builds and generated fixtures without fixed check counts. Makefile recipes and product behavior are unchanged.

Local validation at `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55` passed with exit 0 for both complete builder modes, declaration checks, the firmware self-test, both default suites, both documentation inventory modes, and every assigned documentation and source gate. The compiler-absent run records compiler-dependent checks as unmeasured; the separate pinned-SDK run covers them. The existing historical area-calibration report remains unavailable. Independent re-review is still required.

## Round 5

Merged dev `220cb5a34507bb79bbf976b031bb55eb05543d6f` and remeasured the composed product firmware. The refreshed receipt contains 96 graded captures: 16 per traffic arm for both contract shapes at aligned 50 MHz, plus both arms of the labelled 100 MHz 8x8 comparison. Firmware and hold behavior are unchanged by this round.

The 8x8 contract maximum is **24.30246 ms**, down from 24.30454 ms. It is **0.19754 ms below the 24.5 ms limit**, with **2.0163x margin against the guaranteed 49 ms floor**. The stop condition was not triggered. The 1x1 maximum remains 6.60642 ms; the non-contract 100 MHz 8x8 maximum remains 19.79024 ms. Section 18 and UNRESOLVED 6 now describe the refreshed measurements and firmware binding.

Local validation passed at `a07a75de78b19369e228d4ab8403a52f7435fd64`: the capture gate and its controls, both simulation controls, the complete documentation gate set including all 22 steps after the capture gate, git and no-git documentation modes, both builder modes, declaration checks, firmware self-tests, and the three assigned simulation suites. Saved-state co-simulation passed 465 checks and detected 39/39 mutants. Both CI-event checks, bare-metal scope, the assigned em-dash base check and whitespace checks passed. Existing prerequisites were verified without downloads.

The compiler-absent mode deliberately leaves target-compiler checks unmeasured; the separate pinned compiler run covers them. The historical placed-utilization calibration report remains unavailable. Physical timing and memory ordering remain unmeasured. Independent re-review and hosted validation remain required.
