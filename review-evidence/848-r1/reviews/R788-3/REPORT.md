[R788] POSITIVE - exact head 171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22

Round R788-3, external independent review of #848 / PR #849. Tree `9d8daa835aa16f477d3af405fa2bb1b1ec0d5883`, live dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`, previously reviewed head `91c115b576601139c53038440f0987412d5172e8`.

**Why positive:** both items of the round 3 ruling (issuecomment-6694897633) are met at their cause, and no BLOCKER, MAJOR or MINOR is open.

- A control fails when an entry leaves its lane or when lanes merge. W8, W9, W11 and W12 are killed.
- A banner on line 15 is read and one on line 16 is not. N14, N16 and N19 are killed.
- The module is 1000 lines, the ratchet is unchanged, the digest is re-pinned and dev `3f6bef88` is merged cleanly.

**What this verdict does not cover:** `gate_25_0` is not proved at this head. The author's attempt ended rc 124 at a 585 s step limit with no gate verdict, and I did not run it. #848's third acceptance clause ("the docs gates pass") stays open on that one step until the manager's replay or the hosted run closes it. This is a pending duty, not a finding.

## Findings

No BLOCKER, MAJOR or MINOR.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| S1 | SUGGESTION | Tests | The lane needles bind two lanes and have no tail, so a duplicate past the needle or a third file passes |
| S2 | SUGGESTION | Tests | The audience scan shares the window constant, but its own boundary is unpinned |
| S3 | SUGGESTION | Tests | Retained: R788-2 S1, the route's closing sentence has no needle (T4) |
| S4 | SUGGESTION | Tests | Retained: R788-2 S2, the page's two baselines can swap (B1) |
| S5 | SUGGESTION | Tests | Retained: R787-2-S3 remainder, the `--findings-dir` exit status is not read (W20) |
| S6 | SUGGESTION | Robustness | Retained: R788-2 S4, a reused DIR keeps a stale lane file |
| S7 | SUGGESTION | Conformance, Robustness | Retained: R788-2 S5, the Evidence cell moves when a marker leaves the window |
| R1 | RESIDUE | Docs | The PR body states the lane arm's reach more widely than it proves |

### S1 - SUGGESTION - Tests - `scripts/docs_inventory.py:854-858`, `:762`

- **Authority:** AGENTS.md section 6 `Tests`, and the ruling's sentence "a control fails when an entry is filed outside its page's lane".
- **Evidence:** every plausible slip of the one-line group-by at `:620` is killed: L01 to L06 and L09. Four other mutants survive (`receipts/mutants-matrix.tsv`):
  - L07 and L10 keep each entry in its own lane and also file one after the point where the needle ends. The reference needle stops at `Contradicted by: Copy`, and neither needle binds a file's end.
  - L11 files an archive page's entry under `overview and guides`. The arm at `:873-876` keeps an unanchored `## D0-` needle, and only two lanes are bound.
  - L08 writes a third file holding every entry.
- **Why not MINOR:** L07, L10 and L11 each need a branch that names a fixture page or a lane, which is not a slip of a generic group-by, and no finite fixture can exhaust such branches. L08 leaves every entry in its own lane too. The named mutants are the ruling's stated test, and all are killed. On the real tree 76 entries sit in 5 lane files, 0 misfiled (`receipts/probes.txt`).
- **Also unpinned:** the lane file's name. L14 renames each file, and L12 uses the first letter as the name. The fixture's two lanes cannot collide under L12. The 5 real lanes do not collide either, though `reference` and `repository contract` would if both had findings.
- **Optional outcome:** end each file with a marker as well, for example `"\0" + text + "\0"` at `:762`, and let the needles close on it; pin the file count. The module has no headroom, so a line must be paid for.

### S2 - SUGGESTION - Tests - `scripts/docs_inventory.py:265`, `:136`

`audience_of` reads the same `BANNER_SCAN_LINES` window, and its fixture line is on line 3. B37 and B38 move only that site by one line, and both survive at this head and at `91c115b5`. This predates the delta and is outside the ruling, which names the banner. The banner sites are fully pinned: B31 and B32 move only the status window, and both are killed. Optional outcome: one Audience arm on line 15 and one on line 16.

### S3 to S7 - SUGGESTION - retained from earlier rounds

Each stays as filed in R788-2 and R787-2. The ruling kept suggestions out unless the same edit covered them.

- **S3:** T4 survives at this head.
- **S4:** B1 survives at this head.
- **S5:** L20, which makes `--findings-dir` exit non-zero, survives because `:761` ignores the return code. This is R787's W20.
- **S6 and S7:** the product AST is unchanged since `91c115b5`, so both stand as measured there. S7 needs no action.

### R1 - RESIDUE - Docs - PR #849 body, "Added controls", line 40

"An entry filed outside its lane, or lanes merged into one file, fails it." reads as covering every lane and every extra filing. S1 shows the arm binds the two lanes it plants, and only as far as each needle runs.

**Exact fix:** "Moving an entry of either planted lane out of it, or merging those lanes into one file, fails it."

## Prior findings, each at its cause

| Prior finding | State | Evidence at this head |
|---|---|---|
| R788-2 F1 = R787-2-F1, lane control | RESOLVED | `:762` marks each file's start with NUL and `:764` routes those needles to the lane text. `:854-858` require each lane file to open with its own title and baselines, then its own entries. L01 = W8 = W11, L03 = W9 = W12 and L04 (merged, titled sections kept) survive at `91c115b5` and are killed here, each by the copy arm. |
| R788-2 F2 = R787-2-F2, banner window | RESOLVED | Computed from the fixture text: `"\n" * 10 + banner` lands on line 15 and `"\n" * 11 + banner` on line 16 (`receipts/probes.txt`). Windows of 14, 16, 17, 18 and 19 survive at `91c115b5` and are killed here. On the real tree a banner over line 15 of `docs/testing/CI_WORKFLOWS.md` gave rc 1, and over line 16 gave rc 0. |
| R788-2 S1 | RETAINED | S3 above. |
| R788-2 S2 | RETAINED | S4 above. The lane file's own baselines are now pinned: L17 is killed. |
| R788-2 S3 | RESOLVED | The copy note (L19) and the lane header (L15, L16, L17) survive at `91c115b5` and are killed here. |
| R788-2 S4 = R787-2-S4 | RETAINED | S6 above. |
| R788-2 S5 = R787-2-S1 | RETAINED | S7 above. |
| R787-2-S2 | RETAINED | Same route needles as R788-2 S1: S3 above. |
| R787-2-S3 | RESOLVED IN PART | Lane fields are bound by the same needles. W20 stays as S5 above. |
| R788-2 R1 | RESOLVED | The arm now plants on line 16, and the PR body names both arms, so "pin both edges" is true. |
| R788-2 R2 | RESOLVED | PR body line 114 carries the exact fix. |
| Earlier-round findings | UNCHANGED | Banked as resolved at `91c115b5`. Only three selftest definitions changed since, and the 56 arms lost no needle. |

## The round 3 constraints

- **Delta shape:** AST comparison with `91c115b5` shows only `control`, `copy_controls` and `selftest` changed, with no name added or removed.
- **Arms:** 56 before and after. One is renamed (`supersession banner` becomes `a supersession banner on line 15 is read`, planted lower) and two others change. I read each by eye: the old `## D0-` needles of the copy arm are subsumed by the anchored ones, and the line-16 arm is tighter. Nothing weakened. The renamed arm's old banner position stays covered by `a line added above a banner`.
- **Module limit:** 1000 lines. `long module: 10 <= 10`, `over-long line: 0 <= 0`, and `scripts/py_idiom.budget` has no diff from base or dev.
- **Digest:** the table's `scripts/docs_inventory.py` entry equals the file's SHA-256, `092505ae...`. The diff against dev is that one line.
- **Audit page:** byte-identical to `91c115b5`. `--write` on a disposable clone left the tree clean, so no regenerate commit was needed.
- **Dev merge:** `d8a6cfb3` has parents `91c115b5` and `3f6bef88`. Head differs from dev in the PR's four files only, and no gitlink differs. The merge's first-parent change list equals dev's own list, less the audit page (`receipts/merge-and-scope.txt`). Dev is still at `3f6bef88`.
- **Comment rule:** no new instance. A scan of added lines in the script and template for lane labels, reviewer IDs, round numbers and comment IDs found none.
- **Commit form:** `171fd56b` is one line with no trailer.

## Evidence checked

- **Gates rerun at this head** (`receipts/gates.txt`):
  - `docs_inventory.py --check` rc 0.
  - `--selftest` rc 0, 56 controls.
  - `check_py_idiom.py` rc 0, and its selftest 54 of 54.
  - `check_doc_style.py` and its selftest OK.
  - `docs_check.py` rc 0 across 213 pages.
  - `git diff --check` rc 0 from dev.
- **Mutants:** 37 runs at this head, 25 killed and 12 passed. The 12 are IDENTITY (the harness control), L07, L08, L10, L11, L12, L14 (S1), B37, B38 (S2), T4, B1 and L20 (S3 to S5). The same set at `91c115b5` shows the change is what kills them. Every mutant applied exactly once.
- **Real tree** (`receipts/probes.txt`): a line appended to every tracked page gave rc 0, and lane filing is as stated under S1.
- **Author packet at `9014f7e7`:** all 1008 manifest rows match, with none missing or unlisted (`receipts/evidence-check.txt`). Spot checks:
  - All 72 docs.yml step logs name the exact head on their first line.
  - The table reads 72 ran, 24 not run, 1 bad, which is `gate_25_0`.
  - `ruling-mutants.txt` and the W11, W12 and B01 to B03 rows of the R787 rerun match what I measured.
  - The `gate_25_0` attempt receipt and `HANDOFF.md` agree with the REVIEW READY comment.

These remain author receipts.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling issuecomment-6694897633 and #848 acceptance against `scripts/docs_inventory.py:762-764`, `:854-858`, `:945-947`, `:136`; `receipts/mutants-matrix.tsv`, `receipts/probes.txt`, `receipts/merge-and-scope.txt`. Limit: the "docs gates pass" clause rests on `gate_25_0`, which is pending. | R788-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| RTL | CLEAN | Not applicable: `receipts/merge-and-scope.txt` shows head differs from dev only in `.github/ci-templates/docs.yml`, `ci/image/command-table.json`, `docs/DOCUMENTATION_AUDIT.md` and `scripts/docs_inventory.py`, with 0 gitlink changes. The RTL in `87e9d03a..171fd56b` is dev's own, byte-identical to dev. | R788-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Robustness | CLEAN | Product AST unchanged since `91c115b5` (`receipts/probes.txt`), so the prior verdict stands there. Reprobed: the NUL marker at `:762-764` (needles stay within one file, and glob order cannot matter because they are substring tests), the real banner boundary, and real lane filing. S6 and S7 are suggestions. | R788-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Tests | CLEAN | `scripts/docs_inventory.py:731-771`, `:843-972`; `receipts/mutants-171fd56b.tsv`, `receipts/mutants-91c115b5.tsv`, arm comparison in `receipts/probes.txt`; author `ruling-mutants.txt`, `mutants-r787-2.txt`. S1 to S5 are suggestions. | R788-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Docs | CLEAN | `scripts/docs_inventory.py:738` against the behaviour at `:762-764`; `docs/DOCUMENTATION_AUDIT.md`, byte-identical to `91c115b5`; `check_doc_style.py` and `docs_check.py` in `receipts/gates.txt`; PR body, REVIEW READY and `HANDOFF.md` against measurements. R1 is residue and does not hold the lens open. | R788-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |

## Real limits

- **`gate_25_0`:** not run by me, and rc 124 is not a verdict either way. The only supporting fact I add is a text search: 0 files under `sw/` or `tests/` name `docs_inventory`, `DOCUMENTATION_AUDIT` or `command-table`. That is not a trace of what the gate reads.
- **Hosted state:** a read-only snapshot at 2026-11-06T21:44:54Z shows all exact-head runs queued or pending, with no completed job (`receipts/hosted-snapshot.txt`). It is not acceptance evidence.
- **Packet signature:** I was asked to verify a signed packet, but evidence commit `9014f7e7` is unsigned on GitHub (`verified=false`). What I checked is manifest hash integrity, which does not prove who published it.
- **Not run here:**
  - `gen_toc.py` refused with rc 2: its pinned renderer is absent.
  - `ci_tool_inventory.py --check` refused with rc 2: the pinned Bash parser is absent. I compared the digest directly instead.
  - `check_em_dash.py`, the full `docs.yml`, the local replica and full banks. No hardware was used.
- **Command-table drift:** beyond the one entry this PR owns, 37 of 147 path-keyed digests differ from their files. The set is identical at dev and at head, so this PR neither causes nor changes it (`receipts/table-digests.txt`).
- **Calibration and banks:** physical calibration NOT RUN, and field skips are not hardware proof. There is no manager source bank at this head, and none is claimed.
- **Mutant coverage:** the mutants are a chosen set, not an exhaustive one. I reran my own set and spot-checked the author's receipts; I did not rerun the earlier reviewers' full campaigns.
- **Process disclosure:** the first gate pass ran on a clone without submodules, so `check_py_idiom.py` refused there with rc 2. `receipts/gates.txt` shows that refusal and the rerun in the review clone, whose required submodules are initialised.
- **Clone state:** exact head, tree, index, blob bytes and modes, and the six gitlinks are verified after the probes, with 0 changed or ignored paths (`receipts/clone-integrity.txt`). Three submodules are not initialised there, and I made no submodule change.

## Pending manager duties

- Close `gate_25_0` through the act replay or the exact-head hosted run, and record it against #848's third acceptance clause. The author's decision request in `HANDOFF.md` is still unanswered.
- Own hosted and replica acceptance and the current-dev merge candidate.
- Obtain the second required positive review. This verdict is one of two.
- Carry R1 to the residue checklist.
- Confirm that #838 covers the `ci/image/tool-inventory.json` drift and the wider digest measure above, as the author asks.
- Note that `scripts/docs_inventory.py` has no headroom, so any added needle must be paid for by a rejoined line.

R788-3 FINISHED
