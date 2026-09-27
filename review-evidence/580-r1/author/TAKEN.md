[A366] TAKEN
Branch: `580-pp-pin-16be6768`, from `682ecf0cb995473b72d5b4921088053ba753fc93`.
Executor: [A366]. Independent reviewers: [R352] and [R353].
Authoritative references: the issue body, all four [A10] comments through the assignment, REQ-VER-03/04, `docs/reference/SUBMODULES.md`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`, and the capture README/checker.
Interpreted scope: adopt processor `16be6768`; retain prior ROM ledger rows and record the new pin; update pin documentation/diagram, packer-test disposition, F7 ownership wording and capture receipt; compare all five configurations' AEM and builder artifacts between pins. The assignment settles the former dependency hold; the board is now In progress.
Validation plan: full builder bank in both compiler modes; OOC digest check; capture, test-evidence and port-contract checks; default pp_shadow and milan_dp suites; documentation gates and diff whitespace check. Stop if required capture remeasurement exceeds 24.5 ms for 8x8.
Blockers: none. Local commit and review handoff only, per assignment.
