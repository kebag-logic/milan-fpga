[R739] POSITIVE - exact head 9bd82bfb8739de2312da54a9a7b16fa596ec3a91

# Independent delta review R739-5: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `9bd82bfb8739de2312da54a9a7b16fa596ec3a91`, tree `5efc7a96017df6babc2b119c28696418c4244db9`.
- Delta against round 4 head `db9ab221`: 4 commits, one file (`scripts/check_docs.py`, mode unchanged). No Markdown, RTL, generator, bench or Makefile path changed.
- Authority: the round 5 ruling on #96 (issuecomment-6525270244) and the CommonMark 0.31.2 specification it names.
- Order of work: delta and author packet first, with my own probes written from them. The round-4 reports were read only after that pass.

## Verdict basis

R739-4 F1 and F2 are closed at their cause, and so are R740-4 F1 and F2. No MINOR, MAJOR or BLOCKER is open. Three wording items stay as RESIDUE, and the rest are suggestions.

**One decision the manager should see: S-1.** The scanner's list tracking goes past the ruling, and it adds a new way to hide a copy. Three plants that the round-4 head reported now pass at this head (`receipts/compare_heads.log`). I rate this SUGGESTION, not MINOR, for these reasons:
- The cause is list recognition (CommonMark 4.1 and 5.3), not section 4.5 or the ruling's inline list.
- It is the same class as the recorded lazy-line arm.
- It needs an unusual shape: a list-like line that is not a list, then a fence indented under it.
- No page on the tree is affected: the parser comparison found 0 hidden lines on all 33 pages (`receipts/oracle_tree.log`).
- This round's scope excludes searching for further escape forms. I met these while testing the claim that only one divergence hides text, and I did not widen the search.

## The manager's four checks

| Check | Result | Evidence |
|---|---|---|
| (1) Round-4 findings closed | **Met.** See the resolution table. | `receipts/r739_4_fence_cases.log`, `receipts/r739_4_copy_probes_head.txt`, `receipts/rerun_tree_probes_head.log` |
| (2) Fences follow section 4.5 in one scanner; inline markup is neutralised before matching | **Met.** `unfenced_lines` (`scripts/check_docs.py:169-210`) is the only fence parser, and `without_fences` (`:213-215`) and `copy_findings` both call it. `without_markup` (`:502-507`) runs before the value patterns, which are unchanged. | `receipts/oracle_specjson.log`, `receipts/oracle_fuzz.log`, `receipts/markup_and_forms.log` |
| (3) The ten recorded forms stay outside the ruling's lists, and no current page uses any | **Met.** See the ten-form table. One log row does not measure its form; independent checks close that gap (RES-3, S-2). | `receipts/rerun_xfail_real_tree.log`, `receipts/oracle_tree.log`, `receipts/markup_and_forms.log` |
| (4) The gate passes on the tree, and each planted arm fails as stated | **Met.** `make -j16 docs` gives rc 0: 14 current and 18 historical pages, 127 self-test arms. Every copy-rule arm, planted on a real Current page, behaves as stated. | `receipts/gate_head.log`, `receipts/make_docs.log`, `receipts/arms_on_tree.log` |

### Fence evidence for check (2)

| Probe | Result |
|---|---|
| The 29 published examples of "Fenced code blocks" (119-147, read from `spec.json`), line by line against a CommonMark parser | 0 examples hide a line outside the parser's code. Example 128, a blockquoted fence, is returned rather than hidden, which is the safe direction. |
| Fuzz of fence shapes only: character, run 2-6, indent 0-4, trailers including tab, form feed and info strings. 150,000 documents, seed 739, 224,787 sentinels | **0 escapes, 0 fence lines returned** |
| Author's fuzz with lazy continuation made impossible, new seed 7395, 60,000 documents | 0 escapes, 0 wrong-fence cases. The only disagreements are indented code that the copy rule has always scanned. |

Ruling item 1's sentences map to `FENCE_OPEN_RE`, `FENCE_CLOSE_RE` (`:32-33`) and the close test (`:189-192`). The ruling says "nothing but trailing spaces", and the scanner also accepts tabs. Section 4.5 says "spaces or tabs", and the ruling names that section, so I agree with the author's choice.

### Markup evidence for check (2)

- Nine delimiter runs were placed at every position of 13 spellings, giving 5,040 documents. There are 0 escapes outside underscores between word characters, which CommonMark does not treat as delimiters.
- The ruling says to replace every `_`, and also that `snake_5_min` must pass. These conflict if read literally. The author took "delimiter" in the CommonMark sense (`:129`), which I agree with.
- All six non-copies pass as arms on the real tree.
- The extra closed-up view adds matches only, because both views are searched. Each view has its own killed mutant.

### Arms and mutants for check (4)

- `arms_on_tree.py` reads the arm tables from the head's own `selftest()`:
  - 42 must-fail arms give the named finding and rc 1.
  - 26 pass arms and 9 expected-failure arms give no copy finding.
  - 0 differ. The tenth expected-failure arm embeds the fixture table, so it is covered by `open_indented_heading_home` in `rerun_tree_probes_head.log`.
- My first run of this probe showed 3 differences. The cause was the probe: the page ends in a list item, so an appended indented plant joined that item. CommonMark treats it the same way. With a closing paragraph first, all 3 behave as stated, and the published log is that run.
- 46 mutants were rerun, including the ruling's three. All are killed at the expected arm, and the control passes (`receipts/rerun_checker_mutants.log`). Mutant, rc and kill status match the author's log line for line.
- 46 tree probes were rerun: 0 differ from expectation.

## The ten recorded real-copy forms

The ruling's lists are:
- **Fence behaviour:** character, run length, close rule, content lines.
- **Inline delimiters:** `*`, `_`, backtick.
- **Plants:** those from the four named findings.
- **Non-copies:** the six from R739-4.

| Form | In the ruling's lists? | Real tree |
|---|---|---|
| `0.375 s` | No. R739-4 S-1 and R740-4 S2 are suggestions, not F1/F2 plants, and S-1 asked for labelled arms. | 0 hits |
| `375 milliseconds` | No, same. | 0 hits, including other spelled units and `parts per million` |
| Value and unit on two lines | No. Line matching, not markup. | 0 hits |
| `[375](x.md) ms` | No. `[` is not a listed delimiter. | 0 hits |
| `<b>375</b> ms` | No. HTML is not listed. | 0 hits for any tag |
| `375&nbsp;ms` | No. | 0 hits for any entity |
| `~~375~~ ms` | No. `~` is not listed, and strikethrough is not CommonMark. | 0 hits |
| Fence marker in `<pre>` | No. Section 4.6, not 4.5. | 0 hidden lines; no raw HTML start on any current page |
| `  ## Aside` after the home section | No. Heading detection. | 0 indented headings |
| Fence after a lazy list line | No. The form rests on section 5.2 laziness and paragraph tracking. The parser confirms it is a real divergence (`receipts/oracle_forms.log`). | 0 hidden lines |

Real-tree column:
- The hit counts come from `markup_and_forms.py`, which does not use the gate's patterns.
- The hidden-line counts come from `fence_oracle.py tree`: over all 33 Markdown pages, 0 lines are hidden outside the parser's code, and 0 fence lines are returned.
- The only copies in these forms that a probe found are the planted ones.

## Resolution of named prior findings

| Prior finding | Resolution at this head | Evidence |
|---|---|---|
| R739-4 F1 / R740-4 F1 (fence run length and trailing text) | **Closed at cause.** The toggle is gone. All plants are verbatim must-fail arms (`:843-854`). | `fence_cases.py`: 0 disagreements (5 at round 4). `c_after_*` give rc 1. `r740_*` behave as expected. |
| R739-4 F2 / R740-4 F2 (underscore emphasis) | **Closed at cause.** The neutraliser runs first, with no boundary-rule change. All plants are arms, with the six non-copies passing. | `copy_probes_r4.sh`: 35 copies caught, 12 non-copies pass, 6 table plants caught. The 2 remaining passes are `c_decimal_s` and `c_word_ms`, both recorded forms. Matches the author's receipt. |
| R739-4 RES-1 / R740-4 R2 (pointer scope wording) | **Retained as RES-1.** The ruling allowed no prose changes. The author's point holds: my proposed wording has 14 words and fails the page gate, which I reproduced. A passing form is below. The live PR body takes the wording. | Direct `style_findings` run |
| R740-4 R1 (PR body enumeration) | **Resolved.** The list is gone from the live PR body. | PR body line 46 |
| R739-4 S-1 / R740-4 S2 (decimal and unit words) | **Resolved** as expected-failure arms. Unitless rows have no arm, because the rule reads only rows with a unit. | `:921-922` |
| R739-4 S-2 / R740-4 S6 (`usage ={`) | **Resolved.** | `:936` |
| R739-4 S-3 / R740-4 S7 (shared fence parser) | **Resolved.** | `:215`, `:526` |
| R739-4 S-4, S-5, S-6; R740-4 S1, S3, S4, S5 | Unchanged and not taken. They stay suggestions. | Outside this delta |

## Findings

No BLOCKER, MAJOR or MINOR is open.

### RESIDUE (wording only; does not change the verdict)

- **RES-1 - RESIDUE - Docs.**
  - **Where:** `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59`, `docs/README.md:48`.
  - **Authority and evidence:** `make docs` also runs other checks (`Makefile:28-36`). The sentence means the rules for the table beside it.
  - **Impact:** scope wording only.
  - **Exact fix:** "Rules for this table: `scripts/check_docs.py`; its [`selftest()`](../scripts/check_docs.py) cases specify them."
  - **Verification:** that sentence gives 0 `style_findings`. This replaces my round-4 wording.
- **RES-2 - RESIDUE - Docs.**
  - **Where:** PR body line 54, "The one divergence that hides text is recorded as an expected failure below."
  - **Authority and evidence:** the sentence is true of the fuzz grammar, but the PR body does not state that limit. `receipts/oracle_forms.log` shows other divergences outside the grammar (S-1). The handoff does state the limit.
  - **Impact:** a reader may take it as the only divergence anywhere.
  - **Exact fix:** "The fence scanner was fuzzed against a CommonMark parser over 600,000 documents from a fixed grammar of fence, list and comment shapes. In that grammar, the one divergence that hides text is recorded as an expected failure below. List-recognition divergences outside the grammar remain."
- **RES-3 - RESIDUE - Docs.**
  - **Where:** PR body line 57, "With each form's rule widened, the real tree still passes, so no current page holds such a copy."
  - **Authority and evidence:** the conclusion is true, and I verified it independently. The method is stated too broadly: `xfail_lazy_list_line` widens nothing on a real page (S-2).
  - **Impact:** the sentence describes one log row as a measurement it is not.
  - **Exact fix:** "Each form was checked on the real tree, by a widened rule or, for the lazy-line form, by comparison with a CommonMark parser. No current page holds such a copy."

### SUGGESTION (non-blocking)

- **S-1 - SUGGESTION - Robustness, Tests.**
  - **Where:** `scripts/check_docs.py:31`, `:194-200`.
  - **Authority:** CommonMark 0.31.2 4.1 (a thematic break takes precedence over a list item), 5.2 rule 2 (content offset of an item starting with indented code or a blank line), 5.3 (only an ordered list starting at 1 can interrupt a paragraph).
  - **Evidence:** each plant ends in a real copy, which a CommonMark parser shows as text (`receipts/oracle_forms.log`). The results at both heads are in `receipts/compare_heads.log`:

    | Plant | `db9ab221` | Head |
    |---|---|---|
    | `text`, `2. ` + fence, then an indented copy | reported | **hidden** |
    | `* * *`, an indented fence, `x`, `y`, a fence line, then a copy | reported | **hidden** |
    | `text`, `2. item`, an indented fence, `x`, `y`, a fence line, then a copy | reported | **hidden** |
    | `-` + six spaces + `x`, an indented fence, `y`, then a copy | hidden | hidden |
    | `-` + three spaces, an indented fence, `y`, then a copy | hidden | hidden |
  - **Cause:** the scanner treats these lines as list items, or sets the wrong content offset. A false item then closes a real fence early, or opens one where CommonMark has none.
  - **Impact:** no page is affected. The first three are new hiding paths that came with the list tracking the author added past the ruling.
  - **Optional outcome:** check for a thematic break before the list marker, and apply the 5.2 offset rule. Both are small. Record the paragraph-dependent forms beside the lazy-line arm.
  - **Verification:** rerun `compare_heads.py` and `fence_oracle.py forms`.
- **S-2 - SUGGESTION - Tests.**
  - **Where:** author `receipts/checker_mutants.py`, used by `xfail_real_tree.py`.
  - **Evidence:** `xfail_lazy_list_line` tests `line != "lazy"`, so it can only fire on a line reading exactly `lazy`. Three others are narrower than their form: `<pre` only, `&nbsp;` only, `milliseconds` only.
  - **Impact:** those log rows prove less than they appear to. My independent scans close the gap at this head, with no change to the gate.
  - **Optional outcome:** keep a parser comparison over the tree as the receipt for the fence forms.
  - **Verification:** `fence_oracle.py <repo> tree`.
- **S-3 - SUGGESTION - Robustness.**
  - **Where:** `scripts/check_docs.py:502-507`.
  - **Evidence:** `receipts/false_positive_notes.log`. "twenty-*five* minutes" and "1**375** ms" are reported through the spaced view, and "3*75 ms" through the closed-up view.
  - **Impact:** loud only. The first two follow from the ruling's own space replacement.
  - **Optional outcome:** none needed unless a page ever trips one.
- **S-4 - SUGGESTION - Robustness.**
  - **Where:** `scripts/check_docs.py:383` (`section_lines`).
  - **Evidence:** read only, not probed. It does not use the scanner, so a fenced `## ` line still moves its section boundary. The delta does not touch it.
  - **Optional outcome:** use the scanner there too if the helper is next changed.

## Other statements checked

- **Author decisions 1-5:** I agree with all five, apart from the method wording in RES-2 and RES-3.
- **Comment rule:** the delta's added lines contain no lane label, review round, reviewer ID or issue-comment ID.
- **Scope:** one file changed. `git diff --check` from `135afd04` is clean.
- **PR body and line references:**
  - The live PR body differs from the packet copy only by one blank line.
  - Its `selftest()` link points to the correct line (`:631`).

## Published author evidence (milan-fpga `7e657bcd`, `review-evidence/gptp96-r1/author-r5`)

- 71 files were fetched and checked against `MANIFEST.json`: 71 match, none missing or extra. Eight are marked path-redacted (identity, lint, gate-script and parent docs logs).
- Parent gates, author's run:
  - The rc 1 rows fail on the gitlink pin; the head of the log shows that error, and the author records it for all rows.
  - After normalising the SHA, the four logs at `db9ab221` and the head are identical, which I re-checked.
  - Re-pinned, `check_gptp_docs.py --with-submodule` gives rc 0.
  - `make -C gptp-processor docs` shows 127 arms.

## Clone integrity (`receipts/clone_integrity.txt`)

Head, tree and `git write-tree` agree. Status and ignored status are empty, and index and worktree match the head. Blob and mode listings hash the same. The repository has no submodule gitlinks. A probe left one ignored bytecode directory under `scripts/`, which I removed; the ignored-status line in the receipt was refreshed after that removal. No probe wrote to a tracked path.

## Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling items 1-3 against the code, published section 4.5 examples, the ten forms against the ruling's lists; earlier clause coverage retained, as no page changed | R739-5 delta; earlier rounds for unchanged pages | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| RTL | CLEAN (no delta) | `git diff --raw db9ab221 HEAD` shows no `hdl/` path; prior verdict retained | R739-5 scope check; earlier rounds | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Robustness | CLEAN | Scanner, neutraliser, parser comparison on spec, fuzz and tree, markup product; S-1 and S-3 recorded | R739-5 | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Tests | CLEAN | 127 arms, all copy-rule arms planted on the tree, 46 mutants and 46 probes rerun, round-4 probes rerun; S-1 and S-2 recorded | R739-5 | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Docs | CLEAN (RES-1 to RES-3 are residue) | No Markdown delta; `make docs`; live PR body; form scan and tree comparison on current pages | R739-5 delta; earlier rounds for unchanged pages | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |

## Real limits

- By instruction, I did not search for escape forms beyond the ruling. S-1 is what I met while testing a claim, not a survey of list shapes.
- The parser comparison uses one CommonMark implementation (`receipts/parser_identity.txt`). Its section 4.5 result was not repeated on a second parser.
- Not run by me: `make lint`, `make contract`, and the parent gates. Lint reads `hdl/` and contract reads `tb/check_phc_contract.py`, neither changed by the delta, so I rely on the author's published receipts for those. `make docs` did run the diagram check.
- No suite, build, hardware or physical calibration was run or implied. Physical calibration is NOT RUN, and field skips are not hardware proof.
- PR #97 reports no hosted check at this head, and the author records no hosted workflow in the repository. This is not hosted evidence.

## Pending manager duties

- Validate the current-dev merge candidate (source base `135afd04`, live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`) at the merge turn, and link its receipts. No manager source bank ran at this head.
- Own hosted and act acceptance.
- Re-pin the parent gPTP docs and the submodule-docs page and diagram when the parent bump lands, since the parent gates fail on any gitlink move until then.
- Carry RES-1 to RES-3 to the residue checklist.
- Decide whether S-1 should be recorded as arms before merge.

R739-5 FINISHED
