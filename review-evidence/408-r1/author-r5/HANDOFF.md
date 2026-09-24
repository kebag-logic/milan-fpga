# HANDOFF — [A261] PR #535 (#408/#409) correction round 5

Status: DONE — head 991d59653ff82ccf73ef4df9477de1df8c8c5964 (local, NOT pushed; push is not
allowed for this role). "[A261] REVIEW READY" posted on #408 (see the end of this file). Stopped.

- Start head: 4a56ef08ffb5c6e4dc3d1d31761949870c5bbe23
- Final head: 991d59653ff82ccf73ef4df9477de1df8c8c5964, ONE commit on 4a56ef08, one-line subject,
  no body, no trailer (an earlier local c9d1b582 was amended with two doc-wording fixes before
  any evidence was finalised; every receipt under receipts/ is from 991d5965, see head.txt)
- PR-BODY.md: full updated PR #535 body for the manager to apply (starts with [A261], keeps
  Closes #408 / Closes #409, no home paths, no tool/model names, no footer)
- REVIEW-READY.md: the exact text posted on #408
- Scratch (outside this dir): $VALIDATION_STORAGE/408-a261/ — disposable pinned SDK
  (sdk/br-milan-rv32/host, `ci_rv32_sdk.py --verify-only` clean), reviewer scripts extracted from
  archives e73f083b (R272-5) and 87777959 (R273-6), large receipts listed in
  receipts/LEFT-IN-SCRATCH.txt
- Verilator: $VALIDATION_TOOLS/verilator-v5.050/bin (5.050) prepended to PATH for every gate run

## Inputs read
- Assignment #408 comment 5816286265; R272-5 (PR #535 comment 5816276559, archive e73f083b);
  R273-6 (PR #535 comment 5815827587, archive 87777959); decision #408 comment 5815136430

## What changed (991d5965; files: sw/builder/test_builder.py, docs/integration/BAREMETAL_FIRMWARE.md)
1. R272-5 F1, option (b): R272-5's 14 boundary templates B1-B14 appended to
   `_CLOSURE_POSITIONS` byte-identical to its BOUNDARY (checked by scripts/gen_closure.py), in-code
   flags equal. 6440 cells (23 x 280). `_CLOSURE_KEPT` re-recorded on the pinned GCC one file per
   call (receipts/closure_kept-recorded.txt); first 2520 letters unchanged; no new letter.
   Lone `#` at EOF named in `_CLOSURE_READERS_REFUSE`; `assert_character_closure()` asserts GCC
   keeps (a, z), readers refuse, `assert_directive_set_is_closed` refuses; a registry/cell
   mismatch stops the gate. Function kept at 99 lines (idiom gate limit 100).
   Sentences scoped: page cost row, S comment, lexer-bound comment; also S-table row 305, the
   closure paragraph (now a two-bullet list of the 9 + 14 positions), `_CLOSURE_SEQUENCES` comment,
   `assert_character_closure` docstring.
2. R273-6 F1: page S-table row (inside comment/literal), cost row (why + remedy "save the file as
   UTF-8"), refusal message, S comment. Measured: receipts/gcc-invalid-utf8.txt.
3. R272-5 S1: page uses correction-round numbering throughout; ledger paragraphs name commits;
   "first round" -> first head a13b6e2e; "#408's second round" -> PR #535's round one;
   "[R272] F1 on PR #535, round two" -> "...round-one head"; new round-five ledger paragraph;
   counts paragraph says 6440 (2520 before round five).
- Reviewer patch anchors (R272-5 r1/r5 patches, R273-6 disconnect patch) all still match once.

## Gates at 991d5965 (receipts/; all exit 0; gates never piped)
- gate 1b SDK: 280/280, 29/29 + 4/4, 1845/1845 + 6440/6440 re-measured, 0 NOT RUN, 467 compiles
- gate 1b absent: 222/222, 29/29 + 4/4, 1845 + 6440 as recorded, 1 NOT RUN, 0 compiles
- closure split: 3647 allowlist (226 closes), 246 other S, 1 named reader refusal, 2546 read
- whole test_builder.py: SDK-mapped wrapper exit 0 (EXCEPT 1 NOT RUN, gate 11); plain
  `--require-rv32` exit 0 (same); absent wrapper exit 0 (EXCEPT 2 NOT RUN, 0 compiles)
- static/rc.txt: docs_check git + no-git export, baremetal --check/--selftest, em_dash --base
  759da623, doc_style, gen_toc --check, doc_paths, py_idiom, git diff --check, tfc --selftest

## Can-fail evidence at 991d5965 (receipts/canfail/)
- NBSP added to phase-2 splice blanks: stops on "U+00A0 between a backslash and the line end in
  a line comment" (absent + SDK); lexer corpora pass first
- same patch with the table cut to 9 positions: GATE PASS both modes (222/222, 280/280)
- registry emptied / extra name / directive-set closure admitting a nameless `#`: each stops

## Reviewer probes at 991d5965, unchanged (receipts/r272-5, receipts/r273-6, comparisons.txt)
- R272-5 cases_r5_closure.py as-is: Part A AssertionError 6440 (its `== 2520`), exit 1
- same through its driver's --patch (9-position view): Part A 1470/32/1018 0 mismatches;
  Part B identical to its receipt row by row (4656); only disagree = lone `#`, reader null
- 3920 new table cells vs R272-5 Part B: 0 mismatches
- R273-6: subset 24/0; lexer_oracle 0/0 (+2 extra_lost as receipt); boundary 32/0; regex_audit
  197 (identical but line numbers); closure_extend exit 1 on raw count: A 1 = named lone `#`,
  B/C unchanged from receipt (32 GCC-refuses, 4 reader-refuses), 0 real holes; case probes 338
  cases, 0 verdict/pin changes vs its receipts at 4a56ef08; round2 0 changes; allowlist
  disconnect 12/12 fail both modes; intact 222/222; round3 lexer_probe same NameError

## Notes for the next session
- The Bash tool caps a foreground call at 10 min; the "probes" chunk of scripts/final_run.sh ran
  past it, was continued by the harness as a tracked task and completed exit 0 before I went on.
- Other sessions (546 lane) were loading the machine (load ~21 on 8 cores) during the runs.
- Not done (not in scope / not allowed): push, PR body edit, hosted/act, candidate merge.

## Commits
- 991d59653ff82ccf73ef4df9477de1df8c8c5964

## Posted
- [A261] REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5818553202
