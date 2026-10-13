[A613] REVIEW READY - Round 4

Head: `59354ffe75697e17a16fd117d9ba853e104394bc`. Two new local commits; no push or PR edit.

R632-3-F1: the CI step now runs the complete mode-0555 single-file installation with isolated Python and the explicit checkout. The ordinary selftest also runs the complete isolated child. The reviewer's unrelated sibling import reproduces the previous CI escape, then fails both corrected forms; R01 and R03 remain rejected.

R632-3-R1: TESTING.md now distinguishes empty-delta relevance from failed PR revision or ancestry resolution. The prepared PR body retains one Closes #734 for later publication.

Validation: the exact CI step passes inside a disposable isolated job (566 ordinary assertions, 564 flat assertions). Scope: 197 assertions and 48 killing history mutations; CI-events: 2021 contract items and 2860 arms. All 30 before/after scope rows agree, including REV, REV+E and historical B16. Documentation, source-list, evidence-reader and image-audit gates pass. All five rebuilt linked images are byte-identical. Every accepted gate exits 0.

HANDOFF.md and PR-BODY.md contain Round 4 changes, gate/control receipts, scope, coverage, mutation and image tables. The corrected no-Git export setup failure is retained. Source is clean; product inputs and all gitlinks are unchanged. Independent re-review, manager publication, trusted replay, hosted acceptance and current-dev candidate banks remain pending, with the stated 697c-then-696 sequencing.
