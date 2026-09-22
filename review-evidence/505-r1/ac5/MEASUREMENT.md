# Issue407 AC5: observed workflow rejection

Normal candidate: 6af65a151663e1301f1983a6c9d22650a0b35da9.
Normal validation base: b17580b91deb11f3441dfc5d7f9fafe539d929b8.
Scratch candidate: 66ba210630ff7f412e5706427b3ea976ebee3ba2, PR506.

The scratch commit adds only ` || true` to docs.yml's Python idiom command.
Its complete diff is mutation.diff. The scratch PR must never merge.

The standard trusted live-dev runner executed the original workflows.
No candidate copy ran as the host orchestrator.
No custom AC5 fixture or instrumented workflow copy was executed.
Normal docs passed as the positive control in ../act-draft-fast/01.log.
Scratch commands and raw output are in ../ac5-act/.
Each invocation returned workflow-failure exit1, not setup-refusal exit2.
Both invocations completed, including the runner's cleanup checks.
The scratch checkout remained clean at its unchanged head afterward.

| Observed step or job | Result |
|---|---|
| Normal candidate docs workflow | PASS |
| Scratch Python idiom gate step | SUCCESS |
| Scratch CI event and SHA contract gate step | FAILURE |
| Scratch docs-check job | FAILURE |
| Scratch Hold every workflow file to its contract step | FAILURE |
| Scratch full-ci-gate job | FAILURE |
| Scratch verilator-suites aggregate | FAILURE |
| Scratch yosys-portability aggregate | FAILURE |

Both contract diagnostics identify job docs-check, Python idiom gate,
and canonical script line1. They print the original and altered commands.
The exhaustive aggregates actually run their mandatory verification steps.
They reject missing shard evidence: expected five Verilator and four Yosys
shards, with zero found after the failed selector.
Their SHA, inventory and worker-result checks fail too.
These are expected failures; they are not green candidate evidence.

The receipt checker passed, and the manager inspected raw step/job context.
The normal implementation remains unchanged by this experiment.
Independent review must still assess these receipts against AC5.
