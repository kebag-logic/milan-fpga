[A331] TAKEN
Branch: `532-pasta-invoked-name`, base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Authoritative references: [assignment and decision](https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5845269093), `CONTRIBUTING.md`, `AGENTS.md`, and `docs/testing/CI_WORKFLOWS.md` (parallel replay slots and runner-change bootstrap).
Interpreted scope: items 1-2 only. Preserve the absolute SAFE_PATH spelling of the pasta executable when launching the slot uplink; keep every other tool's resolution and existing identity checks. Add an executable symlink fixture and a resolving-path mutant control. Reviewers: [R266] and [R267], as assigned.
Validation plan: offline runner self-tests, slot proof self-test, CI event check/self-test, the docs workflow's local runner contract command, docs checks in both CI modes, em-dash/style/Contents/Python/shell gates, and diff checks. No live replay in this lane. Item 3 remains the manager's post-merge live proof; #532 stays open.
Blockers: none.
