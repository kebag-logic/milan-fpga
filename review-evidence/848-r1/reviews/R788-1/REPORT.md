[R788] NEGATIVE - exact head 212b7d6ec506489a4c371e1f214b89a58a60b21e

Round R788-1, external independent review of #848 / PR #849. Tree `7836fb527a84f46df4ea551a14e78d17b6937d29`, base `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.

**Why negative:** the feature works, and the three focus questions below hold on the real tree. One open MINOR stands under `Tests`. The change widened the selftest's needle match, and that removed a control base still had: a page copy row can now lose its recording page with `--selftest` green. It is a one-line fix that leaves the module at 999 lines (tried on a disposable copy, see F1).

## Focus answers

**1. Length-only edits against real changes: holds.** All probes ran on a disposable clone of the head (`receipts/real-tree-probes.txt`, `receipts/finding-probe-located.txt`).

| Edit | `--check` rc |
|---|---:|
| One line appended to all 212 pages | 0 |
| 500 lines appended to all 212 pages | 0 |
| Blank line above every recorded finding (14 pages) | 0 |
| Supersession banner | 1 |
| Status recorded as a judgement, no document edit | 1 |
| New tracked page | 1 |
| Page removed with `git rm` | 1 |
| Page deleted on disk only | 1 |
| Recorded quote removed from its page (D0-002) | 1 |
| Finding added to the data file | 1 |
| Hand edit of a `Located` cell | 1 |
| Hand edit marking a stale page current | 1 |

- An untracked new page stays rc 0, as designed.
- The same-named probe on D0-001 in the first receipt was vacuous, because that quote was already lost. D0-002 replaces it.
- Two branches that each lengthen a different page merge clean with `--check` rc 0 and do not touch the audit page. At base the same pair touches the page in both branches and the merged result is rc 1 (`receipts/merge-sim.txt`).

**2. Traceability through `--findings-dir`: holds on the real tree.**
- The 76 page rows match 76 lane entries one to one on (id, page), with no duplicates and nothing missing either way.
- All 73 named lines really carry their statement.
- The other 3 (D0-001, D0-033, D0-056) render `?`. They are the same 3 `re-verify: quote not found` rows base already had, so this delta did not cause them (`receipts/findings-trace.txt`, `receipts/page-semantic-diff.txt`).
- 7 rows are not literally greppable on their page, so for those rows `--findings-dir` is the only locator (see F3).

**3. Removed arms and the re-pin: arms not clean, re-pin clean.**
- `planted stale page: one added line` is inverted to rc 0. The stale direction is carried by the banner, status and page-set arms; the "check never stale" mutant is killed.
- `lines as wc -l counts them`, `an unterminated last line counts` and the own-row check went with `line_count()`, and nothing on the page reads that behaviour any more.
- The status-reader re-index (9 to 8 columns, index 5 to 4) is held by `hand-edited status hides a finding`; both mutants are killed.
- Six line arms moved to lane-file headings and are killed on the head, where base had no lane-file control at all. That is a real gain.
- The gap is the widening itself, F1.
- Re-pin: `numstat` is 1/1, and the digest equals the head blob's SHA-256 (`f502dac7...`). The table round-trips through the canonical serializer. Eight earlier `docs_inventory.py` changes used the same 1/1 shape with `tool-inventory.json` untouched, so this is the established method (`receipts/digest-and-modlimit.txt`).

## Findings

### F1 - MINOR - Tests - `scripts/docs_inventory.py:764`, with `:738` and `:853-854` - the needle widening removed the page-side control for a copy row's recording page

- **Authority/evidence:** AGENTS.md section 6 `Tests`: each test can fail for the defect it claims to detect. `control()` now tests `if text not in rendered + listed`. Its docstring says a needle "may instead head a `--findings-dir` file", but the code accepts any needle anywhere in the lane text. The needle ``Copy of the D0-002 statement on `README.md`.`` is also written by `write_findings` under `- Contradicted by:`. It is the only one of the 53 needles in both outputs, and 6 more are lane-only as intended (`receipts/needle-sources.txt`).
- **Measured:** planting `cell(finding.source)` for `cell(source_of(finding))` at `:598`: base kills it (`rendered page lacks 'Copy of the D0-002 statement...'`), head SURVIVES with 53 controls OK (`receipts/mutants.txt`).
- **Impact:** the page still promises "It names the recording page." (`:592`), but a generator that drops that from copy rows now passes `--selftest`. The 11 real copy rows are the ones affected. The committed page is correct today, so this is a lost guard and not a wrong output. The author's 13 mutants hold no mutant for this duty, so their all-killed result could not show it.
- **Required outcome:** a page needle must be satisfied by the page, and only a lane-file needle by the lane text. Keeping `rendered page lacks` accurate for lane needles is welcome but optional.
- **Verification:** the planted mutant is killed at the fixed head, the selftest stays green and the module stays within its limit. Trial on a disposable copy: `if text not in (listed if text.startswith("## ") else rendered):` gives 53 controls OK and 999 lines, and kills the mutant (`receipts/fix-feasibility.txt`). The digest needs re-pinning afterwards.

### F2 - SUGGESTION - Tests - `scripts/docs_inventory.py:623-626` - no control pins lane-file completeness

- `--findings-dir` is now the only output naming a finding's line. A mutant keeping only each lane's first finding survives, as do mutants dropping the Statement, Contradicted by or Correction line.
- All four also survive at base, so this is not a regression, and the real tree is complete (focus 2).
- Optional outcome: add the D0-001 heading needle to the copy arm, plus one field needle.

### F3 - SUGGESTION - Docs - `scripts/docs_inventory.py:590-594` - the page does not say where a finding's line now lives

- A search of `docs/`, `CONTRIBUTING.md`, `AGENTS.md` and `.github/` finds no mention of `--findings-dir`; it appears only in the script. A reader of the Findings table has no pointer, and 7 rows cannot be found by searching for their statement.
- Optional outcome: one sentence in the rendered Findings intro. This changes the generated page, so it is not residue.

### F4 - RESIDUE - `scripts/docs_inventory.py:42-43`, `:738` - the docstrings overclaim

- "No line count or number reaches the page" and "the only output naming a line" are literally false: 32 page lines carry recorded citations such as `line 4097` in `Contradicted by`. Those are static data pinned at `cited_at`, they do not move with a page, and the behaviour is correct.
- **Exact fix at `:42`:** "No line count, and no line number of an inventoried page, is computed onto the page (#848)".
- **Exact fix at `:738`:** "the only output naming a finding's line".

## Prior public findings

None to resolve. At this head PR #849 carries only the two review-start comments, and the Issue carries the author's TAKEN and REVIEW READY. I did not read any other reviewer's report.

## Author evidence and the listed departures

**Judgement: the departures do not weaken the evidence for this delta.**
- All 177 manifest rows match their published hashes (`receipts/evidence-check.txt`).
- All 96 `run:` steps are accounted for (72 ran, 24 not run with a stated reason). Every rc is 0, and every log header names the exact head. All 8 tree-after records are clean; the no-Git job strips its metadata and has none.
- Resuming across calls on one clone matches a hosted job's single workspace. An `.rc` file is written only when a step completes, so the interrupted `gate_28` could not inherit a result; it reran to rc 0.
- The runner's `bash -e` matches the hosted default, because the workflow names no shell.
- Of the expression-valued step env entries the runner drops, only `gate_8` executed with any, and the runner supplies those three itself.
- `gate_25_0` ran in a user unit and is a builder gate; nothing in this delta feeds it.
- I reproduced the gates that read this delta: `--check` (also on a no-Git tree), `--selftest`, the Python idiom gate, workflow generation, the archive gate and the style gate (`receipts/gates-local.txt`, `receipts/digest-and-modlimit.txt`).
- These remain author receipts only: `gen_toc` (its renderer is absent here) and gates 41, 42 and 51.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #848 acceptance and #797 column rule against `docs/DOCUMENTATION_AUDIT.md` and `scripts/docs_inventory.py:528-601`. Page delta maps fully to the intended columns plus one rule cell (`receipts/page-semantic-diff.txt`). Audience, Purpose and Describes stay by ruling | R788-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| RTL | CLEAN | Not applicable: `git diff --stat` names four files and none is under `hdl/`, `syn/` or `tb/`. The one `ci/image/command-table.json` line is a script digest read by no RTL flow | R788-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Robustness | CLEAN | Refusal arms, no-Git and checked-out-submodule trees, hand edits, `:596` and `:624` lost-quote paths, 15-line window sweep over 212 pages (`receipts/window-sweep.txt`, `receipts/gates-local.txt`) | R788-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Tests | UNCLEAN (F1) | `scripts/docs_inventory.py:730-971`, 32 mutants on head and base, needle classification (`receipts/mutants.txt`, `receipts/needle-sources.txt`) | R788-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Docs | CLEAN | Docstring `:37-43`, `.github/ci-templates/docs.yml:423-433`, repository search for stale audit line-count claims, PR body against measurements. F3 is optional, F4 is residue. New comments carry no lane, round, reviewer or comment IDs | R788-1 | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |

Mutants: 9 of 32 survive on the head.
- 1 is F1, the only regression.
- 4 are F2.
- 4 are the same at base and out of scope: the verified baseline line, the correction cell, a line count reaching a heading-less page's purpose, and the status-rule branch that is unreachable while the render keeps the rule.

## Real limits

- A pure blank-line edit moves a derived cell in one measured case: 20 lines inserted above the marker of 18 generated pages push it past the 15-line window, and the Evidence cell changes. 1 to 5 lines at the top move nothing. No page currently takes its audience from its own line, and none is superseded. This follows the stated window rule, it is not a line number, and generated pages are not hand-edited, so it is an observation and not a finding.
- Not run: the full `docs.yml`, the replica runner, full banks, any hardware. Physical calibration NOT RUN; field skips are not hardware proof. There is no manager source bank at this head, and none is claimed.
- Hosted snapshot at 2026-11-06T17:32:25Z, read only: 25 success, 28 still running or queued, 1 skipped (`Physical gPTP`, nightly and manual). This is not acceptance evidence (`receipts/hosted-snapshot.txt`).
- The review clone is restored and verified: tree, index, the four changed blobs and modes, and all six gitlinks (`receipts/clone-integrity.txt`).

## Pending manager duties

- Route F1 to the author, then re-review at the new head. `Tests` must be re-covered, and any lens whose scope the fix touches must be re-covered too. The fix changes the script, so the digest must be re-pinned.
- Carry F4 to the residue checklist.
- Open the Issue the author asked for. The drift is wider than their note says: 85 `tool-inventory.json` inputs are stale, and 37 of 147 commit-readable command-table digests mismatch. Both counts are identical at base and head, and `scripts/docs_inventory.py` is not among them, so this delta adds none.
- Own hosted and replica acceptance and the current-dev merge candidate.
- `scripts/docs_inventory.py` has one line of headroom under the module limit. The trial F1 fix adds none.

R788-1 FINISHED
