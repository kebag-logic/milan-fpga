[A261] REVIEW READY
Commit: 991d59653ff82ccf73ef4df9477de1df8c8c5964 (branch `408-409-boot-gate-retire`, one commit on `4a56ef08`, local and not pushed: the push and the PR body update are the manager's. The updated body is in the packet)

Changed (correction round 5, assignment https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5816286265):
- R272-5 F1, option (b):
  - `_CLOSURE_POSITIONS` gains R272-5's fourteen comment and literal boundary positions B1-B14. The templates are byte-identical to its Part B. The table now holds 6440 cells, 23 positions x (256 bytes + 24 sequences).
  - `_CLOSURE_KEPT` was re-recorded on the pinned GCC one file per call. The first 2520 letters are unchanged, and no new outcome letter was needed.
  - The lone `#` at end of file stays refused, fail-closed. It is named in `_CLOSURE_READERS_REFUSE`, and the table checks that GCC keeps (a, z), that the readers refuse it and that `assert_directive_set_is_closed()` refuses it.
  - The three sentences (`BAREMETAL_FIRMWARE.md` cost row, the S comment, the lexer-bound comment) now say what the table holds. Refusal is position-independent, because the allowlist scans the whole code text. Agreement is measured at the 23 positions the table holds, and elsewhere it rests on the lexer corpora. "Each position a lexing difference moves a directive" is removed. The S-table row, the closure paragraph and the `_CLOSURE_SEQUENCES` comment are aligned.
- R273-6 F1: the four sites (page `:306` row, cost row, refusal message, S comment) state that the pinned GCC accepts a byte that is not UTF-8 in a comment or a literal. S refuses it by decision, as a fail-closed choice, and that is a cost. The cost row's remedy adds: save the file as UTF-8. Re-measured: the pinned GCC gives rc 0 at `-E` and `-S` for a block comment, a line comment, a string literal and a char literal, and warns only under `-Winvalid-utf8`.
- R272-5 S1: the page uses one scheme, PR #535's correction rounds, throughout. The ledger paragraphs are renumbered, and each names its commits (round one `75066c16` `d8abee3e` `ef903457`, round two `8fd74a99` `479a2175` `8e12d31f`, round three `11b1b86c`, round four `4a56ef08`). A new round-five paragraph states the table extension and its disconnect result.
- Files: `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md`. No other acceptance change.

Validation (all at 991d5965, gates not piped; every gate and static check exits 0):
- `python3 -B sw/builder/test_firmware_compiler.py --sdk-destination <verified pinned SDK> --audit ...`: GATE 1b PASS, 0 NOT RUN, 467 compiles.
  - 280/280 mutations, 29/29 + 4/4 accepted edits, 1845/1845 spellings.
  - 6440/6440 closure cells in 23 positions, re-measured on riscv32-linux-gcc: 3647 refused by the allowlist (226 closes), 246 by another S rule, 1 by the readers and the directive-set closure (byte 0x23 at the end of the file), and 2546 read as GCC.
- `python3 -B sw/builder/test_firmware_compiler.py --absent --audit ...`: GATE 1b PASS, 1 NOT RUN, 0 compiles. 222/222, 29/29 + 4/4, the same 6440 split as recorded.
- Whole `sw/builder/test_builder.py`, run three ways:
  - selector mapped to the verified SDK: exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11);
  - plain `--require-rv32`: exit 0, the same;
  - every cross compiler hidden: exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN`, 0 compiles.
- Static checks, each exit 0:
  - `python3 -B scripts/docs_check.py`, with git and on a git-less export;
  - `check_baremetal_only.py --check` and `--selftest`;
  - `check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9`;
  - `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`;
  - `git diff --check`;
  - `test_firmware_compiler.py --selftest`.
- The new cells can fail (in-memory patches):
  - Widening phase 2's splice blanks by U+00A0 passes both lexer corpora, then stops the gate on "U+00A0 between a backslash and the line end in a line comment", with the SDK and absent.
  - The same widening with the table cut back to its nine round-four positions passes the whole gate in both modes (280/280, 222/222).
  - Each of these also stops the gate: `_CLOSURE_READERS_REFUSE` emptied, an extra name added to it, and a directive-set closure that admits a nameless directive.
- R272-5 `scripts/r5/cases_r5_closure.py`, unchanged, through its own `probe_gate1b.py --absent`:
  - Run as is, its Part A stops on its own `== 2520` assertion. The table is 6440 now.
  - With its own `--patch` presenting the nine round-four positions, Part A gives 1470/32/1018 with 0 mismatches.
  - Part B is identical to R272-5's `partB-boundary.json` row by row (4656 cells): 1595 admitted, all agreeing but the lone `#` at end of file, which the readers refuse (`reader: null`), fail-closed.
  - The 3920 new table cells match R272-5's Part B outcomes cell for cell.
- R273-6's probes, unchanged:
  - subset_probe 24 spellings, 0 holes. lexer_oracle 0/0, as its receipt. boundary_probe 32 spellings, 0 holes. regex_audit 197 calls, identical to its receipt but for line numbers.
  - closure_extend re-derived all 6440 table cells, with 0 record mismatches, 226 closes and the negative control present. It exits 1 on its raw HOLE count. Part A holds 1 of them, the named lone `#`, which the reader refuses. Parts B/C are unchanged from its receipt: 32 GCC refusals and 4 reader refusals. 0 cells where both read names and differ.
  - Case files r1, r2, bom, extra, grader, hi, md, published, unread and v272, in both modes: 338 cases, 0 verdict or pin changes against R273-6's receipts at `4a56ef08`.
  - Round-two gate probe: 0 changes. Allowlist disconnected: 12/12 fail in both modes. Intact: 222/222.
  - round3 lexer_probe: the same pre-existing `NameError`.

Acceptance criteria:
- Assignment item 1 is met. B1-B14 are all in the table: every new cell is refused or agrees, the lone `#` is refused, and the three sentences are scoped.
- Item 2 is met at the four sites. Item 3 is met: one scheme, with the commits named.
- #408/#409 acceptance 4: 280/280 SDK and 222/222 absent, 29/29 + 4/4 (not below 280/222).
- Nothing else the gate accepts or refuses changed.

Open risks/questions:
- The table's claim is now scoped to its 23 positions. Agreement at any other position still rests on the two lexer corpora, as the page states.
- The table's one fail-closed cell, the lone `#`, is a pre-existing refusal of an edit GCC accepts. It is named, not changed.
- Hosted and act evidence at this head, and the candidate merge, are the manager's once it is pushed.
