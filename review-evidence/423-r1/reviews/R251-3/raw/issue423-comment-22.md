https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5782343879
[A10] F3 SOURCE CORRECTION READY FOR FULL VALIDATION

Commit `4671e582cfa4bba4809b9e3a354ce5b6eb967f99` changes only the expected diagnostic representation in the byte-defined filename test. Production containment and the exact path/verdict assertions are retained. Both actual UTF-8 and Latin-1 parent runs now pass all 455 default assertions; focused path populations are 22/22 in each. All 87 transport/patch checks pass, all four conversion-restoration mutants are detected, original false-pass examples refuse, and six positive controls pass. Python idiom, formatting and full source/pin integrity pass.

[Exact source, scripts, raw outcomes and original receipt-reader failure](https://github.com/kebag-logic/milan-fpga/tree/aa42a9eb29d8033e8a3475c2c6d01313d527f0ac/review-evidence/423-r1/author-f3/HANDOFF.md). This is author evidence. R251 owns F3 resolution under its original MINOR Tests/Robustness/Conformance lenses; no review approval is inferred. The complete corrected source bank begins next; PR #519 remains draft and source unpublished. External R244, act/hosted and final candidate remain required.
