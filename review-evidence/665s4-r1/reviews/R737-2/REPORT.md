[R737] POSITIVE - exact head 4d9b901cd42fb21ac7c05432b88bb6c00061064a

# R737-2: internal independent delta review of PR #812 (issue #665, S4, round 4)

Head `4d9b901cd42fb21ac7c05432b88bb6c00061064a`, tree `605f043b826040650960b98b9392bf8da5ebdcc1`, source base `f4c9ad4f`. The delta reviewed is `ac45db8f..4d9b901c`: two commits, `75126928b8` and `4d9b901cd4`. They change three files only: `tb/verilator/nvm_split_target/run.py`, `target_selftest.py` and `README.md`. Code the delta does not touch keeps its prior lens verdict (R737-1 at `ee1c0be0`, R738-2 at `ac45db8f`), because nothing it depends on changed.

No open BLOCKER, MAJOR or MINOR. One RESIDUE and three new SUGGESTIONs are recorded below. Three earlier SUGGESTIONs are retained.

## 1. Scope reconstructed from public state

- The S4 round-4 assignment on #665 (issuecomment-6514339158) accepts the MINOR R738-F2 from R738-2 (issuecomment-6514335214). The finding: `run.py` wrote `results.json` before checking clock provenance and never removed an existing table, so a refused run in a reused output directory left an earlier run's success `table.md` beside a new, refused record.
- The frozen required outcome has five parts:
  - a refused run (exit 2) leaves no table that looks current and successful;
  - the accepted `results.json`/`table.md` are one validated run's (validate first, then write both);
  - a diagnostic failure record is allowed if it cannot be mistaken for an accepted one;
  - new same-directory success-then-refusal tests cover a missing build clock, a wrong build clock and misconverted results, and the fresh-directory controls stay;
  - the self-test and its mutants are re-run, both points are regenerated at CPU 50 MHz / bus 100 MHz, and the step-bound and D5 controls are unchanged.
- No RTL change, and new commits go on top of `ac45db8f` with no rebase.
- The authorities used are CONTRIBUTING/AGENTS (lenses, completion bar, comment rule) and the target harness README's output contract.
- Requirement clauses FR_NFR 3.4.1/3.4.2 and the option (c) owner decision are not touched by this delta. Their lens verdicts stand from the earlier rounds.

## 2. Delta examined

The current code (`run.py:242-326`):

- `clear(out)` unlinks `results.json`, `table.md` and `refused.json`. `main` calls it inside the `try` at `run.py:315`, after `out.mkdir` and before any build. Any later failure therefore starts from an empty pair.
- `accept(out, rec, specs)` (`run.py:253-262`) runs `against_build` first, then `table(rec)`, which runs `provenance` (missing clocks or misconverted figures). Only after both pass does it write `results.json`, then `table.md`.
- `refuse(out, words, rec)` (`run.py:265-273`) clears again, so it also covers a pair half-written by an OSError in `accept`. It then writes `refused.json = {refused: words, record: rec | null}`. If that write fails with an OSError, it says so on stdout instead of raising.
- `main` (`run.py:313-326`) sets `rec = None`. Every caught refusal (RuntimeError, OSError, ValueError) calls `refuse` and returns 2.

Taken together, R738-F2's write-before-validate ordering and its stale table are both removed at their cause.

The self-test (`target_selftest.py:194-295, 600-687`):

- `main_run` now takes a reusable `root` and reads back `refused.json`.
- `reused_checks()` adds seven checks:
  - four success-then-refusal arms in one directory: a build without its CPU clock, builds that disagree, clocks not the builds', results misconverted;
  - one refusal-then-success arm;
  - a direct `accept` check (it writes nothing for a refused record);
  - a direct `refuse` check (it removes a pair already written).
- `refused_alone` requires all of these: exit 2, no `results.json`, no `table.md`, the refusal's words in `refused`, and no `cpu_hz`/`sys_hz`/`results` key at the top of the file.
- Five mutants are added to `MUTANTS`. The fresh-directory `run.py` checks in `clock_checks()` remain (`target_selftest.py:339-349`), now also requiring neither file.

Docs: README:43-53 (output contract), README:263-269 (self-test requirements) and README:300-304 (mutant table). The `run.py` and `target_selftest.py` module docstrings also changed.

Comment rule: added lines in the delta were scanned for bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. None found. Source comments cite `#665` only.

## 3. Independent execution at the exact head

All of these ran in the foreground, in this clone, with Python 3 under `-I` where untrusted paths were read (`receipts/python-version.txt`). No simulator or native build was run, because the delta is Python-only. The simulation compiler was therefore not used, and its identity check did not apply.

- **Target self-test** (`receipts/target-selftest.log`): `python3 -B tb/verilator/nvm_split_target/run.py --self-test` gives `checks: 73   failures: 0`, rc 0. That is 48 ordinary checks and 25 mutants, and the 25 include the five new reuse mutants and the D5 removal mutant. The count matches the author's `gates-short/nvm_target_selftest.log` (73, rc 0).
- **Reviewer mutation probes** (`probe_reuse.py`, `receipts/reuse-probes.log`, rc 0). These patch in memory only; no file was written.
  - P1: the previously reviewed `main` from `ac45db8f` is restored into the head module. All four success-then-refusal checks fail, plus the refusal-then-success check and both fresh-directory `run.py` refusal checks. **The new tests detect the exact R738-F2 defect.**
  - P2: removing only `main`'s initial `clear` makes the refusal-then-success check fail.
  - P3: removing `main`'s `refuse` call makes all four success-then-refusal checks fail.
  - P4: `accept` without `against_build` makes both "not its builds'" checks fail.
  - P5: `accept` writing `table.md` before validating makes the direct `accept` check fail.
  - P6: a success, then a crash outside the caught classes (planted `KeyError`). No pair and no refusal is left, because the initial `clear` already ran.
  - P8: after a success, a misconverted run leaves a `refused.json` whose top keys are exactly `record` and `refused`. The refused record is nested, at CPU 62.5 MHz.
  - P7 (informational): a success, then a usage error (an unknown case) exits 2 through argparse before `--out` is touched. The earlier accepted pair is left untouched; see S1.
- **Published figures re-rendered** (`receipts/checkout-integrity.log`, first section). Each of the round-4 author `target-1x1/results.json` and `target-8x8/results.json`, run through the head's `run.table`, reproduces its published `table.md` byte for byte, with `provenance` empty.
- **Round-3 identity** (`receipts/round3-identity-check.log`). In the published MANIFEST, the round-4 target 1x1/8x8 `results.json`/`table.md` and both budget tables carry the same sha256 as the round-3 ones. The output regeneration therefore changed no figure.
- **Scope** (same log):
  - `ac45db8f..HEAD` changes exactly the three files above;
  - `f4c9ad4f..HEAD` changes no `.sv/.v/.svh/.vh` file and no gitlink (its `sw/` Python/README changes are earlier rounds' and untouched here);
  - all six gitlinks are listed, the five populated submodules sit at their pins with no dirty entries, and `external` remains unpopulated.
- **Checkout integrity** (same log). All 1,470 tracked blobs hash to their index entries, the index equals the HEAD tree (`605f043b…`), executable modes are intact, and `git status` shows no entry. No tracked restoration was needed.

## 4. Public evidence verified

- `verify_public.py` (`receipts/public-verification.log`) fetched 29 round-4 author receipts from the immutable evidence commit `efd9f61c563776a3db0306e5abc4ff6537df695e`. All 29 match `MANIFEST.json` `published_sha256`, with 0 mismatches.
- That commit is **unsigned** (verification reason `unsigned`). Hash consistency is verified; signer authentication is not claimed.
- Gate summaries: `scope/HEAD.txt`, `gates-short/HEAD.txt`, `gates-long/HEAD.txt` and `gates-long-rest/HEAD.txt` all name `4d9b901c…`.
  - Short gates: "0 of 97 gates nonzero or left the tree dirty", and `nvm_target_selftest` is rc 0.
  - Long gates: "0 of 11 gates nonzero or left the tree dirty". These are builder_require_rv32, ctrl_nvm, ctrl_firmware, fw_coverage(_selftest), nvm_cosim(_lint), publication_census, firmware_boundary(_verilator) and ctrl_memory, all rc 0 and clean.
  - The long-gate receipt set includes `nvm_cosim-cut-by-host-reset.log`. `nvm_cosim` was re-run in `gates-long-rest`, rc 0.
  - These are author source executions, not manager banks and not reviewer reruns.
- Real-build refusals (`probes/real-refusal-1x1.log`, `-8x8.log`). On the fresh real builds, deleting `cpu_hz` from the capture build's record makes `--regrade` return 2 and leaves only `refused.json` (top keys `record`, `refused`). After the record is restored, the regrade returns 0 and leaves `results.json` and `table.md` byte-identical to the fresh run. Both probes report PROBE PASS.
- `probes/reuse-probe.log`: round 3 shows STALE OUTPUT in all five sequences and the checkout shows SOUND. `probes/reuse-mutant-failures.txt` lists every check each round-4 mutant fails, and each one fails its named check.
- Regenerated points:
  - `target-1x1/run-tail.log` and `target-8x8/run-tail.log` are RC=0, with every case passing and all five controls caught.
  - The slow-step control is rejected at 30.2216 ms (1x1) and 30.2139 ms (8x8) against T_svc 10.0 ms. Every phase's at-T_svc and one-over step control is caught.
  - In `build-clocks.txt`, all seven arms record 50,000,000 / 100,000,000 Hz.
  - Both `results.json` carry `cpu_hz` 50,000,000 and `sys_hz` 100,000,000 with 11 results, all passed, and each `table.md` has three clock lines.
- D5: `d5-plant/plant_d5_removed.log` shows the unplanted run at rc 0. With the 24.5 ms check removed, it fails with "OFF timing limit was ignored" (PLANT CAUGHT).
- Hosted state (`receipts/hosted-check-runs.txt`): at this exact head there are 0 check runs, 0 status contexts and 0 workflow runs. The PR is not a draft, its base is `dev-soft-core`, and GitHub reports `mergeable: CONFLICTING`.
  - No hosted job is inferred.
  - The author's `scope/merge-check.txt` shows a clean merge onto `5b5f4336` and conflicts onto `a68536fa` in `tb/verilator/ctrl_service_budget/README.md` and `split_soc.py`. Neither file is in this delta. This is recorded as a manager duty, not as a source-head finding.

## 5. Findings

**R737-2-R1 | RESIDUE | Tests, Docs | `tb/verilator/nvm_split_target/target_selftest.py:201-203` | `main_run` docstring broken mid-sentence.**
Evidence: line 202 ends "... ({} or '' for each it did not leave). graded_at" and line 203 continues "plants a CPU clock ...". This is a re-wrap artefact in a docstring the delta added; it changes no behaviour.
Exact fix: re-wrap so that "graded_at plants a CPU clock for the grading, planted the run's clocks, other than the builds', and builds an arm's recorded clocks in place of cpu_hz and sys_hz." reads as one sentence after "...for each it did not leave)."
Verification: read the docstring.

**R737-2-S1 | SUGGESTION | Robustness, Docs | `run.py:301-306`; README:43-53 | A usage error exits 2 without touching `--out`.**
Evidence: P7. A success followed by `--cases no-such-case` exits 2 through argparse and leaves the earlier accepted pair in place. That pair is still one validated run's, with no mixed record and no new write, so the frozen outcome is met. The `run.py` docstring, though, says "2 = a build or an input failed", and a reader of `--out` cannot tell that a later invocation was rejected.
Optional outcome: either say in the README that a usage error is not a run and leaves `--out` as it was, or resolve `--out` and clear it before argument validation.

**R737-2-S2 | SUGGESTION | Tests | `target_selftest.py:600-687` | Main-level ordering mutants are only probed, not committed.**
Evidence: `_refuse_kept` and `_accept_unvalidated` are caught only by the direct unit checks. Through `main`, the layered `clear` in `refuse` masks both, as `reuse-mutant-failures.txt` also shows. The main-level property itself is caught by the existing checks under P1 (the round-3 `main` restored) and P2/P3. Those mutants are not in `MUTANTS`.
Optional outcome: add a committed mutant restoring the write-before-validate `main`, plus one dropping `main`'s initial `clear`, so the self-test keeps guarding the whole sequence rather than each helper.

**R737-2-S3 | SUGGESTION | Docs | `tb/verilator/nvm_split_target/README.md:52` | "alone in their place".**
Evidence: correct for the pair. However, the earlier run's per-case `.txt`, `.journal.in`, `.journal.out` and `.log` files stay in `--out` by design, because `--regrade` reads them (README:40). "Alone" could be read as the only file in `--out`.
Optional wording: "A refused run leaves `refused.json` in the pair's place (`run.refuse`); the cases' recorded scripts, journals and logs stay for `--regrade`."

## 6. Prior public findings, reconciled after the independent pass

| Prior ID | Disposition at `4d9b901c` |
|---|---|
| R738-F2 (MINOR; Conformance, Robustness, Tests, Docs) | **Resolved at its cause.** The pair is cleared before any build and written only after `against_build` and `provenance` pass (`run.py:246-262,313-324`). A refusal leaves only `refused.json`, which has no top-level clock or result key. Same-directory tests cover the three required refusal classes plus disagreeing builds, and fresh-directory controls are retained. They fail on the round-3 `main` (P1). Real 1x1/8x8 regrade refusals leave only `refused.json`, and restored regrades reproduce the published pair byte for byte. Both points were regenerated at 50/100 MHz with no figure change, and the step and D5 controls are unchanged. README:43-53 and 263-269 match the code. |
| R738-F1 (MINOR) | Remains resolved. `clocks`, `record`, `against_build`, `provenance` and `table` are unchanged; the delta only moves the `against_build`/`table` calls into `accept`, in the same order. The published tables re-render byte for byte. |
| R737-1-R1 (RESIDUE, Docs) | Remains resolved: `docs/ARCHITECTURE_HW_SW_SPLIT.md:223` names CPU 50 MHz and bus 100 MHz, and docs are untouched by the delta. |
| R737-1-S1 (SUGGESTION) | Remains resolved: results and tables carry their clocks. |
| R737-1-S2 (SUGGESTION, Tests/Robustness) | Retained, optional. Map-placement and map-clock negative controls are still absent; those files are untouched. |
| R737-1-S3 (SUGGESTION, Robustness) | Retained, optional. `sw/firmware/ctrl_nvm/plat/gen_flash_port.py:246` `base % size` is still unguarded for a zero size; it is untouched. |
| R737-1-S4 (SUGGESTION, Tests) | Retained, optional. The target self-test is still not referenced by `.github` or `scripts/suite_shards.py` (it runs in the author's short gates); workflows are untouched. |

PR #812 has no submitted reviews and no review-thread comments. No other prior finding was found.

Independence note: the round-4 assignment quotes R738-F2 as the scope, and the R738-F2 paragraph and its disposition table were read as part of that scope before this pass. No other reviewer's report at this head was read; the R738-3 start comment was seen by its first line only.

## 7. Lens coverage at this head

```text
[R737] PASS Conformance - run.py:242-326; README:43-53; issuecomment-6514339158 required outcome - every clause of the frozen R738-F2 outcome checked against code, probes P1-P8 and real-build refusal receipts; points regenerated at 50/100 MHz unchanged
[R737] PASS RTL - git diff --name-only ac45db8f..4d9b901c (three Python/Markdown files); f4c9ad4f..HEAD has no HDL or gitlink change - inapplicable to the delta; the R737-1 baseline at ee1c0be0 and R738-2 at ac45db8f stand unchanged
[R737] PASS Robustness - run.py:246-273,313-324; probes P2-P8 - pre-build clear, validate-then-write, half-written pair removal, refusal-write failure path, uncaught crash leaves nothing stale; usage-error path noted as S1 (optional)
[R737] PASS Tests - target_selftest.py:194-295,600-687; receipts/target-selftest.log (73/0); receipts/reuse-probes.log - each new check and mutant fails on the defect it names, and the restored round-3 main is caught; S2 optional
[R737] PASS Docs - README:43-53,263-269,300-304; run.py and target_selftest.py docstrings; live PR body - match the code and the self-test labels; R1 residue and S3 wording optional
```

## 8. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-4 required outcome; run.py:242-326; README:43-53; real refusal and regenerated point receipts; probes P1-P8 | R737-2 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| RTL | CLEAN | Delta file list; f4c9ad4f..HEAD HDL/gitlink scan; unchanged RTL/firmware baseline | R737-2 (delta, inapplicable); baseline R737-1 at ee1c0be0, R738-2 at ac45db8f | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Robustness | CLEAN (S1 optional) | run.py clear/accept/refuse/main; probes P2-P8; real-build missing-clock regrades | R737-2 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Tests | CLEAN (R1 residue, S2 optional) | target_selftest.py reused_checks, main_run, five mutants; self-test 73/0; probe P1 against the round-3 main | R737-2 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |
| Docs | CLEAN (R1 residue, S3 optional) | README output contract, self-test and mutant table; module docstrings; live PR body; comment-rule scan of the delta | R737-2 | 4d9b901cd42fb21ac7c05432b88bb6c00061064a |

## 9. Real limits

- No simulator, native build, campaign or bank was run by this review. The real 1x1/8x8 regenerations and real-build refusals are the author's published receipts, verified by hash and spot-checked, not re-executed. Reviewer execution is the portable self-test, in-memory mutation probes and re-rendering of the published records.
- The evidence commit `efd9f61c` is unsigned. Hashes match its MANIFEST; signer authentication is not claimed. Large logs were read by summary and tail only.
- There is no manager source bank at this head, and none is claimed or inferred.
- No hosted job ran at this head (0 check runs, 0 contexts). The PR is CONFLICTING against its current base.
- Physical calibration is NOT RUN. Field skips and simulated flash waits are not hardware proof.
- T_svc is the 10 ms value at this base, and the approved 20 ms belongs to S2b. F1 has no total capture bound (option (c)). D5 stays on the current writer. None of these is a finding here.

## 10. Pending manager duties

- Resolve the base conflict reported by GitHub (`mergeable: CONFLICTING`; the author's merge-check names `ctrl_service_budget/README.md` and `split_soc.py` against `a68536fa`). Then build the final current-dev candidate (source base `f4c9ad4f`, live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`, not present in this clone and not validated here), and publish builder/native receipts on the PR.
- Own hosted and local workflow acceptance at the candidate head.
- Carry R737-2-R1 to the residue checklist. The SUGGESTIONs S1-S3 and the retained R737-1-S2/S3/S4 are optional.
- Obtain the second independent positive review, then follow explicit merge authorization and post-merge containment. Issue #665 is broader than S4.

## 11. Receipts

These are listed in `MANIFEST.sha256`:

- **Scripts:** `verify_public.py`, which fetches and hash-checks public receipts read-only; and `probe_reuse.py`, which runs in-memory mutation probes as `python3 -I probe_reuse.py CHECKOUT OLD_RUN_PY`, where `OLD_RUN_PY` is from `git show ac45db8f:tb/verilator/nvm_split_target/run.py`.
- **Receipts:** `receipts/public-verification.log`, `receipts/target-selftest.log`, `receipts/reuse-probes.log`, `receipts/round3-identity-check.log`, `receipts/checkout-integrity.log`, `receipts/hosted-check-runs.txt` and `receipts/python-version.txt`.

Disposable copies stay under `scratch/` and are not published. No source fix, commit, push, GitHub write, Docker/act, hardware, shared install or other-checkout edit was made.

R737-2 FINISHED
