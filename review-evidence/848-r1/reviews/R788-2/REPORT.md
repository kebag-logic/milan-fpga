[R788] NEGATIVE - exact head 91c115b576601139c53038440f0987412d5172e8

Round R788-2, external independent review of #848 / PR #849. Tree `1de81797082b66499a6ce277b90904039e12b1d7`, source base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. Previously reviewed head `212b7d6ec506489a4c371e1f214b89a58a60b21e`.

**Why negative:** the product is correct, and all three acceptance criteria of #848 hold on the real tree. Every named prior finding is fixed at its cause except one part of the lane-file control. Two MINOR findings stay open, both in selftest controls, and neither is a wrong output:

- **F1:** the lane-file control reads all lane files joined together, so a finding can leave its lane with `--selftest` green. On the real tree that mutant empties 3 of the 5 lane files.
- **F2:** the new arm `a banner past line 15 is not read` plants its banner on line 20, so windows of 16 to 19 lines pass it.

Both close inside the 1000-line limit. A disposable trial reached 1000 lines and 120 columns with the selftest green (`receipts/fix-trial.txt`).

## Findings

| ID | Severity | Lenses | Title |
|---|---|---|---|
| F1 | MINOR | Tests, Conformance | The lane-file control cannot see which lane a finding is filed in |
| F2 | MINOR | Tests | The banner-window arm does not test the boundary it names |
| S1 | SUGGESTION | Tests | The sentence that gives the route has no needle |
| S2 | SUGGESTION | Tests | Both baselines are required, but not in the right sentences |
| S3 | SUGGESTION | Tests | A lane entry's copy note and the lane file header are unpinned |
| S4 | SUGGESTION | Robustness | Reusing a `--findings-dir` DIR keeps a stale lane file |
| S5 | SUGGESTION | Conformance, Robustness | R787-1-S1 retained: the Evidence cell moves when a marker leaves the window |
| R1 | RESIDUE | Docs | The PR body says the banner arm pins the window |
| R2 | RESIDUE | Docs | The PR body's length exception says 18 pages at 7 lines |

### F1 - MINOR - Tests, Conformance - `scripts/docs_inventory.py:762`, `:764`, `:620`, needles at `:854-856`

**Title:** the lane-file control cannot see which lane a finding is filed in.

- **Authority:** the [A10] ruling, item R787-1-F3 = R788-1 F2: "add a control that `--findings-dir` keeps every finding of a lane and its statement". AGENTS.md section 6 `Tests`: each new test can fail for the defect it claims to detect. The new page sentence also says "one file per lane".
- **Evidence:** `control()` builds `listed` by joining every lane file, and every `## D0-` needle is graded on that join, so nothing observes which file holds an entry. Two mutants of `:620` survive with 56 controls OK (`receipts/mutants-head.tsv`):
  - W9 files a copy under its origin page's lane.
  - W8 writes every lane into one file.
- **Measured on the real tree** (`receipts/real-w8-w9.txt`): under W9 the `archive`, `design` and `testing-and-ci` lane files disappear and `reference` grows from 54 to 65 entries, so 11 findings leave their lanes. At this head the output is right: 76 entries, 0 misfiled (`receipts/real-tree.txt`).
- **Impact:** this is a lost-guard gap, not a wrong output. `--findings-dir` is now the only source of a finding's line, so a lane could lose its work list with every gate green. That is the risk R787-1-F3 raised. The gap is inherited, since no earlier head graded this either, but this round's control is what the ruling asked to close it.
- **Why Conformance too:** the three acceptance criteria in the issue body are met. The lens is recorded because the ruling's clause is met for "every finding" and not yet for "of a lane".
- **Required outcome:** a control fails when an entry is filed outside its page's lane, or when lanes merge into one file.
- **Verification:** W8 and W9 are killed, the selftest stays green, the module stays within 1000 lines and the digest is re-pinned. In the trial, one needle running from `# D0 findings: reference` through the `REQUIREMENTS.md` entry kills W8, W9, W13, W15, W16 and W17 (`scripts/fix_trial.py`).

### F2 - MINOR - Tests - `scripts/docs_inventory.py:947`, `:136`

**Title:** the banner-window arm does not test the boundary it names.

- **Authority:** AGENTS.md section 6 `Tests`. The page rule at `scripts/docs_inventory.py:546` says "A banner in the first 15 lines".
- **Evidence:** `docs/guides/B.md` has 3 lines, so `"\n" * 15 + banner` puts the banner on line 20, not 16. Windows of 16 and 19 survive, and 20 and 21 are killed. The lower edge is open too: a window of 14 survives, while 5 is killed by another arm (`receipts/mutants-head.tsv`, N14, N16, N19, N20).
- **Impact:** R787's S6 (a window of 10000) is killed, so the ruling's named survivor is answered. But this arm is new in the delta, and it claims more than it proves. A window off by up to 4 lines would misjudge a page's status with the selftest green.
- **Required outcome:** a banner on line 16 is not read, and a banner on line 15 is read.
- **Verification:** N14, N16 and N19 are killed. The trial changes `15` to `11` here and plants the `supersession banner` arm at `"\n" * 10`, with no added line.

### S1 - SUGGESTION - Tests - `scripts/docs_inventory.py:942`, `:595`

Commit `91c115b5` split one sentence in two, and the needle `search misses` covers only the first half. Mutant T4 drops "That command still names its line." and survives. The command stays one sentence above, so the route is still readable, which is why this is not MINOR. Optional outcome: add a needle such as `still names its line`.

### S2 - SUGGESTION - Tests - `scripts/docs_inventory.py:963`

R788-1's "verified baseline" survivor is killed. But the needles are ``at dev `1111111` `` and ``at dev `0000000` ``, so mutant B1, which swaps the two baselines between their sentences, survives. Optional outcome: needles naming each sentence, as in the trial.

### S3 - SUGGESTION - Tests - `scripts/docs_inventory.py:623-627`

Now that page and lane grading are separate, the copy note in a lane entry is not graded (W13), and neither are the three lane file header lines (W15, W16, W17). The F1 needle closes all four at no extra cost.

### S4 - SUGGESTION - Robustness - `scripts/docs_inventory.py:617-630`

`write_findings` never clears DIR. After a lane's last finding is removed, a rerun into the same DIR leaves that lane's old file in place (`receipts/stale-lane-probe.txt`). This predates the PR, but the page now sends readers to this command. Optional outcome: say to use an empty DIR, or remove lane files the run does not write.

### S5 - SUGGESTION - Conformance, Robustness - `scripts/docs_inventory.py:136`, `:438-446`

R787-1-S1 is retained. With blank lines prepended to every page (`receipts/acceptance-probe.txt`):

| Lines prepended | `--check` | Rows changed |
|---:|---:|---:|
| 1 | rc 0 | 0 |
| 6 | rc 0 | 0 |
| 7 | rc 1 | 2 |
| 15 | rc 1 | 18 |

Every changed row keeps status `current`. This is a fixed position window, the PR body now discloses it, and no action is required.

### R1 - RESIDUE - Docs - PR #849 body, "Added controls"

"`a banner past line 15 is not read` pins the banner window." overstates what the arm proves at this head.

**Exact fix, if F2 is not fixed first:** "`a banner past line 15 is not read` shows that a banner on line 20 is not read." Once F2 is fixed, the sentence is true as written.

### R2 - RESIDUE - Docs - PR #849 body, "Length exception"

"18 generated pages change their Evidence cell, not their status, if 7 or more lines are added above the marker." reads as all 18 changing at 7 lines. Measured: 2 at 7 lines and 18 at 15 lines.

**Exact fix:** "Up to 18 generated pages change their Evidence cell, not their status, as lines are added above the marker: 2 at 7 lines, all 18 at 15."

## Prior findings, each at its cause

| Prior finding | State | Evidence at this head |
|---|---|---|
| R787-1-F1 = R788-1 F1 | RESOLVED | `:764` grades a `## D0-` needle on lane text and every other needle on the page. P1 (page row loses its recording page) is killed. Restoring the old grading makes P1 survive again (P1+G0), so the grading is the cause. |
| R787-1-F2 | RESOLVED | `:941` requires the page's own row. O2 (row dropped but still counted) and O3 (row rendered from a short header) are killed by that arm alone. O1 is killed too. |
| R787-1-F3 = R788-1 F2 | PARTLY RESOLVED | A lane's second finding and every field are pinned: W1 to W5, W14, W18 and W19 are killed. Per-lane filing stays open as F1. |
| R787-1-F4 = R788-1 F3 | RESOLVED | The page defines `Located`, names the command and says a search misses a wrapped or marked-up copy (`docs/DOCUMENTATION_AUDIT.md:463-467`). I found the 7 rows independently, and each named line opens its statement. T1, T2, T3 and T5 are killed. T4 is S1. |
| R787-1-F5 = R788-1 F4 | RESOLVED | Both docstrings are fixed in the same edit (`:42`, `:738`), so nothing goes to #495. |
| R787-1-S1 | RETAINED | S5 above. No action required. |
| R788-1 surviving mutants (9) | 8 KILLED, 1 ANSWERED | Rerun with the published R788-1 runner: 1 of 32 survives (`receipts/r788-1-mutants-rerun.txt`). |
| S9, `check ignores the status rule` | ANSWER ACCEPTED | With the render intact `broken` cannot be non-empty when `actual == expected`, and a hand edit differs from the render. The rule-lost mutant is killed alone and with S9 on top (S9b, S9c). |

## Round 2 constraints

- **Rejoined statements changed no behaviour: confirmed.** AST comparison with docstrings removed covers 102 definitions, and only `control`, `copy_controls`, `render` and `selftest` differ (`receipts/gates-head.txt`). Arm by arm: 53 arms become 56, none is removed, 3 are added and 4 changed, each change adding a needle or moving to a stronger one (`receipts/arm-delta.txt`). `render` differs only by the new intro text: the page diff from `212b7d6e` is 6 added lines and no removed line.
- **Module limit: holds.** 1000 lines, and the gate fails only above 1000. `long module: 10 <= 10`. `scripts/py_idiom.budget` is not in the diff.
- **Command table digest: one line.** Numstat is 1/1 from both the base and `212b7d6e`, and the value equals the SHA-256 of `scripts/docs_inventory.py` (`25dda680...`).
- **Audience, Purpose and Describes:** unchanged, as ruled.
- **Comment rule:** no new instance in the delta. The only scan hit is the page text "Its area lane fixes it", which names no lane label.

## Acceptance on the real tree

All on a disposable clone of the head (`receipts/acceptance-probe.txt`).

| Edit | `--check` rc |
|---|---:|
| Unchanged head | 0 |
| One line appended to all 212 pages | 0 |
| 500 lines appended to all 212 pages | 0 |
| Supersession banner | 1 |
| Page added | 1 |
| Page removed | 1 |

A status change with no document edit is proved by the selftest arm `a status change alone makes the page stale`, which the R788-1 mutant `status count ignores the status` shows can fail. I did not repeat that edit on the real tree this round.

## Evidence checked

- **Gates rerun by me at this head** (`receipts/gates-head.txt`): `--check` rc 0, `--selftest` rc 0 with 56 controls, `check_py_idiom.py` rc 0 and its selftest 54 of 54, `check_doc_style.py` and its selftest OK, `docs_check.py` rc 0 across 213 pages.
- **Published packet at `66691a88`:** all 759 manifest rows match their published SHA-256, with none missing or unlisted (`receipts/evidence-check.txt`).
- **Author gates:** 72 step rc files are all 0, and the logs I sampled name this exact head. These remain author receipts.
- **Mutants:** 60 runs at this head, 45 killed. Of the 15 that passed, IDENTITY is the harness control, G0 and P1+G0 are the expected grading controls, and the other 12 are W8, W9, W13, W15, W16, W17, T4, B1, S9, N14, N16 and N19.
- **Fix trial:** on the trial copy every one of those 12 is killed except S9. The three G0 controls cannot apply there because the trial rewrites that line (`receipts/mutants-trial.tsv`).

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #848 acceptance and the [A10] ruling against `scripts/docs_inventory.py:528-603` and `docs/DOCUMENTATION_AUDIT.md:28-34`, `:452-468`; `receipts/acceptance-probe.txt`, `receipts/real-tree.txt`. The issue's three criteria are met; the lens is open only for the ruling's "of a lane" clause. | R788-2 | `91c115b576601139c53038440f0987412d5172e8` |
| RTL | CLEAN | Not applicable: `git diff --stat 87e9d03a..91c115b5` names `.github/ci-templates/docs.yml`, `ci/image/command-table.json`, `docs/DOCUMENTATION_AUDIT.md` and `scripts/docs_inventory.py`. None is under `hdl/`, `syn/` or `tb/`, and no gitlink changed (`receipts/clone-integrity.txt`). | R788-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Robustness | CLEAN | Non-test code outside `render` has an unchanged AST since `212b7d6e`, so the prior verdict stands there (`receipts/gates-head.txt`). Reprobed: `scripts/docs_inventory.py:612-631` and the unlocated and wrapped rows (`receipts/real-tree.txt`), stale DIR (`receipts/stale-lane-probe.txt`), top-of-page shifts (`receipts/acceptance-probe.txt`). S4 and S5 are suggestions. | R788-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Tests | UNCLEAN (F1, F2) | `scripts/docs_inventory.py:731-771`, `:843-972`; `receipts/mutants-head.tsv`, `receipts/mutants-212b7d6e.tsv`, `receipts/r788-1-mutants-rerun.txt`, `receipts/arm-delta.txt`, `receipts/arm-delta-base.txt`. | R788-2 | `91c115b576601139c53038440f0987412d5172e8` |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md:452-468`, `scripts/docs_inventory.py:37-43`, `:738`, PR body and REVIEW READY against measurements, `check_doc_style.py` and `docs_check.py` in `receipts/gates-head.txt`. R1 and R2 are residue and do not hold the lens open. | R788-2 | `91c115b576601139c53038440f0987412d5172e8` |

Any fix changes `scripts/docs_inventory.py`, so Conformance, Robustness, Tests and Docs must be covered again at the new head under AGENTS.md section 7.

## Real limits

- **Packet signature:** I was asked to verify a signed packet, but the evidence commit `66691a88` is unsigned on GitHub (`verified=false, reason=unsigned`). The check I made is manifest hash integrity, which does not prove who published it.
- **Not run here:**
  - `check_em_dash.py` (its pinned renderer is absent). As a substitute, the added Markdown lines carry 0 em dashes.
  - `ci_tool_inventory.py --check` refused with rc 2 because the pinned Bash parser is absent. I compared the digest directly instead.
  - `gen_toc.py`, the full `docs.yml`, the local replica and full banks. No hardware was used.
- **Calibration and banks:** physical calibration NOT RUN, and field skips are not hardware proof. There is no manager source bank at this head, and none is claimed.
- **Hosted state:** a read-only snapshot at 2026-11-06T20:28:52Z showed 15 runs queued, 1 in progress and 1 complete. It is not acceptance evidence (`receipts/hosted-snapshot.txt`).
- **Mutant coverage:** the mutants are a chosen set, not an exhaustive one.
- **Fix trial:** it proves the fixes fit and is not a prescribed design. It joined five opening lines to pay for the added lines. It ran only the selftest and a line and column check, not the full idiom gate.
- **Process disclosures:**
  - My first mutant run was invalid. A relative path stopped every mutant from launching, and the IDENTITY control exposed it. The harness was fixed and rerun, and it now counts a kill only when a named control fails. Only the valid run is published.
  - A non-isolated `ci_tool_inventory.py` run left an ignored `scripts/__pycache__` in the clone, which I removed.
- **Clone state:** exact head, tree, index, the four changed blobs and modes, and all six gitlinks are verified after the probes (`receipts/clone-integrity.txt`).

## Pending manager duties

- Route F1 and F2 to the author, then re-review at the new head. S1 to S3 close at little or no line cost if the author takes them in the same edit.
- Carry R1 and R2 to the residue checklist.
- Note that `scripts/docs_inventory.py` has no headroom, so any added needle must be paid for by a rejoined line.
- Own hosted and replica acceptance and the current-dev merge candidate.

R788-2 FINISHED
