[R446] NEGATIVE - exact head b5894838d6c47180ac4169e7d52dd746f461af21

# R446-3 internal review: issue #234 / PR #638, round 3

- Head `b5894838d6c47180ac4169e7d52dd746f461af21`, tree `c2f454c490913470a1609bb66a9e82aa89c395a7`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`. The round-3 delta is `0feff20f..b5894838`: four one-line commits with no trailers, 6 files (`receipts/r3-commits.txt`).
- Rebuilt from public state, in this order:
  - AGENTS.md and CONTRIBUTING.md;
  - the issue body, the lane assignment (5966260488), the takeover, REVIEW READY rounds 1 to 3, the manager rulings (5967852698), the owner decision (5967924270), and the round-2 (5968015720) and round-3 (5968718943) assignments;
  - the full diff `1269cdaf..b5894838` and the round-3 delta;
  - the public evidence tree `43ad8362:review-evidence/234-r1`;
  - the live PR body, including its round-3 tables and the 61-site self-audit;
  - hosted check runs at the exact head.
- The real A and B measurement directories were read only for the gate's own inputs: the reports, the cell census and the route status report.
- This verdict, the findings and the ledger were written before any other reviewer's round-2 findings were read. My own round-1 and round-2 findings were judged after the independent pass. The resolution table for prior findings is at the end.
- The rulings and the owner decision were applied as given. None of them is counted as a defect.

Verdict: **NEGATIVE**. Three MINOR findings are open:

- **F1:** round 3 removed the round-2 finiteness check on the slack. A WNS or WHS of 309 or more integer digits now reads as infinity and passes.
- **F2:** an integer too large for a float in the baseline, or a route status count longer than the integer-text limit, still reaches a traceback and exit 1.
- **F3:** seven claimed refusals that the head does enforce have no arm, and the mutants relaxing them survive.

Everything else in round 3 holds: the validator's 25 classes, the route-row guards, the policy-pin arms, the ASCII-digit parsers, the unchanged hierarchy output, real data, the gates and the docs.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - `syn/ooc/pp_resource_gate.py:81`, `:137-142`, `:118-120`; PR body self-audit row 34 - a slack too long to be a finite float reads as infinity, and the route passes

- **Requirement/evidence:**
  - R446-1 F1 and round-2 item 1 (5968015720) required that a WNS or WHS of `inf` or `nan` is refused with exit 2.
  - Round 2 met this with `math.isfinite` after `float()` (`0feff20f:syn/ooc/pp_resource_gate.py`, `timing()`).
  - Round 3 replaced that check with `SLACK = -?[0-9]+\.[0-9]+` (`:81`, `:137`) and dropped `isfinite`. Self-audit row 34 records the change.
  - The regex bounds the characters but not the length. `float()` of a decimal with 309 or more integer digits returns `inf`.
  - `receipts/r3-probes/probe-r3-numbers.log` used a symlink copy of A's real route directory with only one report edited, against the shipped baseline with the input digest zeroed so that the candidate is judged. Each case went through the CLI:
    - WNS `1` followed by 400 zeros `.063`: **rc 0, `RESULT: PASS`**. The table prints `WNS_ns 0.063 inf inf ok` and "re-baseline recommended" (`receipts/r3-probes/wns-overflow-check-output.log`).
    - WHS of the same length: **rc 0, PASS**.
    - The negative WNS of the same length: rc 1 "MATERIAL REGRESSION" where the contract says 2.
    - Block RAM Tile `<401 digits>.5`, through the utilization `float()` at `:120`: rc 1 (ceiling exceeded) where the contract says 2 for an unreadable measurement.
    - Control: the unedited copy gives 0, and a finite WNS of 0.500 gives 0.
  - `record` of that directory prints `"WNS_ns": Infinity`, so `record --write` would put a non-finite value in the baseline. `load()` then refuses it.
  - No arm plants an overflowing slack. The arms at `_selftest.py:161-165` plant only `nan`, `inf` and other-script digits. The shipped mutant `finite slack` cannot find a missing `isfinite`.
- **Impact:**
  - A refusal that round 2 delivered is reopened by round 3. A non-finite WNS or WHS can pass the gate with exit 0.
  - The exit status is mislabelled for the negative and half-count cases.
  - No tool build prints such a figure today, so this is not an observed field failure. But the contract states that non-finite timing never passes, and round 2 had proven that.
  - The self-audit's row 34 claims a guard the code no longer has.
- **Required outcome:**
  - Every number the measurement parsers convert with `float()` (slack and the utilization half-count) is refused with exit 2 and a named reason unless it is finite. This means restoring the `isfinite` check or bounding the digits.
  - An arm plants an overflowing slack for WNS and for WHS, and an overflowing half count.
  - A mutant that removes the finiteness check is killed.
  - Self-audit row 34 states the guard as it holds.
- **Verification:** `probe_r3_numbers.py <checkout> <A route dir> <scratch>`. The four slack and BRAM-tile cases must give rc 2, and the controls must stay 0.

### F2 - MINOR - Conformance, Robustness, Tests, Docs - `syn/ooc/pp_resource_gate.py:424`, `:313`, `:339-342`, `:268-276`; `docs/design/AREA_BUDGET.md:189-196`; PR body self-audit preamble and rows 1-2, 50 - an oversized integer still reaches a traceback and exit 1

- **Requirement/evidence:**
  - Round-3 item 1 asked to "close the class". `AREA_BUDGET.md:189-190` and `:195` (and recipe `:468`) make the claims at issue:
    - `check` exits "2 for every input it cannot judge", and "no input reaches a traceback";
    - "NaN, Infinity or a number too large to be finite" exits 2.
  - **Baseline integers.** `load()` passes `parse_float=finite`, but JSON integers go through the default `parse_int` and are unbounded, up to the 4300-digit text limit.
    - A recorded route `WNS_ns` or `WHS_ns` written as a 401-digit integer passes `number()` and `check-baseline` (**rc 0, "baseline PASS"**).
    - `check` then subtracts the measured float from it in `verdict_for()` (`:341`) and dies with `OverflowError: int too large to convert to float`: **rc 1, traceback**.
    - A 1e400 decimal is refused correctly with rc 2 in both commands (control).
  - **Route status counts.** `routing()` maps `OSError` and `ValueError` only around `read_text()` and `findall()` (`:268-271`).
    - The `int(value)` at `:276` sits outside that `try`. A count of 4401 ASCII digits passes `COUNT` and then raises `ValueError: Exceeds the limit (4300 digits)`: **rc 1, traceback**.
    - The self-audit preamble says `routing()` maps `ValueError` to exit 2, and row 50 calls `COUNT.fullmatch` sufficient. Neither is true at this line.
  - The other report counts (utilization, timed endpoints, hierarchy) are inside `record()`'s `try`, so the same 4401-digit text exits 2 there.
  - Evidence: `receipts/r3-probes/probe-r3-numbers.log`, the cases "route status count of 4401 digits" and "baseline route WNS_ns/WHS_ns recorded as a 401-digit JSON integer".
- **Impact:**
  - A malformed baseline, or an unreadable route status report, is reported with the material-regression status 1 through a traceback. This is the R446-2 F3 / R447-2 MINOR 1 class at two sites the round-3 self-audit missed.
  - `check-baseline`, the hosted guard, passes the baseline case, so it would reach the merge bank as exit 1.
  - The trigger is a hand edit or a corrupted file, not a tool output.
- **Required outcome:**
  - In both commands, a baseline number that cannot be represented as a finite float exits 2 with a named reason. For example, `load()` bounds integers through `parse_int`, or `number()` requires the value to convert.
  - A route status count that `int()` cannot convert exits 2 with a named reason.
  - An arm covers each, and a mutant removing each guard is killed.
  - The self-audit preamble and row 50 state the guards as they hold.
- **Verification:** `probe_r3_numbers.py`. The three cases must give rc 2 in `check`, and the baseline cases rc 2 in `check-baseline`, with no traceback.

### F3 - MINOR - Tests - `syn/ooc/pp_resource_gate_selftest.py` (malformed-baseline arms `:335-382`, route arms `:174-196`, hierarchy arm `:243`); `syn/ooc/pp_resource_gate_mutants.py` - seven claimed refusals that the head enforces have no arm

- **Requirement/evidence:**
  - Round-3 item 1: "Self-test arms drive each class through `main()`, and each class has a killed mutant". Item 2: "Mutants relaxing either guard are killed".
  - The claims at issue are in REVIEW READY round 3 and the PR body:
    - "an identity with exactly the recorded keys";
    - "exactly the kind's recorded figures";
    - scopes of exactly the six counts;
    - "a sha256 hex input digest";
    - "`check` now refuses a baseline file in which any endpoint is malformed";
    - "exactly one ... `nets with routing errors` row";
    - every count cell of a hierarchy row (recipe `:242`).
  - `receipts/r3-probes/probe-r3-mutants.log` ran 20 partial-relaxation mutants against the shipped 181-arm self-test. The control passes, 11 are killed, and these **survive**:

    | Mutant (one unique span) | Claim it relaxes |
    |---|---|
    | identity: an extra key accepted (`:395`, equality to subset) | exactly the recorded keys |
    | figures: an extra figure accepted (`:404`) | exactly the kind's figures |
    | scopes: an extra count accepted (`:408`) | exactly `SCOPE` |
    | digest: type test dropped (`:401`) | a non-text digest then crashes `re.fullmatch` |
    | `load()`: only the first endpoint validated (`:431`) | any endpoint malformed is refused |
    | routing-errors row: duplicates accepted (`:280`, `!= 1` to `< 1`) | exactly one errors row |
    | hierarchy: last count cell unchecked (rank `:30`, `fields[2:-1]`) | every count cell is ASCII digits |

    Two further survivors are not counted: the upper-case hex digest and the integer slack without a fraction change no verdict.
  - The head enforces every one of the seven. `receipts/r3-probes/probe-r3-untested.log` drives each through the CLI on a copy of A's real route directory: all 9 cases give rc 2 with a named reason, and the control gives 0.
  - So this is a test gap only: every arm adds a missing key or a wrong type, malforms the first endpoint, or plants the first count cell.
- **Impact:**
  - An edit that weakens any of these seven checks to the shown variant stays green in the hosted self-test and mutant campaign, which are the only automated protection of the baseline file and parsers.
  - For example, a `<` for `!=` lets a doubled errors row pass, and a subset test lets an unknown identity field pass.
- **Required outcome:** for each of the seven rows, an arm through `main()`, and a shipped mutant of that relaxation that is killed:
  - an extra identity key, an extra figure and an extra scope count;
  - a non-text digest;
  - a malformed endpoint other than the first;
  - a doubled errors row;
  - an other-script digit in a count cell other than the first.
- **Verification:** `probe_r3_mutants.py <checkout> --jobs 12`. The seven rows must be KILLED and the control must pass.

## Verified clean, with evidence

- **Validator classes:**
  - The 25 malformed-baseline arms each exit 2 through `main()` by both commands (`receipts/gates/gate-selftest.log:131-155`).
  - My unchanged `probe_malformed_record.py` gives 0 cases not exit 2, with no traceback.
  - The 11 killed partial mutants include both bypasses of `load()` (in `check` and in `check-baseline`), the missing-key, missing-figure and missing-count variants, the any-length digest, the kind type test, a text-accepting `number()`, an absent errors row, any utilization fraction, and the first hierarchy cell.
- **Route rows:**
  - My unchanged `probe_route_status.py` on A's real directory is 15/16. Both CONTRACT cases (both rows removed, both rows relabelled) give rc 2.
  - The 16th is the declined S1 layout (want 1, got 2; fails closed).
- **Policy pin:**
  - My unchanged `probe_extra_mutants.py` (control passes) gives 8 KILLED. These include all four of R446-2 F2's mutants: tolerances only, table figures only, floors read as zero, and ceiling column ignored. They also include the timed-endpoint columns mutant.
  - Two of its mutants no longer apply because round 3 rewrote their spans. The shipped `timed endpoint boundary` and `baseline route ceiling` mutants cover them and are killed (`receipts/gates/gate-mutants.log:35`, `:109`).
  - `probe_policy_pin.py`: 105/105.
- **Hierarchy parser** (`receipts/r3-probes/probe-hierarchy-equiv.log`, `ranking-vs-published.log`):
  - The round-2 and round-3 `hierarchy()` give equal tables on all seven real reports: A and B route, 1x1 and 8x8, and A at 10 ns.
  - The ranking command's TSV is byte-identical between the two versions on all seven.
  - On the six published rankings, the TSV is byte-identical to `43ad8362:.../evidence/*-ranking.tsv`.
  - The only 10-field non-count row in each real report is the `Total LUTs` head.
  - A planted non-count row is refused, where round 2 skipped it.
- **Self-audit sample:** a seeded random sample (seed 4463) of rows 13, 21, 22, 26, 27, 40, 41, 44, 46, 52, 53 and 61 was checked against the head. Each named guard precedes its index or conversion as stated.
  - The misses are rows 34 and 50 and the preamble (F1, F2), and the baseline-integer arithmetic at `:313` and `:341`, which no row lists (F2).
  - `syn/ooc/pp_baseline_rank.py` has one conversion, `int()` at `:42`, guarded by `:30` and inside `record()`'s `try` when the gate calls it.
- **Real data at this head** (`receipts/real/`):

  | Run | rc | Result |
  |---|---|---|
  | A route | 0 | route status complete |
  | A 1x1 | 0 | |
  | A 8x8 | 0 | |
  | A 1x1 at 10 ns | 2 | `standalone_clock_ns` |
  | B route | 1 | +625 LUT over 500; route status complete |
  | B 1x1 | 0 | |
  | B 8x8 | 0 | |

- **Gates** (`receipts/gates/summary.txt`): 31 of 31 rc 0, GNU Make 4.3 first on `PATH`, with the em-dash and TOC gates under the pinned Markdown environment. They cover:
  - the gate self-test, 181 arms; its mutants, 122 of 122 fail; `check-baseline`, 3 endpoints;
  - the `pp_baseline` self-tests and its mutants;
  - `ci_scope` and `ci_events`;
  - the docs set, including `make -C gptp-processor docs`;
  - the Python ratchets.
  - `git diff --check 1269cdaf HEAD` is clean.
- **My round-1 probes, unchanged:**
  - `probe_gate_cli.py` 116/117. The one is `inf` with 0 endpoints at rc 2 against round 1's literal 1, which R446-1 F1 allowed.
  - `probe_gate_mutants.py`: 21 KILLED, 0 survived, control passes. 2 are not applied: shipped `count format decimals` and `baseline floor value` are killed.
  - `probe_pr_mutant_reasons.py`: 119 of 119 ARM.
  - `reconcile.py`: 2 mismatches, both its hard-coded round-1 sentences.
  - `partition_rederive.py`: 0 mismatches.
- **Docs:**
  - R446-2 R1 is taken exactly (`AREA_BUDGET.md:170`).
  - The stale-report note is in the recipe (`PP_SHADOW_BASELINE_RECIPE.md:459-460`).
  - The exit-code paragraphs (`AREA_BUDGET.md:189-196`, recipe `:456-471`) match the code except where F1 and F2 falsify them.
  - The `armq_r` census reproduces from the runs' cell censuses: 1,153 in A and 1,260 in B (`receipts/r3-probes/armq-census-rederive.log`).
- **RTL:**
  - `1269cdaf..b5894838` touches no HDL, constraint or Tcl file (`receipts/diff-name-status.txt`, 15 files).
  - The gitlinks are equal at base and head: `631eeb34`, `5dce647a` and `efeb541a`.
  - The gate is tooling, so the clock, CDC and FSM checks have no artifact in this diff.
- **Hosted, exact head** (`receipts/hosted-check-runs.txt`, 12:44Z):
  - Succeeded: `rtl-fast`, `yosys-elaboration` (step 9, which runs the gate's self-test, mutants and `check-baseline`), `verilator-lint`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3 and Verilator shard 3.
  - In progress: `docs-check`, `elaborate`, Verilator shards 0, 1, 2 and 4.
  - `Physical gPTP` was skipped. That is not evidence.
- **Probe hygiene** (`receipts/final-tree-verify.log`):
  - HEAD, the tree and the index tree are exact. `ls-files -s` equals `ls-tree -r HEAD` for blob, mode and path.
  - Nothing is untracked or ignored, and the submodules are clean at their gitlinks.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `pp_resource_gate.py:81-142`, `:268-287`, `:421-434`; round-2 and round-3 assignments; `probe-r3-numbers.log`; real data A/B | R446-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| RTL | CLEAN | `receipts/diff-name-status.txt` (no HDL/XDC/Tcl in `1269cdaf..b5894838`); gitlinks base = head; `armq_r` census rederived from the A/B `baseline_cells.tsv` | R446-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Robustness | UNCLEAN (F1, F2) | `probe-r3-numbers.log`, `probe-r3-untested.log`, `probe-route-status.log`, `probe-malformed-record.log` | R446-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Tests | UNCLEAN (F1, F2, F3) | `pp_resource_gate_selftest.py` (181 arms), `pp_resource_gate_mutants.py` (122), `probe-r3-mutants.log`, `probe-extra-mutants.log`, `probe-gate-mutants.log`, `probe-pr-mutant-reasons.log` | R446-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Docs | UNCLEAN (F1, F2: the self-audit rows 34 and 50 and its preamble, and `AREA_BUDGET.md:189-196`, falsified by the code) | `AREA_BUDGET.md:140-196`, recipe `:242`, `:452-471`, PR body round-3 tables, `probe-hierarchy-equiv.log` | R446-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |

## Real limits

- No Vivado run. Every real-data check reads the existing A and B run directories. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The F1 and F2 inputs are crafted. No tool build is known to print them. They are reported because they falsify a stated exit-code contract and reopen a refusal that round 2 proved.
- The author's round-3 packet (HANDOFF, the armq census file) is not public at review time. The census figures were rederived from the run directories instead.
- Hosted Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate` were still running at 12:44Z.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the in-progress contexts.
- The merge-turn candidate on live dev `bbf704ec`, which is distinct from this source review.
- The merge-bank Vivado `check` (manager ruling).
- Publishing this packet.

## Prior findings at this head

This section was written after the verdict and ledger above. The other reviewer's round-2 findings (5968715741) were read only at this point, and their cases were re-planted with my own script, `probe_r447_2_cases.py`.

| Prior finding | Status at `b5894838` | Evidence |
|---|---|---|
| R446-2 F1: route status without its net rows reads complete | **Resolved** | `pp_resource_gate.py:277-281` require one row of each. My unchanged `probe_route_status.py`: both CONTRACT cases rc 2. The arm at `_selftest.py:194`. Shipped mutants `routable and routed rows present` and `fully routed row required` are killed. The doubled errors row is enforced but has no arm (F3). |
| R446-2 F2: policy pin proven only for tolerance cells | **Resolved** | My unchanged `probe_extra_mutants.py`: all four F2 mutants and `timed endpoint columns optional` are KILLED, and the control passes. The fixture's WNS floor is non-zero. |
| R446-2 F3: malformed record fields exit 1 by traceback | **Resolved for every listed case; class retained narrowly in F2** | My unchanged `probe_malformed_record.py`: 0 cases not exit 2. 25 arms run through both commands. Oversized JSON integers still reach a traceback (F2). |
| R446-2 R1 (RESIDUE) | **Resolved** | `AREA_BUDGET.md:170`, exact text. |
| R446-2 S1 (wholly unrouted layout) | **Declined by the assignment** | It still gives 2 and fails closed. Not a defect. |
| R446-2 S2 (stale route status report) | **Taken** | Recipe `:459-460`. |
| R446-2 S3 (B's `armq_r` census) | **Taken; author packet not yet public** | Re-derived here: 1,153 in A and 1,260 in B. |
| R446-1 F1: non-finite slack passes | **Reopened (worsened) at this head, as F1** | Round 2 resolved it with `isfinite`, and round 3 removed that. `inf` and `nan` text are still refused, but an overflowing decimal reads as `inf` and passes. |
| R446-1 F2, F3, R1-R4, S1-S5 | **Resolved** (unchanged since round 2) | `probe_gate_mutants.py` 21 KILLED with 2 not applied, both covered by killed shipped mutants. `partition_rederive.py` 0 mismatches. `probe_policy_pin.py` 105/105. |
| R447-2 MINOR 1: malformed record fields and a superscript route count exit 1 or pass | **Resolved for every listed case; class retained narrowly in F2** | `receipts/r3-probes/probe-r447-2-cases.log`. Every one of these gives rc 2 with a named reason and no traceback in both `check` and `check-baseline`: kind `[]` and `{}`, LUT as text, null or `NaN`, identity `"x"` and `[]`, scopes `[]`, WNS `NaN`. The superscript errors count gives rc 2 in `check`. Oversized integers remain (F2). |
| R447-2 MINOR 2: route status without its routable and fully-routed rows reads complete | **Resolved** | As R446-2 F1. |
| R447-2 SUGGESTION: route status not bound to the run | **Taken as a recipe note** | Recipe `:459-460`. |

R446-3 FINISHED
