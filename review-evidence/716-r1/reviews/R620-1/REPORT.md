[R620] POSITIVE - exact head f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48

# R620-1: internal cleared-context review of PR #724 (Issue #716)

- Head: `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`, tree `6fab4d33da2dfeb5c349911088b17d40e23b81f3`.
- Source base `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. Live dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0` was not built here; the manager builds it at the merge turn.
- Commits reviewed: `b27c5537b` and `f41e4f2dd`, both with `ci:` subjects.
- Diff reviewed: 5 files, +538/-46. They are `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`, `sw/firmware/ctrl/test/test_ctrl_firmware.py`, the new `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py`, and `docs/testing/CI_WORKFLOWS.md`.
- Reconstruction order:
  1. AGENTS.md and CONTRIBUTING.md (required contexts, lines 55-65).
  2. docs/README.md.
  3. Issue #716: body, assignment comment 6107547907, TAKEN, and REVIEW READY.
  4. REQUIREMENTS.md REQ-VER-04.
  5. The diff and history.
  6. Public evidence tree `3dff3266:review-evidence/716-r1` and the PR #724 comments.
- Prior public review findings on PR #724: none exist. The PR has 0 reviews and 0 review comments, and its only issue comments are the manager's item-2 table and the review-start notice. There is nothing to resolve or retain.
- Verdict: no BLOCKER, MAJOR or MINOR finding. There are two RESIDUE items (wording only) and one SUGGESTION. All five lenses are clean.

## Judged points (the assignment's focus list)

| Point | Result | Evidence |
|---|---|---|
| Command census keeps every original command and its `if` gating, adding only shard arguments | Met | Two censuses agree. (1) The PR's generator: `ci_events.py --firmware-census` returns rc 0 with `"preserved": true` (`receipts/firmware-census.json`). (2) My own independent census, which does not import `ci_events.py` (`scripts/independent_census.py` → `receipts/independent-census.json`). It parsed the base and head YAML and compared (command, job if, step if, env, continue-on-error, shell, working-directory, cache `with`). Nothing is missing or added after stripping a trailing ` --shard N/4`. The shard arguments are exactly {0/4, 1/4, 2/4, 3/4}, and the only head lines not in base are those four driver commands. The census baseline `FIRMWARE_BASE_STEPS` (`scripts/ci_events.py:2401`) equals the base workflow's firmware-unit set (16 = 16 rows). The census itself collapses jobs, so on its own it cannot tell four copies of `--shard 0/4` apart. The exact step-list contract closes that gap: probes `wf-control-job-runs-shard0` and `wf-srp-job-runs-shard2-duplicate` both fail `--check` (`receipts/probes.txt`). |
| Each discovered suite lands in exactly one shard; the check fails on none or two; planted mutants fail it | Met | `test_ctrl_firmware_shards.py:136-159` compares the multiset of live invocations, per shard, with the unsharded default. It passes standalone (`receipts/shards-selftest.log`: 844 invocations, shard sizes [59, 472, 75, 238]). It also runs inside every sharded hosted job (`test_ctrl_firmware.py:264-266`; `receipts/hosted-attempt10-excerpts.txt`, all four jobs). The built-in mutants (missing suite, duplicate suite) fail it. My extra probes also fail it: shard mode skipping SRP if1, skipping pin controls, halving the control table, AECP in two shards, and losing the SRP phase. Each failure is an `AssertionError` from the inventory comparison, with an unmodified-tree control passing (`receipts/probes.json`). |
| A future suite is discovered automatically | Met | Built-in case: an injected suite from `run_suites` lands in shard 0. Real-source probe `future-endstation-shape`: adding `configs/endstation_r620_probe.yaml` to the probe tree raised the inventory from 844 to 849, with shard 0 going from 59 to 64. The check stayed green and no ownership list was edited. |
| Coverage ratchet keeps thresholds and suites, unsplit | Met | `git diff base..head -- sw/firmware/gtest` is empty. `coverage()` (`test_ctrl_firmware.py:202-224`) is unchanged and is returned at line 263, before any shard handling. `--shard` together with `--coverage` refuses (lines 253-255; self-test refusal case). The coverage step is unchanged in firmware-unit, and its removal is caught by both `--check` and `--firmware-census` (probes `wf-unit-drops-coverage-check*`). Local `fw_coverage.py --selftest` gives 28/28, and `--check --jobs 16` gives PASS (30 files) (`receipts/fw_coverage-*.log`). The hosted attempt-10 firmware-unit log also shows PASS (30 files). |
| rtl-fast aggregate requires every new job | Met | `rtl-fast.yml:403` `needs` and lines 408-437 (env and loop) name all four jobs. Probes catch each of these: dropping a job from `needs`, dropping a loop pair, and rebinding an env source. The required context stays `rtl-fast`, so no ruleset change is needed (CONTRIBUTING.md:55-58). |
| `ci_events.py` pins the layout | Met | `check_firmware_layout` (`scripts/ci_events.py:3589`) checks the census, each 45-minute timeout and each policy budget row. Per-job `RTL_STEP_LISTS` pins exact steps. `--check` passes with 1944 items, and `--selftest` passes with 2672 arms, including the 10 new firmware-layout arms (`receipts/ci_events-selftest.log:275-284`). Probes also fail `--check` for: a job `if: false`, a 60-minute timeout, an added step, a step `if`, `continue-on-error`, and a raised budget row. |
| CI_WORKFLOWS.md records each job's budget | Met | `docs/testing/CI_WORKFLOWS.md:75-80` has a table row per job (45 min / 1890 s / 1620 s), and the contract pins these rows. |
| No build-output cache | Met | Each of the four jobs has one cache step: `~/br-milan-rv32/host` with the unchanged digest key, identical to base (independent census `head_cache_paths == base_cache_paths`). Probe `wf-control-adds-build-output-cache` fails `--check` (step count and order). |
| Item 1: steps that cost the time are measured and named | Met | Evidence `HOSTED-SUMMARY.md` and `HOSTED-SUITES.md` (17 jobs). I spot-checked the base job 114339840343 against the API (`receipts/base-job-114339840343-steps.txt`): step 8 control 1882 s, step 9 saved-state 103 s, step 10 coverage 255 s, matching the author's figures exactly. |
| Item 2: slowest of 10 consecutive hosted runs ≤ 70 % of each job's own timeout | Met | `scripts/actions_attempts.py` → `receipts/actions-38162821680.{txt,json}`. Run 38162821680 attempts 1-10 are all `pull_request` at head `f41e4f2dd56e`. All 40 firmware job conclusions are success, every firmware step concluded success, and `rtl-fast` succeeded in every attempt. All 40 durations equal the manager's table (comment 6113578810) and the PR body's table. The slowest is 841 s (attempt 2, `firmware-control-mutants`) = 31.1 % of 2700 s, against a bound of 1890 s. Every timeout is still 45 minutes. |
| Issue item 3 | Met | Covered by the layout-pinning and budget rows above. |

## Findings

### R620-1-RES1: stale CI prose in files this PR touches

- Severity: RESIDUE.
- Lenses: Docs.
- Locations and exact fixes:
  - `.github/workflows/rtl-fast.yml:242-243`: the comment above `firmware-unit` still says it runs "plus the control mutation campaign". Fix: replace that phrase with "while the three mutation jobs below run the campaigns (#716)", or delete the phrase.
  - `docs/testing/CI_WORKFLOWS.md:2333-2335`: the text says host suites run locally "as `firmware-unit` runs them … the required RV32 control build and its `--self-test` mutation campaign". Fix: "as the four firmware jobs run them together".
  - `docs/testing/CI_WORKFLOWS.md:86`: "Issue #716 records measurements and the hosted acceptance table." Measurements are on #716, but the hosted 10-run table is on PR #724 (comment 6113578810 and the PR body). Fix: "Issue #716 records measurements; PR #724 records the hosted acceptance table." The other option is for the manager to cross-post the table to #716.
  - `docs/testing/CI_WORKFLOWS.md:83`: "below 60%". The assignment says "at most 60 %". Fix: "at most 60%".
- Evidence: the head contents at the lines cited above, read against the head workflow, where `firmware-unit` runs only `--shard 0/4`.
- Impact: a reader is pointed at the wrong job or the wrong record. No measurement, check, test, generated artifact or verdict changes. `docs_check`, `check_doc_style` and `gen_toc --check` are green at head.
- Required outcome: the wording is corrected, or carried on the residue checklist.
- Verification: re-read the lines, then rerun `ci_events.py --check`, `docs_check.py` and `check_doc_style.py`.

### R620-1-RES2: stale single-job CI descriptions outside the assignment's permitted file set

- Severity: RESIDUE.
- Lenses: Docs.
- Locations and exact fixes:
  - `sw/firmware/gtest/README.md:398-411` currently reads: "`rtl-fast`'s `firmware-unit` job … runs … the ctrl gate"; "`scripts/ci_events.py` pins the job's steps"; "The control gate includes lwSRP, SRP and its mutation campaign". Fix: name the four firmware jobs, say that `firmware-unit` runs the normal ctrl suites, saved-state, tally and coverage while the three mutation jobs run the control, AECP and SRP campaigns, and say that `ci_events.py` pins all four.
  - `sw/firmware/ctrl/README.md:336` currently reads: "The CI firmware step also requires the control mutation campaign." Fix: "The `firmware-control-mutants` job runs the control mutation campaign (#716)."
- Evidence: docs/README.md:90 routes "Run or extend the firmware's host unit tests" to that harness page. The assignment's STOP clause confines the lane to the listed files, and neither README is in that list, so the executor could not edit them without a STOP.
- Impact: wording only. Nothing reads these lines as a contract.
- Required outcome: the manager either authorizes the edits in a follow-up or carries them on the residue checklist.
- Verification: re-read the lines, then rerun `docs_check.py`.

### R620-1-S1: the shard inventory observes invocations, not participation in the verdict

- Severity: SUGGESTION.
- Lenses: Tests.
- Location: `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:47-99`. The stand-ins always pass and `report` is patched to `False`.
- Evidence: two probes in `receipts/probes.json` stay green by design and are recorded as observation-point limits.
  - `limit-shard-mode-discards-one-suite-outcome`: in shard mode the arm is still invoked, but its outcome is popped before `report`.
  - `limit-shard-mode-ignores-aecp-verdict`: in shard mode the AECP campaign's return value is ignored.
- The head itself is correct. `scripts/verdict_probe.py` → `receipts/verdict_probe.txt` (rc 0) shows that, for every shard, the all-passing stand-ins give a green verdict and a single failing suite, control, AECP, SRP if2, SRP if1 or pin entry gives a red one. `main` maps that to exit 1 (`test_ctrl_firmware.py:180-199,277-278`).
- A separate note: the check is written with `assert`, so a `python3 -O` or `PYTHONOPTIMIZE` invocation would disable it. The hosted commands use neither.
- Impact: none at this head. A future edit that discards one shard's result without dropping the call would pass the shard check. It would need code conditional on `args.shard`.
- Suggested change (optional): let the stand-ins return a failure for one chosen entry per phase, and require `run_selected` to be true for exactly the owning shard. Also consider raising explicitly instead of using `assert`.
- Verification: the two limit probes above turn into failures.

## Lens results (each with the artifact examined at the exact head)

- `[R620] PASS Conformance — Issue #716 items 1-3 and assignment 6107547907; receipts/actions-38162821680.{txt,json}, receipts/independent-census.json, receipts/firmware-census.json, receipts/base-job-114339840343-steps.txt, docs/testing/CI_WORKFLOWS.md:59-97, CONTRIBUTING.md:55-65 — each acceptance item and assignment bullet was checked against API data or an independent recomputation (table above).`
  - Item 2 matches the manager's 10-run table exactly, with the slowest at 841 s = 31.1 % of 2700 s.
  - The pre-review prediction bullet was met as stated: the slowest prediction was 879 s ≤ 1620 s.
  - Against the hosted maxima, the conservative predictions were low for three jobs: firmware-unit 703 s versus 631 s, AECP 260 s versus 256 s, and SRP 625 s versus 608 s. They were high for the slowest job: control 841 s versus 879 s. That is prediction error only. Acceptance is the hosted 70 % ceiling, and every job met it with wide margin.
  - All five changed files are inside the permitted set. No STOP condition applies: there are four jobs, and the slowest indivisible phase (control, 841 s hosted) is under 1890 s.
- `[R620] PASS RTL — git diff --stat ac2c5e77..f41e4f2d (no .sv/.v/HDL file), .github/workflows/rtl-fast.yml:247-437 job graph, sw/firmware/ctrl/test/test_ctrl_firmware.py:123-199,235-278 driver interface — no HDL, CDC, FSM, width or clock artifact is in scope, so the lens was applied to the architecture and interface contracts.`
  - Default invocation: unchanged, with the same order (suites, then control, AECP, SRP if2, SRP if1 and pins, as at base).
  - `--slice` and `--mutation-shard`: unchanged.
  - Coverage entry point: unchanged and evaluated before shard handling.
  - A `Refusal` from a campaign now returns 2 instead of propagating. Both outcomes are nonzero.
  - Each new job has `needs: changes`, the same `if`, a 45-minute timeout, and `runs-on: ubuntu-latest`. No artifacts cross job boundaries.
  - Resource effect: setup is repeated three more times, about 40 s of runner time per job. That is understood and is not a correctness issue.
- `[R620] PASS Robustness — receipts/probes.{txt,json} (26 probes on a disposable copy of the head tree), receipts/verdict_probe.txt, test_ctrl_firmware_shards.py:112-133 refusal cases, ctrl_mutants.py:555-571 and srp_mutants.py:864-890 catch criteria — malformed, boundary, ordering and configuration paths.`
  - Malformed shard arguments refuse with exit 2: `0/0`, `0/3`, `4/4`, `-1/4`, `x/4`. Narrowing combinations also refuse: `--coverage`, `--slice`, `--mutation-shard`, and `--shard` without `--self-test`.
  - Within one run, a failed normal suite still stops the mutations.
  - Across jobs, the mutation shards now run even when shard 0 fails. That is acceptable for two reasons. The aggregate fails on any failed or cancelled job. And a mutant counts as caught only when its named test fails with its own diagnostic, so a broken baseline reads as ESCAPED, not caught.
  - `--check` refuses each of these: a job gated off, a step gated off, `continue-on-error`, a raised timeout, an added cache, and a wrong env binding.
  - A docs-only change skips all four jobs together (same `if`, pinned).
- `[R620] PASS Tests — receipts/shards-selftest.log, receipts/ci_events-selftest.log:275-284, receipts/probes.json, receipts/shard{0,1,2,3}.{log,rc}, receipts/shard-summary.txt, receipts/fw_coverage-*.log, receipts/gates.txt, receipts/hosted-attempt10-excerpts.txt — new checks fail for their claimed defects; real shards pass locally and hosted.`
  - Every new `ci_events` arm is caught.
  - The shard check fails on all seven dispatch defects planted by the self-test and by me.
  - Locally, with the pinned SDK (fresh verified install) and four concurrent shards at `--jobs 4`, all four `--shard i/4` runs exit 0:
    - shard 0: 309 s, 59 suite arms.
    - shard 1: 936 s, 471 of 471 mutants caught.
    - shard 2: 219 s, AECP controls plus 74 defects.
    - shard 3: 638 s, 169 SRP-if2 and 68 SRP-if1 defects plus 2 pin controls.
  - Hosted attempt 10 shows the same verdicts in all four jobs.
  - The touched gates are green: `ci_scope --selftest`, `check_py_idiom` and its self-test, `check_em_dash --base` and its self-test, `gen_toc --check`, `check_doc_style`, `docs_check` and `git diff --check`.
  - SUGGESTION S1 records the inventory's observation point. It does not leave the lens unclean.
- `[R620] PASS Docs — docs/testing/CI_WORKFLOWS.md:40-97,2333-2360, sw/firmware/ctrl/test/test_ctrl_firmware.py:86-89, PR #724 body, sw/firmware/gtest/README.md:398-411, sw/firmware/ctrl/README.md:336 — the changed contract (four jobs, budgets, shard semantics, census, unsplit coverage, SDK-only cache) is recorded in the authoritative policy page and pinned by the contract.`
  - The PR body's 10-run table matches the API in all 40 cells, and `Closes #716` is present.
  - Stale wording is recorded as RES1 and RES2 (RESIDUE, wording only). Under the owner rule of 2026-10-02 that does not leave the lens unclean.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #716 body and assignment; Actions API run 38162821680 attempts 1-10; independent and PR census; base job 114339840343 steps; CI_WORKFLOWS.md:59-97; CONTRIBUTING.md:55-65 | R620-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| RTL | CLEAN | diff stat (no HDL); rtl-fast.yml:247-437 job graph; test_ctrl_firmware.py:123-199,235-278 interface | R620-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Robustness | CLEAN | 26 probes (receipts/probes.json); verdict probe; refusal cases; mutant catch criteria | R620-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Tests | CLEAN | shard self-test; ci_events self-test arms; four local shard runs; coverage self-test and check; touched gates; hosted attempt-10 logs | R620-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Docs | CLEAN (RES1, RES2 carried as residue) | CI_WORKFLOWS.md; driver docstring; PR body; gtest and ctrl READMEs | R620-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |

## Real limits

- No manager source bank exists at this head, and none is claimed or inferred. Source-head execution evidence here is my own focused runs, the author's published receipts, and the hosted run.
- I did not build the current-dev merge candidate (base ac2c5e77, live dev cfadd767).
- I did not run the full parent, PP, gPTP, Yosys or builder banks; that is not allowed in this round.
- I did not run the default unsharded `test_ctrl_firmware.py` invocation. Its equivalence to the union of the shards rests on the inventory comparison and on code reading.
- I did not run `test_ctrl_nvm.py`, `tally_selftest.py`, `fw_rv32_selftest.py` or `ci_rv32_sdk_selftest.py` locally. They are unchanged, and their hosted steps concluded success in all 10 attempts.
- Local toolchain: GCC 16.2.1, GoogleTest 1.18.0, CPython 3.14.7. Hosted toolchain: GCC 13.3.0, GoogleTest 1.14.0. Local shard wall times came from four concurrent runs on a 16-CPU host and are not a hosted prediction.
- I downloaded and inspected hosted job logs for attempt 10 only. For attempts 1-9 I used API job and step conclusions and durations.
- No Docker, act, `act_ci` or hosted dispatch was used. Hosted and act acceptance belong to the manager.
- Physical calibration was NOT RUN. Field skips are not hardware proof, and no hardware was involved.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts on the PR.
- Obtain the external review (R621) and its separate verdict.
- Carry RES1 and RES2 to the residue checklist, and decide whether the README edits in RES2 may be authorized.
- Own hosted and act acceptance, the complete local bar under CONTRIBUTING.md, the merge authorization, post-merge containment, and moving #716 to Done.

## Restoration

- The probes edited only a disposable `git archive` copy under `scratch/`.
- The review clone ends at HEAD `f41e4f2dd56e…`, with the index tree equal to the HEAD tree (`6fab4d33…`) and `git diff --quiet HEAD` returning 0. There are no untracked or ignored files.
- All five gitlinks are unchanged. `third_party/lwSRP` was initialized at its pin `9197193e` for the runs and then deinitialized back to its original state (`receipts/restore-verify.txt`).

R620-1 FINISHED
