[R226] POSITIVE - exact head 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba

Round R226-1 is an external cold review (Opus) of kebag-logic/milan-fpga PR #507 for issue #440.

- Head: `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`, tree `c0e67508d3b753c21a28a243d365c4c37ed86d43`. Both match GitHub.
- Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. At 2026-09-22T09:17+02:00 this was also the live `dev` tip, and the PR was open and ready at this head (receipt 04).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

**Verdict basis.** There is no BLOCKER or MAJOR.

- The head implements the settled rules of decision 5771170243 exactly. It agrees with GitHub's renderer on an independent population.
- The global refusal, provenance, container and reader code is unchanged.
- One MINOR (R226-F1) is open under Tests and Docs. Neither lens is covered clean at this head.
- Five SUGGESTIONs are optional.

This is a code-review verdict only. Pending execution gates are listed separately below.

**Authority read:**

- AGENTS.md, and CONTRIBUTING.md sections 2, 3 and 6.1.
- docs/README.md, and REQUIREMENTS.md section 8 (REQ-VER-04).
- Issue #440: the body, scope comment 5651705425, decision 5771170243, assignment 5771559992, and A158's TAKEN and handoff comments.
- PR #507: the body and all six comments.
- CommonMark 0.31.2 sections 4.5 and 4.6, fetched live (receipt 11).
- The public R85-8 and R86-9 reports on PR #428.
- The PR diff, and the `ada8bf7b` evidence archive.

## Findings

```text
[R226] MINOR Tests, Docs - scripts/gen_toc_closer_cases.py:43-68, scripts/gen_toc.py:481, docs/DOC_GENERATION.md:55 - R226-F1: the literal type-1 closer set is held against narrowing, not against widening at the closer site
Requirement/evidence: decision 5771170243 says exactly the four literal names end a type-1
  block. AGENTS.md section 6 (Tests) requires positive, negative and boundary behavior to be
  covered. DOC_GENERATION.md:55 says "`I440` controls cover each closing property and shipped
  label decisions".
  The I440 arms test every name positively. The negative closer-name rows are the Unicode
  lookalikes (`_FOLDS`), `</prelude>` and `</ pre>`; none is a closing tag of another ASCII
  name. gen_toc_closer_cases.py:20 states the aim as "a narrowed population fails".
  Adding `div`, `title` or `xmp` to the joined names at gen_toc.py:481 (mutants R15, R16, X04)
  passes `gen_toc.py --selftest` 683/683 and `check_em_dash.py --selftest` 51/51.
  With the R15 or R16 mutant, the shipped CLIs on a real repository exempt the label copied
  from a base heading placed after `<pre>` + `</div>` (or `</title>`). GitHub renders no such
  heading in markdown or gfm mode (e2e E14/E15; mutR15/mutR16 logs). All 24 sweep rows
  `R226-T-othername-*` render 0 headings.
  Widening the shared RAW_HTML_TAGS constant is already caught by the existing arm "the
  type-1 names are the renderer's four" (mutant X01). Only an edit at the closer site itself
  goes unnoticed.
Impact: current behavior is correct. But a future edit at the closer site could reopen the
  escape #440 exists to close, with every control green. That escape is a Contents label, and
  an em-dash waiver, for a heading the page does not render.
Required change: some control must fail when the closer site accepts a closing tag whose name
  is outside the four. A raw-walk arm is the minimum; one shipped-label row is preferred. An
  equivalent structural proof that the site reads only RAW_HTML_TAGS would also do.
  DOC_GENERATION.md:55 must then be true as written, or be narrowed to what the controls hold.
Verification: rerun probes/r226_mutants.py and probes/r226_mutants_extra.py. R15, R16 and X04
  must each fail at least one arm. Rerunning probes/r226_e2e.py with those mutants must not
  exempt E14/E15 unless a self-test has already failed.
```

```text
[R226] SUGGESTION Tests - scripts/gen_toc.py:497 - no control holds "a longer closing run closes the fence"
Requirement/evidence: mutant R08 changes `>=` to `==` and passes 683/683 and 51/51. Behavior
  at head is correct: rows R226-F-*-longer-* and R226-F-*-much-longer agree with the renderer.
  The rule predates #440 and lies outside the settled scope. A regression here would withhold
  a heading, not let one escape.
Impact: optional; a candidate for a follow-up control.
```

```text
[R226] SUGGESTION Tests, Docs - scripts/gen_toc.py:895, docs/DOC_GENERATION.md:48 - the generator reader's CR normalization is stated but not pinned
Requirement/evidence: DOC_GENERATION.md:48 says both shipped readers normalize CR and CRLF.
  The gate's reader is held: mutant R24 fails I440-E-fence-crlf, I440-E-fence-cr and
  I440-E-inner-cr. The generator's reader is not: mutant R25 (`read_bytes().decode()` at :895)
  passes both self-tests.
  A regression would fail closed: a CRLF page would be refused and named "NOT READ", not
  exempted.
Impact: optional; one control would pin a documented property.
```

```text
[R226] SUGGESTION Docs - docs/DOC_GENERATION.md:44, :46; scripts/gen_toc.py:315-318 - counts from one population, in an archive the page does not link
Requirement/evidence: "205-fixture" and "withhold five headings" count the author's
  reconstructed sweep. That sweep lives in an unmerged evidence archive that the page does not
  link, and docs/README.md asks authors to avoid copied test counts.
  The independent 283-row R226 population gives 9 raw CR withholds. All 9 are refused, and all
  agree after reader normalization.
  Outside the closer rows, a lone CR before an opener lets the raw helper list a heading the
  renderer hides (`foo` CR `<pre>` LF `## Probe`: raw 1, renderer 0; the page is refused, and
  the normalized text agrees; receipt 12).
  A population-independent statement of the boundary would be: CR stays inside an LF-split
  line; the closing-condition rows withhold; such a page is refused; both readers normalize.
Impact: optional clarity.
```

```text
[R226] SUGGESTION Docs - scripts/gen_toc_guards.py:53-65 - the guard docstring still describes REFUSAL as an accepted site kind
Requirement/evidence: the docstring still calls REFUSAL one of "two" honest kinds and adds
  that #440 removes the last such sites. But gen_toc_cases.py:827 now fails any refusal-kind
  site, as mutant R04 shows. Saying at the guard that a new refusal-kind site fails the
  self-test would state the tightened policy where a contributor meets it.
Impact: optional.
```

```text
[R226] SUGGESTION Tests - scripts/check_em_dash.py:945-950 - the em-dash self-test has no arm-count floor
Requirement/evidence: the 17 I440-E rows are counted into the total with no floor. Removing
  a row still prints PASS with a smaller count. gen_toc.py holds its own families with
  MIN_ARMS for this reason (PR #428 round 6); the check_em_dash design predates this PR.
Impact: optional.
```

## Clean lenses

```text
[R226] PASS Conformance - scripts/gen_toc.py:473-481, :495, :497-498, :521 at 0d43ff25; sweep/comparison.tsv; e2e/head-e2e.json with e2e/e2e-oracle.json; receipts/11-commonmark-clauses.txt - both closing rules match decision 5771170243 and the CommonMark 0.31.2 text in 4.5 and 4.6, and GitHub agrees on an independent population
  The fence trailer strips only CLASSES["blank"] (space and tab).
  `_type_1_end` finds `</(pre|script|style|textarea)>` anywhere in a line under
  IGNORECASE|ASCII, on the opening line and on later lines.
  283 independent fixtures went to GitHub's renderer. The rendered h2 count is the same in gfm
  and markdown modes on all 283. With the real reader, the head agrees on 283/283.
  The shipped answer is 211 agree and 72 globally refused, with 0 escapes and 0 withholds. At
  the base, the same population gives 15 escapes and 41 withholds.
  Every opener x closer pair agrees in lowercase and alternating case on later lines, and in
  alternating case on the opening line. The in-tree I440 arms also hold lowercase and upper
  case at both positions.
  In 18 real-Git pages run through both shipped CLIs, each copied label is exempt exactly when
  GitHub renders the base heading.
```

```text
[R226] PASS RTL - receipts/03-pr507.diff (git diff b17580b9..0d43ff25) - no RTL artifact is in scope
  The diff touches only docs/DOC_GENERATION.md and five Python files under scripts/. It
  changes nothing under hdl/, tb/, syn/ or sw/, and no workflow, version, budget or gitlink.
  So no clock, reset, CDC, FSM, width or interface contract is affected.
  Manager-attributed native evidence at this head (archive ada8bf7b, manager/) is not
  reproduced here: 43 builder/static commands and 5 full-native commands exit 0. The
  full-native set is 55 parent suites, Yosys, both processor suites and behave.
```

```text
[R226] PASS Robustness - sweep/comparison.tsv families fence-eof, type1-eof, fence-length, fence-indent, fence-kind, type1-malformed, type1-reset, type1-precedence, type1-embedded, cr; receipts/14-ast-changed-units.txt; receipts/10-gate-gen_toc-check.txt - boundary and malformed inputs all agree with the renderer after the real reader
  EOF cases: a truncated closer at EOF; fence and type-1 blocks left open to EOF; EOF without
  a final LF.
  Fence closers: 40-character runs; shorter, longer, other-character and indented closers.
  Characters that are neither blank nor refused: as fence trailers, NUL, U+200B, U+FEFF,
  U+180E and U+2060; inside the closing tag, NUL and U+200B.
  Malformed closers: attributes, self-closing, split across lines, prefix and suffix names.
  State: reset after a same-line close; precedence against fence, comment and type 6.
  Line endings: CRLF and lone CR.
  The closer pattern has no nested quantifier.
  At AST level, the refusal, provenance, reader, container and opener code is unchanged.
  `gen_toc.py --check` reports no drift at head.
```

## Reviewer-owned ledger at this head

| Lens | Covering round | Head | Status |
|---|---|---|---|
| Conformance | R226-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | covered clean |
| RTL | R226-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | covered clean (no RTL artifact in scope) |
| Robustness | R226-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | covered clean |
| Tests | R226-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | applied; not clean: R226-F1 MINOR open |
| Docs | R226-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | applied; not clean: R226-F1 MINOR open |

## What was checked

1. **Identity** (receipt 04). The local head tree equals GitHub's, the commit's only parent is the base, and the live `dev` tip equals the base.
2. **Existing controls retained.**
   - The base carries 279 TOC arms and 34 em-dash arms; the head carries 683 and 51.
   - Matched by (family, name, fixture hash), every base arm is present at head except two directly affected guard arms. Those were reworded: the family list names eight families, and the site-kind arm now expects single source only (pages/arms-base.json, pages/arms-head.json).
   - In check_em_dash.py only the `selftest` return changed, so the existing em-dash controls are intact (receipt 14).
3. **Sensitivity.** R226 designed its own 33 mutants and ran them on disposable copies; results are in mutants-summary.tsv, with patches and logs.
   - Reverting both sites (R00) fails 157 I440 arms and 10 I440-E arms.
   - Every changed property fails at least one arm. The mutants cover: widening the trailer by FF, NBSP, ZWSP or the blank class body; an argless rstrip; a space-only trailer; ignoring the trailer; a word boundary or attributes at the closer; dropping a name; an end-of-line anchor; lower-or-upper-only matching; case sensitivity; Unicode folding; an optional slash; a fence or type 6 ended by a type-1 closer; the gate reader without newline translation; the base-side refusal dropped; CR removed from REFUSED.
   - Survivors: R08 and R25 (SUGGESTIONs), and R15, R16 and X04 (R226-F1).
   - The input tree's sha256 was identical before and after the runs.
4. **Renderer sweep.**
   - 283 R226 fixtures, rendered in both gfm and markdown modes (sweep/).
   - 97 of the author's 205 fixtures are byte-identical to R226 fixtures. The renderer gives the same result on all 97 when re-rendered independently.
   - The author's instrument reproduces the published sweep-base.json and sweep-head.json byte for byte.
   - The author's base-script snapshot and author-change.patch are byte-identical to the real base scripts and to the base..head diff (receipt 13).
5. **Real Git paths** (e2e/). 18 pages were committed as base and head. At head, each engine's own `gen_toc.py --write` wrote the Contents block. Both shipped CLIs then judged the pages, with GitHub's rendering of each base page as the oracle.
   - At head: 7 labels exempt and 13 findings, all consistent with the oracle. The consistency covers hidden-label escapes rejected (E01, E02, E06, E07, E09, E13-E17), refusal named (E08), accepted labels (cross-name E03, E04, E18; longer fence closer with a tab E05; CRLF cross-name E10; ASCII mixed case E12), and lone CR (E11: label exempt, heading line judged as added).
   - The base engine on the same pages: 3 escapes (E01, E02, E16) and 5 withholds (E03, E04, E10, E11, E18).
6. **Tracked pages** (pages/pages.json).
   - 163 pages, classified by both engines on both the base and head populations.
   - The engines agree on every page, including blocks, kinds, headings, refusals, ownership and generated blocks.
   - 105 pages carry provenance. None is refused, none contains CR, and none has raw-HTML lines.
   - Only DOC_GENERATION.md differs between the populations, and that is its content edit.
7. **Gates R226 ran at head** (receipts 05, 06, 10); all exit 0:
   - `gen_toc.py` with `--selftest` (683/683), `--check` (105 pages), `--verify-anchors` (144 links) and `--sites` (25 sites, all single source).
   - `check_em_dash.py --selftest` (51 arms) and `--base b17580b9` (0 findings over 32 added lines).
   - `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, and `git diff --check`.
8. **Scope.** REFUSED, CLASSES, the openers, ASCII_FOLD, `refusals`, `generated_block`, `owns`, `base_labels`, `judge_page`, both readers and the container logic are unchanged (receipt 14). #437 is untouched.

## Evidence limits

- **Renderer.** GitHub's renderer is a live service, observed on 2026-09-22 between 09:20 and 09:40 +02:00.
  - Only synthetic fixture text was sent, by POST to the `/markdown` endpoint. That endpoint returns HTML and creates no repository, issue or comment object.
  - Parallel requests hit a secondary rate limit, so rendering finished sequentially. Every stored response came from a request that exited 0.
  - Four bodies are empty. `<!--` + `</pre>` + `## Probe` is empty in both modes. The two NUL-in-closer rows for `script` and `textarea` are empty in markdown mode; their gfm bodies show the escaped text and no heading. All four count 0 headings, as the head does.
  - The oracle is the rendered h2 count, not byte-identical HTML across modes.
- **Ratchets.** `check_py_idiom.py` and `check_hygiene.py --check` exited 2 in the R226 scratch clone because the processor submodules are uninitialized there. Their passes are manager-attributed.
- **Not run by R226** (manager-attributed where evidence exists): the full parent, processor, builder, Yosys and behave suites; xvlog; the milan_dp sweep; the act replicas; hosted CI.
- **Historical instruments.** The R85-8 and R86-9 instruments are not public. The historical rows (every refused character at the fence closer and inside `</pre...>`, plus CR) were checked against those reports' public text. They are covered by the R226 population, the author's population and the in-tree arms.
- **Object store.** The scratch clones reached the lane's object store through the review clone's alternates, read-only. The head's commit ID and tree ID were verified against GitHub.

## Pending execution gates (separate from this verdict)

- **Local replica.** The trusted all-four ready-head act replica was started per comment 5772565104; no result was published at the time of this review.
- **Hosted exhaustive contexts.** For the ready head, run 35698385927 still had Verilator shard 4/5 pending at 09:36 +02:00. The ready run had not yet reported `verilator-suites` or `yosys-portability`. The listed skipped aggregates belong to the earlier draft run (receipt 15).
- **Remaining bar.** The R225 review, validation of the candidate merge against the live `dev`, and post-merge containment.

## Integrity

- **Review clone.** The isolated clone at $VALIDATION_STORAGE/reviews/r226-507-r1 stayed detached at `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`.
  - Index sha256 `64afe894...` and tracked-content sha256 `accfa456...` were identical at 09:11:58 and at 09:43:51.
  - `git status` was empty, including untracked and ignored files. There is no stash, and the refs are unchanged (receipts 00 and 99).
- **Submodules.** `external`, `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` were uninitialized (`-`) and empty both before and after. Nothing was initialized.
- **Probe locations.** All probes ran in disposable clones and copies under /tmp/r226-scratch.
- **Actions not taken.** No commit, push, public comment, review, merge, subagent, Docker/act run, hardware access, privileged action or installation. There was no contact with the author or with R225.

## Receipts

All paths are relative to $WORKSPACE_HOME/milan-fpga-management/2026-09-22/507-r1-r226/, and MANIFEST.sha256 covers every file.

- **`receipts/`**
  - 00 and 99: integrity.
  - 01 and 02: public issue and PR text.
  - 03: the diff.
  - 04: identity.
  - 05 to 08: self-tests at head and base.
  - 10: gates.
  - 11: CommonMark clauses.
  - 12: the CR-opener probe.
  - 13: the author-evidence cross-check.
  - 14: AST changed units.
  - 15: the hosted snapshot.
  - 16 and 17: the public R85-8 and R86-9 reports.
- **`probes/`**: the R226 instruments (fixtures, sweep, e2e, mutants, pages, arm population).
- **`sweep/`**: 283 fixtures, byte-exact requests and HTML with SHA-256 receipts for both modes, the base and head observations, and the comparison and summary.
- **`e2e/`**: CLI logs, per-page verdicts, diffstats and oracle HTML for the head, base, mutR15 and mutR16 runs.
- **`mutants/`, `mutants-extra/`, `mutants-summary.tsv`**: patches, self-test logs and results.
- **`pages/`**: all-page classification and the arm populations.
- **`sweep-cr-extra/`**: renderer receipts for receipt 12.

R226-1 FINISHED
