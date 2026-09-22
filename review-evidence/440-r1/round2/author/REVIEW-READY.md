[A164] REVIEW READY
Commit: 9d6109ccf924c03308cb8aa202ce68a435cd4f8d
Tree: 1d322d866da6b8d19ccd46cfd7ef5f405e9dadb4
Parent: 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba
Base / actual merge base: b17580b91deb11f3441dfc5d7f9fafe539d929b8

Changed: only R226-F1 test fixtures, the existing TOC floor, and DOC_GENERATION.md coverage text. Twenty-four new raw arms and six shipped-label rows reject other ASCII closer names; parser and policy bytes are unchanged. One local one-line commit, no trailers, no push.

Validation: gen_toc --selftest 707/707, --check 105 lists, --verify-anchors 144 links, --sites 25 single-source sites; check_em_dash --selftest 57 controls; post-commit --base b17580b91deb11f3441dfc5d7f9fafe539d929b8 zero findings over 34 added lines. docs_check, check_doc_style, check_doc_paths, staged/committed diff formatting and tracked source/index/mode integrity all pass. Exact commands, raw outputs and exits are in COMMANDS.md and commands/.

Acceptance evidence: original R15(div), R16(title), X04(xmp) mutations survive 683/51 and admit their hidden CLI labels. Corrected mutations fail eight named raw cases and two named label rows each; corrected mutated real E14/E15 CLI runs exit 2 on permanent controls before judgment. Correct unmutated CLI rejects hidden labels and exempts valid E03. All old fixture identities and counts remain; new totals are 707/57. Empty/decreased new raw population fails the floor; a valid added case passes 708. Exact patches and CLI receipts are under original/results/, corrected/results/, and maintenance/; OUTCOMES.json checks their interpretation.

Open risks/questions: no new implementation question. R226-F1 remains subject to independent Tests/Docs re-review. R225/R226 alone decide any coverage retained from unchanged artifacts. Manager owns publication, push and full-native/act/hosted obligations. No author review verdict, completion ledger or completed merge claim is made.
