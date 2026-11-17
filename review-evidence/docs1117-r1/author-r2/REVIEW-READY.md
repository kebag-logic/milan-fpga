[A795] REVIEW READY (round 2; replaces the round-1 REVIEW READY for review)
Commit: ee5c6f92 (branch docs-batch-merge: 490d54ee, then ee5c6f92, on dev 6b66f66d; the manager pushes it and opens the PR)
Changed: docs only, 3 files, +122/-3.
- 490d54ee applies the draft's text at its anchors. CONTRIBUTING.md gets section 2.3 "Batched merges", the batch path in the 2.1 diagram and the step-7 batch note. AGENTS.md gets the section 6 and 7 paragraphs, the amended completion bullet and two section 8 rules. docs/testing/CI_WORKFLOWS.md gets "Fast feedback".
- ee5c6f92 splits the three paragraphs over 30 words into short paragraphs, wording and order unchanged. AGENTS.md section 6 went from 40 to 19 + 21 words, section 7 from 63 to 23 + 21 + 19, and the CI_WORKFLOWS block from 70 to 24 + 19 + 27. Ignoring whitespace, the diff from 490d54ee is empty.
- Every new or changed paragraph is now 30 words or fewer (largest 29), and every new bullet 20 or fewer. The draft's standing-process wording is kept, as the owner asked.
Validation: the five docs workflow jobs (wire-accountability, docs-check-no-git, docs-gates-0/1/2), replayed step by step on a clean clone of ee5c6f92: 71 run steps, all rc 0, every job success (the two builder legs and the RV32 SDK install included; the three gate jobs re-run in full after a host restart). Hosted-only plumbing (evidence upload, the docs-check receipt union, apt resolution) was not run.
- docs_check 0 findings; check_doc_style OK; check_em_dash 0 findings over 122 added lines; gen_toc --check OK; check_doc_paths OK; docs_inventory fresh; check_feature_status 0 findings.
- gen_toc --verify-anchors: 620 cross-page fragment links (617 on dev). The three new ones are CONTRIBUTING.md#23-batched-merges from AGENTS.md (twice) and CI_WORKFLOWS.md.
- Planted mutants: a broken #23-batched-merges fragment in AGENTS.md or CI_WORKFLOWS.md fails gen_toc --verify-anchors ("MISS ... #23-batched-mergez"). A wrong ../CONTRIBUTING.md path fails docs_check ("broken link").
- Both CONTRIBUTING.md flowcharts render (the file is unchanged since 490d54ee).
Acceptance criteria: met. Section 2.3 is added, and the pointers and amendments are in CONTRIBUTING.md 2.1, AGENTS.md sections 6, 7 and 8, and CI_WORKFLOWS "Fast feedback", all on dev as docs only. The head descends directly from the unchanged dev tip, so its tree is the candidate merge tree.
Open risks/questions:
1. No docs gate checks a same-page (#fragment) link: a broken #23-batched-merges inside CONTRIBUTING.md would pass. The new one resolves under gen_toc's anchor walk. This gap needs its own Issue.
2. Member PRs marked merged by ancestry are not yet proved against check_merge_review_integrity and check_merge_containment --merged-prs. #940 records this as a follow-up after the first batch merge.
