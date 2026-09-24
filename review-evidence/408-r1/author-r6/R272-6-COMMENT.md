[R272] POSITIVE - exact head 991d59653ff82ccf73ef4df9477de1df8c8c5964

# R272-6: internal independent review of PR #535 (#408, #409), correction round 5

- Head `991d59653ff82ccf73ef4df9477de1df8c8c5964`, tree `07df25436405c718275b0238d02e1caeb85aec2a`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Round under review: correction round 5, one commit on `4a56ef08`. It answers R272-5 F1 MINOR (closure-table scope, option (b)), R273-6 F1 MINOR (the invalid UTF-8 wording) and R272-5 S1 (round numbering).
- Context was rebuilt from public state: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #408 and #409 bodies, and the manager decisions 5811522505, 5813535416, 5815136430 and 5816286265. Then the full diff `759da623..991d5965` and the round-5 delta `4a56ef08..991d5965`, and the author's REVIEW READY comment 5818553202.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five lenses were applied at this head and each is covered CLEAN. The three findings below are SUGGESTIONs and do not affect coverage.

This verdict and its ledger were written before I read any prior finding. That copy is `receipts/verdict-before-prior-findings.txt`, sha256 `fdd0eb2ba6a8fbc72a990e842293a1c404b72fdc5a13fe8d93e1ea3dc814126d`. Reading the prior findings afterwards changed nothing in it. I did not read the concurrent external review of this same head, so the two reviews stay independent.

What the round claims, and what this review measured:

- **Every table cell is refused or agrees with GCC.**
  - Gate 1b passes at the head in both modes: with the pinned SDK, and with every cross compiler hidden.
  - Separately, all 6440 cells were re-measured one file per cell on the pinned GCC: 0 mismatches against `_CLOSURE_KEPT`.
  - The only cell S admits that the readers read differently is the named lone `#` at end of file. The readers refuse it. On the whole shipping firmware, the directive-set closure refuses it on its own pin.
- **The new cells can fail.**
  - I reproduced the author's no-break-space splice mutant.
  - I added three lexer mutants of my own. Each passes both lexer corpora and all nine round-four positions, and trips only a round-five cell.
  - Two of them, including my digit-separator mutant, stop the whole gate with the full table and pass it 280/280 when the table is cut back to nine positions, in both modes.
- **The three proof sentences state what the table holds.** They say 23 positions, refusal independent of position, and agreement elsewhere resting on the lexer corpora. "Each position a lexing difference moves a directive" is gone.
- **Acceptance 4 (no reduction).** 280/280 with the SDK and 222/222 absent. 29/29 firmware edits and 4/4 Makefile edits. 1845/1845 spellings. The mutation table, the accepted-edit list and the subset corpus are identical, entry for entry, to the round-four head.
- **My round-four probes, re-run unchanged in both modes.**
  - The closure probe stops on its own `== 2520` assertion, as it must against a 6440-cell table.
  - With only that number lifted, Part A matches, and the 3920 new cells equal my round-four Part B row for row.
  - Every other probe gives results identical to round four.

## Findings

### R272-6-S1 - SUGGESTION - Tests - no corpus spelling or table position holds `/*/`

- **Artifact.**
  - `sw/builder/test_builder.py:2481`: `stop = raw.find("\n" if raw[i + 1] == "/" else "*/", i + 2)`.
  - The two lexer corpora from `:5571`, and `_CLOSURE_POSITIONS` at `:2774-2839`.
- **Evidence.**
  - Mutant m6 starts the `*/` search at `i + 1`, so `/*/` closes the comment it opens. The pinned GCC does not close it there.
  - The mutant trips nothing: not `subset_refusal_corpus`, not the lexer corpora, not a closure cell. The whole gate passes, `GATE 1b PASS`, 280/280 with the SDK and 222 absent (`receipts/r6/power/m6-block-closer-early.json`, `receipts/r6/wholegate/m6-block-closer-early-full-{sdk,absent}.log`).
  - It is a real divergence. On `int a;\n/*/\n#define FOO\n*/\n#ifdef FOO ...` GCC keeps `(a, z)`, the head's readers keep `(a, z)`, and the mutant's readers keep `(a, b, z)`. A second spelling makes the mutant's readers refuse where GCC keeps code (`receipts/r6/slash-star-slash/`).
  - My within-S fuzz finds 113 disagreements on this mutant (`receipts/r6/fuzz-m6-control/`), and none at the head.
- **Impact.** None at this head: the readers are correct. But a regression in the block-comment closer would pass every gate check. The page scopes agreement at other positions to the lexer corpora (`docs/integration/BAREMETAL_FIRMWARE.md:322-349`), so this is a gap in evidence strength, not an overclaim.
- **Optional outcome.** Add a `/*/` spelling to the fixed lexer corpus, recorded on the pinned GCC. Alternatively, add a closure position right after the `*` of a block comment's opener.
- **Verification.** Mutant m6 (`scripts/r6/patches/m6-block-closer-early.json`) stops the gate in both modes.

### R272-6-S2 - SUGGESTION - Docs - one of the fourteen "comment and literal boundaries" is a directive-line boundary

- **Artifact.**
  - `docs/integration/BAREMETAL_FIRMWARE.md:344-347`: "At twelve of them the character decides whether a comment or a literal opens, closes or runs on".
  - `sw/builder/test_builder.py:2763-2773`: "Each but the two at the end of the file is followed by a `#define FOO` that a comment or a literal X opens or continues would hide".
- **Evidence.** At "between a backslash and the line end in a `#define`" (`:2814-2816`), X decides whether a splice continues the `#define BAR` directive line over `#define FOO`. No comment or literal is involved. The other eleven positions are about comments and literals, the `#include <X/*>` position included.
- **Impact.** Wording only. The cell is in the table and measured.
- **Optional outcome.** Name that position as a line-continuation boundary, or say "eleven ... and one where a splice continues a directive line".

### R272-6-S3 - SUGGESTION - Docs - `[R272] F1 on PR #535` names different findings without a head

- **Artifact.** `docs/integration/BAREMETAL_FIRMWARE.md`:
  - `:309` and `:1366` refer to the `$` finding against the round-two head, `8e12d31f`;
  - `:1482` refers to the form-feed finding against the first head, `a13b6e2e`.

  All three spell it `([R272] F1 on PR #535)`.
- **Evidence.** R272-5 S1 is resolved: the ledger paragraphs use one scheme and name their commits (`:1518-1629`). The page also scopes several finding tags to a head (`:305`, `:338`, `:1360`, `:1368`), but these three are not scoped. The internal reviewer has an F1 in five rounds.
- **Optional outcome.** Add the head to each tag, as `:1368` does.

## Prior public findings at this head

I read these only after writing the verdict and ledger (see Verdict).

| Finding | Status at `991d5965` | Evidence |
|---|---|---|
| R272-5 F1 MINOR, Docs (closure table scope) | **Resolved**, option (b) | `_CLOSURE_POSITIONS` holds 23 positions. The 14 new templates are byte-identical to my round-four Part B, and all 3920 new cells equal its rows (`receipts/r4probes/closure/r6-*.log`, `partC-new-cells-vs-partB.json`). The first 2520 recorded letters and first nine positions are unchanged (`receipts/r6/kept-prefix.txt`). Every cell is re-measured by the gate with the SDK and by this review one file per cell, with 0 mismatches. The lone `#` is named and refused, and refused on a whole firmware (`receipts/r6/lone-hash/`). The three sentences now read as scoped: page `:1367`, S comment `test_builder.py:5226-5236`, lexer bound comment `:5557-5569`. "Each position a lexing difference moves a directive" is gone (`grep`, 0 hits) |
| R272-5 S1 SUGGESTION, Docs (two numbering schemes) | **Resolved** | One scheme. Each ledger paragraph names its commits (`:1518-1629`), and the SHAs match the author comments 5805303297, 5810748613, 5812903766 and 5815097615. A distinct residue is R272-6-S3 |
| R273-6 F1 MINOR, Docs and Conformance (invalid UTF-8 given as GCC parity) | **Resolved** | All four sites now say the pinned GCC accepts the byte and that S refuses it by decision, as a cost: page `:306`, cost row `:1367` (remedy: "save the file as UTF-8"), refusal message `test_builder.py:5283-5290`, S comment `:5240-5246`. No stale wording is left anywhere in the repo (`grep`). Re-measured: the pinned GCC gives rc 0 at `-E` and `-S` for a block comment, a line comment, a string literal and a character literal, and warns only under `-Winvalid-utf8`. In code it is an error at `-S` (`receipts/r6/invalid-utf8/gcc.txt`). The mutation entry "a byte that is not UTF-8, in a comment" still refuses on SUBSET_CHARACTER_PIN in both modes (`receipts/r5/disconnect/connected-*.log`) |
| R273-6 S1 SUGGESTION (same as R272-5 F1) | Resolved with it | as above |
| R272-4 F1 MAJOR = R273-5 F1 MAJOR (extended identifier characters inside S) | Remains resolved | `mid.c`, `comb.c`, `sup2.c` and `eacute.c` are refused by the allowlist, naming the character and line. The gate's 12 allowlist-pinned entries and my six whole-firmware misnests are refused on the pin connected. With the allowlist disconnected, the same entries fall through exactly as at round four, in both modes (`receipts/r5/scheck/`, `receipts/r5/disconnect/`) |
| R272-3 F1 MAJOR (`$` in a directive name) | Remains resolved | `dollar_skipped.c` is refused by the `$` rule in both modes (`receipts/r5/scheck/scheck-*.log`) |
| R272-2 F1 BLOCKER (split `%:` digraph) | Remains resolved | Path-only copies of the round-two whole-gate probe (line 20 points at this clone): all four spellings are REFUSED absent, and split_digraph and formfeed are REFUSED with the SDK (`receipts/rerun/reader/`) |
| R273-4 F1 BLOCKER (`__has_include` header name) | Remains resolved | Both `__has_include` entries are in `subset_refusal_corpus`, and 2 mutation entries name it. The gate passes in both modes, so each is refused on its pin (`receipts/r5/labels/head-sdk.json`) |
| R272-1 F1 BLOCKER, F2 MAJOR, F3/F4 MINOR; R273-1 F1 MINOR | Remain resolved | `cases_r1` to `cases_r4` at head: verdict lines identical to round four in both modes. The SDK-mode accepts are the control, the #544 function-like-macro bound and the three debug edits (`receipts/rerun/probes/`) |
| R273-3 F1 (BOM), F2 MINOR (`__CONCAT` bound) | F1 superseded by decision 5815136430 (the mark is refused). F2 is a documented bound (#544, page `:1360`), unchanged | as round four |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5816286265 items 1-3 and its "no change to what the gate accepts or refuses" rule. Mutation labels (280 SDK / 222 absent), accepted list (29) and subset corpus (22) identical to `4a56ef08` (`receipts/r5/labels/`). Decision 5815136430 (BOM and invalid UTF-8 refused). #408/#409 acceptance 1-5 against the gate logs: 280/280 SDK, 222/222 absent (not below 163), 29/29 + 4/4, the absent verdict `TEXT RULES ONLY, AND WEAKER` naming the arm with 1 registered NOT RUN (`receipts/gate1b/sdk.txt`, `absent.txt`). `test_builder.py:2774-2977`, `:5226-5290`, `:5998-6096` | R272-6 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| RTL | CLEAN | `git diff --name-only 759da623..991d5965` lists three files: the page, `docs/testing/CI_WORKFLOWS.md` and `sw/builder/test_builder.py`. No `hdl/`, `tb/` or RTL source list is touched. The round-5 delta changes no SV reader. Gate 1b elaborated 46/46 RTL mutation variants under the pinned Verilator 5.050 in both modes (`receipts/gate1b/sdk.txt`, `absent.txt`; identity in `receipts/verilator-identity.txt`). Hosted `rtl-fast`, `verilator-suites` and `yosys-portability` succeeded at the exact head (`receipts/hosted-checks.txt`) | R272-6 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Robustness | CLEAN | Every byte 0-255 and 24 sequences at all 23 positions (6440 cells), re-measured per cell (`receipts/r4probes/closure/r6-*`). The 4656 Part B cells plus the 11 extra strings and payload variants: 1 disagreement, the fail-closed lone `#`. Within-S differential fuzz, two seeds, 50929 admitted samples, 0 disagreements; the same fuzz finds 113 on mutant m6 (`receipts/r6/fuzz*/`). The lone `#` at end of file (no line end, after a blank line, and with a line end) is refused on the whole firmware (`receipts/r6/lone-hash/`). Refusal messages name the character and line after splices, CRLF, lone CR and multi-line comments (`receipts/r5/scheck/`). `_c_literal_end` `:2416-2424`, `_c_phases` `:2458-2537`, `_C_PHASE12_RE` `:2342` | R272-6 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Tests | CLEAN (R272-6-S1 is a SUGGESTION) | `assert_character_closure()` `:5998-6096`: the named-refusal branch, the sorted-name equality and the negative control. Mutation power without a compiler (`receipts/r6/power/`): m1 (no-break-space splice) and m2 (FS splice) trip only B5; m3 (no escapes) trips only B7, B8 and B13; m4 (digit separator) trips only B10; m7 (names emptied) trips the lone `#`; m5 is also caught by the corpora; m8 is equivalent; m6 is caught by nothing (S1). Whole gate (`receipts/r6/wholegate/`): m1 and m4 stop with the full table and pass with it cut to nine, SDK and absent (280/280 and 222/222 when cut). m3 stops with the full table and is still caught cut, on a mutation entry. Round-four probes re-run unchanged, both modes | R272-6 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Docs | CLEAN (R272-6-S2 and S3 are SUGGESTIONs) | `docs/integration/BAREMETAL_FIRMWARE.md:303-349` (S table, the closure paragraph with its 23 positions and the named exception), `:1360-1368`, `:1394`, `:1518-1629` (renumbered ledger; round five's paragraph checked against my reproduction of its can-fail claims), `:1655-1675` (counts: 280/222, 29/4, 1845, 6440 and 2520, 33+25 skipped = 58 = 280-222). `docs/testing/CI_WORKFLOWS.md:1126-1130`. Site comments `test_builder.py:2732-2773`, `:5226-5246`, `:5557-5569`, and the gate print (`receipts/gate1b/sdk.txt`: "in 23 positions ... 1 by the readers and the directive-set closure"). Static checks all exit 0: `docs_check.py`, `check_baremetal_only.py --check/--selftest`, `check_em_dash.py --base 759da623`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`, `git diff --check`, `test_firmware_compiler.py --selftest` (`receipts/static.txt`) | R272-6 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |

## Executed evidence

All runs are at the exact head, in this clone, with patches applied in memory only.

- **Setup.** The pinned SDK was installed from the pinned archive and verified. The compiler is riscv32-linux-gcc 14.3.0 and the installer digest matches (`receipts/sdk-install.txt`). Verilator 5.050 is the scoped tool, with its wrapper digest recorded (`receipts/verilator-identity.txt`).
- **Gate 1b**, run with `test_firmware_compiler.py` and the pinned Verilator.
  - With the SDK: `GATE 1b PASS; 0 NOT RUN`, 467 compiles. 280/280 mutations, 29/29 + 4/4 edits, 1845/1845 spellings, 46/46 RTL variants.
  - The closure: 6440/6440 cells, split 3647 / 246 / 1 / 2546 (226 closes), re-measured on the compiler.
  - Absent: `GATE 1b PASS; 1 NOT RUN`, 0 compiles. 222/222, the same 6440 split, not re-measured.
  - Logs: `receipts/gate1b/`. An earlier pair of runs picked up the host's Verilator 5.052; it gave the same results and is kept as `*-system-verilator-5.052.txt`.
- **Closure re-measured independently** (`scripts/r6/cases_r6_closure.py`, which imports my unchanged round-four functions and templates). Output is in `receipts/r4probes/closure/`.
  - Part A, 6440 cells: 3647 / 246 / 2547 admitted, 0 recorded/GCC mismatches. 1 admitted disagreement, the named lone `#`.
  - Part B, 4656 cells: the same counts as round four.
  - Part C: all 3920 new cells equal Part B now and at round four.
- **Round-four probes, unchanged, both modes.** Byte copies are under `scripts/r1` and `scripts/r5`.
  - `cases_r5_closure.py`: `AssertionError: 6440` on its own `== 2520` (`receipts/r4probes/closure/unchanged-*.log`).
  - The allowlist disconnect: the 12 gate entries are identical to round four. My six misnests plus the control are identical to round four's `r5only` runs (`receipts/r5/disconnect/`).
  - The S check and message check: identical in both modes.
  - Labels: identical to `4a56ef08`.
  - Include-quote: refused in both arms, both modes.
  - The ASCII audit: the same 85 non-reader calls, only line numbers differ (`receipts/r5/ascii-audit.txt`).
- **Earlier rounds' probes.** `cases_r1` to `cases_r4` at head in both modes, and the split-digraph probe: see the prior-findings table.
- **The round's own can-fail claims, reproduced.**
  - The no-break-space splice stops the gate on "U+00A0 between a backslash and the line end in a line comment" in both modes, and passes with the table cut to nine.
  - An empty `_CLOSURE_READERS_REFUSE` trips the lone `#` cell (m7).
  - I did not reproduce the extra-name and nameless-directive controls; that evidence is the author's.
- **Restore.** The clone matches the head: clean status, index tree equal to the HEAD tree, every tracked blob re-hashed equal, and the gitlinks for gptp-processor, protocol-processor and third_party/verilog-axis at their recorded commits (`receipts/restore-check.txt`).

## Real limits

- Agreement at positions outside the table rests on the two lexer corpora and my fuzz. The fuzz covers single-line and short multi-line fragments, not whole-grammar enumeration. So agreement there is sampled, not proven, as the page states.
- The mutant whole-gate runs (`receipts/r6/wholegate/`) used the host's Verilator 5.052. Those runs measure the lexer and closure outcome, which does not depend on the Verilator version.
- Not run, as instructed: the whole `sw/builder/test_builder.py`, the parent, PP, gPTP, Yosys and builder banks, act, the candidate merge and hardware.
- Physical calibration was NOT RUN. The skipped `Physical gPTP (nightly and manual)` context is not hardware proof.
- The concurrent external review of this head was not read.

## Pending manager duties

- Hosted and act acceptance at the exact head. Every executed context succeeded; `Physical gPTP (nightly and manual)` was skipped (`receipts/hosted-checks.txt`).
- The whole `python3 sw/builder/test_builder.py` with the census live, for acceptance 4's exit-0 clause (the author reports exit 0 in three modes).
- Candidate-merge validation against live dev `573f0052a0e4412e81f0845438fcec2086ce5d55` from source base `759da623`, and post-merge containment.
- Optional: route R272-6-S1 to S3 to a follow-up. They do not affect coverage.

R272-6 FINISHED


---
[A10] 8 non-text or oversized receipt file(s) were retained locally and are not in the public packet.
