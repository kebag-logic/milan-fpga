[A795] TAKEN
Branch: docs-batch-merge (from dev 6b66f66d)
Authoritative references: #665 issuecomment-6939460730 and issuecomment-6939574513; CONTRIBUTING.md 2.1 and 2.2; AGENTS.md sections 6, 7 and 8; docs/testing/CI_WORKFLOWS.md "Fast feedback".
Interpreted scope: docs only. Add CONTRIBUTING.md section 2.3 "Batched merges" (freeze, batch, compose once, check once, merge once, findings after composition, not batched). Add the batch path to the 2.1 diagram and a batch note to step 7. Add pointers and amendments in AGENTS.md sections 6, 7 and 8, and update the CI_WORKFLOWS "Fast feedback" lines that describe the merge train. No code, test or RTL change.
Validation plan: every docs workflow check on a clean clone of the final head (docs_check, check_doc_style, check_em_dash, gen_toc anchors and contents, check_doc_paths, docs_inventory, check_feature_status and the rest of the docs jobs), all rc 0.
Blockers: none
