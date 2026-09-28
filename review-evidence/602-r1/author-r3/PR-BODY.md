[A383]

Closes #602

## Description

A PHC-only presentation-time re-base preserves outgoing `mr` and adds no MEDIA_RESET under the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355). Render re-base, `tu` holdover, genuine source changes, selected-CRF disruption and received-`mr` propagation retain their behavior. The ruling supersedes only the PHC-step restart obligation of #387.

## Round 3

Local candidate: `6b2ebd1c435136966f84ffc16d28a80c7d6b9387`. All assigned local gates passed at this committed head.

- Correct the firmware gate contract to two `media_rebase_p_w` references and the CRF-only `mcr_restart_p_w` initializer, citing #602. Both reviewers' stale-document scans now find zero stale current claims.
- Grade adjtime after settling, immediately before the settime baseline. The retained 16-cycle and 256-cycle delayed-cause controls fail only the adjtime check. The three existing controls keep their exact failure sets; clean option-off remains 234/0.
- Name the coincident check for suppression and document its pending-merge limit. Cite the round-2 reviewers' 42-phase measurement and correct the Makefile labels.
- Update the full inventory to fifteen gmstep and five option-off controls. The five default controls are unchanged.

RTL, builder, configurations and submodule pins remain unchanged from round-2 head `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`.

## Round 2

The preceding round corrected the FPGA design, register map, roadmap, changelog and harness narratives; made option-off checks event-relative; and added 32 timings of received CRF `mr` against software settime. Round 3 addresses the two remaining findings and the accepted wording suggestions.

## Validation

- Full `milan_dp` target: rc 0; gmstep 103/0; option-off 234/0; render controls 6/6; default gmstep campaign 6/6.
- Full gmstep campaign: 22/22, comprising two clean baselines and twenty caught mutants.
- `tkdiag`: 96/0, with all four mutants caught.
- Full builder bank in both compiler modes, both AX datapath OOC shapes, RTL lint, CI-scope self-test, baremetal checks, documentation gates and diff hygiene: rc 0.
- All fifty generated artifacts across the five configurations remain byte-identical. Both stale-document rescans are classified with zero stale claims outside history.

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273) closes the earlier OOC-area question. Release area remains a placed-build measurement.

## Evidence bounds

The gmstep harness uses compressed clocks and the streaming escape; it does not prove physical clock continuity or an lwSRP reservation. The compiler-absent mode omits compiled instruments; both builder modes omit the unavailable historical placed calibration report. `HANDOFF.md` records per-finding evidence, controls, scans and exact-head gate receipts. Independent re-review, hosted checks and merge-candidate validation remain separate completion requirements.
