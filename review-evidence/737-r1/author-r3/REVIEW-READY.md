[A614] REVIEW READY

Commit: `cf9c936697a06e44c41681bcc12dc612a3242eb2`

Changed: round-one workflow splitting, inventory-derived union proofs, exact install caches and manifest collection base; the resumed CPU rules now reserve manager-supplied 16-wide ranges (named 12-wide fallback), create containers directly on those ranges, retain leases through cleanup, and derive job build budgets from visible CPUs. Four jobs remain the global limit. No staging or post-creation movement remains.

Validation:
- Workflow contract: 2,186 items and 5,020 mutation controls pass.
- Complete offline runner self-test, 44 slot-proof controls, repeated race-enabled dispatcher controls and unchanged upstream common tests pass.
- All 16 selected suite workers pass; all six real case unions, physical collector and original tally pass: 62 physical logs, 2,187,186 checks, zero in-suite failures.
- Original documentation, firmware/RV32/coverage, boundary, builder, seven standalone simulations and 58-top synthesis gates pass. Every accepted command returned zero; failed environmental attempts remain identified with passing replacements.

Simulation workers used retained head `9a76ed5cf99996f433c82bcfde2fdb01fc05d743`. The final candidate reread their unions; `source-correspondence.json` records six unchanged source groups and the narrow scheduling/receipt differences. The candidate and four scratch source worktrees are clean; no worker container remains.

Evidence: final `HANDOFF.md`, template-based `PR-BODY.md`, 94-command receipt index, source correspondence, CPU controls, build provenance and log size/SHA-256 records are in the assigned handoff directory. No large build products are included.

Remaining coordination: hosted after-times and the full trusted replay are still required. The authorized continuous media-clock exception remains projected at 33m52s before downstream collection; its history is unchanged. Prebuilt-layer adoption, signing and the trigger/signature-gate scope change remain round two. No firmware behavior, linked image or test predicate changed. No push was performed.
