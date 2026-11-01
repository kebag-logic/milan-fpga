[A720i] TAKEN
Branch: 640-mark2-charter, from 20933ef48a9b174e58a9d17ddd59078a072024af. Nothing is pushed from this lane.
Authoritative references: R757-9 on PR #828 (issuecomment-6563425814), findings F1 and F2; docs/reference/FR_NFR.md NFR-RES-01; REQUIREMENTS.md; docs/ARCHITECTURE_HW_SW_SPLIT.md; docs/overview/ARCHITECTURE.md.
Interpreted scope: docs only. F1 makes docs/design/AREA_BUDGET.md agree with NFR-RES-01, keeping 60 percent and 38,040 only as marked history, with measured and gate-read figures unchanged. F2 makes the listed pages state the transition and end state, or point at the split contract. A docs-tree sweep follows, with what changed and what stayed listed. R758-8-R1 and R758-8-R2 are applied if the fix is exact. The charter's own figures and decisions do not change.
Validation plan: the full docs workflow on the committed head; check_doc_style on every touched page; git diff --check against the merge base; the reviewer's two searches re-run.
Blockers: none.
