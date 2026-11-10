[R804] POSITIVE - exact head 9405010ff5def3275eecda7271a4b1ccc1aa2be0

# External independent review R804-5: issue #854 / PR #862 (second dev-sync delta)

Scope: this is a delta review of merge commit `9405010f`. Its first parent is `b5d17214`, which R803-4 reviews. Its second parent is live dev `45c0b56c` (PR #835). The tree is `482cd44164d18a3f27306dc8bb2cd04478ac5062`. I reconstructed the task in a cleared context from AGENTS.md, the issue #854 body, the round 3 ruling (issuecomment-6743871886), the two PR #862 sync notes (6759682744, 6760255365 and its correction 6760258197), the diff and its history, and the published evidence tree. Under the maintainer decision of 2026-11-10 (a delta with no behaviour change gets one reviewer), R803-3 and R804-3, both POSITIVE at `a853461d`, stand for every artifact that this delta and the `b5d17214` sync do not touch.

**Verdict: POSITIVE.** This delta has no BLOCKER, MAJOR or MINOR finding. It has one RESIDUE (R804-5-R1, a stale head in the PR body) and one optional SUGGESTION (R804-5-S1). All five lenses are covered clean at `9405010f`.

## The three requested checks

### (1) The delta equals dev's #835 step, except `docs/findings/README.md`

Receipt: `receipts/delta_compare.txt`, produced by `scripts/delta_compare.sh`.

- **Range note.** The brief names the range `ac0a01e3..45c0b56c`. Literally, that range spans 271 files, because it holds two dev steps: #825 (`ac0a01e3..123f57a9`) and #835 (`123f57a9..45c0b56c`). `b5d17214` already absorbed #825, and `merge-base(b5d17214, 45c0b56c) = 123f57a9`. So the change this merge brings in from dev is #835's first-parent step, `123f57a9..45c0b56c`, and that is what I compared. Taken as a whole, `ac0a01e3..45c0b56c` is covered by check (d) below: the head against live dev is exactly #854's own files plus `b5d17214`'s two generator sources.
- **(a) File sets match.** `b5d17214..9405010f` and `123f57a9..45c0b56c` change the same four files: `docs/design/AREA_BUDGET.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md` and `docs/findings/README.md`.
- **(b) How each file arrived.** `MAILBOX_SPLIT.md` at the head is dev's blob `12b31086`. Both sides edited the other three, so they went through a 3-way merge (`receipts/blob_compare.txt`).
- **(c) Independent replay.** `git merge-tree --write-tree b5d17214 45c0b56c` (git 2.56.0) auto-merges `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` and conflicts only in `docs/findings/README.md`. The replay tree and the head differ only in that file (`receipts/replay_vs_head.diff`). Every other byte of the head is therefore the mechanical merge, so #854's hunks in the two area documents survive by construction. The full patches of both sides are saved as `receipts/delta_pr_side.diff` (`b5d17214..9405010f`) and `receipts/dev_835_side.diff` (`123f57a9..45c0b56c`).
- **(d) Head against live dev `45c0b56c`.** The head differs from dev in 17 paths (`receipts/head_vs_dev_name_status.txt`): #854's 15 paths from `ac0a01e3..a853461d` (`receipts/a853_vs_base_name_status.txt`), plus `b5d17214`'s two generator sources (`scripts/register_descriptions.json` and `docs/design/CSR_REGISTER_NOTES.md`). Of those 17, every `hdl/`, `tb/`, `syn/` and CHANGELOG blob, plus `docs/testing/TESTING.md` and `234_PP_SHADOW_AREA_BASELINE.md`, is byte-identical to `a853461d`. The delta touches no `hdl/`, `tb/`, `syn/`, `scripts/`, `sw/` or `third_party/` path. The gitlinks are identical at `a853461d`, `b5d17214`, `45c0b56c` and `9405010f` (`receipts/gitlinks.txt`).

### (2) The README resolution

Receipt: `receipts/readme_resolution.txt`, produced by `scripts/check_readme_resolution.py` with base `123f57a9`, PR side `b5d17214`, dev side `45c0b56c` and the head. Result: **PASS.**

- All four versions have 36 lines. The PR side changed only line 25 (the 234 row), and dev changed only line 26 (the 649 row). The two changes do not overlap.
- At the head, line 25 equals the PR side byte for byte, line 26 equals the dev side byte for byte, and every other line equals the base.
- The 234 row carries this PR's sentence: "The gate's current record is #854's re-baseline of 2026-11-09, the control-frame drop count on the image with all four lab fixes, in the [area budget](../design/AREA_BUDGET.md#headroom-target)". The anchor still resolves: `### Headroom target` is at `docs/design/AREA_BUDGET.md:141`.
- The 649 row carries #835's "gap to NFR-RES-01's former 60 % target".

### (3) The gates, rc 0 at the head

| Command | Result | Receipt |
|---|---|---|
| `python3 -I scripts/docs_inventory.py --check` | rc 0: "documentation inventory: OK (533 lines, docs/DOCUMENTATION_AUDIT.md is fresh)" | `receipts/docs_inventory_check.log` |
| `python -I scripts/gen_register_reference.py --check`, in a disposable venv with `wavedrom==2.0.3.post3` (version verified) | rc 0: "register reference: fresh (203 registers, 34 modules, 240 files)" | `receipts/gen_register_reference_check.log` |
| `git diff --check origin/dev HEAD`, with origin/dev = `45c0b56c`, fetched and checked by `git ls-remote` | rc 0 | `receipts/git_diff_check.log` |

## Cross-document coherence of the 3-way merge

- **No conflicting figures.** #835's added lines contain none of the record figures that #854 re-baselined: 53,428 / 53,534 LUT, 15,829 / 15,820 slices, +0.210 / +0.166 ns. I searched for each one, and none appears in a `+` line of `123f57a9..45c0b56c`. #835 also adds no "record", "anchor" or "re-baseline" claim that could contradict #854's.
- **Each figure has one meaning at the head.** "Current" always means record 16: `MARK_II_AREA_PLAN.md:61` (+0.166 ns) and `:1101` (#854's 53,534 / 15,820). The #851 figures appear only as history ("then re-recorded" at `MARK_II_AREA_PLAN.md:1100`, and "The preceding" at `AREA_BUDGET.md:264`).
- **#835's AREA_BUDGET edits fit with #854's.** #835's edits at `docs/design/AREA_BUDGET.md:143-144` ("the accepted target") and `:287-289` ("The image must also fit Block RAM, with timing met") sit beside #854's record table at `:154-162` and its record paragraphs at `:245-264` without contradicting them.
- **The `b5d17214` generator sources (R803-4's scope; I only spot-checked them).** Against dev, the head's `scripts/register_descriptions.json`, `docs/design/CSR_REGISTER_NOTES.md` and generated `docs/reference/REGISTER_MAP.md` add only #854's "or longer than the FIFO; saturates at 255" wording and the drop-counter paragraph. This matches the issue's Required clause ("saturating at 255"), and the generated page is fresh (gate (3)).

## Findings

### R804-5-R1: RESIDUE (lens `Docs`), the PR #862 body names a superseded head

- **Where:** live PR #862 body (`receipts/pr-body-live.md`): the Status paragraph at lines 16-18 ("the head is its own merge result. Head `a853461dd57f8e493ca079e0faa1f07229c3cb16` (seven commits …)"), line 184 (`git checkout --detach a853461d…` under "How to get into the same state"), and line 206 ("Local gates on a clean clone of the head `a853461d`").
- **Evidence:** the PR head is `9405010f`, two dev-sync merges later. The body does not mention `b5d17214`, `9405010f`, #825 or #835. The merges and their gates are recorded only in the sync-note comments 6759682744 and 6760255365.
- **Why this is RESIDUE:** this is wording only. The body's gate claims are true for the commit it names, and the delta adds no gate, figure, measurement, test or verdict. The current head's evidence is public in the sync notes and in this report.
- **Exact fix:** after the "Head `a853461d…` (seven commits: …, text only)." sentence, add: "The head is now `9405010ff5def3275eecda7271a4b1ccc1aa2be0`: two manager merges of dev, `b5d17214` (dev `123f57a9`, #825; the PP_DIAG drop wording is carried into `scripts/register_descriptions.json` and `docs/design/CSR_REGISTER_NOTES.md`, and the register page is regenerated) and `9405010f` (dev `45c0b56c`, #835; `docs/findings/README.md` keeps this PR's 234 row and #835's 649 row). Both are documentation only; `docs_inventory.py --check`, `gen_register_reference.py --check` and `git diff --check` return 0 at `9405010f`." Then change line 184 to `git checkout --detach 9405010ff5def3275eecda7271a4b1ccc1aa2be0`. Line 206's gate list stays as it is, because it describes the round 3 head.
- **Verification:** the live PR body names `9405010f`, and the checkout recipe reaches the head.

### R804-5-S1: SUGGESTION (lens `Docs`), the 234 row's "its 60 % target" next to #835's "former 60 % target"

- **Where:** `docs/findings/README.md:25`: "NFR-RES-01 was then 11,917 LUT over its 60 % target". Line 26 (#835) now says "NFR-RES-01's former 60 % target".
- **Evidence:** this phrase is dev text that predates the PR. #854 changed only the record sentence in that row (word diff `ac0a01e3..b5d17214`: `#851's`→`#854's`, the date, and "the control-frame drop count on"). "Was then" already makes the claim historical, so the row is not wrong.
- **Optional:** "over its then 60 % target" would read in parallel with line 26. This is outside #854's frozen scope, so it belongs to whoever next edits the findings index. It affects no lens.

## Prior public findings at this head

I read these only after my own pass.

| Finding | Severity | Status at `9405010f` | Evidence |
|---|---|---|---|
| R803-2-F1 = R804-2-F1 (the +13 FF credited to the change) | MINOR | **Resolved** (R803-3, R804-3); still resolved | `234_PP_SHADOW_AREA_BASELINE.md` is byte-identical to `a853461d`. Its `AREA_BUDGET.md` counterpart (`:256-257`, "Of those FFs the change carries +10") is present at the head and arrived through the clean 3-way merge (`receipts/replay_vs_head.diff` shows README only). |
| R804-2-R1 (`drops_mutant.py` docstrings) | RESIDUE | **Resolved**; still resolved | `tb/verilator/pp_shadow/drops_mutant.py` is the same blob as at `a853461d` (`receipts/delta_compare.txt` (d)) |
| R804-2-S1 (LUT share is a remainder change) | SUGGESTION | Taken; unchanged | `AREA_BUDGET.md:259-261` at the head |
| R803-2-S1 = R804-2-S2 (hosted `RXFILT=0 --drops-only` run) | SUGGESTION | **Carried** to #495 by ruling item 4. The PR body still names it. I found no #495 comment recording it yet (manager duty, below). | `receipts/pr-body-live.md` (6 `RXFILT=0` mentions); #495 comment scan |
| R803-3-S1, R803-3-S2 (optional wording) | SUGGESTION | Optional; the delta does not touch their artifacts | `234_…` is byte-identical; the PR body is not rewritten |
| Round 1 findings | various | Resolved or carried at round 2, per the R803-2 and R804-2 tables; the delta does not touch their artifacts | `receipts/delta_compare.txt` |

## Comment rule

The delta adds no source comments. All four changed files are documentation pages: two design pages and two findings or index pages, which may name lanes. So this delta adds no new instance of the comment rule. Both merge commit messages are a single line with no trailers.

## Reviewer-owned completion ledger (R804-5)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| `Conformance` | CLEAN | The issue #854 Required clause against the head. `hdl/milan/KL_pp_shadow.sv`, `hdl/common/csr/milan_csr.sv` and `syn/ooc/pp_resource_baseline.json` are byte-identical to `a853461d` (`receipts/delta_compare.txt` (d)). The `docs/findings/README.md:25` record sentence and its `AREA_BUDGET.md:141` anchor. The record figures are single-sourced across `AREA_BUDGET.md:154-162,245-264` and `MARK_II_AREA_PLAN.md:61,1100-1101`. The generator wording matches the Required clause ("saturating at 255"). | R804-5 (delta); R803-3 / R804-3 for the unchanged content | `9405010ff5def3275eecda7271a4b1ccc1aa2be0` |
| `RTL` | CLEAN | Zero `hdl/`, `syn/` or `third_party/` paths in `b5d17214..9405010f`. RTL blobs equal `a853461d`. All six gitlinks are equal at `a853461d`, `b5d17214`, `45c0b56c` and `9405010f` (`receipts/gitlinks.txt`, `receipts/clone_integrity.txt`). | R804-5 (delta); R804-3 (unchanged RTL) | `9405010ff5def3275eecda7271a4b1ccc1aa2be0` |
| `Robustness` | CLEAN | `tb/verilator/pp_shadow/sim_main.cpp`, `drops_probes.vlt`, `Makefile` and `drops_mutant.py` are byte-identical to `a853461d`, and the delta changes no input to the `[DR]` overflow, runt, oversize or saturation grades (`receipts/delta_compare.txt` (d)) | R804-5 (delta); R804-3 / R803-3 | `9405010ff5def3275eecda7271a4b1ccc1aa2be0` |
| `Tests` | CLEAN | Three gates re-run at the head, all rc 0: `docs_inventory.py --check`, `gen_register_reference.py --check` (pinned wavedrom) and `git diff --check origin/dev HEAD` (`receipts/*_check.log`). The README resolution is checked line by line (`scripts/check_readme_resolution.py`). The merge-tree replay agrees with the head outside README (`scripts/delta_compare.sh`). No test file is in the delta. | R804-5 | `9405010ff5def3275eecda7271a4b1ccc1aa2be0` |
| `Docs` | CLEAN (R804-5-R1 is RESIDUE; S1 is a SUGGESTION) | `docs/findings/README.md:25-26`. The 3-way-merged `docs/design/AREA_BUDGET.md` (`:141-162,245-264,287-289`) and `docs/design/MARK_II_AREA_PLAN.md` (`:61,1100-1101`). Dev's `docs/design/MAILBOX_SPLIT.md`. The commit messages of `9405010f` and `b5d17214`. The live PR #862 body (`receipts/pr-body-live.md`). The sync notes 6759682744, 6760255365 and 6760258197. | R804-5 | `9405010ff5def3275eecda7271a4b1ccc1aa2be0` |

## Evidence spot-checks

- **Published evidence tree** (`review-evidence/854-r1` at `edebc85d`): `MANIFEST.json` has 1,169 entries (author 559, author-r2 535, reviews 75). I fetched six files (`author-r2/{HANDOFF,PR-BODY,REVIEW-READY}.md`, `author/{HANDOFF,PR-BODY}.md` and `author-r2/receipts/scripts/viv.sh`), and each one matches its `published_sha256` (`receipts/evidence_spotcheck.txt`). That tree covers rounds 1 and 2. This delta has no author receipts, and none were needed: the three sync gates were re-run above.
- **Hosted contexts at the exact head** (snapshot taken 2026-11-10T06:16:33Z, in `receipts/hosted_check_runs_9405010f.txt`):
  - Completed with success: 5 (`changes`, `bdd-conformance`, `docs-check-no-git`, `docs-gates-1`, `wire-accountability`).
  - In progress: 5 (`docs-gates-0`, `docs-gates-2`, `verilator-lint`, and two `Fail fast across this head`).
  - Queued: 8 (the firmware jobs, `Prepare pinned Yosys` and `publication-census`).
  - None of these is verdict evidence here. The manager owns hosted and act acceptance.

## Real limits

- This round reviews the `b5d17214..9405010f` delta. It does not re-review `b5d17214`'s own resolution, which is R803-4's scope, beyond the spot-check above. R803-4's verdict was not published when this report was written.
- No RTL simulation, mutant campaign, synthesis or route was run. None is needed, because every input to them is byte-identical to `a853461d`, where R803-3 and R804-3 ran or accepted them. The area figures are the author's record 16, checked in earlier rounds, not re-measured.
- Physical calibration was NOT RUN, and field or hardware skips are not hardware proof. No manager source bank ran at this head, and none is claimed.
- `git merge-tree --write-tree` and `git fetch` wrote unreferenced objects and a remote-tracking ref into this clone. Tracked bytes, modes, the index and the gitlinks are verified unchanged (`receipts/clone_integrity.txt`: HEAD and tree match, the porcelain is empty, and the index digest equals the tree digest).

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live dev `45c0b56c`, or later if dev moves, and link its receipts on the PR.
- Act and hosted acceptance at `9405010f`. The exhaustive hosted contexts were still queued or running at the snapshot.
- Obtain R803-4's verdict on `b5d17214`. The full CONTRIBUTING review bar (two positives, one external) still applies at the merge head.
- Carry R804-5-R1 (exact fix above) to the residue checklist, or apply it to the PR body. Record ruling item 4 (the hosted `RXFILT=0 --drops-only` run) on #495; I found no #495 comment for it.
- Merge only with explicit maintainer authorization.

R804-5 FINISHED
