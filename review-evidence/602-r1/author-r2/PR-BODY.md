[A383]

Closes #602

## Description

A PHC-only presentation-time re-base preserves outgoing `mr` and adds no MEDIA_RESET under the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355). Render re-base, `tu` holdover, genuine source changes, selected-CRF disruption and received-`mr` propagation retain their behavior. The ruling supersedes only the PHC-step restart obligation of #387.

## Round 2

Local candidate: `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`. All assigned local gates passed at this committed head.

- Correct the FPGA design, register map, roadmap and changelog. Current documents consistently exclude PHC-only `mr` and MEDIA_RESET causes.
- Correct campaign routing and inventory: fifteen gmstep controls, three option-off controls, five default controls, and the restart-engine source among the triggers. Mark historical counts explicitly. The restart-engine harness describes genuine restart requests.
- Compare each option-off event against its preceding `mr` level. Adjtime-only fails only its own event check; settime-only and both-causes fail the settime check. The mutation driver enforces the sibling-check exclusions.
- Add 32 timings of received CRF `mr` against software settime. Every trial steps the PHC and transmits exactly one outgoing toggle. The run observes same-cycle overlap at delay 8. A mutant that suppresses the received restart on that cycle fails only the new check.

RTL, the five configurations, builder code and submodule pins remain unchanged from round-1 head `49012143b335ea48d6a71c441a05d0c1796887ff`.

## Validation

- Full `milan_dp` target: rc 0; gmstep 103/103; render controls 6/6; default gmstep controls 6/6 including the clean baseline.
- Complete gmstep inventory: 20/20, comprising two clean baselines and eighteen caught mutants.
- `tkdiag`: 96/96, with all four mutants caught.
- Both complete builder modes, both AX datapath OOC shapes, RTL lint, CI-scope self-test, baremetal checks, documentation gates and diff hygiene: rc 0.
- All fifty generated artifacts match across the five configurations; RTL/configuration/builder bytes and submodule pins/contents match the starting head. Final stale-document rescan: 41 candidates inspected, zero stale claims.

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273) closes the earlier OOC-area question. R366-1 measured exactly one fewer OR gate before LUT mapping; the mapped LUT changes reflect mapping sensitivity. Release area remains a placed-build measurement.

## Evidence bounds

The gmstep harness uses compressed clocks and the streaming escape. It does not prove physical clock continuity or an lwSRP reservation. The compiler-absent mode omits compiled instruments; both builder modes omit the unavailable historical placed calibration report. Controls and exact gate receipts are recorded in `HANDOFF.md`. Independent re-review, hosted checks and merge-candidate validation remain separate completion requirements.
