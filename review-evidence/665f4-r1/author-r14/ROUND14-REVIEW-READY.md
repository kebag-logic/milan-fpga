[A560] REVIEW READY
Commit: fe1cd0679f5028c749af7242c903a82ca2b3d692
Round 14, parent 154722e14781c7373f3229420b6e007f9bcf9835.

Added the exact lwSRP tuple to the trusted replay manifest. Updated its independent inventory/materialization checks, six refusal cases, two standing trust plants and the enumerated CI contract. Only scripts/act_ci.py and docs/testing/CI_WORKFLOWS.md change.

Validation: 442 offline runner checks; eight named source-mutation check/plant pairs; CI contract 1741 items / 2362 controls; 75 docs commands plus both source-archive gates; complete ctrl suite 51 arms / 1252 checks; builder; pinned SDK audit with 2146 compiler invocations and zero omitted arms. All 87 final command receipts return 0. Builder gate 11 calibration is explicitly NOT RUN because its physical place report is absent.

All assigned criteria are met. HANDOFF.md and PR-BODY.md retain earlier rounds and add Round 14 evidence, limits and reproduction details. Independent review and manager-owned trusted replay remain pending.
