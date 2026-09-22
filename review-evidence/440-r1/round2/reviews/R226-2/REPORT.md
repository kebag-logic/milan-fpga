[R226] POSITIVE - exact head 9d6109ccf924c03308cb8aa202ce68a435cd4f8d

Round R226-2 is the external cold re-review (Opus) of kebag-logic/milan-fpga PR #507 for issue #440, after the correction for R226-F1.

- Head: `9d6109ccf924c03308cb8aa202ce68a435cd4f8d`, tree `1d322d866da6b8d19ccd46cfd7ef5f405e9dadb4`. The PR head, `refs/heads/440-markdown-closers` and `refs/pull/507/head` all equal it. This was checked at 11:38 and again at 11:58 +02:00. The PR was open and ready (receipt 04).
- Prior reviewed head: `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba` (tree `c0e67508d3b753c21a28a243d365c4c37ed86d43`). It is the head's only parent.
- Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. It is also the live `dev` tip, and an ancestor of the head.
- Lenses applied at this head: Conformance, RTL, Robustness, Tests, Docs. All five were applied afresh at `9d6109cc`. The ledger below banks no prior coverage.

**Verdict basis.**

- R226-F1 (MINOR; Tests, Docs) is resolved at this head (next section).
- No BLOCKER, MAJOR or MINOR is open under any lens.
- This round adds two optional SUGGESTIONs, S1 and S2. The five R226-1 SUGGESTIONs are unchanged and remain optional.
- The production walk and gate are byte-identical to `0d43ff25`, except the self-test floor `MIN_ARMS`.

This is a code-review verdict only. Pending execution gates are listed separately below.

**Authority read:**

- AGENTS.md, and CONTRIBUTING.md sections 2, 3 and 6.1.
- Issue #440: the body, scope comment 5651705425, decision 5771170243, assignment 5771559992, and the A158 and A164 comments.
- PR #507: the body and 13 of the 14 comments present when this round started. These include R226-1 (5772986192), the F1 acceptance (5772995412), the correction notices (5773270202, 5773298390), the native evidence (5774050784) and the re-review start (5774292729). The body of R225-1's review (5772722112) was not read. Of the two comments posted later (5774554247 and 5774554525), only the first lines were read.
- CommonMark 0.31.2 sections 4.5 and 4.6 (R226-1 receipt 11).
- The diff and commit history.
- The public evidence commits `26f9c867` (R226-1), `4c39e5fb` (A164 author) and `87c0683b` (manager native).

## R226-F1 result: resolved under Tests and Docs

R226-F1 asked for three things:

- a control that fails when the closer site accepts a closing tag of another ASCII name (a raw-walk arm at minimum; a shipped-label row preferred);
- R15 (div), R16 (title) and X04 (xmp) to each fail at least one arm;
- DOC_GENERATION.md:55 to be true as written, or narrowed to what the controls hold.

| F1 item | Evidence at `9d6109cc` | Result |
|---|---|---|
| Raw-walk control (minimum) | 24 `I440-T-other-name` arms, `scripts/gen_toc_closer_cases.py:25, :56-58`. They cover 4 openers, a later-line and an opening-line closer, and div, title and xmp. Each is graded on the real `blocks()` classification of the probe line. | met |
| Shipped-label control (preferred) | 6 `I440-E-other-*` rows, `:91-96`. They cover `<pre>`, both positions and the three names. Each runs the real `check_em_dash.judge_page` on real base and head commits. Each requires 1 finding, 0 exemptions and the "mirrors no heading" note. | met |
| R15, R16, X04 each fail at least one arm | Each fails exactly its 8 raw arms (`gen_toc.py --selftest` exit 1, 699/707) and its 2 label rows (`check_em_dash.py --selftest` exit 2). No other arm fails (mutants-head/). | met |
| E2E: no E14/E15 exemption unless a self-test already failed | Under R15, R16 and X04 the real `check_em_dash.py --base` exits 2 on its own controls before judging any page (e2e/e2e-vs-oracle.txt). | met |
| DOC_GENERATION.md:55 true or narrowed | `:55` now reads "`I440` controls cover fence trailers and literal type-1 closer boundaries." `:57` reads "Raw-walk and shipped-label controls reject `div`, `title`, and `xmp`." Both are true at this head. | met |

These controls test closer-site widening, not a widened `RAW_HTML_TAGS`:

- In the R15, R16 and X04 runs, `RAW_HTML_TAGS` is still the four names. The existing arm "the type-1 names are the renderer's four" passes, and only the new controls fail.
- Widening at one call site catches only that site's controls:
  - `_still_open` alone fails the 4 later-line raw arms and the later-line label row;
  - `_opens` alone fails the 4 opening-line raw arms and the inline label row;
  - both also trip the existing site-count guard.
- A literal alternation that no longer reads `RAW_HTML_TAGS` fails the same 8 raw arms and 2 label rows.
- At `0d43ff25`, R15, R16, X04 and the three literal-alternation mutants pass both self-tests. There, the shipped CLI exempts the hidden labels: E14 and E20 (div), E15 and E21 (title), E19 and E22 (xmp). So the new controls are what detect the defect.
- The actual effect on each consumer:
  - Under R15, `gen_toc.py --check`, which runs no self-test, reports NO TOC for the E14 and E20 base pages. That is, the generator would list a hidden heading.
  - Under each mutant, the docs workflow's `gen_toc.py --selftest` step (`.github/workflows/docs.yml:380`) fails, and its `check_em_dash.py --base` step (`:87`) refuses.
- GitHub's renderer confirms the new expectations. None of the 30 new fixture sources renders its probe or Old heading, in either gfm or markdown mode. Six positive controls from the same session do render theirs (render/).

## Findings

```text
[R226] SUGGESTION Tests, Docs - scripts/gen_toc_closer_cases.py:20, :25 - the other-name controls sample three names; widening to any other name still passes
Requirement/evidence: R226-F1's stated minimum (one raw-walk arm) and its verification
  (R15, R16, X04) are met, and DOC_GENERATION.md:57 names exactly the three sampled names.
  Adding any other name at the closer site still passes 707/707 and 57. Measured: iframe,
  noscript, plaintext, noembed, noframes, listing, p, span, code, b, and the synthetic name
  pre2 (mutants Z-*, mutants-head/summary.tsv).
  R226-1 rows R226-T-othername-{pre,script}-{iframe,noscript,plaintext,noembed,noframes,
  listing,p,span,code} render 0 headings, so each of those widenings would reopen the escape.
  The comment at :20 says the fixtures "hold both name-set boundaries".
Impact: optional. The residual needs an edit at the closer site that names an unsampled tag.
Required outcome: optional. Either a population-wide or structural control of the closer's
  name set, or wording at :20 that says the widening side is sampled.
Verification: the Z-* mutants fail at least one arm, or the comment at :20 matches
  _OTHER_NAMES.
```

```text
[R226] SUGGESTION Robustness, Tests - scripts/check_em_dash.py:947-949; scripts/gen_toc_closer_cases.py:136-139 - a git refusal inside the label rows exits 1 with a traceback, not 2
Requirement/evidence: check_em_dash.py:954 documents "0 clean, 1 findings, 2 cannot judge
  or an arm did not bite". selftest() wraps the planted controls (:935-938) so that a Refusal
  is rc 2. The em_dash_arms call at :948-949 sits outside that wrapper, as the base's
  _base_derivation_arms call at :947 already does.
  In a disposable copy, a Refusal injected into the label rows makes the real CLI print a
  traceback and exit 1 (receipt 11b). The same injection into a planted control returns rc 2
  (receipt 11).
Impact: optional. Only a git failure during the self-test reaches this path. The run still
  fails, so a clean result is impossible; only the meaning of the exit code is wrong. The
  correction adds six rows to this harness and does not change the path.
Required outcome: optional. A Refusal inside these arms is reported as an arm that did not
  hold (rc 2), as it already is for the planted controls.
Verification: rerun the injection in receipt 11b; the CLI exits 2 and names the problem.
```

## Clean lenses

```text
[R226] PASS Conformance - scripts/gen_toc.py:473-500 at 9d6109cc; scripts/gen_toc_closer_cases.py:25, :56-58, :91-96; render/render-report.json; render/render-positive-report.json; sweep-r2/summary.json; e2e/e2e-vs-oracle.txt; R226-1 receipts/11-commonmark-clauses.txt - the closing rules still match decision 5771170243 and CommonMark 0.31.2 sections 4.5 and 4.6, and the new expectations agree with GitHub
  The closer sites are byte-identical to 0d43ff25 (receipt 03). The fence trailer strips only
  CLASSES["blank"]. `_type_1_end` searches `</(pre|script|style|textarea)>` under ASCII_FOLD,
  on both the opening line and later lines.
  CommonMark 4.6 end condition 1 names only those four end tags, so div, title and xmp end no
  type-1 block.
  All 30 new fixture sources render without their heading in gfm and markdown modes, and the
  six positive controls render theirs.
  The real reader at this head, over the 283 R226-1 fixtures: 283/283 agree. The shipped
  answer is 211 agree and 72 globally refused, with 0 escapes and 0 withholds. At the base:
  15 escapes and 41 withholds.
  Every base-to-head change falls in a fence-trailer or type-1-closer row.
  22 real Git pages through both shipped CLIs: each label is exempt exactly when GitHub
  renders the base heading (E01-E22).
  Issue acceptance criteria 1-4 hold. Every R226-1 mutant caught at 0d43ff25 is still
  caught; R00, the revert, fails 157 I440 arms and 10 I440-E diagnostics.
```

```text
[R226] PASS RTL - receipts/09-rtl-scope.txt (git diff b17580b9..9d6109cc and 0d43ff25..9d6109cc) - no RTL artifact is in scope at this head
  The PR changes docs/DOC_GENERATION.md and five Python files under scripts/; the correction
  changes three of those six. Nothing under hdl/, tb/, syn/, sw/ or the RTL submodules
  changes, and no workflow, budget, VERSION, .gitmodules or gitlink.
  Manager-attributed native evidence bound to this head is not reproduced here (archive
  87c0683b, round2/manager: candidate.json, native-integrity.json):
  - 43 static and builder commands exit 0;
  - 55 parent suites, 2,118,264 checks, 0 in-suite failures;
  - Yosys; protocol-processor 14,903 checks; gPTP `make all`;
  - behave: 14 features, 316 scenarios, 1,515 steps.
```

```text
[R226] PASS Robustness - sweep-r2/comparison.tsv (families fence-eof, type1-eof, fence-length, fence-indent, fence-kind, type1-malformed, type1-reset, type1-precedence, type1-embedded, cr); receipts/03-identity-and-scope.txt; e2e/head-e2e.json; receipts/11, 11b - boundary, malformed and line-ending inputs agree with the renderer at this head, and the refusal, reader and container code is unchanged
  After the real reader at 9d6109cc, every row of those families agrees. The raw walk
  withholds 9 CR rows; all 9 are in the refused CR family, and all agree after reader
  normalization.
  Since 0d43ff25 the only production-file change is MIN_ARMS. REFUSED, CLASSES, the openers,
  refusals(), both readers, base_labels, judge_page and the container logic are byte-identical.
  The added fixtures open no new input path: they reuse the gate's isolated fixture Git and
  its temporary repositories.
  The e2e pages at this head include CRLF, lone CR, EOF without a final LF, a refused base
  character and unrefused ZWSP. All agree with the oracle.
  One failure path is recorded as S2, which is optional.
```

```text
[R226] PASS Tests - scripts/gen_toc_closer_cases.py:25, :56-58, :91-96; scripts/gen_toc.py:55; mutants-head/summary.tsv; mutants-prev/summary.tsv; receipts/06, 07; maintenance/results.json; e2e/e2e-vs-oracle.txt - the new controls fail for the defect they claim, and only for it
  Positive: 707/707 TOC and 57 em-dash pass at head. The label rows pass only through the
  "mirrors no heading" judgment.
  Negative: R15, R16 and X04 each fail exactly 8 raw arms and 2 label rows. The per-site and
  literal-alternation variants fail too. At 0d43ff25 the same mutants pass.
  Boundary: every opener and both closer positions (raw arms); both positions with <pre>
  (label rows).
  Integration: the raw arms use the real blocks(); the label rows use the real judge_page on
  real commits; the real CLI stops at rc 2 under each mutant.
  Independence: `_OTHER_NAMES` is a literal tuple, independent of RAW_HTML_TAGS, and the
  renderer confirms every expected answer.
  Regression: every mutant caught at 0d43ff25 is still caught. All 683 prior TOC arms and 17
  prior label rows are retained unchanged. The focused gates pass (receipt 08).
  Removing any new raw arm trips the 707 floor (M1, M2). The label rows have no floor (M3
  passes at 51); that is R226-1's optional em-dash-floor SUGGESTION, which is still open.
```

```text
[R226] PASS Docs - docs/DOC_GENERATION.md:55, :57 at 9d6109cc; PR #507 body; receipts/08-gates-head.txt - the coverage statement now matches what the controls hold
  :55 claims fence-trailer and literal type-1 closer-boundary controls. :57 names exactly the
  three names that the raw-walk and shipped-label controls reject. Both are true at this head
  (receipt 07, mutants-head/).
  No tracked page cites the old 683 or 51 totals.
  All pass: gen_toc --check (105 pages), --verify-anchors (144 links) and --sites (25, all
  single source); check_em_dash --base b17580b9 (0 findings over 34 added lines); docs_check,
  check_doc_style and check_doc_paths.
  The PR body's 707/57 totals, its retained-controls statement and its div/title/xmp
  statement are accurate.
  The public archives let a cold reviewer rebuild the evidence (archive MANIFEST.json
  verifies). The commit message is one line with no trailers.
```

## Reviewer-owned ledger at this head

| Lens | Covering round | Head | Status | Prior coverage (not banked) |
|---|---|---|---|---|
| Conformance | R226-2 | 9d6109ccf924c03308cb8aa202ce68a435cd4f8d | covered clean; applied afresh | R226-1 clean at 0d43ff25. Re-applied because the correction changed scripts/gen_toc.py and the closer expectations. |
| RTL | R226-2 | 9d6109ccf924c03308cb8aa202ce68a435cd4f8d | covered clean; applied afresh (no RTL artifact in scope) | R226-1 clean at 0d43ff25. Retainable, since 0d43ff25..9d6109cc touches no RTL-scope artifact, but not relied on. |
| Robustness | R226-2 | 9d6109ccf924c03308cb8aa202ce68a435cd4f8d | covered clean; applied afresh; S2 optional | R226-1 clean at 0d43ff25. Re-applied because scripts/gen_toc.py changed. |
| Tests | R226-2 | 9d6109ccf924c03308cb8aa202ce68a435cd4f8d | covered clean; R226-F1 resolved; S1 and S2 optional | R226-1 at 0d43ff25 not clean (R226-F1). |
| Docs | R226-2 | 9d6109ccf924c03308cb8aa202ce68a435cd4f8d | covered clean; R226-F1 resolved; S1 optional | R226-1 at 0d43ff25 not clean (R226-F1). |

**Retained prior coverage: none.**

- Every row is an R226-2 application at the exact head.
- R226-1's stored renderer outputs serve only as the oracle for fixed fixture bytes (the 283-row sweep and pages E01-E18).
- No R226-1 execution result at `0d43ff25` is counted as evidence for `9d6109cc`.

## Author claims checked

- **Parser unchanged except the floor.** `0d43ff25..9d6109cc` changes 3 paths, with no mode change. In `gen_toc.py` the word diff is `683` -> `707` only. `check_em_dash.py`, `gen_toc_cases.py` and `gen_toc_guards.py` are blob-identical (receipt 03). Confirmed.
- **24 raw and 6 shipped-label controls added** (receipt 07). Confirmed.
- **All 683 TOC and 51 em-dash controls preserved.**
  - The 683 TOC arms are retained by (family, name, fixture hash, expected kind), with 0 removed and their order kept.
  - The 17 label rows are retained byte for byte, in order.
  - `check_em_dash.py` is unchanged, so its other 34 arms are too.
  - Totals are 707 and 57 (receipt 06). Confirmed.
- **Each exact mutant fails 8 raw and 2 label controls.** Confirmed. The FATAL line reads "4 of 57 arm(s)" because each failed row emits two diagnostics, as the author's RESPONSE.md says.
- **Author archive integrity.** The per-folder `MANIFEST.sha256` fails on 24 path-neutralized files. The top-level `MANIFEST.json` at `87c0683b` matches all 2,950 round-2 and R226-1 files by published hash. It records original hashes for the 90 neutralized entries (receipt 10).

## Evidence limits

- **Renderer.** GitHub's renderer is a live service.
  - This round sent 80 sequential POSTs of synthetic fixture text to `/markdown`, between 11:46:53 and 11:52:59 +02:00. That endpoint creates no object.
  - The 283-row sweep and E01-E18 use R226-1's stored renders (09:20-09:40 +02:00). Six new fixtures are byte-identical to R226-1 fixtures; re-rendered, they gave the same counts.
  - The oracle is whether the heading renders as an h2, not byte-identical HTML.
- **Residual names.** The residual other-name widening is described in S1.
- **Not run by R226-2** (manager-attributed where the `87c0683b` evidence exists):
  - the full parent, processor, builder, Yosys and behave suites;
  - xvlog and the milan_dp sweep;
  - `check_py_idiom.py` and `check_hygiene.py`, which need initialized submodules;
  - the act replicas and hosted CI.
- **Hosted results.** Results for `9d6109cc` were not inspected or polled. No public manager notice recorded the actual trusted-runner start (last checked 12:04 +02:00, when the PR head, `refs/heads/440-markdown-closers` and `dev` were also unchanged).
- **Independence.** R225's rounds were not read or used for this verdict.
- **Object store.** Scratch clones read the review clone's object store through `--shared` alternates, read-only.

## Pending merge gates (separate from this verdict)

- **Local replica.** The trusted all-four ready replica at `9d6109cc` is queued behind PR505 (5774050784, 5774292729). No actual start or result was public at the time of this report.
  - The earlier ready replica at `0d43ff25` was interrupted (5773029272) and is not a PASS.
  - Draft replica evidence at `0d43ff25` does not transfer to this head.
- **Hosted contexts.** The hosted exhaustive and other required contexts on `9d6109cc` were not inspected; no claim is made.
- **R225-2.** R225-2 has published a line reading `[R225] POSITIVE - exact head 9d6109cc...` (5774554247, 11:59:20 +02:00). R226 did not read its body or ledger. Whether that ledger clears every lens is for the manager to confirm.
- **Candidate merge.** The candidate merge must be validated against live `dev` at merge time. The manager records candidate tree = head tree over `b17580b9` (`87c0683b` candidate.json); this must be rechecked if `dev` moves.
- **After merge.** Post-merge containment and the move to Done.
- **Physical gate.** Physical calibration gate 11 remains NOT RUN under the existing deferral (manager statement).

## Integrity

- **Review clone.** `$VALIDATION_STORAGE/reviews/r226-507-r2` stayed detached at `9d6109cc`. Snapshots at 11:41:30 and 12:04:38 +02:00 are identical (receipts 00 and 99):
  - index sha256 `356fbdc2...` and `ls-files -s` sha256 `a7709436...`;
  - the index equals the HEAD tree, and the working-tree blobs equal the index blobs;
  - on-disk modes match the index, and no assume-unchanged or skip-worktree flag is set;
  - `git status` is empty, including untracked and ignored files;
  - there is no stash, and the refs are unchanged.
- **Submodules.** `external`, `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` were uninitialized and unchanged throughout.
- **Probe locations.** No Python ran in the review clone. Every probe ran in `/tmp/r226-2-scratch`, in scratch clones and disposable copies. Each mutant run verified that its input scripts' digest was unchanged.
- **Actions not taken.** No commit, push, public comment, review, metadata change, merge, Docker/act run, hardware access, privileged action, installation or subagent. There was no contact with the author, R225 or other agents.

## Receipts

All paths are relative to $WORKSPACE_HOME/milan-fpga-management/2026-09-22/507-r2-r226/, and MANIFEST.sha256 covers every file.

- **`receipts/`**
  - 00 and 99: integrity.
  - 01 and 02: public issue and PR text; 02b: first lines of the later PR comments.
  - 03: identity and scope.
  - 04: remote identity.
  - 05 and 06: environment and self-tests at head, prior head and base.
  - 07: arm populations.
  - 08: focused gates.
  - 09: RTL scope.
  - 10: the archive manifest.
  - 11 and 11b: the refusal path.
  - COMMANDS.txt: exact commands.
- **`probes/`**: the R226-2 instruments. `probes/r226-1-public/` holds the public R226-1 instruments, with SOURCE.txt blob identities.
- **`population/`**: head and prior-head arm populations.
- **`render/`**: 36 fixtures, each with byte-exact requests and HTML and SHA-256 receipts, in both modes.
- **`mutants-head/`, `mutants-prev/`**: patches, logs, results and summaries.
- **`e2e/`**: CLI logs, per-page verdicts, the oracle for E19-E22, and the comparison.
- **`sweep-r2/`**: head and base observations and the comparison.
- **`maintenance/`**: the deletion-resistance probes.

R226-2 FINISHED
