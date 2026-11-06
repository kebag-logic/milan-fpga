[R787] NEGATIVE - exact head 91c115b576601139c53038440f0987412d5172e8

Round R787-2, issue #848, PR #849. Tree `1de81797082b66499a6ce277b90904039e12b1d7`, source base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. Previously reviewed head `212b7d6ec506489a4c371e1f214b89a58a60b21e`.

## Verdict

The product change is correct, and the round 2 fixes work. All three acceptance criteria hold, every prior mutant the ruling named is killed, the rejoined statements changed no behaviour, and the page's new text is true on the real tree.

The verdict is NEGATIVE because of two open MINOR findings, both under `Tests`. Neither is a defect in the output at this head. Both are controls that cannot see the defect they exist to catch.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R787-2-F1 | MINOR | Tests | The lane-file control joins every lane into one string, so it cannot see which lane a finding is filed under |
| R787-2-F2 | MINOR | Tests | `a banner past line 15 is not read` plants its banner on line 20, so windows of 16 to 19 pass it |
| R787-2-S1 | SUGGESTION | Conformance, Robustness | Retained R787-1-S1: 7 or more lines above the marker change a generated page's Evidence cell |
| R787-2-S2 | SUGGESTION | Tests | The route control pins three fragments of four sentences |
| R787-2-S3 | SUGGESTION | Tests | Lane-file fields are sampled on one entry, and the command's exit status is not read |
| R787-2-S4 | SUGGESTION | Robustness | A reused `--findings-dir` directory keeps a lane file from an earlier run |

Both MINOR findings close inside the limit. A disposable sketch changes six existing lines, stays at exactly 1000 lines with none over 120 columns, keeps the selftest green, and kills W11, W12, B01, B02, B03 and P04 (`receipts/fix_feasibility.txt`, `fix_feasibility.py`). It is evidence of feasibility, not a required design.

## Prior findings, at their cause

Read after my own pass over the diff. Each row was rerun at this head.

| Prior finding | State | Evidence at this head |
|---|---|---|
| R787-1-F1 = R788-1 F1, needle grading | RESOLVED | `scripts/docs_inventory.py:764` grades a needle on `listed` or `rendered`, never both, and `:738` says so. R1 is killed here, and survives at `212b7d6e` in the same campaign. X01 restores the old grading with the same defect and survives; X02 keeps the new grading and kills it. H02 shows lane needles really are graded on the lane text. |
| R787-1-F2, own Inventory row | RESOLVED | The arm `the audit page lists itself` at `:941`. O1 and O4 are killed. My own O03 (row hidden at render only) is killed by that arm alone. |
| R787-1-F3 = R788-1 F2, `--findings-dir` completeness | RETAINED IN PART | The named mutants are closed: W7, W8 and the source and correction droppers are all killed. The cause is not closed: the ruling asks for "every finding of a lane", and the control cannot see lanes. Carried as R787-2-F1. |
| R787-1-F4 = R788-1 F3, route to a line | RESOLVED | `docs/DOCUMENTATION_AUDIT.md:463-467` says what `Located` means, names the command and says how to reach a copy a search misses. All 7 rows a literal search misses are reached, and every named line is right (below). Control strength is R787-2-S2. |
| R787-1-F5 = R788-1 F4, docstring overclaim | RESOLVED | `:42` reads "No computed line count or number"; `:738` reads "the only output naming a finding's line". Both are true at this head. Fixed in the same edit, so nothing goes to #495. |
| R787-1-S1 | RETAINED | SUGGESTION, unchanged. The ruling is silent on it. See R787-2-S1. |

**Surviving mutants, one by one.** My published campaign of 37 was rerun unchanged (`receipts/r787_campaign_*.txt`). It reports the same seven survivors at `212b7d6e` as round 1, which shows the campaign is live, and one at this head.

| Mutant | base | `f5ccb318` | `212b7d6e` | this head |
|---|---|---|---|---|
| R1 | killed | killed | survived | killed |
| O1 | killed | killed | survived | killed |
| O4 | survived | killed | survived | killed |
| W7 | survived | survived | survived | killed |
| W8 | survived | survived | survived | killed |
| S6 | survived | survived | survived | killed |
| S9 | survived | survived | survived | survived, answered |

R788-1's other named survivors, by its published wording, are killed here: verified baseline (V02), correction cell (V03), a count reaching a heading-less purpose (V04), and the lane-file source and correction droppers (W05, W06).

**S9 is correctly answered as equivalent.** `broken` with `actual == expected` at `:673` needs a fresh render that marks current a page its own Findings table lists. `status_rule()` at `:456` prevents that for every page with a finding, so the branch cannot be reached while the generator keeps the rule. C04 (generator loses the rule) and C05 (loses it with S9 on top) are both killed.

The author's count of 16 rows, 12 distinct mutants and 11 killed agrees with these receipts.

## Focus checks

**The rejoined statements changed no behaviour.** Comparing the module's syntax trees with docstrings removed, 98 top-level names are identical between `212b7d6e` and this head. Only `control`, `copy_controls`, `render` and `selftest` differ (`receipts/ast_delta_round2.txt`). With layout normalised, the differences in those four are exactly the intended ones (`receipts/unparse_diff_round2.txt`):

- `render`: the four new sentences.
- `control`: the grader and its message.
- `copy_controls` and `selftest`: added needles, the new arms and the heading-less fixture page.

**Module limit and ratchet.** `scripts/docs_inventory.py` is 1000 lines. The gate fails only above 1000 (`scripts/check_py_idiom.py:355`). `scripts/py_idiom.budget` is unchanged, `long module` reads 10 <= 10 and `over-long line` reads 0 <= 0 (`receipts/gates_summary.txt`, `receipts/hygiene.txt`).

**Digest re-pin.** One line differs in `ci/image/command-table.json`. The new value `25dda680...` equals the `sha256` of the file at this head (`git diff --numstat` 1/1).

**Page delta.** Against `212b7d6e` the page gains exactly six lines, all in the Findings intro, and loses none. `scripts/docs_inventory.json` is unchanged. Audience, Purpose and Describes are unchanged, as ruled.

**The route on the real tree** (`receipts/real_tree_probe.txt`, `receipts/line_truth.txt`):

- 76 page rows match 76 lane entries one to one.
- 73 are located: 66 carry the statement literally on the named line, and 7 reach it through the generator's own normaliser. None is wrong.
- The 7 are the rows a literal search misses, as the ruling says.
- 3 report `?` (D0-001, D0-033, D0-056), the same 3 rows the page flags `re-verify`.

**Length independence, all 212 pages at once** (`receipts/real_tree_probe.txt`):

| Edit to every page | `--check` rc | Page lines moved |
|---|---:|---:|
| 1 line appended | 0 | 0 |
| 500 lines appended | 0 | 0 |
| 1 blank line prepended | 0 | 0 |
| 6 blank lines prepended | 0 | 0 |
| 7 blank lines prepended | 1 | 2 (Evidence only) |
| 20 blank lines prepended | 1 | 18 (Evidence only) |

**Gates run directly at this head** (`receipts/gates_summary.txt`, `receipts/hygiene.txt`), all rc 0: `docs_inventory.py --check` and `--selftest` (56 controls), `--check` on a tree with no Git metadata, `check_py_idiom.py` and its selftest, `check_doc_style.py`, `docs_check.py`, `check_hygiene.py`, `check_doc_paths.py`, `measure_fail_fast.py`, `measure_naming.py`, `measure_test_evidence.py`, `check_todo_ownership.py`, `ci_gate_workflows.py --check`, `ci_events.py --check` and `DOC_MAP.gen.py --check`. `gen_toc.py --check`, `gen_toc.py --verify-anchors` and `check_em_dash.py` gave rc 2 under the system interpreter because the pinned renderer was absent. All three passed in a private environment built from the hash-pinned `tools/markdown/requirements.txt`, so `gates_summary.txt` shows rc 2 for them and `hygiene.txt` shows the pass.

**Author evidence.** 10 sampled files from the published round 2 packet match the manifest's digests, and `head.txt` and the sampled log name the exact head (`receipts/evidence_spotcheck.txt`). The gate table reads 72 ran, 24 not run with a reason, 0 bad. I did not re-verify all 759 manifest rows.

**Comment rule.** No new instance. The 25 lines added since `212b7d6e` carry no bench lane label, review round, reviewer ID or comment ID, no em dash, and only the reference `#848` (`receipts/hygiene.txt`). All five commits are one line with no trailers.

## Findings

### R787-2-F1 - MINOR - Tests

**Title:** The lane-file control joins every lane into one string, so it cannot see which lane a finding is filed under.

**Where:** `scripts/docs_inventory.py:762` (`listed = "".join(...)`), the needles at `:854-856`, and the behaviour at `:619-620`.

**Authority and evidence:** The [A10] ruling's third item asks for a control that `--findings-dir` keeps "every finding of a lane". AGENTS.md section 6, `Tests`: a test must be able to fail for the defect it claims to detect. The delta's own page text promises "one file per lane" (`docs/DOCUMENTATION_AUDIT.md:464`), and the page says a finding's "area lane fixes it".

`control()` concatenates all lane files before grading, so every needle passes wherever the entry lands. Two mutants survive with `--selftest` rc 0:

- W11 files every finding under one lane.
- W12 files a copy under its recording page's lane, `lanes[finding.origin or finding.page]`. That is a plausible slip, because a copy row carries both pages.

Measured on the real tree (`receipts/lane_routing_probe.txt`), with `--check` rc 0 in both cases:

| Mutant | Lane files written | Entries in the wrong lane's file |
|---|---|---:|
| head | 5 | 0 of 76 |
| W12 | 2 (`overview-and-guides`, `reference`) | 11 of 76 |
| W11 | 1 | 76 of 76 |

Under W12, all 11 copy rows move, and the `archive`, `design` and `testing-and-ci` lanes lose their work lists entirely. Those 11 rows include all 7 that the ruling's fourth item is about.

**Why MINOR and not SUGGESTION:** R787-1-F3 was MINOR because this output became the only source of a finding's line. The same reasoning applies here with more force. The output is not committed, so `--check` cannot see it and no review diff shows it. The selftest is its only guard. R787-2-S2 is rated lower for exactly this reason: that text is committed, so `--check` and the review diff do see it.

**Why not `Conformance`:** the output at this head is correct and #848's frozen acceptance does not concern lanes, so this is a control gap, not a non-conformance.

**Impact:** A regression could send findings to the wrong lane, or leave a lane with no work list, with every gate green. A lane reading its own file would see nothing to fix.

**Required outcome:** A control fails when a finding is not in its own lane's file.

**Verification:** W11 and W12 are killed, the selftest stays green and the module stays within 1000 lines. In the disposable sketch, a needle that requires the copy's heading to follow straight after a lane file's header does this on an existing line, because a misfiled entry no longer opens the file.

### R787-2-F2 - MINOR - Tests

**Title:** `a banner past line 15 is not read` plants its banner on line 20, so windows of 16 to 19 pass it.

**Where:** `scripts/docs_inventory.py:947`, with the window at `:136` and `:438`.

**Authority and evidence:** AGENTS.md section 6, `Tests`: each new test can fail for the defect it claims to detect, and boundary behaviour is covered. This control is new in the reviewed delta. The commit subject of `2344d147` says it pins the banner window, and the PR body says it "pins the banner window".

The fixture page has 3 lines. `"\n" * 15` adds 15 more, and `banner` opens with its own newline, so the banner lands on line 20. A banner on line 16 is past line 15, and a window of 16 reads it, yet the control passes:

| `BANNER_SCAN_LINES` | Result |
|---|---|
| 5, 6 | killed |
| 14 | survived (B01) |
| 15 | the rule |
| 16 | survived (B02) |
| 19 | survived (B03) |
| 20, 21 | killed |

17 and 18 were not run; they lie between two survivors. This is not a regression: R787-1's S6 (window 10000) is killed, as the author says. It goes beyond the ruling's minimum, but it is new code that claims a boundary it does not test.

**Impact:** The window decides a page's status and Evidence cell. A drift of up to four lines passes `--selftest`, and the control's name tells a reader that cannot happen.

**Required outcome:** The control fails for a window of 16. Pinning the lower edge, a banner on line 15 being read, is welcome.

**Verification:** B02 and B03 are killed. The sketch does both edges by changing two numbers, with no added line: `"\n" * 11` on this arm, and `"\n" * 10 + banner` on the `supersession banner` arm. Renaming the arm alone would not meet this. If the fix changes the claim instead, the PR body line changes with it.

## Suggestions

**R787-2-S1 - Conformance, Robustness.** Retained R787-1-S1, reproduced at this head: 7 lines prepended moves 2 Evidence cells and 20 moves 18, from `generated by ...` or `generated page` to `no recorded contradiction`. Status stays `current`. The PR body records it. No code change is needed.

**R787-2-S2 - Tests - `scripts/docs_inventory.py:942`.** The new control pins `Located`, `--findings-dir DIR` and `search misses`, so these survive:

- P04: `That command still names its line.` is dropped. This is the sentence that answers the ruling's "how to reach".
- P05: the command loses its script path.
- P06: the sentence says `status` instead of `line`.
- P07: the sentence is negated.
- L07: the column header stops being `Located` while the intro still explains it.

This is a SUGGESTION because the text is a constant that reaches a committed page, so `--check` and the review diff both expose any change to it. The author's statement that three mutants drop the new text is true as written; the fourth sentence is the one with no mutant. Replacing `search misses` with `copy.\nThat` kills P03 and P04 together, at no line cost.

**R787-2-S3 - Tests - `scripts/docs_inventory.py:761`, `:854-856`.** Fields are pinned on one lane entry, D0-001. The loop at `:625-628` has no per-entry branch, so sampling is reasonable. These survive:

- W15: the first entry of a lane loses its statement.
- W18: a copy's entry loses its statement.
- W19: a lane entry loses `Copy of the ... statement`, the lane-side mirror of R1.
- W13 and W14: a lane file drops a baseline.
- W20: `--findings-dir` exits nonzero, because the rc of the `gate()` call at `:761` is discarded.

One needle on the copy's entry would close W18 and W19.

**R787-2-S4 - Robustness - `scripts/docs_inventory.py:617`.** `write_findings` never clears its directory, so a lane with no findings left keeps its old file in a reused `DIR` (`receipts/hygiene.txt`). The behaviour predates this PR, but the page now sends readers to this command. A note on the page or a fresh directory would avoid it.

## Wording to carry with the fix

If F2 is fixed by changing the control, no text changes. If it is answered any other way, the PR body line "`a banner past line 15 is not read` pins the banner window" must change to match. No RESIDUE item is open at this head.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #848 acceptance and the [A10] ruling against `scripts/docs_inventory.py:562-603`, `:471-498`, `docs/DOCUMENTATION_AUDIT.md:452-467`, `ci/image/command-table.json:13706`, `receipts/real_tree_probe.txt`, `receipts/line_truth.txt`. Audience, Purpose and Describes unchanged, as ruled. S1 is a SUGGESTION. | R787-2 | `91c115b576601139c53038440f0987412d5172e8` |
| RTL | CLEAN | Inapplicable by artifact: `git diff --raw 87e9d03a..91c115b5` names four files, none under `hdl/`, `tb/` or `syn/`, and no gitlink changes (`receipts/hygiene.txt`, `receipts/clone_integrity.txt`). | R787-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Robustness | CLEAN | Round 2 touches only the selftest and fixed page text, shown by `receipts/ast_delta_round2.txt`, so the round 1 verdict on `:637-683` and `:610-629` stands for code the delta leaves identical. Rechecked: `--check` with no Git metadata, reused `DIR`, the 3 unlocated rows, prepended and appended lines on all 212 pages. S1 and S4 are SUGGESTIONs. | R787-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Tests | UNCLEAN | `scripts/docs_inventory.py:731-771`, `:843-899`, `:902-972`, `receipts/mutants_head.txt` (62 mutants), `receipts/r787_campaign_*.txt` (37, on three script pairs), `receipts/lane_routing_probe.txt`, `receipts/fix_feasibility.txt`. Open: R787-2-F1, R787-2-F2. | R787-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md:452-467` against `receipts/line_truth.txt`, the docstring at `scripts/docs_inventory.py:4-48` and `:735-738`, `.github/ci-templates/docs.yml:423-433`, the PR body and `[A739b] REVIEW READY` against these receipts. The PR body's banner line is tied to F2, which is held under `Tests`. | R787-2 | `91c115b576601139c53038440f0987412d5172e8` |

The fix changes `scripts/docs_inventory.py`, which un-covers every lens whose scope includes it under AGENTS.md section 7. Conformance, Robustness, Tests and Docs must be covered again at the new head, and the digest re-pinned.

## Real limits

- **Mutants:** 62 of mine plus 37 published are a chosen set, not an exhaustive one. At this head my 62 give 42 killed and 20 survivors:
  - 16 sit under the findings: 2 under F1 (W11, W12), 3 under F2 (B01, B02, B03), 5 under S2 and 6 under S3.
  - C03 is S9, which is equivalent.
  - H01, H03 and X01 are harness and attribution mutants. They edit the grader, not the generator, so a green selftest is the expected result. X01 is the one that proves the old grading was blind.
- **Probe noise, corrected:** a first version of `real_tree_probe.py` reported 13 suspect lines. That was my own loose word match, not a defect. It was removed, the receipt regenerated, and `line_truth.py` makes the exact check: 0 wrong.
- **`ci_tool_inventory.py --check`:** not run, because the pinned parser is not available in my allowed area. The digest was checked by direct comparison instead.
- **Private environment:** `gen_toc.py` and `check_em_dash.py` ran from a disposable environment under my scratch directory, installed from the repository's hash-pinned requirements. Nothing shared was installed.
- **Not run, by assignment:** the full `docs.yml`, full banks, the local replica and its host selftest, Docker and hardware. No manager source bank exists at this head and I infer none. Physical calibration NOT RUN; field skips are not hardware proof.
- **Author evidence:** spot-checked by sample as stated. The builder gates `gate_25_0` and `gate_25_1` are author receipts only; I read their rc files and nothing in this delta feeds them.
- **Hosted state:** a read-only snapshot at 2026-11-06T20:26:19Z shows PR ready, not draft, with 1 check completed successfully, 1 in progress and 15 queued on this head, so this is not acceptance evidence (`receipts/hosted_snapshot.txt`). The manager owns hosted acceptance.
- **Probe clones:** they had no submodules initialised, and `--check` gave rc 0 on them unmodified.
- **Clone state:** the review clone is at the exact head with a clean tree, no ignored entries, index equal to tree, the four changed blobs and modes verified, and all six gitlinks present (`receipts/clone_integrity.txt`).

## Pending manager duties

- Publish this report and return R787-2-F1 and R787-2-F2 to the executor, with the suggestions for the same pass if wanted.
- Re-review at the new head. Both findings are in `scripts/docs_inventory.py`, so the digest needs re-pinning. The module has no headroom; the sketch shows a fix needs none.
- Record R787-2-S1 with the retained-columns ruling if the owner wants it.
- The stale digest in `ci/image/tool-inventory.json` stays with #838.
- Build the current-dev merge candidate, and own hosted and local-replica acceptance, at the merge turn.

R787-2 FINISHED
