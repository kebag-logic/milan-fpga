[A276] Retire gate 1b's text rules onto per-selection grading, preprocessing, resolved include paths and the resolved store census (#408, #409)

## Status

Correction round 6 is prepared at `062e89ad098806ae5def8341fcb8c2815583ca00`, based on `991d59653ff82ccf73ef4df9477de1df8c8c5964`. The lane's source base is `759da623072358afdb0e9d570a7b4b6a788492c9`.

`408-409-boot-gate-retire` targets `dev`. This body is prepared for the manager to publish with the correction. All required round-six local checks returned 0 at this head. Independent re-review and manager publication remain pending.

Closes #408
Closes #409

Executor: [A276], correction round 6.
Internal independent reviewer: [R272].
External independent reviewer: [R273].

## Description

The pinned RV32 compiler supplies three instruments: preprocessing with `-E`, resolved include paths with `-H`, and the resolved store census. Gate 1b retires or narrows the text rules that these instruments replace. Hosted builder consumers require the pinned SDK. A run without an RV32 compiler explicitly registers the missing instruments and counts their mutations as skipped.

Within the declared lexical subset S, conditional groups are graded one arm selection at a time. Each selection passes through the whole boot-contract gate. Groups testing whether one macro is defined are graded together. The verifier's QSPI-slot group and the saved-state error guards remain subject to their retained restrictions.

S begins with a character allowlist. Outside comments and literals it admits printable ASCII, tab, line feed, vertical tab, form feed, carriage return and NUL. Unsupported characters and token classes are refused before directive readers run. Inside comments and literals, UTF-8 characters are permitted; undecodable bytes are deliberately refused even where the pinned compiler accepts them.

Reader agreement is measured by two lexer corpora and a character-closure table. Allowlist refusal is independent of position. Character agreement is measured at the table's 23 positions; elsewhere it rests on the lexer corpora. These are bounded measurements, not exhaustive coverage of the language.

| Rule | Disposition | Evidence or surviving cost |
|---|---|---|
| Conditional reaching a boot-path body | Retired onto per-selection grading | A debug `printf` conditional inside `milan_init()` is accepted; every selected firmware is graded |
| Conditional carrying a definition or include | Narrowed to the verifier group and error guards | A conditional choosing a definition in a UART handler is accepted |
| Token-joining splice and token paste | Narrowed to six boot-path bodies and reachable macros defined in this file | A splice inside a macro body and a paste building a call outside the boot path are accepted with the instruments live |
| Read-only macro accessor | Narrowed | A macro over `milan_read()` is accepted; macro bodies naming `milan_write()` or `milan_reg()` remain refused |
| Firmware-directory listing | Retired onto resolved include paths | A README and a notes file beside the firmware are accepted; a shadowing pinned header is refused by its resolved path |
| Include-name set | Retained | Resolution is measured in the tree handed to the compiler; pinned header contents remain trusted |
| Ordered pointer-cast, pointer-store and inline-assembly sets | Retired onto the resolved census | Outside-window casts/stores, a fence and reordering two functions are accepted; window stores are refused by value, subject to the helper limitation below |
| Directive set and lexical subset S | Retained or explicitly narrowed | Unsupported directives, null directives, unsupported lexical constructs and characters outside S remain stated costs |

Earlier corrections established the shared translation-phase lexer, closed S, added the character allowlist, and expanded the closure table from 9 to 23 positions. Round five also corrected the invalid-UTF-8 explanation and the correction-round ledger. Round six preserves those mechanisms and every existing mutation and accepted-edit entry.

## Correction round 6

Assignment: [#408 correction round 6](https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5820090472).

Reviews: [R273-7](https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5818979463) and [R272-6](https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5820082965), both at `991d5965`.

| Finding | Change | Validation |
|---|---|---|
| R273-7 F1, MINOR, Docs | The gate-call comment now states position-independent refusal, agreement measured at 23 table positions, and the lexer-corpus bound elsewhere | Scoped wording agrees with the other corrected sites; documentation gates pass |
| R273-7 S1 | The page and cost row name null-directive refusal wherever the directive appears | Documents the existing directive-set restriction |
| R272-6 S1 | One fixed corpus case holds `/*/` followed by a hidden definition and its conditional use | The pinned compiler keeps `a` and `z`; the early-closer regression keeps `a`, `b`, `z` and stops gate 1b in both modes |
| R272-6 S2 | Comments and the page distinguish the directive-line continuation boundary from comment/literal boundaries | Eleven comment/literal positions, one directive-line position and two file-end positions remain the same table entries |
| R272-6 S3 | Three ambiguous finding references now name the reviewed heads | Dollar-identifier references name `8e12d31f`; the form-feed reference names `a13b6e2e` |

The added corpus case is the only executable change. Removing that row makes the syntax tree identical to `991d5965`; all remaining changes are comments or documentation. The corpus now holds 1846 spellings: 79 fixed and 1767 generated. The 6440 closure cells are unchanged.

## Validation

| Check | Exit | Result |
|---|---|---|
| Full builder, verified SDK mapped, `--require-rv32` | 0 | 280/280 mutations; 29/29 + 4/4 accepted edits; 1846/1846 spellings; 6440/6440 cells; 1 named NOT RUN |
| Full builder, cross compilers hidden | 0 | 222/222 mutations; 29/29 + 4/4 accepted edits; 1846/1846 spellings; 6440/6440 cells; 0 firmware compiles; 2 named NOT RUN |
| `python3 -B scripts/docs_check.py`, repository mode | 0 | 0 findings |
| `python3 -B scripts/docs_check.py`, no-metadata CI mode | 0 | 0 findings |
| `python3 scripts/check_baremetal_only.py --check` | 0 | PASS |
| `python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9` | 0 | PASS |
| `python3 scripts/check_doc_style.py` | 0 | PASS |
| `python3 scripts/gen_toc.py --check` | 0 | PASS |
| `python3 scripts/check_doc_paths.py` | 0 | PASS |
| `python3 scripts/check_py_idiom.py` | 0 | PASS |
| `git diff --check` | 0 | Clean |
| `git diff --check 991d59653ff82ccf73ef4df9477de1df8c8c5964 HEAD` | 0 | Clean |

The compiler-absent result is deliberately weaker. It reports `TEXT RULES ONLY, AND WEAKER`, with the three missing instruments registered as one NOT RUN. Gate 11 also remains NOT RUN because no implementation report is available. These skips are named in the final suite verdict.

The `/*/` control was measured separately on the pinned compiler. A disposable, in-memory mutation starts the block-comment closer search at `i + 1` instead of `i + 2`; the new corpus case refuses that regression in SDK and compiler-absent modes. The worktree lexer was never mutated for this control.

The current round's full-suite runs and static checks are recorded in the author handoff. Earlier rounds' extensive probes remain earlier evidence; this round does not claim to have repeated them.

## Reproduction

Use the lane head and initialise its pinned source dependencies. Run the full `sw/builder/test_builder.py` with the pinned SDK selected and `--require-rv32`. The local SDK run uses the assignment's runner method: only the existing absolute compiler selector's argument zero is mapped to the verified SDK, preserving every other argument and subprocess option. The full compiler-absent run hides all cross-compiler candidates through the repository's existing audit helper and verifies zero firmware compilations.

The handoff includes both full-suite runners and their argument receipts. The focused repository drivers remain available:

```sh
python3 sw/builder/test_firmware_compiler.py --sdk-destination <sdk-dir> --audit <sdk-audit.jsonl>
python3 sw/builder/test_firmware_compiler.py --absent --audit <absent-audit.jsonl>
python3 sw/builder/test_builder.py --require-rv32
python3 -B scripts/docs_check.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
git diff --check
```

Repeat the documentation check on a tracked-source export without repository metadata for the second CI mode. All required commands must return zero. Acceptance 4 requires at least 280/280 mutation refusals with the SDK and 222/222 without it.

## Known limitations

- Without an RV32 compiler, the retired instruments cannot refuse an outside-boot-path token join/paste, a resolved shadow include, a store whose address only the census resolves, or a conditional-arm defect outside the retained text rules.
- The lexer corpora and the 23-position closure table provide bounded agreement. They are not a per-firmware compiler oracle. The table's named lone-`#` cell is refused by the readers and directive-set closure although the compiler accepts it.
- A byte-order mark in code and invalid UTF-8 anywhere remain explicit refusal costs. Save the source as UTF-8 and spell code within the allowlist.
- Boot-path identifier anchors, one definition per name, macro-body restrictions and the retained directive/include-name sets remain costs documented in the page.
- Header-defined macros are trusted. The pre-existing identity-forging function-like macro and header-paste limitation remains #544. The verifier-group missing-else limitation is also unchanged.
- Stores planted in the address helper are refused first by its return-provenance rule, before the resolved census.
- `-H` proves resolution in the supplied tree, and `-E` compares against the census stub definitions. Different product definitions are outside that comparison.

## Authoritative references

- #408 and #409, especially acceptance 4's no-reduction requirement.
- [Round-six assignment](https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5820090472), [round-five assignment](https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5816286265), and [the encoding decision](https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5815136430).
- PR #498, #504 / PR #521, and the #153 retirement pattern in PR #241.
- C11 5.1.1.2, 5.2.1, 6.4 and Annex D.
- `docs/integration/BAREMETAL_FIRMWARE.md`: the subset, closure, cost and retirement tables.
- `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`: verification, review and merge requirements.

## Definition of Done

- [x] Scoped round-six corrections implemented
- [x] Existing mutation and accepted-edit entries retained
- [x] Added regression spelling measured and shown to detect its defect
- [x] Required round-six local checks complete
- [x] Documentation reflects the bounded evidence
- [ ] Correction published with exact-head evidence
- [ ] Independent reviews and reviewer-owned lens ledger cover the final head
- [ ] Required hosted checks and local workflow replicas accepted at that head
- [ ] Candidate merge validated against current `dev`
- [ ] Maintainer authorizes merge
- [ ] Post-merge containment and issue completion
