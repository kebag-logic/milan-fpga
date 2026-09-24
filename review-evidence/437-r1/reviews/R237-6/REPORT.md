[R237] POSITIVE - exact head 26a0cc3042300d5213edf7b1c0037a3ae2612ecd

Round R237-6, internal independent review of issue #437 / PR #538 (it also closes #516). This was a cleared-context session working from public state only. The head is `26a0cc3042300d5213edf7b1c0037a3ae2612ecd` with tree `dd03278237b213f237e911ce3c370e6471bc8be8`. It is correction round 1, one commit on `196cb7d9`. The merge base is `759da623072358afdb0e9d570a7b4b6a788492c9`. All five lenses were applied. No BLOCKER, MAJOR or MINOR is open at this head. Three SUGGESTIONs follow; they do not affect coverage.

## Reconstruction

Sources, read in this order:

- AGENTS.md and CONTRIBUTING.md 6.1 (lines 557-627).
- The #437 body: acceptance 1 as restated and amended on 2026-09-23, and acceptance 2 to 5.
- The owner decisions of 14:15 and 17:45 on 2026-09-23.
- The manager's rulings on N1, N2 and AC4 (PR opening comment on #437).
- The A228 correction assignment and A228 REVIEW READY.
- `git diff 759da623..26a0cc30` and `git diff 196cb7d9..26a0cc30`.
- The public evidence tree `5750da43:review-evidence/437-r1/correction-a228` (recorded renderings and depth probes).
- The hosted check runs at the exact head.

I read the prior review findings (R237-5, R238-4) only after my own pass. My draft verdict and ledger were fixed first, with a timestamp, in `receipts/independent-draft-verdict.txt`. That draft counts 4 surviving mutants of 32; two prior-equivalent mutants were added later, both killed. I did not read the R238-5 report posted on the PR during this round.

The correction does three things:

- **Forged positions.** `render()` also renders each page without positions, which is the HTML GitHub draws. If that HTML spells the position attribute in any ASCII letter case, the page is read as rendering nothing (`scripts/gen_toc_renderer.py:293-297`, `:319-333`).
- **Depth.** A parse that nests an element more than `DEEPEST = 200` deep also renders nothing (`:81-87`, `:334-336`). The syntax-tree walk is now a stack (`:258-290`).
- **Refusals.** `refusals()` also names any line whose text spells the attribute, in any ASCII case (`scripts/gen_toc.py:108-164`).

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Robustness, Docs - `scripts/gen_toc.py:143-152`, `:637-651`; `scripts/gen_toc_renderer.py:324-336` - pages withheld but not named still lead `--write` to delete their hand-written Contents block

- **Evidence** (`receipts/check-write-unrefused.txt`, `scripts/check_write_unrefused.py`):
  - Some pages render nothing but are not named by `refusals()`: the attribute spelled through a backslash escape or a character reference, or block quotes nested 201 deep.
  - `--check` answers `TOC DRIFT ... Run: python3 scripts/gen_toc.py --write <page>`, and `--write` then deletes the block and all three hand-written descriptions.
  - A literal spelling, even inside inline code, is named `NOT READ` and left intact. A page at depth 199+1 is read.
- **Scope.** This is the residue of R237-5 S2 and R238-4 S1 for the spellings the text does not carry. The author discloses it as open risk 1. It only withholds, so no exemption follows from it. No tracked page spells the attribute, and none nests deeper than 8.
- **Optional outcome.** Either name such a page (for example, `render()` reports why it read nothing and `main()` treats that as a refusal), or say in 6.1 that `--write` removes the block on such a page.

### S2 - SUGGESTION - Tests - `receipts/mutations-r237-6-at-26a0cc30.txt` - four surviving mutants, none of which changes an anchor or an exemption

1. **Heading tag.** `gen_toc.py:254` matched to any heading tag, not to the node's level. GitHub's file view shows `<h3 foo`, a blank line and `## Real` as an h3 `Real` with anchor `real` (`receipts/render-probe-level.json`). The head withholds it. The mutant lists it as level 2 with the same anchor, so only the level differs.
2. **Repeated spellings.** `refusals()` names only the first spelling on a line. The page is still refused; only the note count changes, against the docstring's "every place".
3. **Letter folding.** `refusals()` folds with `str.lower()`. Only the reported column changes, after a character such as U+0130; the reason is stated in the comment at `gen_toc.py:84-88`.
4. **Forged page nodes.** A forged page keeps its nodes but no elements. Only the line labels of a page that lists nothing change (COMMENT against TEXT). `check_em_dash.py` uses those labels only in the wording of a finding.

Arms for (1) and (2) would pin the stated properties.

### S3 - SUGGESTION - Robustness - `scripts/gen_toc_renderer.py:334-336` - the depth bound applies only after a full HTML5 parse

A 20,000-deep block quote takes about 61 s and 20,000 raw `<div>` tags about 55 s, then list nothing (`receipts/deep-pages-robustness-at-26a0cc30.txt`). The answer is correct and withholding, and there is no crash, which was the R237-5 F2 failure. Only CI time is exposed. An optional cheap pre-check (container depth in the syntax tree, or raw tag count) would bound it.

## Focus verification

### Forged position, every spelling

`scripts/forge_e2e.py` writes one page per spelling. Each page has three visible sections and a raw element carrying the position of a `## Secret <em dash> x`. GitHub hides that heading behind a `> <!--` (#516). The Contents block is written by the pre-correction generator, so the forged label is present. The only change between the base and head commits is that entry's description. The shipped `check_em_dash.py --base` runs on real commits in a disposable repository holding each tree (`receipts/forge-e2e-196cb7d9-vs-26a0cc30.{txt,json}`).

| spelling | at 196cb7d9 | at 26a0cc30 |
|---|---|---|
| lower-case raw (control of the old guard) | withheld, rc 1, exempt 0 | refused by name, rc 1, exempt 0 |
| upper raw, mixed raw, mixed unquoted raw | hidden heading listed, **rc 0, exempt 1** | refused by name, rc 1, exempt 0 |
| decimal, hex, upper-case and hyphen character references; fully encoded name | hidden heading listed, **rc 0, exempt 1** | withheld (renders nothing), rc 1, exempt 0 |
| backslash escape, lower and upper | hidden heading listed, **rc 0, exempt 1** | withheld, rc 1, exempt 0 |
| benign near-miss attribute | not listed, exempt 0 | not listed, exempt 0 |

The probe bites at `196cb7d9` for all 10 forgeries, and every one is closed at the head.

Both prior reviewers' forged pages are closed at the head too:

- R238-4 `emdash_spoof_e2e.sh`: the spoof is refused like the control, rc 1, 0 exempt, and named `DATA-SOURCEPOS` at column 5 (`receipts/prior-R238-4-emdash-spoof-e2e-at-26a0cc30.txt`).
- R238-4 `set2` and `set4` pages: no hidden heading is listed (`receipts/prior-R238-4-set2-set4-pages-at-26a0cc30.txt`).
- R237-5 `probe_emdash_gate.py`: nothing listed, 0 exempt (`receipts/prior-R237-5-probe-emdash-gate-at-26a0cc30.txt`).

On soundness: the only bytes the positioned HTML adds over the position-free HTML are the renderer's own ` data-sourcepos=L:C-L:C` insertions (unquoted by `unquoted()`). An HTML tokenizer reads attribute names from literal bytes, lowering ASCII letters only, and never decodes references in a name. So a page that can make the parse see the attribute must spell it in the position-free HTML, which `spells_position()` checks.

In the other case, the renderer's own position lands on a raw tag the page left open. There the element keeps the heading's text, and GitHub shows it. The file-view recordings "an open raw tag reads a heading's position as an attribute / unquoted value" show only `real`. The level check withholds a mismatched tag (S2 item 1).

### Reverse mutant and armed properties

My own mutation set (`scripts/mutate_r237_6.py`, `receipts/mutations-r237-6-at-26a0cc30.{txt,json}`) killed 31 of 35 mutants, each at a named arm. Among the killed:

- **Reverse mutant.** The position-free check made case-sensitive is killed at `I437 a page whose raw element carries the position attribute spelled in upper case lists nothing`.
- **Removed or weakened guards.** Killed: the old raw-text guard restored, the check removed, and the check reading raw text.
- **Refusals.** `refusals()` made case-sensitive or naming nothing is killed.
- **Depth.** Killed: bound removed, off by one, raised to 255, counted from 0, the walk made recursive again, and sibling order lost.
- **Own elements.** Each of the six own-element kinds dropped is killed.
- **Heading tag and binding.** Killed: the heading-tag check removed, `bind()` ignoring the release it is handed, and `cmarkgfm` unchecked.
- **Extensions.** Strikethrough, autolink and tasklist dropped are killed.
- **Quoting.** Positions left quoted are killed.
- **File view.** The file-view check ignoring anchors or allowing any heading is killed, and so is the permalink left unread.
- **Both guards case-sensitive.** This also fails the real-Git em-dash rows (em-dash self-test rc 2), so those rows hold the property through the shipped consumer, not only through the TOC arms.

The four survivors are S2.

The prior reviewers' mutation scripts were re-run at the head:

- R238-4 `mutate.py`: all 19 applicable mutants are killed, including M11, M15 and M17 (`receipts/prior-R238-4-mutations-at-26a0cc30.txt`).
- R237-5 `mutate.py`: all 13 applicable mutants are killed (`receipts/prior-R237-5-mutations-at-26a0cc30.txt`).
- R237-5 `mutate_own_element.py`: 6/6 killed (`receipts/prior-R237-5-own-element-at-26a0cc30.txt`).

Five prior mutants no longer apply, because their target lines were rewritten, and each maps to a killed equivalent:

- R238-4 M04 and R237-5 M03 map to "tight-list paragraphs given an element".
- R238-4 M06 and R237-5 M02 map to "plain-HTML check removed".
- R238-4 M22 and R237-5 M16 were candidate-fix probes.

### Depth

The GitHub recordings in the public evidence (`correction-a228/probes/rendered-depth*.json`, gfm mode, 2026-09-24) agree with the stated limit:

- 254 block quotes keep `## B`; 255 lose it.
- 127 list levels keep it; 128 lose it.
- 254 unclosed `<div>` keep it; at 255 the heading is kept but empty; at 256 it is gone.
- 199 and 200 block quotes keep it.

The fixture's `markdown`-mode file-view pages at 201, 256 and 1101 deep are hash-verified. The walk withholds from depth 201, a margin of 55 below GitHub's cut. The tracked maximum is 8 (`receipts/tracked-pages-196cb7d9-vs-26a0cc30.json`).

### Limitation text

- **CONTRIBUTING.md:595-616** has four withholding limits. The position-attribute bullet (`:600-608`) matches `spells_position` together with `refusals()`, and the depth bullet (`:609-612`) matches `DEEPEST` and the recordings.
- **DOC_GENERATION.md:62-81** states the same, and points to 6.1 for the file-view difference (`:70-71`).
- **The docstrings** at `gen_toc_renderer.py:40-60` and `gen_toc.py:132-141` also state that an escaped or referenced spelling is withheld and not named.

Every statement was checked against the behaviour above. The only thing the text omits is the `--write` consequence in S1.

### Raw wrappers absent from the shape set

These were rendered on GitHub for this round with stateless `POST /markdown` requests; exact request and response bytes are in `receipts/render-probe-wrapper-tags.json`. `<noscript>`, `<template>`, `<svg>` and `<math>` around a heading were sent in `markdown` mode, and `noscript` and `template` also in `gfm`. GitHub shows `Mid`, and so does the walk, with the same anchors in the file view. There is no escape here (compare R237-5 S4).

## Acceptance (#437; #516 closes with it)

1. **Met.** The self-test holds 362/362 shapes, and 11 file-view pages carry hash-verified receipts. Every heading `headings()` lists on a file-view page is one GitHub shows, with the same label and anchor. The #516 family is hidden by the renderer, per the 17:45 decision and the manager's N1 and N2 rulings.
2. **Met, unchanged by this commit.** The family-two headings are listed.
3. **Met for every property the reviews named.** See the mutation results above. S2 lists optional refinements.
4. **Met.** All 164 tracked pages give identical `blocks`, `line_kinds`, `headings`, `plan`, `refusals` and `generated_block` under the `196cb7d9` and `26a0cc30` code. No page is refused. `--check` passes at the head.
5. **Met.** In my venv, installed from the lock with `--require-hashes`:
   - `gen_toc.py --selftest` 1501/1501 (floor raised 1433 to 1501), `--verify-anchors` 147, `--check` 106 pages.
   - `check_em_dash.py --selftest` 339, and `--base 759da623` 0 findings, 0 exempt.
   - `check_py_idiom` long module 10 ≤ 10 and long function 9 ≤ 9, with no ratchet or budget file changed.
   - `docs_check`, `check_doc_style` and `check_doc_paths` pass, and `ci_events.py --check` passes (run under the system interpreter, which has pyyaml; the venv run's rc 2 was the missing pyyaml).
   - `git diff --check` is clean.
   - Without the renderer, all three entry points answer rc 2 by name (`receipts/no-renderer.txt`).

## Prior findings at this head

| finding | disposition at 26a0cc30 |
|---|---|
| R237-5 F1 MAJOR (= R238-4 F1) | **Resolved.** See the forged-position table, both reviewers' probes, the killed reverse mutant, and the matching text |
| R237-5 F2 MINOR | **Resolved.** The walk uses a stack; the 1100-deep arm and 1200/20000-deep pages answer; the recursive mutant is killed. It is also bounded by depth |
| R237-5 F3 MINOR | **Resolved.** There is one arm per own-element kind (`gen_toc_renderer_cases.py:137-150`), and 6/6 mutants are killed by both the prior script and mine |
| R238-4 F2 MINOR | **Resolved.** M11, M15 and M17 are killed. The drift arm passes through `bind()` itself (`gen_toc_renderer_cases.py:271-277`) |
| R237-5 S1 | Adopted (DOC_GENERATION.md:70-71) |
| R237-5 S2 / R238-4 S1 | Adopted for spellings the text carries (`gen_toc_cases.py:792-805`). The residue is retained as S1 above |
| R237-5 S3 / R238-4 S4 | Not adopted. They stay optional; not re-measured |
| R237-5 S4 | Partly answered by this round's GitHub renderings (template, noscript, svg, math agree). Object, option and frameset are still unrecorded; optional |
| R238-4 S2 | Pre-existing anchor divergence at REGISTER_MAP.md, outside #437. It stays with the manager for a new issue |
| R238-4 S3 | Adopted (`gen_toc_renderer_cases.py:238-240`, `:278-279`). M10 and M12 are killed |

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #437 AC1-5 as amended; the 14:15 and 17:45 decisions; the manager's N1, N2 and AC4 rulings; `gen_toc_renderer.py:293-337`; `gen_toc.py:108-164`, `:254`; the fixture's `file_view` receipts (11, hashes verified); `receipts/forge-e2e-*`, `render-probe-*.json`, `tracked-pages-*.json` | R237-6 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| RTL | CLEAN | `receipts/rtl-scope.txt`: no HDL, C or RTL file in `759da623..26a0cc30`. Tooling contracts: `Rendered` and `Node` (`gen_toc_renderer.py:129-161`); the consumer imports at `check_em_dash.py:81-82`; stack order and depth indexing (`:258-290`, `:357-377`, mutants killed); both renderer buffers freed (`:326-329`). Hosted `verilator-suites`, `yosys-portability` and `rtl-fast` succeeded at the exact head (`receipts/hosted-check-runs-at-26a0cc30.txt`) | R237-6 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Robustness | CLEAN | 10 forged spellings end to end; depth 199/201/1100/20000 and 3000 list levels; 5000 inline `<b>`; renderer absent (rc 2); drift through the `bind()` arms; unrefused pages under `--check`/`--write` (S1); wrapper tags on GitHub; `receipts/deep-pages-robustness-*`, `check-write-unrefused.txt`, `no-renderer.txt` | R237-6 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Tests | CLEAN | `gen_toc_renderer_cases.py:14-58`, `:137-150`, `:190-214`, `:271-279`; `gen_toc_cases.py:783-805`; `gen_toc_shape_cases.py:103-215`; 35 own mutants (31 killed, survivors judged in S2); prior R238-4 and R237-5 campaigns re-run (all applicable killed; non-applicable mapped); `MIN_ARMS` 1501 | R237-6 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |
| Docs | CLEAN | `CONTRIBUTING.md:586-627`; `docs/DOC_GENERATION.md:59-81`; the docstrings at `gen_toc_renderer.py:4-60`, `:78-87` and `gen_toc.py:108-142`; each statement checked against the probes and recordings; "no tracked page deeper than 8" measured; the only omission is optional (S1) | R237-6 | 26a0cc3042300d5213edf7b1c0037a3ae2612ecd |

## Stated residual limits

- **Unnamed withheld pages, and `--write`.** Acceptable and withholding. Retained as S1.
- **A partial swallow inside containers labels later lines commented.** This predates the PR, affects labels only and withholds. A new issue is appropriate, as the author proposes. Not re-measured here.
- **The depth bound rests on GitHub's limit as measured on 2026-09-24.** The margin is 55, the behaviour is pinned by file-view recordings, and no tracked page is near it. Acceptable. If GitHub's parser changes, the 256-deep file-view arm will not notice, because recordings are static; that is inherent to recorded evidence.
- **The file-view (`markdown` mode) escape on 2 of 1,052 pages** (`<?` carrying `<!--`). It is documented and ruled on by the manager, and unchanged here.
- **Hosted, act and candidate runs are not the author's.** Hosted runs at the exact head are listed below as manager-owned.

## Real limits of this round

- **Not run, as instructed:** full parent, PP, gPTP, Yosys or builder banks; act; host `act_ci` or its selftest; the candidate merge with live dev `615b5a5d`; hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted runs:** at the exact head every executed context succeeded, and `Physical gPTP (nightly and manual)` was skipped by design. `docs-check` ran "Install the pinned Markdown renderer", the em-dash gate and the contents gate on `head_sha=26a0cc30` (`receipts/hosted-docs-check-steps-at-26a0cc30.txt`).
- **Manager bank receipt:** I did not find one keyed to `26a0cc30` in the linked evidence tree. Its `manager/` receipts name head `65df1df5`. I relied on my own focused gates and the exact-head hosted runs instead.
- **GitHub renderings:** 7 stateless `POST /markdown` requests were sent (6 wrapper-tag pages, 1 level page), and their bytes are kept. No other GitHub operation wrote anything.
- **Scoped Verilator:** not used, since the diff contains no HDL.
- **Interpreter:** CPython 3.14 in a private venv from the lock. CPython 3.12 was not re-run by this reviewer.
- **Clone integrity** after all probes (`receipts/clone-integrity.txt`):
  - HEAD, tree and index are equal to the reviewed head.
  - No porcelain change and no untracked file.
  - 880 index entries match the tree in modes, blobs and paths, and every tracked blob hashes identical with no filters.
  - The four gitlinks are unchanged (`external efeb541a`, `gptp-processor c1b61743`, `protocol-processor 424c688f`, `third_party/verilog-axis 48ff7a7e`).

## Pending manager duties

- Publish a manager bank receipt keyed to `26a0cc30`, or confirm which receipt covers it.
- Build and validate the candidate against live dev `615b5a5d` at the merge turn (the paths are disjoint per the author).
- Act and hosted acceptance.
- File the new issues the author proposes (partial swallow in containers) and the R238-4 S2 anchor issue.
- Decide on S1 to S3 as optional follow-up.
- Merge only with explicit maintainer authorization, after two independent positive reviews and the full completion bar.

R237-6 FINISHED
