[A795] REVIEW READY (round 3; answers R859-1 on PR #942 and replaces the round-2 REVIEW READY for review)
Commit: eade77c9 (branch docs-batch-merge: 490d54ee, ee5c6f92, eade77c9, on dev 6b66f66d; the manager pushes it to PR #942)
Changed: docs only. +14/-6 against ee5c6f92 and +130/-3 against dev, in AGENTS.md, CONTRIBUTING.md and docs/testing/CI_WORKFLOWS.md.
- R859-001: freezing applies only to a PR a maintainer has named in a batch. An unbatched PR follows section 2.1 as before. It may merge the moving base, and that merge is reviewed under 2.1 as new change. This is stated in CONTRIBUTING.md 2.3 Freeze (447-448, 454-455), AGENTS.md section 6 (298-303) and section 8 (475).
- R859-001, the urgent-fix case: an urgent fix that conflicts after two positives is unbatched (2.3:509), so it is not frozen (447). It merges the base, that merge is reviewed under 2.1 (454-455), and it then goes through step 7's candidate.
- R859-002: 2.3 links the maintainer decision (#940 issuecomment-6941861692) next to the two #665 decisions (CONTRIBUTING.md:428). No rule text changed for it. Every 2.3 rule traces to one of those three comments.
- R859-003: in CI_WORKFLOWS "Fast feedback", the two batch lines now follow the "Those banks" paragraph, so "Those banks" sits after its antecedent again. No word changed.
- R859-004: the 2.3 flowchart gains the edge CR -->|finding| CO.
- R859-006: not taken. Three of the four Contents entries are already over 30 words (31, 36 and 76), so adding to them would break the limit.
- Every new or changed paragraph is 30 words or fewer (largest 30), and every new bullet 23 or fewer.
Validation: the five docs workflow jobs (wire-accountability, docs-check-no-git, docs-gates-0/1/2), each replayed step by step on its own clean clone of eade77c9 in a booked unit: 71 run steps, all rc 0, every job success. The two builder legs and the RV32 SDK install are included. Hosted-only plumbing (evidence upload, the docs-check receipt union, apt resolution) was not run.
- docs_check 0 findings; check_doc_style OK; check_em_dash 0 findings over 130 added lines; gen_toc --check OK; check_doc_paths OK; docs_inventory fresh; check_feature_status 0 findings.
- gen_toc --verify-anchors: 621 cross-page fragment links (617 on dev). The new ones are three CONTRIBUTING.md#23-batched-merges links and one CONTRIBUTING.md#21-the-issue-to-merge-lane link.
- Planted mutants: a broken fragment in AGENTS.md (either link) or CI_WORKFLOWS.md fails gen_toc --verify-anchors. A wrong ../CONTRIBUTING.md path fails docs_check.
- Both CONTRIBUTING.md flowcharts render.
Acceptance criteria: met. The head descends directly from the unchanged dev tip, so its tree is the candidate merge tree.
Open risks/questions:
1. Same-page (#fragment) links are not gated (#941). The new one resolves.
2. Member PRs marked merged by ancestry are not yet proved against check_merge_review_integrity and check_merge_containment --merged-prs. #940 records this as a follow-up after the first batch merge.
