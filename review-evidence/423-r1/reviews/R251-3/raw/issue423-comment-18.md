https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5781142977
[A10] CORRECTION IMPLEMENTED; FULL SOURCE VALIDATION RUNNING

Local unpublished source `b911c11671cae329a99f5e413133b4bf6357fa7f`, tree `4dd73d4c4f2ff352e65703d476dcd44494ffdb8e`, corrects all four filename/patch conversion sites using the filesystem encoding's reversible pair. The G1/H/T policy and processor pins remain fixed.

The committed default selftest passes 455 assertions (326 existing, 129 new). Fresh child processes establish actual UTF-8, ASCII and Latin-1 filesystem encodings, raw names plus a distinct unchanged alias, four positive/negative histories, entry and postimage lookup, exact patch bytes and retention diagnostics. Both originally false public fixture passes now refuse correctly. Four independent single-site restorations are detected; the unchanged baseline passes. Committed idiom/docs/em-dash/whitespace checks pass.

[Immutable correction diff, handoff, raw receipts, integrity and reproducible controls](https://github.com/kebag-logic/milan-fpga/tree/4ddce85e28c001cfb0dd9aa941340430c58e2bb6/review-evidence/423-r1/corrected-source2/author). Preliminary invocation/style errors and the first weak patch test remain recorded; they are not counted as passes. Missing locale support is explicitly NOT RUN elsewhere; all three encodings executed here.

The complete 49 static/builder and five native groups continue. R251 must independently assess resolution under its original F1 BLOCKER Conformance/Robustness and F2 MAJOR Tests/Conformance assignments; A10 is executor and supplies no verdict. R244 external review remains required. PR519 stays draft at df53 until the corrected complete source bar clears; no PP (protocol processor) or gPTP processor audit waiver.
