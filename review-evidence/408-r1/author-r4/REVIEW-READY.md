[A254] REVIEW READY
Commit: 4a56ef08ffb5c6e4dc3d1d31761949870c5bbe23 (on 11b1b86c; a local commit, not pushed, per the assignment)
Changed:
- `sw/builder/test_builder.py`:
  - A character allowlist is checked first in `assert_within_lexical_subset()`, on every machine, before any reader. Pin: `SUBSET_CHARACTER_PIN`. The rule:
    - Outside a comment or a literal, only printable ASCII U+0020..U+007E plus HT, LF, VT, FF, CR and NUL are admitted. Every other character is refused by name: every non-ASCII one, a byte-order mark at offset 0 included, and every other control.
    - Inside a comment or a literal, any UTF-8 character is allowed.
    - A byte that is not UTF-8 is refused anywhere. The firmware read keeps such a byte as an escape so that S names it.
  - Readers: `re.ASCII`/`(?a)` on every C text regex. The lexer's raw-prefix test now uses an ASCII set.
  - A generated closure table: `_closure_corpus()` + `_CLOSURE_KEPT` + `assert_character_closure()`. It has 2520 cells: bytes 0-255, 20 UTF-8 sequences and 4 byte strings that are not UTF-8, each in 9 positions. Each cell is refused by S or read as GCC recorded it, and every cell is re-measured on the pinned GCC. The negative control is U+00B7 inside a directive name.
  - `lexer_keeps` skips groups nested in dropped arms.
  - Mutations: 9 new allowlist entries. The 3 byte-order-mark entries are re-pinned on the allowlist. The accepted byte-order-mark case moved into the mutation table.
- `docs/integration/BAREMETAL_FIRMWARE.md`:
  - The S table gains 5.2.1 rows: the exact allowlist, and the rule for comments and literals with the reason no reader sees those characters.
  - New: the closure-table and ASCII-mode paragraph, an allowlist cost row, and the fifth-round disconnect paragraph.
  - Updated counts.
- The gate print states the allowlist and the closure counts as the gate runs.

Validation (at 4a56ef08; every run's output was written to a file and its rc recorded):
- `python3 sw/builder/test_builder.py --require-rv32` (pinned SDK present): rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report).
- `test_builder.py`'s own `__main__` under the CI compiler-absent audit (every cross compiler hidden): rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's registered instruments, gate 11), 0 firmware compiles.
- `sw/builder/test_firmware_compiler.py --sdk-destination <verified pinned SDK>`: rc 0, `GATE 1b PASS; 0 NOT RUN`.
  - 280/280 mutations; 29/29 + 4/4 edits accepted.
  - 1845/1845 spellings and 2520/2520 closure cells, all re-measured.
  - Closure cells: 1470 refused by the allowlist (43 of them the readers and GCC read differently), 32 refused by another rule of S, 1018 read as GCC reads them.
- `--absent`: rc 0, `GATE 1b PASS; 1 NOT RUN`; 222/222; 29/29 + 4/4.
- `python3 -B scripts/docs_check.py`: rc 0, both with git and on a no-git working-tree copy.
- Also rc 0: `check_baremetal_only.py --check` (and `--selftest`), `check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9`, `check_doc_style.py`, `gen_toc.py --check` (and `--verify-anchors`), `check_doc_paths.py`, `check_py_idiom.py` (and `--selftest`), and `git diff --check` (on the tree and on `759da623..HEAD`).

Acceptance criteria:
- Direction 1, the allowlist: met, with the exact set above. The shipping firmware is inside S (printable ASCII, LF and HT only).
- Direction 2, ASCII readers: met. An audit of all 159 regex calls in the rule range finds none left non-ASCII on C text; the 51 without the flag read SV, Makefile text, assembly, `milan_soc.py`, `-H` output or diagnostics.
- Direction 3, the generated closure: met, with 0 holes.
  - Every reviewer probe of rounds one to four was re-run at this head. Of the 89 reader-level spellings from the reviewers' own files, S refuses 62 and the readers read the other 27 as GCC does.
  - R273-5's `subset_probe.py`, run unchanged: 24 spellings, 0 holes. Its `lexer_oracle.py`, unchanged, is identical to its round-three receipt.
  - 233 whole-firmware cases through the reviewers' own drivers in both modes, plus R272-2's split-digraph probe (4/4 refused). Every verdict change against 11b1b86c is accepted -> refused.
- Disconnect, removing the allowlist:
  - `subset_refusal_corpus` trips first, on U+00B7 after `#if`. With that bypassed, the closure table trips on byte 0x01.
  - With both bypassed, R273-5's `nest.s` shape (MD1 U+00B7, MD1a U+0387, MD1b U+203F) passes the whole gate without a compiler.
  - R272-4's `mid.c`/`comb.c` and R273-5's misnest spellings pass S and disagree with GCC: 22 of 89.
  - 8 of the 12 allowlist-pinned entries pass without a compiler.
- Direction 4, acceptance 4: met. No entry is lost; 280/280 with the SDK (was 271) and 222/222 absent (was 213); the allowlist has 9 entries of its own.
- Direction 5, docs and gate print: met.

Open risks/questions:
- The byte-order mark at offset 0, accepted since round two, is now refused, following "every non-ASCII byte". If it should instead be admitted as a phase-1 artefact, the 3 re-pinned entries return to their round-two pins and the accepted case returns (30/30).
- A byte that is not UTF-8 inside a comment is refused, although GCC accepts it there. That cost is stated.
- ASCII mode is defence in depth, not a second closure, measured: without the allowlist the readers disagree with GCC on extended characters in either mode.
- Reviewer probes: the allowlist is inline and the new constants use the `_C_` prefix, so the round-three extractors load S unchanged. R273-3's round-one-layout `lexer_extract.py` fails with `NameError: _c_phases` at 11b1b86c as well; it is pre-existing.
