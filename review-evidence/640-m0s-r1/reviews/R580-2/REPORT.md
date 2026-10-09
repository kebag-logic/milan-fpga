[R580] NEGATIVE - exact head d10aee62100c7407a86e13e7d54b20ab9050a448

# R580-2: internal cleared-context re-review of PR #702 (Relates to #640, lane M0s step 2, round 2)

- Head `d10aee62100c7407a86e13e7d54b20ab9050a448`, tree `ad7b2cab62ade20b75bfcf6362de5df286e979a2`.
- Delta reviewed: `bc89f84e..d10aee62`, three linear one-line commits with no trailers (`b1f110be`, `d4447e1b`, `d10aee62`). `bc89f84e` is retained with no rebase or amend. The delta touches 7 files: 5 under `syn/ooc/`, plus the recipe page, plus the mutant drivers.
- No RTL, firmware, workflow, baseline JSON or gitlink change. Pins are identical at base `7c1b52be` and head (`receipts/rtl_identity.txt`).
- Reconstruction order: AGENTS.md and CONTRIBUTING.md, then docs/README. Next, the #640 body, assignment 6086604096, STOP 6087021702, round-2 assignment 6087671877, REVIEW READY 6089317518 and ruling 6089329720. Then the PR body, the delta and the full diff from `7c1b52be`. Then public evidence: packet `6aae6d5f`, and R580-1's archived probes at `16b72cd1`.
- R580-1's report was read for its probe definitions after my own pass over the delta. R581-1's public review was read only after this verdict and ledger were drafted (`receipts/verdict_ledger_draft_pre_prior_findings.txt`). The verdict changed afterwards because of hosted exact-head evidence, not because of that review.

## Verdict summary

Both round-2 answers work as specified on the author's interpreter:
- **R580-1-F1 is resolved in code.** Under the default selection, an integrated route that is missing, duplicating or misplacing a control engine exits 2. Both `check` and `record --write` refuse it, naming each role, and the baseline bytes stay unchanged. This is shown by P3 unmodified, by an independent census-free probe on a real post-route report (94 of 94 cases), and by 24 of 24 published integrated reports passing.
- **R580-1-F2 is resolved in code.** The recipe self-test now requires exactly one marker naming the selection. A still-bound retained ROM with bad geometry is refused by image name. P1 unmodified detects B4 and B5.
- **P2 matches the manager's ruling.** The two fixture rows differ. All 210 legacy arm lines are IDENTICAL. Fuzz has 0 failures on both sides. Base and head code on the new fixture differ in exactly 17 of 3000 cases, each a refusal naming a control role.

One BLOCKER is open, found in hosted exact-head evidence:
- The new default-population self-test calls `record --write <directory>`.
- The hosted runner's system interpreter (CPython 3.12.3 on ubuntu-24.04) rejects that argument order.
- So `yosys-elaboration` fails at this head, and the required `rtl-fast` aggregate depends on it.
- I reproduced the failure locally under CPython 3.12.3. Round-1 `bc89f84e` passes on the same interpreter.

Tests is UNCLEAN. Conformance, RTL, Robustness and Docs are CLEAN.

## Findings

### R580-2-F1 - BLOCKER - Tests - the new default-population self-test fails on the hosted interpreter

- **Where:**
  - `syn/ooc/pp_placement_selftest.py:245-246`: `for command in (("check",), ("record", "--write")): result = cli(*command, *arguments)`, with `arguments = (folder, "--endpoint", ...)` (`:221`).
  - `:253-254` uses the same order for the split-census-present case.
  - The resulting argv is `record --write <directory> --endpoint ...`.
  - The gate parser has two `nargs="?"` positionals (`syn/ooc/pp_resource_gate.py:715-716`). The documented usage puts the directory first: `record <directory> --endpoint route-1x1 [--write]` (`:49`).
- **Evidence:**
  - Hosted job `yosys-elaboration`, run 37991906578 / job 114028099557, ran at exact head `d10aee62`. Step 9, "Prove the OOC read sets come from run.sh and refuse a bad one", failed. Its log reads: `pp_resource_gate.py: error: unrecognized arguments: /tmp/pp-placement-gate-.../all-fabric/gateware`, then `AssertionError: wrapper replaced record: wanted 2 / wrapper (KL_pp_shadow), got (2, ['exited through argparse'])` (`receipts/github/yosys_elaboration_job.log`, `yosys_elaboration_steps.tsv`).
  - The job has no Python setup step; it runs `ubuntu-latest` = ubuntu-24.04, whose system CPython is 3.12.3.
  - `rtl-fast` needs `yosys-elaboration` (`.github/workflows/rtl-fast.yml:297`).
  - Local reproduction, `receipts/probes/P9_*`:
    - CPython 3.12.3 at this head: `pp_resource_gate.py --selftest` gives rc 1 with the identical assertion, and `pp_resource_gate_mutants.py` gives rc 1 (`AssertionError: control: rc=1`).
    - The round-1 head `bc89f84e` self-test gives rc 0 on 3.12.3.
    - The head passes on CPython 3.12.13 and 3.14.7.
  - P10 (`receipts/probes/P10_cli_order.txt`) runs a wrapper-retaining F0-F4 fixture with no marker on all three interpreters:
    - In the documented order it exits 2, naming adp, both ACMP engines, srp and maap, with the baseline unchanged.
    - In the self-test's order on 3.12.3 it exits 2 only through argparse.
    - So the product refusal is correct and fails closed; the defect is the test's argument order.
  - The hosted run stopped there, so it executed neither the resource mutation campaign, nor `check-baseline`, nor the `dp_srcs --top` checks, nor steps 10-11 (`receipts/github/yosys_elaboration_executed.tsv`).
- **Impact:**
  - The required `rtl-fast` context cannot pass at this head, so the AGENTS section 7 bar ("current PR head has a successful rtl-fast verdict") cannot be met.
  - The round's validation claim ("28 local commands, all rc 0") holds only on the author's interpreter. On the CI interpreter, the F1 controls and the 191-mutant campaign do not run to completion.
- **Lenses:** Tests only. Not attributed:
  - Robustness: the parser is unchanged since base, and the product's documented order refuses correctly on every interpreter tried.
  - Conformance: the round-2 items are met in substance.
  - Docs: the gate docstring shows the working order.
- **Required outcome:** the gate self-test and the resource mutation campaign (control included) pass on the hosted interpreter. Either invoke `record <directory> ... --write` in the documented order, or make the CLI order-independent portably. No assertion may be weakened, and the role-naming and baseline-byte checks must still run for `record --write`.
- **Verification:**
  - Under CPython 3.12.3, `python3 syn/ooc/pp_resource_gate.py --selftest` gives rc 0 including the `placement gate:` lines, and `pp_resource_gate_mutants.py` reports all mutants detected.
  - Hosted `yosys-elaboration` and `rtl-fast` succeed at the new exact head.
  - Rerun P4 (`scripts/probe_default_population.py`) and P1 unmodified.

### R580-2-R1 - RESIDUE - Docs - PR body still requests a decision that has been made

- **Where:** PR #702 body, the "Known limitations" bullet "A manager decision is requested; see Round 2.", and the Round 2 bold lead "**Decision requested: P2 `fuzz` and self-test line prefix.**".
- **Evidence:** ruling 6089329720 (21:11Z) accepted the two fixture rows as an expected difference, after the body was written.
- **Impact:** wording only. No measurement, figure, verdict, test, code, generated artifact, conformance, clause or privacy claim changes.
- **Exact fix:**
  - Replace the bullet's last sentence with "The manager ruled this difference expected (#640 comment 6089329720); see Round 2."
  - Replace the bold lead with "**P2 `fuzz` and self-test line prefix (ruled expected in #640 comment 6089329720).**"
- **Verification:** read the published PR body. The manager carries this to the residue checklist. Docs stays CLEAN.

### R580-2-S1 - SUGGESTION - Tests - the "printed record is not judged" contract has no control

- **Where:** `syn/ooc/pp_resource_gate.py:763-764` and docstring `:21-23`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:237`.
- **Evidence:** P8 mutant M1 makes the gate judge a printed `record` too, and it survives the gate self-test (`receipts/probes/P8_population_mutants.tsv`). The other six P8 mutants are detected.
- **Impact:** low, because the path writes nothing. A later change could alter documented behaviour with no failing test.
- **Optional change:** add a control that prints a record of a wrong-population route with exit 0.

## Prior findings at this head

| Finding | Status at d10aee62 | Evidence |
|---|---|---|
| R580-1-F1 (MINOR) default selection checks no population | RESOLVED in code; its new controls are subject to R580-2-F1 on the hosted interpreter | See the F1 evidence below |
| R580-1-F2 (MINOR) marker and retained-ROM guards untested | RESOLVED | See the F2 evidence below |
| R580-1-S1 (SUGGESTION) | Partly adopted; remainder optional | See the S1 evidence below |
| R580-1-S2 (SUGGESTION) census breadth | Not adopted, with reason (placement belongs to the integration lane); stays optional, not retained as a finding | Plan removal table unchanged |
| R581-1-R1 (RESIDUE) PR-body status sentence | RESOLVED | The PR body Status now reads "The author completed this work locally before publication." (`receipts/github/pr702.json`) |

R580-1-F1 evidence:
- P3 unmodified (`P3_probe_marker.log`): the three base-defect cases now exit 2 with `baseline_changed=False`.
  - At head the fixture names the full shipping population. P3's unmarked cases are therefore refused first by the census-present rule, and the SRP case also names srp.
- P4 (independent, no census, no marker): 94 of 94 as expected, on the synthetic fixture and on the published route-1x1 post-route report. It covers:
  - the wrapper-retaining F0-F4 shape, also with a mailbox added;
  - SRP removed;
  - each role absent, duplicated or excess;
  - the wrapper subtree removed.
- `receipts/census_published.tsv`: 24 of 24 distinct published integrated reports pass. These are 22 routed plus 2 integrated 8x8 synthesis reports, which subsumes the author's 23. The 8 standalone reports are excluded by design.
- `check-baseline` gives rc 0. The baseline JSON blob is `6a65d8c4`, 27,995 bytes, sha256 `cf2eec5c...`, at base, round 1 and head (`receipts/baseline_identity.txt`).

R580-1-F2 evidence:
- P1 unmodified: 29 of 34 detected, including B4 and B5.
- The recipe campaign detects 45 of 45 with the control passing, both locally and in the hosted step.
- P7 (CLI): each split script carries exactly one marker naming its selection, and the default carries none. A short or narrow bound ROM is refused naming the image under all three selections.

R580-1-S1 evidence:
- B1, B6 and G10 are now detected (P1).
- G13 and B9 are caught by both campaign drivers (`P6_hook_skip_drivers.txt`).
- G1, G3 and G8 still survive. R580-1 classed them as equivalent or partly equivalent; they stay optional.

## Executed evidence (local, exact head)

Interpreter: CPython 3.14.7 unless stated. Pinned Markdown venv in packet scratch. `TMPDIR` in scratch, no bytecode. The commands are recorded in `scripts/run_r580_2.sh`, with raw logs and rc files under `receipts/gates/` and `receipts/probes/`.

| Job | rc | Result |
|---|---:|---|
| `pp_baseline.py --selftest` | 0 | includes the selection-marker and retained-ROM line |
| `pp_baseline_mutants.py` | 0 | control + 45 detected; the control asserts the placement recipe controls ran |
| `pp_resource_gate.py --selftest` | 0 | 260 arms + 500 cases, then 117 placement lines |
| `-X cpu_count=10 pp_resource_gate_mutants.py` | 0 | all 191 mutants fail |
| `pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| `pp_baseline_reports_selftest.py`, `ooc_tcl_selftest.py` (58 arms), `dp_srcs` self-test + both tops (35 arms), `scripts/pp_srcs.py --check --selftest` | 0 | |
| `docs_check.py`, doc style + selftest, doc paths, DOC_MAP, feature status, module matrix, `gen_toc.py --check` / `--verify-anchors` | 0 | 0 findings; 459 anchors |
| `check_em_dash.py --base 7c1b52be` | 0 | 176 added lines, 339 of 339 arms |
| `check_py_idiom.py`, `check_hygiene.py`, `measure_fail_fast.py`, `measure_naming.py`, `measure_test_evidence.py` (`--check`) | 0 | ratchets PASS |
| `git diff --check 7c1b52be HEAD` | 0 | |
| CPython 3.12.3 (hosted interpreter): gate self-test / gate campaign | 1 / 1 | R580-2-F1 |
| CPython 3.12.3: round-1 gate self-test; head recipe self-test | 0 / 0 | |

Probes:
- P1, P2 and P3 are R580-1's scripts, unmodified.
- P4-P10 are this round's (`scripts/`).
- P2 against ruling 6089329720:
  - 18 of 20 IDENTICAL, covering every recipe variant, `check-baseline`, both legacy records and the legacy check.
  - `fuzz 3000 seed 234` and the self-test lines are DIFFERENT, as ruled.
  - The 212 non-tally legacy lines (210 arms, the arm summary, the CARRY4 line) are IDENTICAL in order (`receipts/probes/P2x/legacy_arm_compare.txt`).
  - Fuzz shows 0 failures at both 3000 and 500 cases, on base and head.
  - P5 compares base and head gate code on the head fixture: 17 of 3000 cases differ. All are route-hierarchy mutations (14 truncate, 2 delete line, 1 swap), going from base exit 0 to head exit 2. Each refusal names the control role that was removed or duplicated (`P5_fuzz_cases_compare.txt`, `P5b_fuzz_reasons.txt`).
- Probe provenance (`receipts/probe_provenance.txt`):
  - Exactly one `probe_parity.py` exists in the public refs and at head. Its bytes equal R580-1's manifest entry (`d34043ad...`), as do those of `probe_marker.py` and `probe_mutants.py`.
  - No edited P2 probe is in the tree or the published evidence. The author's round-2 raw evidence is not published.

Hosted exact-head snapshot (`receipts/hosted_checks_final.tsv`, 21:24Z):
- Executed and successful: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, Verilator shard 3/5, and Yosys shards 0-3/4.
- `yosys-elaboration` FAILED (R580-2-F1).
- In progress: `docs-check`, `elaborate`, `firmware-unit`, and Verilator shards 0, 1, 2 and 4.
- Skipped, not executed: Physical gPTP (nightly and manual).
- The aggregates were not yet emitted. The manager owns hosted and act acceptance.

Tree integrity after the probes (`receipts/tree_integrity.txt`):
- HEAD and `write-tree` both give `ad7b2cab`.
- The stage-0 index equals the HEAD tree (1240 entries, mode/oid/path), and the 10 PR files' blob bytes and modes match.
- There are no untracked or ignored files. One reviewer-created `syn/ooc/__pycache__` was removed.
- The three required submodules are clean at `2ad2f845` / `5dce647a` / `48ff7a7e`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6087671877 items 1-2 against `syn/ooc/pp_placement.py:34-48,88-107` and `syn/ooc/pp_resource_gate.py:259,273-277,349-350,763-775`; P3; P4 (94/94, real route-1x1 report); census over 24 published integrated reports; P2 against ruling 6089329720; baseline JSON byte identity; P7 | R580-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| RTL | CLEAN | No hdl/ or gitlink delta (`receipts/rtl_identity.txt`); all 11 census module names declared in RTL (parent or pinned processor); published post-route hierarchy rows match each name once, with the own-row `(instance)` format the census skips (`baseline_hierarchy.rpt` of 645-r1 author-r2f route-1x1) | R580-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Robustness | CLEAN | P4 absent/duplicate/excess/subtree/mailbox cases under `check` and `record --write` with baseline bytes; census-present refusal; identity-first ordering (`pp_placement_selftest.py:259-264`); fuzz 3000 with 0 failures both sides; P5/P5b 17 cases; P10 documented-order refusal on 3.12.3, 3.12.13 and 3.14.7; unknown module renames fail closed (recipe page :241-243) | R580-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Tests | UNCLEAN (R580-2-F1) | `syn/ooc/pp_placement_selftest.py:29-42,107-118,154-188,217-277,342-346`; `pp_resource_gate_mutants.py:284-300,338`; `pp_baseline_mutants.py:26-34,136`; both campaigns (45, 191); P1 29/34; P6; P8 6/7; hosted job 114028099557; CPython 3.12.3 reproduction (P9) | R580-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |
| Docs | CLEAN (R580-2-R1 is RESIDUE) | `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:186-191,232-239,283-286`; `docs/design/MARK_II_AREA_PLAN.md:656-663`; `docs/design/AREA_BUDGET.md:370-374`; gate docstring `:21-23,49`, all checked against code and probes; docs gates rc 0; PR body | R580-2 | d10aee62100c7407a86e13e7d54b20ab9050a448 |

## Real limits

- No Vivado run. The default census was validated against published hierarchy reports and synthetic fixtures. No split export exists (the STOP is unchanged), so no selected route was measured.
- Hosted contexts listed as in progress were not awaited. The `rtl-fast`, `verilator-suites` and `yosys-portability` aggregates were not emitted at fetch time.
- CPython 3.12.3 was obtained into packet scratch only, to reproduce the hosted interpreter. This assumes the hosted job uses the image's system `python3`, consistent with the absence of any setup step and with the identical failure.
- No builder bank, lint_rtl or HDL simulation was run: there is no RTL delta, and the full banks are out of scope. Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank ran at this head, and none is inferred.
- R580-1's archived packet has 7 receipt or script entries whose bytes differ from its own manifest. This is consistent with path scrubbing at publication. The three probe scripts used here match.
- Earlier rounds stand for files unchanged in this delta: `pp_baseline.py`, the plan and the budget page.

## Pending manager duties

- Route R580-2-F1 to the author. Re-review Tests, plus any lens whose scope the fix touches, at the new exact head.
- Carry R580-2-R1 to the residue checklist.
- Hosted and act acceptance at the corrected head, including `rtl-fast`, `verilator-suites` and `yosys-portability`.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn and publish its receipts.
- Collect the second independent positive review and a consolidated ledger.
- Merge only with maintainer authorization, then post-merge containment.

R580-2 FINISHED
