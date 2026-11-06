[R787] NEGATIVE - exact head 212b7d6ec506489a4c371e1f214b89a58a60b21e

Round R787-1, issue #848, PR #849. Tree `7836fb527a84f46df4ea551a14e78d17b6937d29`, base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.

## Verdict

The product change is correct. The page no longer moves with a page's length, and all three acceptance criteria are met.

The verdict is NEGATIVE because of four open MINOR findings: three under `Tests`, one under `Docs`. Two of the `Tests` findings are control gaps created by this PR. The commit that trimmed the script to fit the 1000-line limit, `212b7d6e`, lost two kills that both the base script and the first head `f5ccb318` still have. That is the gap the third focus question asks about. All four are small, and a disposable edit (receipt `fix-feasibility.txt`) closes the three `Tests` findings inside the limit, at exactly 1000 lines.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R787-1-F1 | MINOR | Tests | Page needles are graded against the page plus the lane files, so a page regression passes |
| R787-1-F2 | MINOR | Tests | No control requires the audit page's own Inventory row any more |
| R787-1-F3 | MINOR | Tests | No control proves `--findings-dir` keeps every finding of a lane, or its statement |
| R787-1-F4 | MINOR | Docs | The page gives no route to a finding's line, and 7 rows cannot be found by searching |
| R787-1-F5 | RESIDUE | Docs | The module docstring says no line number reaches the page; 61 rows carry recorded ones |
| R787-1-S1 | SUGGESTION | Conformance, Robustness | 18 generated pages change their Evidence cell when 7 to 12 lines are added above the marker |

## The focus questions

### 1. Length-only edits against status, banner and page-set changes

Answered yes, with one narrow exception recorded as R787-1-S1. Each row below is the real `--check` command on a disposable clone of the head, once per page, for all 212 pages other than the audit page (`realtree-probes.txt`).

| Probe, per page | Result |
|---|---|
| One blank line added at the top | rc 0 on 212 of 212 |
| Added line in the middle | rc 0 on 212 of 212 |
| Added line at the end | rc 0 on 212 of 212 |
| First blank line removed | rc 0 on 212 of 212 |
| Blank lines removed from the first 60 lines | rc 0 on 212 of 212 |
| 20 blank lines added at the top | rc 0 on 194; rc 1 on 18 (see R787-1-S1) |
| Supersession banner added | rc 1 on 190; rc 0 on the 22 archive pages |
| Recorded status judgement | rc 1 on 190; rc 0 on the 22 archive pages |
| Page removed, from disk or from the index | rc 1 on 198; rc 2 on 14 |

- The archive rc 0 rows are correct: `status()` decides an archive page before any judgement or banner (`scripts/docs_inventory.py:434`).
- The 14 rc 2 rows are also correct: they are exactly the 14 pages holding a recorded finding, and removing one refuses with `names an untracked page`. That is still a failing gate.
- `robustness.txt` shows a page added, a finding added and a finding removed each failing the gate.

The purpose of the issue also holds. Two branches each lengthened a different page. At base the merge left the page stale (`STALE (2 lines differ)`). At head neither branch touched the page and `--check` gave rc 0.

Base and head pages compared cell by cell (`page-compare.txt`):

- all 213 Inventory rows are equal apart from the removed count;
- all 76 Findings rows are equal apart from the third cell;
- page counts by status and lane are equal;
- the only reworded prose is the `superseded` evidence cell, as the PR body says.

### 2. Traceability through `--findings-dir`

Yes for the output at this head (`page-compare.txt`, `findings-dir.txt`).

- All 76 Findings rows map to exactly one lane entry, and no lane entry lacks a row.
- 73 rows resolve to a line, and that line really starts the statement.
- 3 rows report `?` (D0-001, D0-033, D0-056). These are the same three rows that read `re-verify: quote not found` at base, so nothing was lost.

Two gaps remain around that output: no control protects its completeness (R787-1-F3), and a reader of the page is never told it exists (R787-1-F4).

### 3. Removed selftest arms and the re-pin

The arms leave a control gap (R787-1-F1, R787-1-F2). Of 37 of my own mutants, 30 are killed at head and 7 survive (`mutants.txt`):

| Surviving mutant | Base script | Assessment |
|---|---|---|
| R1 | killed | Regression at this head, R787-1-F1 |
| O1 | killed | Regression at this head, R787-1-F2 |
| W7, W8 | survive | Inherited, and this PR raises their importance, R787-1-F3 |
| O4, S6 | survive | Inherited and outside this delta |
| S9 | survive | Equivalent: a hand edit that breaks the status rule also differs from the render, so the gate fails either way |

The new arms are otherwise strong. The removed `line_count` arms have no remaining behaviour to guard, and both `not a copy` arms got stronger when they moved to rc 0. The 30 killed mutants include every one that restores a line number or a size to the page, that breaks the `Located` cell or the 8-cell status reader, or that drops a line from `--findings-dir`.

The re-pin is correct:

- the delta changes one digest line in `ci/image/command-table.json`;
- the new value is the exact `sha256` of `scripts/docs_inventory.py`, the same comparison `scripts/ci_command_table.py:219` makes;
- no other file holds the old digest;
- commits `aa3e2d85`, `acc10192` and `808602e0` each made the same one-line change, so this is the established method.

`ci/image/tool-inventory.json` still records an older table digest, but that was already stale at base and is the drift public Issue #838 tracks. It is not a defect of this PR.

### 4. The changed local runner and its departures

The departures do not weaken the evidence. I read the published runner, verifier and `not_run.json`.

- **Step list:** it comes from the workflow in the clone, and the verifier fails any `run:` step with neither rc 0 nor a stated reason. I counted 96 `run:` steps independently, matching the 72 run plus 24 not run. All 72 logs carry the exact head.
- **Shell:** no step names a `shell:`, so `bash -e` is what the hosted runner uses. Nothing uses `GITHUB_PATH`, and each `if:` is `always()`-style or depends on the hosted context.
- **Several calls on one clone:** a hosted job also shares one workspace across its steps, and `GITHUB_ENV` persists in a file between calls. Resuming trusts an existing rc file, but the scratch root is per-head and the verifier requires the head in each log's first line.
- **Interrupted `gate_28`:** no rc was recorded, so nothing was overwritten. It reran on a clean tree and does not read the delta.
- **`gate_25_0` in a unit:** rc 0 in the published log and unit receipt.
- **Integrity:** all 177 published evidence files match their manifest's published digest, and every job's tree-after file is clean.
- **Independence from the runner:** I re-ran directly, without that runner, the gates that read the four changed files. 11 gate commands pass (`independent-gates.txt`). `gen_toc.py` could not run here (see limits).

One real difference remains: `uses:` steps do not run locally, so the local job's submodule state differs from a hosted one. This delta touches no submodule, so it does not matter here.

## Findings

### R787-1-F1 - MINOR - Tests

**Title:** Page needles are graded against the page plus the lane files, so a page regression passes.

**Where:** `scripts/docs_inventory.py:761-765`, and the docstring at `scripts/docs_inventory.py:738`.

**Authority and evidence:** AGENTS.md section 6, `Tests`: each test can fail for the defect it claims to detect. To fit the line limit, `control()` now tests every needle with `text not in rendered + listed`. The docstring says only that a needle "may instead head a `--findings-dir` file", which is narrower than the code. The failure message still says `rendered page lacks`.

Mutant R1 makes the page's Findings row use `finding.source` instead of `source_of(finding)`, dropping `Copy of the D0-002 statement on README.md.` from the page. Result:

- killed at base;
- killed at the first head `f5ccb318`;
- survives at this head, because the same sentence is in the lane file (`mutants.txt`, `survivor-explained.txt`).

**Impact:** The page promises "It names the recording page" (`docs/DOCUMENTATION_AUDIT.md:458`), and that promise is no longer gated. Any later needle whose text also appears in a lane file inherits the same blindness. The PR body lists the changed arms but not this widening.

**Required outcome:** A needle meant for the page is graded against the page alone, and a needle meant for a lane file against the lane files alone. The docstring matches the code.

**Verification:** R1 is killed, the selftest stays green and the module stays within 1000 lines.

### R787-1-F2 - MINOR - Tests

**Title:** No control requires the audit page's own Inventory row any more.

**Where:** `selftest()` at `scripts/docs_inventory.py:901-971`. The check removed from the base script is at its line 965.

**Authority and evidence:** The third focus question, and AGENTS.md section 6, `Tests`. `population()` promises "the audit page itself" (`scripts/docs_inventory.py:238`), and #797 requires every document to be listed. The base check `the audit page's own row does not carry its own line count` also proved the row exists. Commit `212b7d6e` dropped its replacement, and HANDOFF gives the reason as "the added-line arms already fail if any row carries a count". That covers a count on the row, not the row's presence.

Mutant O1 drops that row from the Inventory table while the summary still counts it. Result:

- killed at base;
- killed at the first head, by `the audit page's own row carries no count`;
- survives at this head.

The real page does carry the row, so this is a control gap rather than a product defect.

**Impact:** A generator that lost the row would pass `--check` and `--selftest`, and the summary total would silently disagree with the table.

**Required outcome:** A control fails when the audit page's own Inventory row is missing.

**Verification:** O1 is killed. One needle on an existing arm does this with no extra line.

### R787-1-F3 - MINOR - Tests

**Title:** No control proves `--findings-dir` keeps every finding of a lane, or its statement.

**Where:** `write_findings` at `scripts/docs_inventory.py:610-629`, and its arms at `:852-855` and `:906-907`.

**Authority and evidence:** The second focus question. Mutant W7 keeps only the first finding of each lane, and W8 omits the `- Statement:` line. Both survive at head. No arm grades two entries in one lane, because the arm that lists `README.md` does not list `docs/guides/A.md`, and no arm grades the statement line.

Both gaps predate this PR, and the output at this head is complete. They are recorded as MINOR because this PR changed the risk. At base the committed page still carried each line, so a dropped lane entry was recoverable. At head this output is the only source of a line, and a dropped entry would be silent.

**Impact:** A regression could lose findings from the lanes' work lists with every gate green.

**Required outcome:** A control fails when a lane's second finding, or a finding's statement, is missing from the lane file.

**Verification:** W7 and W8 are killed. One combined needle does this (`fix-feasibility.txt`).

### R787-1-F4 - MINOR - Docs

**Title:** The page gives no route to a finding's line, and 7 rows cannot be found by searching.

**Where:** The Findings preamble at `scripts/docs_inventory.py:590-594`, rendered at `docs/DOCUMENTATION_AUDIT.md:452-463`.

**Authority and evidence:** AGENTS.md section 6, `Docs`: changed contracts are reflected in authoritative docs. #797 scope item 2 asks that a statement be fixed or flagged "with the exact file:line". The committed page used to give that line and now gives `on page`.

`--findings-dir` is named only inside the script, in its docstring, `--help` and selftest. No document names it. The page does not name it and does not define the new `Located` column.

For 7 of the 11 copy rows, the printed statement is on no single line of the page, because the copy is wrapped or marked up (`copy-spelling.txt`). For those rows a text search fails too, so the option is the only route, and a reader of the page cannot learn it exists.

**Impact:** A lane fixing one of those rows has lost information it had at base, with no pointer to where it went.

**Required outcome:** The page, or an authoritative document it links, says how to obtain a finding's line and what `Located` means. This changes the rendered page, so it is not RESIDUE.

**Verification:** `--check` rc 0 after `--write`, the page names the command, and the module stays within 1000 lines. My disposable edit for the `Tests` findings already reaches 1000, so this text must share an existing line.

### R787-1-F5 - RESIDUE - Docs

**Title:** The module docstring says no line number reaches the page; 61 rows carry recorded ones.

**Where:** `scripts/docs_inventory.py:42`.

**Evidence:** The sentence reads "No line count or number reaches the page", but 61 of 76 Findings rows carry recorded `line N` source citations (`page-compare.txt`), and the page says so itself ("Findings cite source lines at dev"). Those citations are recorded text pinned at `cited_at`, not computed values, so behaviour is correct and only the sentence overreaches.

**Exact fix:** Replace `No line count or number reaches the page (#848)` with `No computed line count or number reaches the page (#848)`. The line grows from 106 to 115 characters and the line count does not change. The digest re-pin follows any byte change to the file, so this rides with the fixes above.

### R787-1-S1 - SUGGESTION - Conformance, Robustness

**Title:** 18 generated pages change their Evidence cell when 7 to 12 lines are added above the marker.

**Where:** `BANNER_SCAN_LINES` at `scripts/docs_inventory.py:136`, used by `status()` at `:438-446`.

**Evidence:** With 20 blank lines added at the top, 18 pages gave rc 1 (`top20-explained.txt`). All 18 are generated pages. Their `GENERATED` marker leaves the 15-line window, so the Evidence cell falls from `generated by ...` or `generated page` to `no recorded contradiction`. The status stays `current`. The smallest shift that does this is 7 lines, and a one-line shift changes nothing on any page.

This is a fixed, documented position window rather than a count, it predates this PR, and these pages are do-not-hand-edit output. It is not the churn the issue describes. It is still an exception to a literal "not when a page's length changes", so the owner may want it noted alongside the retained-columns ruling.

**Optional outcome:** Record it with that ruling. No code change is needed.

## Prior public findings

None to resolve. I read the PR thread after my own pass: it holds two review-start notices and no review bodies or findings at this head.

## Comment rule

No new instance in the reviewed delta (`comment-rule-scan.txt`). 73 added source lines carry no label-like token, no em dash, and only the issue reference `#848`.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #848 acceptance and #797 scope against `scripts/docs_inventory.py:528-601`, `ci/image/command-table.json:13706`, `realtree-probes.txt`, `page-compare.txt`, `robustness.txt`. Retained columns not raised, per ruling. R787-1-S1 is a SUGGESTION. | R787-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| RTL | CLEAN | Inapplicable by artifact: `git diff --raw` of the delta names four files, none under `hdl/`, `tb/` or `syn/`, and changes no gitlink (`restore-verify.txt`). The script's column-index change is covered under Tests by mutants C1 and C2. | R787-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Robustness | CLEAN | `scripts/docs_inventory.py:637-683`, `:610-629`, with `robustness.txt`: page deleted, page emptied, old-format page, hand-written line number, hand-marked lost statement, escaped pipes keeping 8 cells, nested and empty `--findings-dir`. Per-page removal in `realtree-probes.txt`. | R787-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Tests | UNCLEAN | `scripts/docs_inventory.py:730-771`, `:843-971`, `mutants.txt`, `survivor-explained.txt`, `fix-feasibility.txt`, the executor's published `mutants.txt`. Open: R787-1-F1, R787-1-F2, R787-1-F3. | R787-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Docs | UNCLEAN | `docs/DOCUMENTATION_AUDIT.md:452-463`, `scripts/docs_inventory.py:4-48`, `.github/ci-templates/docs.yml:423-435`, PR body, `copy-spelling.txt`. Open: R787-1-F4. RESIDUE R787-1-F5 does not hold the lens open. | R787-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |

Any fix changes `scripts/docs_inventory.py`, which un-covers every lens whose scope includes it. Conformance, Robustness, Tests and Docs must therefore be covered again at the new head under AGENTS.md section 7.

## Real limits

- **`gen_toc.py`:** `--check` and `--verify-anchors` exited 2 here because the pinned renderer dependency is absent, so I did not verify them independently. The evidence for that gate is the executor's `gate_45` rc 0. The diff leaves the page's `Contents` section unchanged.
- **`ci_tool_inventory.py --check`:** not run, because the pinned parser is not available inside my allowed area. The digest was verified by direct comparison instead. #838 records that this checker already refuses at dev.
- **Not run, by assignment:** the local runner's host selftest, full banks, Docker and hardware. No manager source bank exists at this head, and I infer none.
- **Hosted state:** a snapshot during this round showed 30 pass, 25 pending and 1 skipping, with no failure; the docs jobs were among the passes (`hosted-snapshot.txt`). The manager owns hosted acceptance.
- **Mutants:** the 37 mutants are a chosen set, not an exhaustive one.
- **Published evidence:** 77 published files have redacted paths, so I verified their published digests, not their originals.
- **Probe clones:** they had no submodules initialised. The page is designed to render the same either way, and `--check` gave rc 0 on them unmodified.
- **Process disclosures:**
  - One filesystem-wide filename search ran outside my allowed area and listed file names, including under the management directory and other review packets. I stopped it, opened none of those files, and used none of them, including a parser binary it found.
  - My first probe command outlasted the foreground limit and finished detached with a complete receipt.
  - A loading script created an ignored bytecode directory in the clone, which I removed.
  - Exact head bytes, modes, index and gitlinks are verified in `restore-verify.txt`.

## Pending manager duties

- Publish this report and return R787-1-F1 to R787-1-F4 to the executor. Carry R787-1-F5 to the residue checklist if it is not fixed in the same change.
- Record the R787-1-S1 note with the retained-columns ruling if the owner wants it.
- Confirm #838 also covers the stale digest in `ci/image/tool-inventory.json`. The executor's handoff asks for a new Issue for it.
- Build the current-dev merge candidate, and own hosted and local-replica acceptance, at the merge turn.

R787-1 FINISHED
