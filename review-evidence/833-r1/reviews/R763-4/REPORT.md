[R763] POSITIVE - exact head c1b2961777809403bd2de833ec1fa00c75394d6c

# R763-4: internal cleared-context review of PR #834 (issue #833), round 4

- Head `c1b2961777809403bd2de833ec1fa00c75394d6c`, tree `28a722419d061920d79833cd95c6c9fabe4a4953`. The published PR head reads the same and the PR is not a draft (`receipts/pr-head.txt`).
- Delta reviewed: `3740565f..c1b29617`, 2 commits, 3 files: `scripts/test_suite_cancellation.py` (+3 −1), `scripts/process_test_support.py` (comment only), `docs/testing/TESTING.md` (2 lines).
- `scripts/owned_process.py` is byte-identical to `3740565f` (`git diff --quiet`). The ASTs of `process_test_support.py` and `owned_process.py` are identical across the delta. In `test_suite_cancellation.py` the only non-comment change is `blocked[0] + 0.7` → `blocked[0] + 1.5` (`receipts/gates/ast-compare.txt`).

**Verdict: POSITIVE.** R763-3-F1 is resolved at its cause. Its required outcome holds as specified, on my own runs and on the author's published receipts. The retained residue (R763-2-X1, R763-2-X2 = R764-2-R2, R764-2-R1) is taken with the reviews' exact fixes, verbatim. No BLOCKER, MAJOR or MINOR is open. This round adds one new RESIDUE (R763-4-X1, wording only: the exact fix R764-2-R2 asked for leaves one exception out) and one SUGGESTION (R763-4-S1).

## Scope reconstructed

- **Authority.** AGENTS.md §§3-8 and CONTRIBUTING (via AGENTS.md precedence) set the five lenses, the severity scale and the reviewer-owned ledger. The owner rules in the assignment add RESIDUE, token economy and the comment rule.
- **Issue #833 acceptance** (frozen): (1) the failure message prints each descendant's `/proc/<pid>/stat` state; (2) a fixed deadline or a real fix from that evidence, with no suite left to fail by chance. The round 4 scope (A726d TAKEN) is R763-3-F1 plus the retained residue. It changes no product code.
- **Published evidence.** I verified evidence commit `ff8233016a903703c4899acc56aad485889887dc`, `review-evidence/833-r1/MANIFEST.json`, against every file under `author-r4/` and `reviews/R763-3/`: 1364 files, 0 hash mismatches, 0 missing, 0 unlisted (`receipts/evidence-manifest-check.txt`). The evidence commit carries no GPG signature, so the integrity claim rests on the manifest. The live PR body equals the published `author-r4/PR-BODY.md` apart from one trailing newline (`receipts/pr-body-sha256.txt`).
- **Order.** I wrote my notes on the independent diff pass (`receipts/independent-pass-notes.txt`) before reading the prior review findings (R763-3, then R763-2/R764-2 for the residue texts). I read no other round-4 reviewer report.

## Findings

**R763-4-X1: RESIDUE. Lenses: Docs.** `docs/testing/TESTING.md:224` reads: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window."

- **Evidence.** In the common case a resume comes *before* 4 s: the children exit on SIGTERM, so the shell is resumed at once. `kill_all` then becomes `resume + 10` (`owned_process.py:311`), and a command the trap starts is spared until then (`:330-332`). So at 4 s that command has not received `SIGKILL` either.
- **Probe.** `scripts/early_resume_probe.py` runs at product constants (`receipts/early-resume/head.log`, rc 0). The resume came at 0.02 s, the trap's 6 s command finished, cleanup ended at 6.02 s, and no `SIGKILL` was sent at or before 4.5 s.
- **Where it comes from.** The sentence is R764-2-R2's exact fix, verbatim. The code is right, and lines 230 and 273 state the trap command's window correctly. Only this one sentence's exception list is incomplete.
- **Impact.** Wording only. It changes no figure, bound, test or code.
- **Exact fix.** "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell and any command its trap started, which keep the shell's own window." Also update the quoted text in the PR body's Round 4 residue table (`R763-2-X2 = R764-2-R2` row).

**R763-4-S1: SUGGESTION. Lenses: Tests.** `scripts/test_suite_cancellation.py:565` holds the child on wall time (`blocked[0] + 1.5`), but the guard it must get past is on owner clock (`owned_process.py:327`, `deadline + 1.0` = 1.2 s).

- I measured the margin with `scripts/resume_margin.py` (8 concurrent runs, host load about 26 on 16 CPUs, `receipts/margin/`): the shell is resumed 1.536 s into cleanup every time, 0.336 s past 1.2 s.
- So the control loses its power against `shell-killed-when-resumed` only if the passes before the resume overran their 0.5 s cap by more than 0.336 s in total. It can never go red unmutated.
- The author disclosed this in the PR body and in REVIEW READY. Optional: `+ 2.0` would widen the margin to about 0.8 s, at a cost of 0.5 s of preflight.

**Retained SUGGESTIONS** (optional, unchanged):
- R763-3-S1 ("listed" half of the resume condition unpinned). It was not taken. The stated reason, that a control for it would change a matrix row in the same round, is the author's literal reading of F1's verification text. It is acceptable, since every bound holds under that variant. A later control that turns `new-fix-census-not-owned` red would be an improvement, not a regression.
- R763-2-S1 (10 s windows unpinned).
- R763-2-S2 (manager actions R763-1-S1/S2).
- R763-2-S3 (census-cost comment figure).
- R764-2-S1 (0.5 s cap pinned only below about 1.5 s).

## Prior findings at their cause, at this head

| Prior finding | Status | Evidence at this head |
|---|---|---|
| R763-3-F1 (MINOR, Tests): `owner_shell_window` did not pin `owned_process.py:317` | **RESOLVED** | Checks (1)-(4) below |
| R763-2-X1: "One started by a resumed shell's trap…" | **RESOLVED**, exact fix verbatim | `TESTING.md:230`; `process_test_support.py:22-24` (same words plus "(TRAP + REAP)"); PR body "The deadline's derivation". All three read "After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started." |
| R763-2-X2 = R764-2-R2: `TESTING.md:224` exception | **RESOLVED** as asked, with R764-2-R2's wording ("cancelled", not "stopped"; the reason is in the PR body and is sound). The remaining gap is new RESIDUE R763-4-X1 | `TESTING.md:224` |
| R764-2-R1: PR body "…where it was 4 s: A true survivor's deadline…" | **RESOLVED**, exact fix verbatim | PR body line 49: "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." |
| Round 1-3 findings | Resolved earlier. The delta does not touch what they depend on | `owned_process.py` byte-identical. My matrix reproduces every old row |

**(1) The control now resumes past `deadline + 1.0`.** I derived this, then measured it.

- **Derivation.** The control stages GRACE 0.2 s and KILL_ALL 0.2 s, so the stubborn-leaf parent spare (`:327`) lasts while clock < 1.2 s. A resume needs no live non-root descendant (`:304`), and the child now dies only at 1.5 s. So in the resume pass only `:317`'s `clock < kill_all` term spares the shell.
- **Measurement.** The resume comes at 1.536 s (`receipts/margin/`).

**(2) Red with the `clock < kill_all` term removed, green unmutated, and the old control was blind to it.** `scripts/repeat_control.py`, 10 runs per cell, in user+PID namespaces (`receipts/repeat/summary.txt`):

| Scripts | `owner_shell_window` |
|---|---|
| head, unmutated | 10/10 green, 3.1 s |
| head + `shell-killed-when-resumed` | **10/10 red**: "the shell was killed in the pass that resumed it, before its trap" |
| 3740565f control + head product, unmutated | 10/10 green, 2.3 s |
| 3740565f control + `shell-killed-when-resumed` | 10/10 green (F1 reproduced on the old control) |

**(3) The rows that must stay red, stay red.**
- In my matrix, `no-trap-window` is red ("shell was killed…") and `trap-commands-no-window` is red ("trap command was killed…").
- My own spot mutants (`scripts/spot_mutants.py`, `receipts/spot/`, 3/3 each):
  - `root-killed-unresumed`, the M06 edit: red, "shell was killed…";
  - `trap-commands-1s`, the M07b / trap-commands-1s edit: red, "trap command was killed…".
- For M05, M06, M07, M07b, `trap-commands-1s` and `no-shell-window` on the author's published `matrix-39`, `owner_shell_window` is rc 1 with these words. `R763-none` is rc 0 in 3.1 s.

**(4) The reviewer's matrix re-run: no other row changed.**
- I ran R763-3's own `mutants.py`, `matrix.py` and `run_control.py`, copied unchanged to `scripts/r763-3/`, at this head: 13 mutants × 8 controls, 14 jobs, namespaces, 39 s (`receipts/matrix/`).
- Against R763-3's table, only the `shell-killed-when-resumed` row differs: `shell_window` ok → RED(1) (`receipts/matrix/diff-vs-R763-3.txt`).
- Against the author's round 4 table it is identical (`diff-vs-author-r4.txt`, rc 0).
- `new-fix-census-not-owned` stays green (R763-3-S1, retained) and `none` is green.

**Whole suite.** `python3 scripts/test_suite_cancellation.py` at head: rc 0, `suite cancellation: PASS (… shell window …)` (`receipts/suite/`). It ran concurrently with the matrix.

## Comment rule and commits

- The new source comment `test_suite_cancellation.py:563-564` states behaviour and reason. The rewrapped `process_test_support.py:19-29` cites `#833` only. Neither carries a lane label, lane name, review round, reviewer ID or comment ID. No new RESIDUE under the comment rule.
- 2 commits, each a one-line subject with an empty body and no trailers (`receipts/gates/delta-commits.txt`).
- No em or en dash appears in the added lines.

## Lens results (each with its artifact, at head c1b29617)

```text
[R763] PASS Conformance - docs/testing/TESTING.md:223-235, scripts/process_test_support.py:19-30, scripts/owned_process.py:289-311 (byte-identical to 3740565f), PR body "The deadline's derivation" and "Round 4", issue #833 acceptance 1-2 - rewritten bound statements derived against code: after a resume limit = max(4, resume+10)+10 = resume+20 for every owned descendant, resume only below 14 s; figures 14/34/44/49.6/59.6 s unchanged; acceptance unchanged (state in report still asserted: report-without-state red on owner_report/owner_survivor in receipts/matrix)
[R763] PASS RTL - scripts/owned_process.py:256-339 unchanged at this head (git diff --quiet 3740565f HEAD; AST identical); no HDL in the delta - guard interplay at :317 vs :327 re-read against the new control; the cleanup state machine's prior verdict at 3740565f stands, and the delta changes nothing it depends on
[R763] PASS Robustness - receipts/early-resume/head.log, receipts/repeat/, receipts/margin/, receipts/suite/ - early resume at product constants (trap command survives past 4 s, cleanup ends 6.02 s, no SIGKILL); 40 shell-window runs under host load about 26 on 16 CPUs, no unexpected verdict; whole suite rc 0 under concurrent matrix load
[R763] PASS Tests - scripts/test_suite_cancellation.py:542-581 (owner_shell_window), :705 preflight; receipts/matrix (R763-3 matrix at head), receipts/repeat, receipts/spot; author-r4 matrix-39 and matrix-r763-3 (manifest-verified) - R763-3-F1 resolved: red 10/10 under shell-killed-when-resumed, green 10/10 unmutated, old control green under the mutant; no other matrix row changed; M05/M06/no-trap-window/trap-commands-* red; R763-4-S1 is a suggestion only
[R763] PASS Docs - docs/testing/TESTING.md:224,230; scripts/process_test_support.py:19-29; scripts/test_suite_cancellation.py:563-564; PR body (live = published author-r4/PR-BODY.md); receipts/gates (docs_check rc 0, check_doc_style rc 0, check_py_idiom rc 0, git diff --check rc 0) - residue fixes verbatim; comment rule holds; RESIDUE R763-4-X1 only (non-blocking)
```

## Executed (each with its own log and rc, under `receipts/`)

| Run | Result |
|---|---|
| Evidence MANIFEST.json check (`author-r4/`, `reviews/R763-3/`) | 1364 ok, 0 bad, 0 missing, 0 unlisted |
| R763-3 matrix at head: 13 × 8, 14 jobs, user+PID namespaces | Only the F1 row changed vs R763-3. Identical to the author's round 4 table |
| `test_suite_cancellation.py` at head (concurrent with the matrix) | rc 0 |
| `repeat_control.py`: 4 script sets × 10, 16 jobs | Table in check (2) |
| `resume_margin.py` × 8 | Resume at 1.536 s, margin 0.336 s |
| `spot_mutants.py` × `owner_shell_window` × 3 | Both red |
| `early_resume_probe.py` at product constants | R763-4-X1 evidence |
| `docs_check.py`, `check_doc_style.py`, `check_py_idiom.py`, `git diff --check 1f29f189 HEAD` | all rc 0 |
| `check_em_dash.py --base 1f29f189` | rc 2: cannot judge, because the pinned renderer (html5lib) is not installed here. Not a finding. A manual scan of the delta's added lines finds no em/en dash. The author's docs.yml receipts cover this step |
| Hosted check runs at the exact head (read-only API) | `hosted-check-runs-at-head.tsv`: 13 runs. 3 completed success (bdd-conformance, docs-check-no-git, wire-accountability); the rest were queued or in progress when read |
| Clone integrity after all probes | `clone-integrity.txt` |

**Integrity.** After all probes, HEAD, the tree and the index tree are `c1b29617`/`28a72241`, and the worktree and index match HEAD. All 1459 tracked blobs match their index bytes and modes. `status --ignored` is empty. The 6 gitlinks are unchanged: external `efeb541a`, gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`. All probes ran on copies under the packet's `scratch/` or imported the clone's scripts read-only, with `-B`. The scoped Verilator was not needed and was not used.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | TESTING.md:223-235; process_test_support.py:19-30; owned_process.py:289-311; PR body derivation and Round 4; issue #833 acceptance | R763-4 | c1b2961777809403bd2de833ec1fa00c75394d6c |
| RTL | CLEAN | owned_process.py:256-339 (byte-identical, AST identical); no HDL in the delta | R763-4 | c1b2961777809403bd2de833ec1fa00c75394d6c |
| Robustness | CLEAN | receipts/early-resume, repeat, margin, suite | R763-4 | c1b2961777809403bd2de833ec1fa00c75394d6c |
| Tests | CLEAN (R763-3-F1 resolved; R763-4-S1 suggestion only) | test_suite_cancellation.py:542-581, :705; receipts/matrix, repeat, spot; author-r4 matrix-39, matrix-r763-3 | R763-4 | c1b2961777809403bd2de833ec1fa00c75394d6c |
| Docs | CLEAN (RESIDUE R763-4-X1 only) | TESTING.md:224, 230, 273; process_test_support.py:19-29; test_suite_cancellation.py:563-564; PR body; receipts/gates | R763-4 | c1b2961777809403bd2de833ec1fa00c75394d6c |

## Real limits

- **No manager source bank** ran at this head, and none is claimed or inferred. The source-head execution evidence is the author's published round 4 gate receipts (docs.yml steps, lifecycle, behave, mutation tables), manifest-verified, plus my focused runs above.
- I did not run the full sweep, the PP/gPTP/Yosys/builder banks, `act` or the lifecycle make target. The delta does not change the lifecycle test or anything it imports, apart from a comment (AST identical).
- `check_em_dash.py` could not judge here (renderer not installed).
- **Hosted contexts** were partly concluded when read. The manager owns hosted and act acceptance.
- **Physical calibration** did NOT RUN. Field skips are not hardware proof.
- **The control's sensitivity** to `shell-killed-when-resumed` rests on a 0.336 s owner-clock margin (R763-4-S1). Under extreme pass stalls it can weaken one run. It cannot make the control red unmutated.

## Pending manager duties

- Carry RESIDUE R763-4-X1 (exact fix above) and the retained suggestions (R763-4-S1, R763-3-S1, R763-2-S1/S2/S3, R764-2-S1) to the residue checklist.
- Validate the current-dev merge candidate: source base `1f29f189279f9fc0132f4918e47342b87d22f33a`, live dev `503bc97cd4f24ad07596c17e7188f2024617972d`, builder and native banks. Link its receipts on the PR.
- Own hosted and act acceptance on the exact head.
- Publish this report. Merge only on explicit maintainer authorisation.

R763-4 FINISHED
