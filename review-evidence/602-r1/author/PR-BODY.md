[A383]

Closes #602

## Status

Ready for review at local head `49012143b335ea48d6a71c441a05d0c1796887ff`. All 34 final-head validation commands returned 0, within the explicit coverage bounds below.

## Description

A PHC-only presentation-time re-base now preserves outgoing `mr` and adds no MEDIA_RESET under the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355). Render re-base, `tu` holdover, genuine source changes, selected-CRF disruption and received-`mr` propagation retain their behavior. The restart engine's executable source is unchanged.

The gmstep and INTERNAL option-off checks follow the ruling. Source-change and CRF-propagation controls prove the legitimate triggers still work. Design documents, compliance rows and module comments record the partial supersession of #387. Under the [scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253), a separate test-only commit updates the builder census, restart initializer, related mutation anchors and diagnostics. Builder generator code is unchanged.

## How to reproduce

Run `make -C tb/verilator/milan_dp gmstep`. The selected-CRF scenario drives a 1.5-second PHC step: one render re-base, continuing transport, `tu` holdover, zero outgoing `mr` transitions and no MEDIA_RESET increment. Real source changes and selected-CRF toggles must still propagate.

## How to validate

The full datapath target returns 0, including its render and default gmstep mutation campaigns (6/6 each). The clean gmstep leg passes 64 checks, and `gmstep-mutants` catches all 16 mutants with both clean controls passing. The restart-engine suite passes 96 checks and four mutants. Both full builder modes return 0: RV32-required gate 1b rejects 358/358 mutations; compiler-absent gate 1b rejects 256/256. Both elaborate 53/53 RTL variants. RTL lint, scope, bare-metal, documentation and whitespace checks return 0.

Both builder modes explicitly skip the absent historical placed-calibration report. Absent mode additionally records its compiler-dependent instruments as not run; the RV32-required run exercises them. These skips are not coverage claims.

The repeated OOC measurements return 0 on both AX shapes. Functional LUT deltas are +182 (1x1) and +1,606 (8x8); FF, memory, DSP and carry counts are unchanged. A semantically neutral base-source rename changes no cell counts on either shape. That control does not reproduce the LUT increase or establish its cause. Release area remains a placed-build measurement.

## Definition of done

All 50 generated artifacts across five configurations remain byte-identical. The executable RTL delta is confined to the restart-request term. Independent review remains pending. Physical clock continuity and placed area are outside this simulation/OOC evidence.
