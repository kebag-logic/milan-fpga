[A613] REVIEW READY - Round 3

Head: `97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab`. Four new local commits; no push or PR edit.

R633-2-F1: the non-writable single-file runner passes the documented isolated invocation in a disposable boundary. Scope fixtures are inline and use the explicit worktree; a restored sibling import is rejected.
R632-2-F1: fixture Git and shell children isolate caller configuration, directories, identities and dates. Signing and GIT_DIR controls preserve the victim repository; automatic maintenance is disabled.
R632-2-F2: replay composes live base and head, then compares live against that tree. Hosted/replay paths agree for base-side renames and identical edits. REV and REV+E stay relevant; historical B16 stays two documentation paths.
R1 wording is corrected; S1 history wiring is independently guarded.

Validation: 197 scope assertions with 48 killing history mutations; 2021 CI-events contract items and 2850 arms; 566 runner assertions in ordinary and isolated flat-install forms; 42 independent paired scope cases. Documentation, source-list, evidence-reader and linked-image audit gates all exit 0. All five rebuilt images are byte-identical.

HANDOFF.md and PR-BODY.md contain the Round 3 scope, coverage, mutation, gate and image tables. Rejected development attempts and the corrected commit-order deviation are retained in the handoff. The prepared PR body retains Closes #734 and removes stale publication wording.

Independent re-review, manager publication, trusted full replay, hosted acceptance and current-dev candidate banks remain pending, with the 697c-then-696 sequence. No firmware behavior, linked-image or submodule-pin change occurred.
