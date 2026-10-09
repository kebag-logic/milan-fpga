[A581] TAKEN
Branch: 640-m0s
Authoritative references: assignment comment 6086604096; REQUIREMENTS.md section 1; docs/design/MARK_II_AREA_PLAN.md; docs/design/AREA_BUDGET.md; #664 and #665.
Interpreted scope: qualify the F0-F4 placement first, extend selected-placement resource measurement while preserving the accepted all-fabric and standalone references, and route only if fabric removal and firmware ownership are connected. If integration is absent, stop the route and complete tooling only, as assigned.
Validation plan: resource-tooling self-tests and named wrong-placement/missing-wrapper controls; affected source, documentation and code-quality gates; selected-placement route only after qualification.
Executor: [A581]. Internal reviewer: [R580]. External reviewer: [R581].
Blockers: placement qualification pending. The parent remains Backlog; this step proceeds under the explicit lane assignment.
