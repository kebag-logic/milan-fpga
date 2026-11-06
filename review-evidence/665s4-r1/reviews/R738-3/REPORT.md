[R738] POSITIVE - exact head 4d9b901cd42fb21ac7c05432b88bb6c00061064a

External cleared-context review R738-3 of issue #665 / PR #812, S4 round 4 (R738-F2). Tree `605f043b826040650960b98b9392bf8da5ebdcc1`. Round delta `ac45db8f..4d9b901c`: two commits, `tb/verilator/nvm_split_target/run.py` (+43 -6), `target_selftest.py` (+144 -20) and `README.md` (+18 -3). No RTL, firmware, shared simulator, grader, D5 gate or gitlink changes (`git diff --stat ac45db8f..4d9b901c`). Whole-lane diff `f4c9ad4f..4d9b901c` (17 files) was used to confirm that no other file changed this round.

Reconstruction order: AGENTS.md / CONTRIBUTING.md, the round 4 assignment on #665 (issuecomment-6514339158) quoting R738-F2's required outcome, the R738-2 report (issuecomment-6514335214) for the finding's cause, the round delta, then the author's round 4 evidence at `efd9f61c` (`review-evidence/665s4-r1/author-r4/`).

## Verdict

POSITIVE. R738-F2 is resolved at its cause. `main` now clears the earlier pair and refusal before building (`run.py:246-250`, `:314`). `accept` validates (`against_build`, then `table`'s `provenance`) before it writes either file (`run.py:253-262`). A refused run writes only `refused.json`, with top keys `refused` and `record` (`run.py:265-273`, `:322-324`). Each of the seven new checks and five new mutants does what it claims. Independent probes through the real `main` and five extra reviewer mutants agree. The gates are rc 0 at the head. No BLOCKER, MAJOR or MINOR is open. One SUGGESTION and one RESIDUE are recorded below.

## Findings

**R738-3-S1 | SUGGESTION | Tests | `target_selftest.py:276-286` (`accept writes nothing for a record it refuses`) | The direct `accept` check covers only a record that `table` refuses, not one that `against_build` refuses.**
Evidence: in `probe_reuse.py` the reviewer mutant `accept: pair written before against_build` calls `table(rec)`, writes both files, and only then runs `against_build`. It fails 0 of the 48 repository checks (`reuse-probes.log`). The planted mutant `_accept_unvalidated` (round 3's ordering: write first, validate after) is caught, as the README row says. The check's record is refused only by `table`'s provenance, so the build-agreement half of "only once both are sound" (`run.py:254-255`) is never exercised directly.
Impact: none through `main`. `refuse` calls `clear`, so a run refused by `against_build` still leaves only `refused.json` (the end-to-end checks pass under this mutant). The gap only matters if the second layer of defence, `refuse`'s own `clear`, is later weakened.
Optional outcome: add a second direct `accept` case whose record passes `table` but disagrees with its specs. Require that it raises and leaves the directory empty.
Verification: the reviewer mutant above then fails that check.

**R738-3-RES1 | RESIDUE | Docs | `tb/verilator/nvm_split_target/README.md:52`; `run.py:32` (module docstring); PR body line 22 | "alone in their place" / "leaves only `refused.json`" says more than the code does.**
Evidence: `clear` removes only `results.json`, `table.md` and `refused.json` (`run.py:242-250`). The cases' recorded `<case>.txt`, `.journal.in`, `.journal.out` and `.log` files, and `shape/`, stay in `--out` (`run.py:78-94`), and `--regrade` relies on them (`run.py:79-83`). The README's own self-test list (line 266) and the PR body's line 151 state it exactly ("neither `results.json` nor `table.md`"). Nothing here is measured, tested or claimed as conformance.
Exact fix: README:52 to "A refused run leaves `refused.json` in their place, and neither `results.json` nor `table.md` (`run.refuse`); the cases' recorded scripts, journals and logs stay for `--regrade`." Make the same change to `run.py:32` ("leaves refused.json, and neither file of the pair, in their place") and PR body line 22 ("leaves `refused.json` and neither `results.json` nor `table.md`").

No new comment residue: the added lines in `git diff ac45db8f..4d9b901c` name no bench lane label, lane name, review round, reviewer ID or issue-comment ID. The README's issue-comment links at lines 4 and 125 predate this round.

## Per-lens results (focus items 1-4)

[R738] PASS Conformance - `run.py:242-273,312-325`; assignment issuecomment-6514339158 "Required outcome" - Checked each required outcome against the code. A refused run (exit 2) leaves no table: `clear` runs first inside `try`, and `refuse` clears again. `results.json` and `table.md` are written together, only after `against_build` and `table`'s provenance pass. The diagnostic `refused.json` has no `cpu_hz`, `sys_hz` or `results` at its top. All three refusal classes are covered (missing clock, wrong/disagreeing clock, misconverted). The fresh-directory controls remain (`target_selftest.py:339-350`). The regenerated 1x1 and 8x8 points record CPU 50,000,000 Hz and bus 100,000,000 Hz in all seven arms (`author-r4/receipts/target-*/build-clocks.txt`), with RC=0 at both. The step-bound control is caught in all seven phases, and slow-step is rejected at 30.2216 ms (1x1) and 30.2139 ms (8x8) against 10 ms (`target-*/run-tail.log`). The D5 plant receipt shows `PLANT CAUGHT`, rc 0 (`author-r4/receipts/d5-plant/plant_d5_removed.log`).

[R738] PASS RTL - `git diff --stat ac45db8f..4d9b901c` and `git diff --name-only f4c9ad4f..4d9b901c` - The round touches only three files under `tb/verilator/nvm_split_target/`. No HDL, firmware, `split_soc.py`, `sim_main.cpp`, build/clock derivation or gitlink changed. The harness still reads clocks from each `build.json`, so the delta changes nothing the R738-1/R738-2 RTL verdict depends on. That verdict is retained.

[R738] PASS Robustness - `run.py:246-273,312-325`; `reuse-probes.log` - Probed through `main` with my own producer substitutions. Success, then each of: one arm without a CPU clock, all arms without one, a disagreeing bus clock, misconverted results. Each gives exit 2 and only `refused.json` among the three output names, with keys {refused, record}. Refusal, then success, leaves the success's pair only, at its own clocks. Paths outside the documented refusal set: an uncaught `KeyError` after a success leaves neither file (the earlier pair was already cleared), and exits by traceback with no `refused.json`. An argparse usage error (exit 2) leaves the earlier run's consistent pair unchanged, because it happens before any run. When `table.md` is an undeletable directory, the refusal exits 2 and prints that it was not recorded, which matches `run.py:271-273`. None of these creates a mixed pair from two runs. The real `--regrade` refusal on fresh builds at both points is in the author's receipts (`probes/real-refusal-{1x1,8x8}.log`, PROBE PASS): missing `cpu_hz` leaves `['refused.json']`, and after restoring, the pair is byte-identical to the fresh run's.

[R738] PASS Tests - `target_selftest.py:194-295,600-626,677-688`; `target-selftest.log`; `reuse-probes.log` - The self-test prints `checks: 73   failures: 0` at the head (48 checks, 25 mutants; 7 checks and 5 mutants new). Each new mutant fails its named check. I also ran five reviewer mutants against the full check list: `against_build` dropped fails 2 checks, `refuse` writing no record fails 7, clocks at `refused.json`'s top fails 3, `clear` keeping `table.md` fails 5. The one survivor, writing before `against_build`, is S1: it has no effect through `main`. The author's `reuse-probe.log` reproduces the defect on round 3's `run.py` (STALE OUTPUT) and shows the fix at the checkout (SOUND), so the new checks distinguish the defect from the fix.

[R738] PASS Docs - `README.md:43-53,263-269,300-304`; `run.py:30-33`; PR body - The README matches the code. "Each accepted run" holds. `clear`, `accept` and `refuse` are described as implemented, and so are `refused.json`'s fields and top-level shape. The self-test list and the five mutant-table rows match `MUTANTS` labels and check names exactly. The fresh-directory controls are restated as "exit 2 and neither file", which `target_selftest.py:341-349` now enforces. No other document describes this output contract: `ARCHITECTURE_HW_SW_SPLIT.md` and `ctrl_nvm/README.md:341` only link to the harness's Results. The PR body's round 4 section and reproduction step (line 151) match. The only wording issue is RES1, which does not leave the lens unclean.

## Execution evidence

- `target-selftest.log` / `.rc`: `run.py --self-test` at the head, rc 0, `checks: 73   failures: 0`, 11.3 s.
- `reuse-probes.log` / `.rc` (`probe_reuse.py`): independent reuse probes, observations and five extra mutants, rc 0, `PROBES PASS`.
- `public-verification.log` (`verify_public.py`): all 204 `author-r4/` files at evidence commit `efd9f61c` match `published_sha256` in `MANIFEST.json`. None are missing or unlisted. Every `HEAD.txt` / `runs-head.txt` names `4d9b901c…`. `gates-short/summary.md` has 97 gate rows, 0 nonzero or dirty. `gates-long-summary.md` has 11 gates, 0 nonzero or dirty. The four gates cut by the host reset re-ran from the start in `gates-long-rest/` (rc 0), and the cut log is explicitly marked non-evidence.
- `checkout-integrity.log` (`verify_checkout.sh`): exact head and tree. Index equals the head tree (1476 entries, all stage 0), and worktree bytes and modes equal the index. Status is empty with ignored files included, after removing seven untracked ignored bytecode caches that appeared during the run. The six gitlinks are unchanged; five are populated at their pins and `external` stays unpopulated.
- `hosted-checks.txt`: at this exact head GitHub lists 0 check runs, 0 statuses and no workflow runs (read-only query). No hosted job is claimed or inferred.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment required outcome; `run.py:242-273,312-325`; author target-1x1/8x8 build clocks and run tails; D5 plant receipt | R738-3 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| RTL | CLEAN | Delta inventory `ac45db8f..4d9b901c` and `f4c9ad4f..4d9b901c`; unchanged RTL/firmware/simulator; retained R738-1/R738-2 baseline | R738-3 (delta); R738-1 baseline retained | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Robustness | CLEAN | `run.py` clear/accept/refuse/main; `reuse-probes.log` reuse classes and out-of-set paths; author real-refusal probes at both points | R738-3 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Tests | CLEAN (S1 optional) | `target_selftest.py:194-295,339-350,600-688`; `target-selftest.log`; reviewer mutants in `reuse-probes.log`; author `reuse-probe.log`, `reuse-mutant-failures.txt` | R738-3 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Docs | CLEAN (RES1 residue) | Target README:40-53,255-307; `run.py` docstring; other docs linking the harness; PR body round 4 section and reproduction | R738-3 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |

## Prior finding disposition

I did this reconciliation after my independent pass, verdict and ledger above. PR #812 has eight issue comments, no submitted reviews and no review-thread comments. Three published reviews carry findings: R738-1 (6510793657), R737-1 (6511284713) and R738-2 (6514335214). R737-2 has started but has not published, and I have not read it.

| Prior ID | Disposition at this head |
|---|---|
| R738-F2 (MINOR; Conformance, Robustness, Tests, Docs) | **Resolved at its cause.** Validation now comes before writing, and the run clears before building and refuses with a refusal record. The success-then-refusal checks cover each class, and the refusal-then-success check is there. The fresh-directory controls are kept and tightened. Verified by the self-test, the reviewer probes and mutants, and the author's round-3-versus-checkout and real `--regrade` probes (see the lens lines). |
| R738-F1 (MINOR; Conformance, Tests, Docs) | Resolved and stays resolved. The round only moves where the record is written; the clock checks and three clock mutants still pass (`target-selftest.log:11-22,60-62`). |
| R737-1-R1 (RESIDUE, Docs) | Resolved. `docs/ARCHITECTURE_HW_SW_SPLIT.md:223` names CPU 50 MHz and bus 100 MHz, unchanged this round. |
| R737-1-S1 (SUGGESTION, Tests/Docs) | Resolved. Results keep CPU/bus clocks, and every table labels them. |
| R737-1-S2 (SUGGESTION, Tests/Robustness) | Retained as optional. Map-placement and map-clock negative controls remain absent; those files are untouched (`git diff ac45db8f..HEAD -- docs sw .github tb/verilator/ctrl_service_budget` is empty). |
| R737-1-S3 (SUGGESTION, Robustness) | Retained as optional. `gen_flash_port.py:246` `if base % size:` is unchanged. |
| R737-1-S4 (SUGGESTION, Tests) | Retained as optional. Workflow files are unchanged. |

Retained suggestions do not affect cleanliness. No other earlier findings exist on this PR.

## Limits and pending manager duties

- Evidence commit `efd9f61c` is unsigned (GitHub verification `false`, reason `unsigned`). I verified the published hashes, but I do not claim signer authentication. Some large receipts are listed in `large-files.txt` by hash only.
- I did not rebuild either point. The real-build `--regrade` refusal at this head is the author's receipt (`probes/real-refusal-*.log`), checked by hash and content, not re-executed. My own probes use substituted producers through the real `main`.
- No manager source bank exists at this head, and I infer none. GitHub shows no hosted runs for this head. Hosted/act acceptance belongs to the manager. The manager must build and validate the current-dev merge candidate (source base `f4c9ad4f`, live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`) and publish builder/native receipts at the merge turn. Neither the candidate nor the conflict the author reports against the live `dev-soft-core` `a68536fa` (`split_soc.py`, `ctrl_service_budget/README.md`; `receipts/scope/merge-check.txt`) was validated here. If that resolution adds a stage to every flash access, every S4 figure moves, and the lenses whose artifacts change must be covered again at the resolved head.
- Physical calibration NOT RUN. Field skips and simulated media waits are not hardware proof.
- T_svc remains 10 ms at this base; the approved 20 ms belongs to S2b and is not a finding here.
- Full parent, processor, gPTP, Yosys and builder banks were not rerun. There were no source fixes, commits, pushes, GitHub writes, Docker/act runs or hardware runs. Disposable trees are only under packet `scratch/`, which is not published.
- Merge still needs a second independent positive review, the candidate and workflow acceptance, explicit maintainer merge authorization, and post-merge containment. Issue #665 is broader than S4.

R738-3 FINISHED
