[R238] POSITIVE - exact head 26a0cc3042300d5213edf7b1c0037a3ae2612ecd

# R238-5: external cold review of issue #437 / PR #538 (closes #516), correction round 1

- Head `26a0cc3042300d5213edf7b1c0037a3ae2612ecd`, tree `dd03278237b213f237e911ce3c370e6471bc8be8`, one commit on the reviewed head `196cb7d99cb06631df514715979a5f82fbb1f7aa`. Source base `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Reconstructed in this order: AGENTS.md and CONTRIBUTING.md (sections 5 and 6.1); docs/README.md; the #437 body with acceptance 1 as restated and amended; the owner decisions of 2026-09-23 14:15 and 17:45; the manager rulings on PR #538 (N1, N2, acceptance 4) and the correction assignment to the author; then the full diff `759da623..26a0cc30` with the correction commit read line by line.
- My verdict and ledger were drafted before I read any prior review report (`receipts/draft-verdict-before-prior-findings.txt`). I then read R237-5 and R238-4 and reran their published probes at this head. Their findings are resolved below.
- Renderer environment: a private venv installed from `tools/markdown/requirements.txt` with `--require-hashes`, under CPython 3.14.7 (`receipts/venv-freeze.txt`: cmarkgfm 2025.10.22, cffi 2.1.1, pycparser 3.0, html5lib 1.1, six 1.17.0, webencodings 0.6.1).

## Verdict

POSITIVE. The correction closes the MAJOR both reviews filed, and each prior MINOR is resolved.

- **The fix.** The forged-position guard now reads the page's position-free rendering (GitHub's own HTML) for the attribute in any ASCII letter case. A page nested more than 200 deep renders nothing, and the syntax-tree walk no longer recurses.
- **My own forgeries.** I wrote 20 forged spellings that no prior round published: every case pattern, both tag-name cases, unquoted, single-quoted and inline tags, and decimal, upper-hex, lower-hex and mid-word character references. At `196cb7d9`, all 20 and both past-depth pages listed the hidden heading, and the shipped em-dash gate exempted a label copied from it. At this head none of them lists it, and the gate exempts nothing.
- **Mutations.** 28 mutations were run: 25 are killed, including the reverse mutant and the prior external fix-probe. The 3 survivors change no decision, and are recorded as suggestions.
- **Findings.** None open at MINOR or above. Four suggestions are recorded; they do not affect coverage.

## Evidence at this head

All receipts are under `receipts/`, and the scripts that produced them are under `scripts/`.

1. **Gates** (`head-gates.txt`), each rc 0:
   - `gen_toc.py --selftest` 1501/1501, `--check` 106 pages, `--verify-anchors` 147;
   - `check_em_dash.py --selftest` 339, and `--base 759da623`: 0 findings, 0 exempt over 100 added lines;
   - `docs_check.py`, `check_doc_style.py`;
   - `check_py_idiom.py`: long module 10 <= 10, long function 9 <= 9; `check_em_dash.py` is at the 1000-line module limit, not over it;
   - `ci_events.py --check` and `--selftest`, run with the system interpreter because the venv has no pyyaml;
   - `git diff --check 759da623 HEAD`.
2. **Forged spellings and depth through the shipped gate** (`probe_forge_e2e.py`).
   - Method: each base page hides `## Old <em dash> heading` from GitHub. The head page carries a valid generated Contents block copying that label, and both are committed to a real Git repository and judged by `check_em_dash.judge_page`.
   - At this head, 31/31 rows are as expected:
     - 20 forged spellings: no hidden heading listed, label refused, exempt 0. Raw-HTML spellings are also named by `refusals()`. Reference and escape spellings are not named, and the renderer withholds every heading.
     - 3 pages GitHub cuts short (256 block quotes, 129 list levels, 1500 block quotes): exempt 0, and no crash.
     - 4 margin pages (201 to 255 deep, which GitHub shows): withheld with exempt 0, the documented direction.
     - 4 controls (a plain page, 200-deep block quotes, 199 raw `div`s, a character reference in a tag's attribute name, which HTML does not decode): exempt 1, as GitHub shows the heading.
   - At `196cb7d9` (`probe_forge_e2e-at-196cb7d9.txt`), all 20 forged rows and both past-depth rows show exempt 1, and the 1500-deep page raises RecursionError.
3. **The premise of the guard** (`probe_plain_vs_positioned.py`).
   - It renders 5537 pages: the 164 tracked pages, the 373 fixture pages and 5000 seeded fuzz pages.
   - With every `data-sourcepos="…"` deleted, the positioned rendering equals the position-free rendering byte for byte on all 5537.
   - The deepest tracked page nests 8, which matches the documents.
   - My reading of the HTML5 tokenizer agrees. An attribute name decodes no character reference and lowers only ASCII letters. The renderer's own attribute name is always preceded by a space, which ends any name a page leaves open, and followed by `=`. So a page supplies the parsed attribute only by spelling it, in some ASCII case, in the position-free HTML, which is exactly what `spells_position()` tests.
4. **Robustness past the recursion limit** (`probe_deep_robustness-at-26a0cc30.txt`, `gates-on-1200-deep-pages-at-26a0cc30.txt`).
   - Six pages are answered with no heading and no exception: 5000 block quotes, 1000 list levels, 600 ordered levels, 3000 raw `div`s, 3000 nested emphasis and 2000 inline spans.
   - On 1200-deep block-quote and list pages, `gen_toc.py --check` answers rc 0 (page below threshold), and `check_em_dash.py --base` answers rc 1 with its real finding and 0 exempt. No traceback from either.
5. **Refusal naming** (`generator-on-named-page-at-26a0cc30.txt`). A tracked page whose prose spells `Data-SourcePos` is reported NOT READ with its line and column, and `--write` changes no file. Every consumer reads `refusals()` through `refusal_notes()` (`check_em_dash.py:228`, and `gen_toc.py` main), and `refusal_notes()` handles both kinds of entry.
6. **Acceptance 4 at this round** (`tracked-answers-196cb7d9-vs-26a0cc30.txt`). For all 164 tracked pages, `blocks()`, `line_kinds()`, `headings()`, `refusals()` and `plan()` are byte-identical between `196cb7d9` and this head (sha256 `915265d7…` for both).
7. **Mutations** (`mutation-at-26a0cc30.txt`, `mutate.py`). Each mutant is a disposable export with one exact replacement, with both self-tests run.
   - **Killed:**
     - guard: M01 case-sensitive (the reverse mutant), M02 back to the raw-text check, M03 removed, M04 reading the positioned HTML, M05 partly lowered, M28 the prior external fix-probe `POSITION in text.lower()`;
     - refusal: M06 case-sensitive, M07 attribute dropped, M10 note wording;
     - depth and stack: M11 removed, M12 off by one, M13 counted from 0, M14 set to 256, M15 recursive walk restored;
     - M16 heading tag not matched to its level;
     - file view: M17 anchors ignored, M18 anchor reader blanked;
     - M19 strikethrough dropped;
     - own-element kinds: M20 list, M21 thematic break, M25 block quote, M26 code block, M27 table;
     - M22 the `bind()` drift refusal skipped;
     - M23 `unquoted()` skipped.
   - **Survived:** M08, M09 and M24 (S2 and S3).
8. **Hosted, exact head** (read only). These check runs completed with success: docs-check, docs-check-no-git, rtl-fast, verilator-suites (5 shards), yosys-portability (4 shards), full-ci-gate, bdd-conformance, elaborate, verilator-lint, yosys-elaboration, wire-accountability and changes. "Physical gPTP (nightly and manual)" was skipped, which is not hardware evidence. The manager owns hosted and local-replica acceptance.
9. **Clone integrity** (`clone-integrity-after-probes.txt`).
   - HEAD, tree and `write-tree` are all `dd032782…`.
   - Index equals HEAD blobs and modes, and nothing is untracked.
   - Gitlinks are unchanged: `external` efeb541a, `gptp-processor` c1b61743, `protocol-processor` 424c688f, `third_party/verilog-axis` 48ff7a7e.
   - An ignored `scripts/__pycache__` created by the gate runs was removed.

## Findings

None at BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Robustness, Docs - `scripts/gen_toc.py:108-153` (`refusals()`), `scripts/gen_toc_renderer.py:332-336`

- **Evidence:** `probe_unnamed_withheld_write-at-26a0cc30.txt`. The probe appends one line to each of two tracked pages: a text spelling of the attribute through a backslash escape, and one line nested 201 block quotes deep (GitHub renders that page in full). `gen_toc.py --check` then reports `TOC DRIFT ... (headings changed, or a description is still 'TODO ...')` with rc 1 and advises `--write`, and `--write` deletes both Contents blocks (24 and 17 lines).
- **Scope:** this is the author's disclosed residual 1. It only withholds: no exemption is granted, and no tracked page is near it (deepest 8, no spelling).
- **Suggested outcome:** name such pages as `refusals()` now names a spelled attribute, from the render outcome, so they are left alone. Or state the generator consequence beside the limit in CONTRIBUTING 6.1.

### S2 - SUGGESTION - Tests - `scripts/gen_toc.py:143-153`

- **Survivors:** M08 (only the first occurrence on a line is named) and M09 (`str.lower()` in place of the ASCII-only fold the comment at `gen_toc.py:84-88` justifies).
- **Scope:** both change only the diagnostic's completeness or column. Refusal, provenance and exemption are unchanged.
- **Suggested outcome:** an arm with two spellings on one line, and one with a non-ASCII letter whose lowering changes length ahead of the attribute.

### S3 - SUGGESTION - Tests - `scripts/check_em_dash.py:946-952`

- **Survivor:** M24. Dropping the real-Git shape rows takes the em-dash self-test from 339 arms to 57, and it still passes.
- **Scope:** the gate has no arm floor, unlike `gen_toc.MIN_ARMS`, and that is pre-existing structure. Every decision those rows exercise is also held by `gen_toc` arms: all decision mutants above are killed there.
- **Suggested outcome:** a floor, or a family-presence arm, for the em-dash self-test.

### S4 - SUGGESTION - Docs - `scripts/gen_toc_shape_cases.py:41-43`, `docs/DOC_GENERATION.md:81`

- **Evidence:** both texts describe the file-view pages as the withheld cases. Three of the 11 are listed pages: the two open-raw-tag pages (`Real` is listed) and the strikethrough setext page.
- **Suggested outcome:** say "including the withheld cases".

## Prior public review findings at this head

| Finding | Severity, lenses | Status at 26a0cc30 | Evidence |
|---|---|---|---|
| R237-5 F1 = R238-4 F1: case-sensitive position guard lets raw HTML list a hidden heading and win the exemption | MAJOR; Conformance, Robustness, Tests, Docs | **Resolved** | Guard at `gen_toc_renderer.py:293-297,321-325`. R238-4 `emdash_spoof_e2e.sh` rerun: the spoof variant lists nothing, the base refusal is named, 0 exempt (`prior-R238-4-emdash_spoof_e2e-at-26a0cc30.txt`). R238-4 `set2-pages.json`: no hidden heading (`prior-R238-4-set2-set5-at-26a0cc30.txt`). R237-5 `probe_emdash_gate.py`: both forged pages list nothing, 0 exempt, lowercase control still withheld (`prior-R237-5-probe_emdash_gate-at-26a0cc30.txt`). Reverse mutant M01 and the fix-probe M28 are killed. Labels and anchors are now compared with recorded file-view renderings (M17 and M18 killed). The three documents match the behaviour (Docs row of the ledger) |
| R237-5 F2: recursive `_nodes()` crashes on 1200-deep pages with the findings exit code | MINOR; Robustness, Tests | **Resolved** | Stack walk at `gen_toc_renderer.py:258-290`. Both gate CLIs answer 1200-deep block-quote and list pages with no traceback. M15 (recursion restored) is killed |
| R237-5 F3: `_OWN_ELEMENT` members unarmed | MINOR; Tests, Conformance | **Resolved** | Arms at `gen_toc_renderer_cases.py:137-150`. M20, M21, M25, M26 and M27 are killed; `heading` was already armed |
| R238-4 F2: M17 heading-tag check, M15 `bind()` drift, M11 strikethrough unarmed | MINOR; Tests, Conformance | **Resolved** | M16 (tag check), M22 (`bind()` skip) and M19 (strikethrough) are killed at the arms named for them. `set5-pages.json` lists `Real` only and `a b` |
| R237-5 S1 (DOC_GENERATION pointer to the file-view divergence) | SUGGESTION | Adopted | `DOC_GENERATION.md:70-71` |
| R237-5 S2 = R238-4 S1 (a prose mention deletes a page's Contents) | SUGGESTION | Adopted for spelled forms | Named and left alone (evidence 5). The unnamed forms remain: this round's S1 |
| R238-4 S3 (spell the extension list) | SUGGESTION | Adopted | `_EXTENSIONS_SPELLED` arm |
| R237-5 S3 = R238-4 S4 (drifted html5lib reported as "not installed") | SUGGESTION | Not adopted; optional | Unchanged |
| R237-5 S4 (template, noscript, object, option, frameset shapes unrecorded) | SUGGESTION | Not adopted; optional | Unchanged |
| R238-4 S2 (pre-existing anchor rule for a heading with a link inside a code span) | SUGGESTION, outside #437 | Not adopted; optional | For the manager to route to its own issue |

## Stated residual limits, judged

1. **Unnamed withheld pages drift, and `--write` drops their Contents.** This only withholds. Accepted, with S1 as an optional improvement.
2. **A comment closing inside a swallowed container labels a later line commented.** This affects labels only. A COMMENT label makes a line judged whole, never exempt, so it only withholds. It is pre-existing. Accepted, and a new issue is appropriate.
3. **The depth bound rests on GitHub's measured limit.** The fixture records the 201-deep page kept and the 256-deep and 1101-deep pages cut (`gen_toc_shapes.json` file view, 2026-09-24), and a bound of 200 leaves 55 levels of margin. Every depth effect of GitHub's own wrappers that I could name adds depth there, not here, which widens the margin. Accepted.
4. **N2 (file view against gfm mode) and N1 (hidden footnote heading).** Both are manager-ruled, documented limitations. They are unchanged by this commit.

## Reviewer-owned completion ledger (round R238-5)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gen_toc_renderer.py:293-337` and `gen_toc.py:108-164,217-262` against #437 AC1-AC5, #516 and CONTRIBUTING 6.1 "none can grant an exemption"; `probe_forge_e2e` 31/31 (24 fail at 196cb7d9); selftest 362 shapes and 11 file-view pages; tracked answers identical; manager rulings N1, N2 and AC4 | R238-5 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| RTL (architecture and module contracts; no HDL path in the diff) | CLEAN | `gen_toc_renderer.py:258-290` (stack walk and document order), `:321-329` (second rendering, both buffers freed), `:357-377` (depth); `refusals()` tuple contract and its consumers (`check_em_dash.py:228`); `probe_plain_vs_positioned` 5537/5537; `git diff --stat 759da623..HEAD` over `hdl tb syn sw` and the submodules is empty | R238-5 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Robustness | CLEAN | `probe_deep_robustness` 6/6; 1200-deep pages through both gate CLIs; 20 forged spellings, margin and control rows; named-page generator behaviour; S1 reproduced (withhold-only) | R238-5 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Tests | CLEAN | `gen_toc_renderer_cases.py`, `gen_toc_shape_cases.py`, `gen_toc_cases.py:783-806`, `gen_toc_shapes.json` file view; 28 mutants, 25 killed at named arms, 3 decision-neutral survivors (S2, S3); both self-tests pass | R238-5 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Docs | CLEAN | CONTRIBUTING.md:595-619 (the four limits), `docs/DOC_GENERATION.md:59-82`, `gen_toc_renderer.py:40-60,81-87,293-305,340-354`, `gen_toc.py:108-140`, each checked against probe behaviour; `check_doc_style.py` and `docs_check.py` pass; S4 wording only | R238-5 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |

## Real limits of this round

- **No new GitHub renderings.** I sent no page to GitHub. The file-view and gfm renderings are the committed receipts: hashes and request bytes are checked by the self-test, not re-fetched. My forged pages are judged by construction (an open raw comment, an open quoted value, depth) and by the prior-head contrast, not by a fresh rendering.
- **Interpreter.** Only CPython 3.14.7 was run. The hosted runner's CPython 3.12 is covered only by the exact-head hosted docs-check success.
- **Fuzz scope.** The positions-only claim is measured on 5000 fuzz pages from one seed, the tracked pages and the fixture. The tokenizer argument, not the fuzz, carries the general case.
- **Banks not run.** No full parent, PP, gPTP, Yosys or builder banks, no act or Docker, no hardware. The scoped Verilator was not needed, since no HDL changed. Physical calibration was NOT RUN, and skipped field or hosted contexts are not hardware proof.
- **Candidate not built.** Source validation here is at the PR head against its source base. The current-dev candidate (live dev `615b5a5d`) was not built.

## Pending manager duties

- The candidate merge result against live dev `615b5a5d7de01b23f15502e3732c6f2cb81ce74b` and its validation; post-merge containment.
- Hosted and trusted local-replica acceptance at the exact head.
- The second independent positive review and the completion ledger under AGENTS.md section 7.
- Optional follow-ups: S1 to S4; a new issue for residual 2; routing R238-4 S2 (the anchor rule for a code-span link) to its own issue.
- Publication of this report and of the files listed in `MANIFEST.sha256`.

R238-5 FINISHED
