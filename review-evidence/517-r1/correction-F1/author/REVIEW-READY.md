[A183] REVIEW READY

Commit: `ff7dac3257a321538a1fd1a310ab3190f646153d`; tree `f72080e7b96b078ce996926d8ccec66c1ca3dc74`. Correction parent: `5874895eb817ed41c0f8be4eb427ad3315c29844`; implementation base: `483a133ed08867ea0d300d2b4a027b5b48a4282f`. Source is clean and unpublished; PR524 remains draft.

F1 correction: ordered replay is retained on disk; nonblocking stdout delivery services cancellation. Owned simulations are killed/reaped before the final non-waiting output attempt and original-signal exit. Per-leg captures remain attributable. All ten commands/models, the two-child bound, exclusive ordered group, frame-presence behavior, build/prerequisite/render phases, policies, budgets and pins are preserved. No #523 driver changed.

Validation: 17/17 original runner arms, 24/24 phase arms, 28 direct/actual-Makefile backpressure controls, and relevant focused gates/selftests pass. INT/TERM copy/flush, descendant, repeated-signal and child-exit controls require shutdown/reaping before any drain. Eight restored-original-defect controls fail specifically for blocked shutdown. Policy controls preserve 264 positive/refusal cases and reject five broadenings. Preliminary failures remain attributed.

Fresh full-suite results at this commit, pinned Verilator 5.050, eight jobs/CPUs, 12 GiB:

| Full suite | Sequential | Two workers | Gain |
|---|---:|---:|---:|
| Cold | 1133.031 s | 1095.719 s | 3.293% |
| Warm | 980.614 s | 933.414 s | 4.813% |

Each run passes **9324 checks, zero failures, 13 tallies and 23 matching render identities**. Per-leg bytes/verdicts, input/executable identities and tracked headers match. Sampled ordinary/group peaks are 1/1 and 2/1; peak aggregate RSS is 2721328 KiB. Cold cleans build artifacts, not filesystem cache; warm retains same-mode builds. These are single local pairs, not guaranteed or hosted gains. Old7ab figures retain their old head.

The designated `517-f1-author` handoff contains HANDOFF.md, PR-BODY.md, commands/environment/exits, raw logs/samples, scripts and manifest. Final byte/kind/mode/index checks cover 854 parent and 539 required-submodule files; no owned simulation remains.

Scoped author acceptance 1-4 is evidenced. F1 remains MAJOR under **Conformance, RTL, Robustness, Tests and Docs**, pending R245 re-review. R246 and all manager publication/full-bank/new-CI/hosted-timing/current-candidate/merge/containment work remain pending. No author clearance, source push, PR mutation, other agent, act/Docker or prohibited host/tool/hardware action. Stopping at this local head.
