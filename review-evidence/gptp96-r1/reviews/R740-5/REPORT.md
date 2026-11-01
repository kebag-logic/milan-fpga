[R740] POSITIVE - exact head 9bd82bfb8739de2312da54a9a7b16fa596ec3a91

Round 5 delta review of issue #96 / PR #97. Tree `5efc7a96017df6babc2b119c28696418c4244db9`. Delta base `db9ab2215ba18aec4c1828090b3611b001dbf2b8`, source base `135afd04`, live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`. Ruling: [issue comment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96#issuecomment-6525270244). Review start: [PR comment](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6563137825).

**Verdict.** No BLOCKER, MAJOR or MINOR is open. My two round-4 findings are closed at their cause. The §4.5 rules agree with two CommonMark parsers on every sentinel in 480,000 generated documents. Markup is neutralised before the value rules, and the value patterns are untouched. The ten recorded forms stay outside the ruling's lists, and no current page uses any of them. The gate passes on the tree, and all 78 planted arms behave as stated.

**One item the manager should read: S1.** Beyond the ruling, the scanner also tracks list containers. Its list arithmetic hides a visible copy in six further forms that are not recorded as arms. Round 4 caught two of the six, because the old code ignored list markers, so those two are regressions of this delta. All six are outside the ruling's lists, no page uses them, and the focus for this round says not to pursue further forms. I therefore record S1 as a SUGGESTION, not a finding. If the manager reads "fences follow CommonMark" as covering container ends, S1 becomes a MINOR.

## The four checks

| Check | Result | Evidence |
|---|---|---|
| (1) Round-4 findings closed | **Yes.** See "Prior findings". | `receipts/real_probes.log`, `receipts/plant_arms.log` |
| (2) §4.5 in one scanner; markup neutralised first | **Yes.** See "Check 2". | `receipts/fuzz_totals.txt`, `receipts/fuzz_pure_*.log`, `receipts/real_pages_diff.log` |
| (3) Ten forms outside the lists, unused on current pages | **Yes.** See "Check 3". | `receipts/rerun_xfail_real_tree.log`, `receipts/ten_forms_grep.log`, `receipts/real_pages_diff.log` |
| (4) Gate passes; each arm fails as stated | **Yes.** See "Check 4". | `receipts/head_*.log`, `.rc`, `receipts/plant_arms.log`, `receipts/rerun_checker_mutants.log` |

### Check 2: fences and markup

**Fences.** `unfenced_lines` (`scripts/check_docs.py:169-210`) is the only fence parser in the file. `without_fences` (`:213-215`) and `copy_findings` (`:526`) both call it. The old toggles and `FENCE_MARKERS` are gone.

| Rule in the ruling or §4.5 | Code | Result |
|---|---|---|
| Opening character and run length kept | `:205-207` (`fence = run.group(1) or run.group(2)`) | Agrees |
| Close: same character, at least as long, only spaces or tabs after | `:33`, `:189-192` | Agrees |
| Shorter or different line inside is content | `:193` (`continue`) | Agrees |
| Backtick info string holds no backtick; tilde info string may | `:32` | Agrees |
| Up to three spaces of indent; four is not a fence | `:190`, `:206` | Agrees |
| Form feed or no-break space after a close marker is not a close | `:33`, line split at `:181` | Agrees |

My own generator exercises these rules alone: run lengths 1 to 6, both characters, indents 0 to 5, tabs, 15 kinds of tail, blank lines and prose. Over 480,000 documents and 540,170 sentinels, it found **0 escapes and 0 loud cases against each parser**.

One limit applies to parser B, whose version predates the 0.31.2 "spaces or tabs" close. It gave 68 escapes on a first run, and all of them disappeared once trailing tabs were given to it as spaces, so they came from that older rule. That first log was not kept. Parser A needed no adjustment and reported 0 on both runs. Identities are in `receipts/parser_identity.txt`.

On real pages, the scanner's hidden lines equal the parser's fence lines on all 33 Markdown files and 38 fences, with 0 pages differing (`receipts/real_pages_diff.log`).

**Markup.** `INLINE_MARKUP_RE` (`:129`) and `without_markup` (`:502-507`) run on every scanned line before the patterns are searched (`:531-537`). `value_spellings` is not in the delta, so no boundary rule gained an underscore case, as the ruling asked.

I accept the author's three departures from the ruling's literal sentences:
- **An underscore between word characters stays.** Item 3 needs `snake_5_min` to pass, and such an underscore cannot delimit in CommonMark §6.2. The mutant `underscore_always_stripped` is killed.
- **A close may have trailing tabs.** The ruling names §4.5, and §4.5 says "spaces or tabs". This errs towards showing the text that follows.
- **A second, closed-up view of the line.** The spaced view is the ruling's replacement; the joined view only adds catches such as `**5**-minute` and `37*5* ms`. All six non-copies still pass.

### Check 3: the ten recorded forms

The ruling's lists are the §4.5 fence rules in its item 1 and the delimiters `*`, `_` and backtick in its item 2.

| Form | Why it is outside the lists |
|---|---|
| Decimal seconds; spelled unit | A different spelling, not markup or a fence |
| Wrapped line | A line break, not a listed delimiter |
| Link, HTML tag or entity on the value | Not `*`, `_` or backtick |
| Strikethrough `~~` | Not listed, and GFM rather than CommonMark |
| Marker in an HTML block | §4.6 block precedence |
| Indented heading after the home section | Heading detection |
| Fence after a lazy list line | §5.2 laziness. The marker is parsed correctly; the container is wrong. |

Each form passes on a real page at this head. The arms are at `:918-935`; `receipts/real_probes.log` and `receipts/plant_arms.log` hold the runs. The link form gives rc 1 with the arm's dangling `x.md`, from the link rule and not a copy finding. With a real target it gives rc 0.

No current page uses any form, by three independent routes:
- The author's widened-rule receipt reproduces byte for byte (`receipts/rerun_xfail_real_tree.log`).
- My own search of the 14 current pages, for all 9 unit-bearing constants and not using the checker's matcher, has 0 hits and finds no indented headings (`receipts/ten_forms_grep.log`).
- The real-page parser comparison shows no HTML-block or lazy divergence.

### Check 4: gate and arms

| Check at this head | Result |
|---|---|
| `check_docs.py`, `--selftest`, `make docs` | rc 0; 14 current, 18 historical pages; 127 arms |
| `make contract`; `make lint` with the pinned 5.050 | rc 0 each |
| `git diff --check` from source base and from round 4 | rc 0 each |
| Every copy-rule arm, read from the source and planted on a real page | 26 pass arms and 42 must-fail arms behave as stated, each must-fail under its named constant; 9 expected-failure arms give no copy finding; 0 bad |
| Tenth expected-failure arm, placed after the real constants table | rc 0, no copy finding |
| Author's 46 mutants, rerun | All rc 1, each at its expected arm; the log matches the published one; control rc 0 with 127 arms |

The first three mutants are the ones the ruling names: fence length ignored, fence character ignored, markup not stripped. All three are killed.

## Prior findings

| Item | Status at this head | Evidence |
|---|---|---|
| R740-4 F1 (fence length and trailing text) | **Closed** at its cause: run length and character are tracked | The two 125 ms plants give rc 1 naming `FU_RTO_MS_C`; the arms are verbatim |
| R740-4 F2 (underscore emphasis) | **Closed** by the neutraliser, no boundary change | `_125 ms_`, `_5 minutes_` and `_five minutes_` give rc 1 with the right constant; the asterisk control still fails |
| R739-4 F1, F2 | **Closed**, same causes | Its plants give rc 1. Its six non-copies give rc 0 on a real page (`receipts/real_probes.log`). |
| R740-4 R1 (PR enumeration) | **Closed** | Removed from the live PR body (`receipts/pr_body_live.txt`) |
| R740-4 R2, R739-4 RES-1 (pointer scope) | **Retained as residue** R2 below | Pages unchanged under "no prose changes"; PR body updated |
| R740-4 S2, R739-4 S-1 (decimal and unit words) | **Closed** as expected-failure arms. Unitless rows have no arm, because the rule reads only rows with a unit. | `:918-935` |
| R740-4 S6, R739-4 S-2 (`usage ={`) | **Closed** | `usage = {` in the delta |
| R740-4 S7, R739-4 S-3 (shared parser) | **Closed** | `without_fences` calls the scanner; the mutant `style_rule_old_toggle` is killed |
| R740-4 S1, S3, S4, S5; R739-4 S-4, S-5, S-6 | **Retained as suggestions**, unchanged | Outside this ruling's scope |

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Robustness, Tests

**Artifact:** `scripts/check_docs.py:184` and `:198`.

**Authority:** CommonMark 0.31.2 §5.2 rules 2 and 3 (content offset, empty items), §5.3 (what may interrupt a paragraph), and the §4.5 sentence that a fence ends with its container. These are not in the ruling's lists.

**Evidence:** `receipts/forms_head.log`, `receipts/forms_db9ab221.log`, `receipts/fuzz_lists_*.log`. In my list grammar, with lazy lines made impossible, 1,178 sentinels out of about 756,000 escape per parser over 480,000 documents. The shortest samples show the forms below. I did not classify every one of the 1,178, so this list may not be complete.

| Form | Plant | Round 4 | Head | Cause |
|---|---|---|---|---|
| Marker and five spaces | `-     x`, `  ` + fence, `  y`, `A 375 ms watch.` | passes | passes | `:198` |
| Empty item, trailing tab | `-` + tab, `   ` + fence, blank, `A 375 ms watch.` | passes | passes | `:198` |
| Empty item, two trailing spaces | `-  `, `  ` + fence, blank, `A 375 ms watch.` | passes | passes | `:198` |
| Paragraph under an ended empty item | `*`, blank, `  Text`, `    ~~~`, blank, `   A 375 ms watch.` | passes | passes | No end-of-item rule for an empty item |
| Ordered marker not 1 after a paragraph | `Text`, `2. ` + fence, blank, `   A 375 ms watch.` | **finding** | **passes** | §5.3, needs paragraph tracking |
| Form-feed-only line in an item fence | `- ` + fence, `  x`, form feed, `  A 375 ms watch.` | **finding** | **passes** | `:184` |

**Impact:** a visible copy passes the gate in these unusual shapes. The last two are regressions of this delta. No page uses any form: the real-page comparison shows 0 differences. The forms are not in the ruling's lists, and the rule for such forms is to record them, so this is not a finding.

The author's statement that lazy continuation accounts for every divergence is true for the author's grammar, whose limit the handoff discloses. It does not extend to these shapes.

**Optional outcome:**
- At `:198`, use the marker plus one space when the item's content is blank or starts with five or more spaces. This closes the first three forms.
- At `:184`, use `line.strip(" ")`, because the line is already tab-expanded. This closes the form-feed form.
- Record the other two as expected-failure arms beside the lazy arm, because they need paragraph or empty-item tracking.

I tried the first two changes on a scratch copy (`receipts/s1_candidate.diff`):
- The self-test still passes with 127 arms, and the real tree still passes.
- The four forms now give findings (`receipts/s1_candidate_forms.log`).
- List-grammar escapes fall from 1,178 to 370 (`receipts/s1_candidate_fuzz_lists_*.log`). The shortest remaining samples are the two forms left to record, or variants of them. I did not classify all 370.

This is a trial only. No source was changed.

**Verification:** rerun `scripts/forms_r4_vs_head.py` and `scripts/fence_diff.py <checker> <repo> lists`. The closed forms must then give a finding, and the existing 127 arms must still pass.

### R1 - RESIDUE - Docs

**Artifact:** live PR body, `receipts/pr_body_live.txt`, the fuzz bullet and "Known limits".

**Evidence:** "The one divergence that hides text" and "Ten real-copy forms still pass" read as complete lists. S1 shows further forms. The measurements themselves stand.

**Exact fix:**
- "The fence scanner was fuzzed against a CommonMark parser over 600,000 documents built from a fixed list of fence, list and comment shapes. In that grammar, the one divergence that hides text is recorded as an expected failure below."
- "Ten recorded real-copy forms still pass the gate."

**Verification:** inspect the refreshed body.

### R2 - RESIDUE - Docs (retained from R740-4 R2, R739-4 RES-1)

**Artifact:** `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59`, `docs/README.md:48`.

**Evidence:** "`make docs` rules are `scripts/check_docs.py`" is narrower than the target, which also runs the diagram and source-evidence checks. The ruling forbids prose changes this round. I confirmed the author's point that my round-4 wording fails the page gate at 14 words.

**Exact fix, for when prose is next touched:** "`scripts/check_docs.py` holds these rules; [`selftest()`](../scripts/check_docs.py) cases specify them." This gives no style finding (run with a placeholder link target).

**Verification:** `make docs`.

### Carried suggestions (unchanged, not taken, outside this ruling)

| ID | Lenses | Item |
|---|---|---|
| S2 (R740-4 S1, R739-4 S-4) | Robustness, Docs | A coincident unrelated figure is reported as a copy. This errs on the safe side. |
| S3 (R740-4 S3) | Robustness, Tests, Docs | The second seeded image is not checked. |
| S4 (R740-4 S4, R739-4 S-5) | Tests | `make lint` takes `verilator` from `PATH`. A `VERILATOR ?=` variable would make the identity explicit. |
| S5 (R740-4 S5, R739-4 S-6) | Docs | `docs/history/v1/RESOURCE_DELTAS_2026_10.md:30` gives no WNS end value. |

The comment rule is met: the delta adds no lane label, lane name, review round, reviewer ID or issue-comment ID to source comments (search of `scripts/check_docs.py`). New comments and docstrings match the code they describe.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling items 1 to 3 and scope; §4.5 rules against two parsers; §6.2 underscore rule; ten forms against the lists; constants table unchanged | R740-5 delta; earlier clause coverage retained | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| RTL | CLEAN | Delta raw diff shows one file, `scripts/check_docs.py`, mode unchanged; no `hdl/`, generator or build input; contract and pinned lint pass | R740-5 dependency check; earlier coverage retained | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Robustness | CLEAN (S1 open as a suggestion) | Scanner state, list and comment paths, both markup views, differential runs, real-page comparison, two-head form comparison | R740-5 | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Tests | CLEAN | 127 arms; 78 copy-rule arms planted on real pages; 46 mutants rerun; ruling's three mutants; 10 expected-failure arms and their widened-rule receipt | R740-5; unchanged simulation coverage retained | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |
| Docs | CLEAN (R1, R2 residue) | No Markdown in the delta; live PR body; docstrings and comments; 14 current and 18 historical pages through the gate | R740-5; earlier page coverage retained | 9bd82bfb8739de2312da54a9a7b16fa596ec3a91 |

## Limits and pending manager duties

- **Independence.** I read the prior reports only after my diff pass and did not read any report from this round. The comment listing I used to find the ruling did show the first line of earlier reviews, and the required author packet names prior finding IDs.
- **Author packet.** All 39 fetched author-r5 files match the published manifest's SHA-256 (`receipts/author_r5_digests.txt`). I did not fetch the 32 parent logs. I read only `parent_gates.txt` and `parent_diff.txt`, whose digests match, so the parent results are author receipts.
- **Signatures.** Both the source commit and the evidence commit report `verified: false, unsigned` (`receipts/commit_signature.txt`). Content integrity is verified; signer identity is not.
- **Fuzz scope.** My grammars contain no blockquotes, which the scanner does not recognise. A copy in one is reported, which is the safe direction. HTML blocks and lazy lines are excluded from my grammars, because they are recorded arms.
- **Hosted evidence.** This head has 0 check runs and 0 commit statuses (`receipts/hosted_check_runs.txt`), so nothing hosted can be credited.
- **Not run.** Suites, the engine mutation arm, `make ooc`, full banks, parent gates and hardware. Physical calibration: NOT RUN. Field skips are not hardware proof.
- **Manager duties.** No manager source bank exists at this head and none is inferred. The manager owns the current-dev merge candidate, builder and native banks, hosted and act acceptance, parent gitlink and documentation re-pins (parent docs gates fail on any gitlink move until re-pinned, per the author's receipts), the ruling on S1, and the residue checklist.
- **Clone state.** No source fix, commit, push or GitHub write. Probes ran on copies under packet scratch. The clone has all 113 tracked blobs and modes equal to HEAD, index equal to HEAD, empty status including ignored files, and no submodule gitlinks (`receipts/clone_integrity.txt`).
- **Reproduction.** Run with the parsers from `receipts/parser_identity.txt` installed in a scratch environment: `scripts/fence_diff.py`, `scripts/plant_arms.py`, `scripts/real_pages_diff.py`, `scripts/forms_r4_vs_head.py`, `scripts/ten_forms_grep.py`, `scripts/real_probes.sh`. One lint log had private paths replaced by placeholders; no result changed.

R740-5 FINISHED
