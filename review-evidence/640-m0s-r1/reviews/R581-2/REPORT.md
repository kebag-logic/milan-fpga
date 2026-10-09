[R581] NEGATIVE - exact head d10aee62100c7407a86e13e7d54b20ab9050a448

# R581-2: external independent review of PR #702 (Relates to #640, lane M0s step 2, round 2)

- Head `d10aee62100c7407a86e13e7d54b20ab9050a448`, tree `ad7b2cab62ade20b75bfcf6362de5df286e979a2`. Base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`; this round reviews the delta `bc89f84e..d10aee62` (commits `b1f110be`, `d4447e1b`, `d10aee62`). Earlier rounds stand for files this delta does not touch.
- The delta changes seven files: `syn/ooc/pp_placement.py`, `pp_placement_selftest.py`, `pp_resource_gate.py`, `pp_resource_gate_selftest.py`, `pp_resource_gate_mutants.py`, `pp_baseline_mutants.py` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`. There is no RTL, firmware, workflow, accepted-baseline or submodule-pin change.
- Reconstruction order: AGENTS.md and CONTRIBUTING.md, then docs/README. Next the #640 body and every manager and owner comment, including assignment 6086604096, the round-2 assignment 6087671877, REVIEW READY 6089317518 and the P2 ruling 6089329720. Then the plan, budget and recipe pages, the diff and history, the published packet at `6aae6d5f`, and the PR body. I read the prior review reports (R580-1, R581-1) only after my own pass over the delta, and only to take their probes and resolve their findings.

## Verdict summary

The round-2 code does what the assignment asks:
- Under the default selection, an integrated route that is missing, duplicating or misplacing a control engine exits 2, naming each role.
- R580-1's probe P3, rerun unmodified, gives exit 2 for each case it previously accepted, and the baseline bytes are unchanged.
- The recipe self-test now pins the split marker and the present-ROM geometry refusal. R580-1's probe P1, rerun unmodified, reports B4 and B5 DETECTED.
- P2 meets the manager's ruling.
- The accepted baseline is byte-identical to the base, and `check-baseline` passes.

One MAJOR finding is open. The new all-fabric self-test calls the gate's command line with `--write` before the directory. Older Python argument parsers reject that order, and the hosted runner uses one. So `pp_resource_gate.py --selftest` fails on the hosted runner, and the exact-head hosted `yosys-elaboration` job **failed**. That job feeds the required `rtl-fast` aggregate. The author's validation ran only on a newer interpreter, which accepts the order.

Tests and Robustness are UNCLEAN. Conformance, RTL and Docs are CLEAN; Docs carries one wording RESIDUE.

## Findings

### R581-2-F1 - MAJOR - Tests, Robustness - the new default-population self-test fails on the hosted interpreter

- **Where:**
  - `syn/ooc/pp_placement_selftest.py:245-246`: `for command in (("check",), ("record", "--write")): result = cli(*command, *arguments)`.
  - `syn/ooc/pp_placement_selftest.py:253-254`: the same order in the split-census arm.
  - Both build `record --write <directory> --endpoint ...`. The documented usage, `pp_resource_gate.py:49`, is `record <directory> --endpoint route-1x1 [--write]`.
- **Authority:**
  - AGENTS.md section 7: the current PR head must have a successful `rtl-fast` verdict. `.github/workflows/rtl-fast.yml:294-297` makes the `rtl-fast` aggregate depend on `yosys-elaboration`.
  - AGENTS.md section 6, Robustness: configuration-dependent behaviour.
  - Round-2 assignment 6087671877 asks for a planted control that runs.
- **Evidence:**
  - Hosted run 37991906578, job 114028099557 (`receipts/hosted/yosys_elab_job.log`) ran on ubuntu-24.04, whose system `python3` is 3.12.3. Its step "Prove the OOC read sets come from run.sh and refuse a bad one" failed:
    - `pp_resource_gate.py: error: unrecognized arguments: /tmp/pp-placement-gate-.../all-fabric/gateware`
    - `AssertionError: wrapper replaced record: wanted 2 / wrapper (KL_pp_shadow), got (2, ['exited through argparse'])`
  - The round-1 head `bc89f84e` passed the same job (`receipts/hosted/round1_head_checks.tsv`).
  - Local reproduction on CPython 3.11.15, which has the older argument parser like the runner's 3.12.3:
    - `receipts/py311/argparse_order_repro.log` shows `record --write <dir> ...` rejected by the parser, while `record <dir> ... --write` parses.
    - The unmodified head's gate self-test fails the same way (`receipts/py311/gate_selftest_py311.log`, rc 1).
  - CPython 3.14.7 and 3.12.13 accept both orders (`receipts/py312/`, `receipts/head/`), which is why the author's 28 local commands passed.
  - Fix-scope control. In a disposable copy (`receipts/py311/order_fix_probe.diff`), only those two calls were changed to the documented order. Under 3.11 the gate self-test, the recipe self-test, the recipe campaign (45 of 45) and the gate campaign (191 of 191) then all pass (`receipts/py311/fixcopy_*`). No other incompatibility was found.
- **Impact:**
  - The required `rtl-fast` verdict cannot succeed at this head.
  - On the hosted runner, the F1 `record --write` refusal controls never run: the arm fails at argument parsing, before any population is judged.
  - The PR's "every command exits zero" validation claim fails under the CI interpreter. The gate code itself is correct, and the documented CLI order parses on every interpreter tested.
- **Required outcome:**
  - The all-fabric and split-census arms invoke the CLI in an order every supported interpreter parses, such as the documented `record <directory> ... --write`.
  - The gate self-test, both campaigns and `yosys-elaboration` pass on the hosted runner's interpreter at the new head.
  - Optional: run the placement self-tests under the CI interpreter locally before handoff.
- **Verification:**
  - Exact-head hosted `yosys-elaboration` and `rtl-fast` succeed.
  - `pp_resource_gate.py --selftest` passes under a CPython with the older parser (for example 3.11.x, or the runner's 3.12.3), including the `wrapper replaced record` and `all-fabric with a split census record` arms.

### R581-2-R1 - RESIDUE - Docs - the PR body still requests the P2 decision the manager has given

- **Where:** PR #702 body, the "Known limitations / out of scope" bullet "Two rows of the first review's parity probe ... A manager decision is requested; see Round 2", and the Round 2 heading "Decision requested: P2 `fuzz` and self-test line prefix."
- **Authority/evidence:** the ruling 6089329720 accepts the two fixture rows as an expected difference.
- **Impact:** wording only. No measurement, figure, verdict, test, code, generated artifact, conformance or clause claim changes, and no privacy rule is touched.
- **Exact fix:**
  - Replace "A manager decision is requested; see Round 2." with "The manager accepted them as an expected difference (#640 comment 6089329720); see Round 2."
  - Retitle "Decision requested: P2 `fuzz` and self-test line prefix." to "Ruled (6089329720): P2 `fuzz` and self-test line prefix."
- **Verification:** inspect the published body. This residue leaves Docs CLEAN.

## Prior findings at this head

| Finding | State at d10aee62 | Evidence |
|---|---|---|
| R580-1-F1 (default population) | **Resolved in code and docs.** Its control's portability is the new R581-2-F1. | `pp_placement.py:88-107`, `pp_resource_gate.py:273-277,349-350,764-767`. P3 rerun unmodified (`receipts/r580-1-probes/probe_marker.tsv`): the three formerly accepted default cases now exit 2 with `baseline_changed=False`; the SRP case names `srp (KL_srp_top)`. Independent real-report probe (below): 11 cases x 3 commands, 0 failures. Recipe line 191 and the new paragraph at 232-239 match the code; plan line 659 and budget line 370 are now accurate. |
| R580-1-F2 (recipe guards untested) | **Resolved.** | `pp_placement_selftest.py:110-115` (exactly one marker naming the selection, accepted by `selection()`, refused as all-fabric) and `:172-188` (still-bound ROM kept in the inventory, depth and width refused naming the image). P1 rerun unmodified: B4 and B5 DETECTED (`receipts/r580-1-probes/probe_mutants.tsv`). Recipe campaign 45 of 45 includes both. |
| R580-1-S1 (survivors, hooks) | **Adopted.** | B1, B6 and G10 are DETECTED in P1. G13 and B9 still survive P1, which runs self-tests directly, but each campaign driver now fails on them: `receipts/hook-drivers/g13_gate_driver.log` and `b9_recipe_driver.log` both raise "the control passed without running the placement ... controls", rc 1. P1's remaining survivors (G1, G3, G8) are the equivalent or partly equivalent ones R580-1 named. |
| R580-1-S2 (census breadth) | **Retained as optional SUGGESTION, not adopted.** The author's rationale (the integration lane owns those blocks' placement) is consistent with scope. | PR body, Round 2. |
| R581-1-R1 (PR Status wording) | **Resolved.** | The PR body's Status now reads "The author completed this work locally before publication." |

## Round-2 assignment checks

**F1. Default selection.**
- The census reads the hierarchy report's module column. It skips own rows and accepts an exact name or `__parameterizedN`. Each role must be at its `limits("all-fabric")` count (`pp_placement.py:39-40`).
- `check` and `record --write` refuse after the kind and identity comparison, naming each role, and a split census left in a default directory is refused too. A printed `record` judges nothing, as documented at recipe line 237 and in the module docstring.
- Standalone endpoints are excluded (`misplaced()`, `pp_resource_gate.py:275`).

Evidence:
- **P3, unmodified:** the wrapper-retaining F0-F4 export with no marker gives `check` exit 2 and `record --write` exit 2, with the baseline unchanged. P3's fixture keeps a full hierarchy, so the refusal reason there is the stray census. The all-fabric export with SRP removed gives exit 2 naming `srp (KL_srp_top)`.
- **Independent real-report probe** (`scripts/f1_real_report_probe.py`, `receipts/f1_real_report_probe.log`). It uses the published accepted `route-1x1` hierarchy report (686 evidence `bf6bd3a1`, r2-48f12dc1) inside the self-test's measurement directory.
  - The unchanged report passes `check` (exit 0) and `record --write` (exit 0).
  - These cases exit 2 on `check` and `record --write`, naming every expected role, with the baseline unchanged:
    - SRP removed;
    - wrapper-retaining F0-F4: ADP, both ACMP engines, SRP and MAAP;
    - ADP duplicated;
    - talker module renamed;
    - mailbox present;
    - processor MAAP present;
    - gPTP removed;
    - AECP and notify removed;
    - every role but the wrapper removed.
  - Specialised `__parameterized` names are accepted. In total, 33 command runs gave 0 failures.
- **Census on 32 published hierarchy reports** (`scripts/census_real_reports.py`, `receipts/census_real_reports.log`). My independent count agrees with the head's `all_fabric_problems()`.
  - All 23 integrated reports pass with zero problems: routed 1x1, synthesized and routed 8x8, and the accepted route-1x1 reports. Each holds exactly one wrapper, ADP, listener, talker, SRP, parent MAAP, AECP, notify and gPTP, and no mailbox or processor MAAP.
  - The 9 standalone reports (design `KL_pp_shadow`) would fail the census, which is why they are excluded.
- **Comparability:**
  - `pp_resource_baseline.json` is unchanged from the base (sha256 `cf2eec5c...e41`, empty base..head diff).
  - `check-baseline` gives rc 0, `baseline PASS: 3 endpoints`.
  - P2 recipe rows (14) and gate rows `check-baseline`, `record` (route, ooc) and `check` against the real record are all IDENTICAL.

**F2. Tests.**
- The marker assertion and the bound-ROM geometry refusal exist and run: `pp_baseline.py --selftest` rc 0, also under 3.11 and 3.12.13.
- P1, unmodified: 29 of 34 detected, including B4 and B5, with the control passing.

**P2, against ruling 6089329720:**
- 18 of 20 rows are IDENTICAL. The two DIFFERENT rows are `fuzz 3000 seed 234` and `legacy self-test lines` (`receipts/r580-1-probes/probe_parity.tsv`).
- All **210 legacy arm lines are IDENTICAL** base vs head, and so are both summary lines (`resource gate CARRY4 ...` and `260 arms and 500 generated cases`). The differing lines are only seeded fuzz tallies. Comparison done in scratch; method in "Executed evidence".
- **Fuzz has zero failures on both sides:**
  - self-test fuzz (500 cases): 0 and 0;
  - `--fuzz 3000 --seed 234`: base 0, head 0, and a hybrid (base gate code on the head fixture) 0.
- **Base and head code on the new fixture differ in exactly 17 of the 3,000 generated cases** (`receipts/p2-ruling/compare.log`). All 17 are route `baseline_hierarchy.rpt` mutations: 14 truncate, 2 delete line and 1 swap lines. In each, the head exits 2 naming roles whose count changed, where the base code exited 0.

**Edited P2 probe.**
- None exists in the clone (tracked, untracked or ignored), in the base..head history, or on the `640-m0s-review-evidence` branch (`receipts/integrity/probe_presence.txt`).
- The evidence holds only R580-1's original, git blob `89b4637b`, sha256 `d34043ad...21ac`, equal to its published manifest. That is the copy I ran. The P1 and P3 scripts also equal their manifest digests (`receipts/r580-1-probes/probe_scripts.sha256`).

## Clean lenses

```text
[R581] PASS Conformance - syn/ooc/pp_placement.py:88-107; syn/ooc/pp_resource_gate.py:253-277,333-351,760-777; receipts/r580-1-probes/{probe_marker,probe_parity}.tsv; receipts/f1_real_report_probe.log; receipts/p2-ruling/compare.log - round-2 F1/F2 items against assignment 6087671877 and ruling 6089329720: default population refused by role after identity, record --write refused, baseline byte-identical, check-baseline rc 0, P2 per ruling
[R581] PASS RTL - syn/ooc/pp_placement.py:19-40 against 32 published Vivado hierarchy reports (receipts/census_real_reports.log); git diff --raw bc89f84e..d10aee62 (no hdl/, firmware or gitlink change) - all-fabric role counts match every integrated 1x1 and 8x8 shipping image, and module identities are unchanged
[R581] PASS Docs - docs/testing/PP_SHADOW_BASELINE_RECIPE.md:191,232-239,283-286; docs/design/MARK_II_AREA_PLAN.md:659; docs/design/AREA_BUDGET.md:370; syn/ooc/pp_resource_gate.py:21-23; PR #702 body - statements checked against the code and probes; docs_check, TOC check/anchors, em-dash --base 7c1b52be (339/339 arms), doc style, doc paths all rc 0; one wording RESIDUE (R581-2-R1)
```

Tests and Robustness are not clean (R581-2-F1). Everything else under those lenses was applied and found sound:
- Robustness: own rows, specialisation suffix, impostor names, duplicate, absent and extra roles, stray census, identity-first ordering, standalone exclusion and the fail-closed missing root.
- Tests: the head self-tests, both campaigns (45/45 and 191/191), P1 and the hook drivers.

## Executed evidence (this round, exact head, local)

The environment: `TMPDIR` inside packet scratch; host CPython 3.14.7; the pinned Markdown venv (cmarkgfm 2025.10.22, html5lib 1.1) for the TOC and em-dash gates; user-local CPython 3.12.13 and 3.11.15 for the interpreter checks. Independent jobs ran concurrently, each with its own log and rc file.

| Job | rc | Result |
|---|---:|---|
| `pp_baseline.py --selftest` | 0 | placement Tcl, selection marker, ROM and endpoint refusals PASS |
| `pp_baseline_mutants.py` | 0 | control + 45 detected |
| `pp_resource_gate.py --selftest` | 0 | 260 arms + 500 cases; placement gate PASS (CPython 3.14.7) |
| `-X cpu_count=12 pp_resource_gate_mutants.py` | 0 | 191 mutants fail |
| `pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| `pp_baseline_reports_selftest.py` / `ooc_tcl_selftest.py` | 0 / 0 | PASS / 58 arms |
| `scripts/pp_srcs.py --check --selftest` | 0 | |
| `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` | 0 | 0 findings / 201 md |
| `gen_toc.py --check`, `--verify-anchors` | 0 | 141 pages / 459 links |
| `check_em_dash.py --base 7c1b52be` | 0 | 176 added lines, 339/339 arms |
| `check_py_idiom.py`, `check_hygiene.py --check` | 0 | ratchets at budget |
| `git diff --check 7c1b52be HEAD` | 0 | |
| R580-1 P1 / P2 / P3, unmodified | 0 / 0 / 0 | 29/34 incl. B4, B5 / 18 IDENTICAL + 2 per ruling / F1 cases now exit 2 |
| `scripts/f1_real_report_probe.py` | 0 | 0 failures |
| `scripts/census_real_reports.py` | 0 | 23 integrated pass; 9 standalone excluded |
| `scripts/p2_ruling_check.py` + `p2_compare_cases.py` | 0 | 0 failures x3; 17 differing cases |
| G13 / B9 campaign drivers on mutated copies | 1 / 1 | drivers refuse the skipped hook |
| head gate self-test, CPython 3.11.15 | **1** | R581-2-F1 reproduced |
| order-fixed copy, CPython 3.11.15 (4 suites) | 0 | fix scope confirmed |

The 210-line comparison: base and head `--selftest` outputs, with temporary names normalised and `resource gate fuzz` and `placement` lines removed, are equal in 212 lines. Those are 210 arm lines and two summaries. The full per-case fuzz logs (about 1 MB each) are kept in scratch, with their digests in `receipts/p2-ruling/cases_digests.sha256`.

Hosted exact-head checks (`receipts/hosted/exact_head_checks_2.tsv`, fetched 2026-10-09T21:29:59Z):
- Executed and successful: bdd-conformance, changes, docs-check, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, Verilator shard 3/5, Yosys shards 0-3/4.
- **Failed:** yosys-elaboration (R581-2-F1).
- In progress: elaborate, firmware-unit, Verilator shards 0, 1, 2 and 4. The `rtl-fast` aggregate had not yet reported, and it depends on the failed job.
- Skipped context, not executed: Physical gPTP (nightly and manual).

Integrity after the probes (`receipts/integrity/`):
- HEAD, `HEAD^{tree}` and `git write-tree` are all `ad7b2cab...`.
- All 1,235 tracked non-gitlink entries match their blob bytes and modes. There are no stage-nonzero entries, and the index equals the HEAD tree.
- Gitlinks: `protocol-processor 2ad2f845`, `gptp-processor 5dce647a` and `verilog-axis 48ff7a7e`, each at its own top level and clean. `external efeb541a` and `lwSRP 9197193e` are uninitialised and unchanged.
- Bytecode caches written into `syn/ooc/__pycache__` by this round's isolated-mode runs were removed. Afterwards the worktree, including ignored files, is empty.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6087671877 and ruling 6089329720 against `pp_placement.py:88-107`, `pp_resource_gate.py:253-277,333-351,760-777`; P2 and P3 unmodified; real-report probe; baseline digest and `check-baseline` | R581-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| RTL | CLEAN | No hdl, firmware or gitlink delta; role identities and counts against 32 published Vivado hierarchy reports (1x1, 8x8, routed, synthesized, standalone) | R581-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Robustness | UNCLEAN (R581-2-F1) | Census parsing (own rows, suffix, impostor, duplicate, absent, extra, stray census, missing root, identity first); interpreter-dependent CLI parsing (`receipts/py311`, `receipts/py312`, hosted job log) | R581-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Tests | UNCLEAN (R581-2-F1) | `pp_placement_selftest.py:110-115,143-188,217-277`; both campaigns (45/45, 191/191); P1 29/34; G13 and B9 drivers; hosted `yosys-elaboration` failure; order-fixed copy under 3.11 | R581-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Docs | CLEAN (RESIDUE R581-2-R1) | `PP_SHADOW_BASELINE_RECIPE.md:191,232-239,283-286`; `MARK_II_AREA_PLAN.md:659`; `AREA_BUDGET.md:370`; gate docstring; PR body; docs gates rc 0 | R581-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |

## Real limits

- No Vivado run was made. The default census was judged on published Vivado hierarchy reports and on synthetic fixtures, not on a new measurement. No integrated split export exists, which is consistent with the route STOP.
- The author's round-2 receipts are not published on the evidence branch. Round-2 source-head execution evidence is the REVIEW READY comment's table plus this packet's own runs. No manager source bank ran at this head, and none is inferred.
- The runner's exact interpreter (Ubuntu 24.04 `python3` 3.12.3) was not run locally. The failure was reproduced on CPython 3.11.15, which shares the older argument parser, and its hosted occurrence is taken from the job log.
- Hosted contexts in progress at fetch time were not awaited. Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Return R581-2-F1 to the author. Re-review the corrected head in Tests and Robustness, at minimum, with exact-head `yosys-elaboration` and `rtl-fast` green.
- Carry R581-2-R1 to the residue checklist.
- Accept the hosted exact-head contexts and the local replica.
- Collect the second independent verdict, consolidate the ledger, and validate the current-dev merge candidate (builder and native banks) at the merge turn.
- Merge only with maintainer authorization. This PR does not meet or close #640's 38,040-LUT acceptance.

R581-2 FINISHED
