[R447] POSITIVE - exact head 79e53831a4f623a594f22765be1d05dffeb696a7

# R447-4 external review: issue #234 / PR #638, round 4

- Head `79e53831a4f623a594f22765be1d05dffeb696a7`, tree `641203eed0fe9d67dfc01694a31dacd52b62638a`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Round 4 is `b5894838..79e53831`: five one-line commits with no trailers, 6 files (the gate, its self-test and mutants, `pp_baseline_rank.py`, `AREA_BUDGET.md`, the recipe). There is no HDL, constraint, Tcl, workflow, baseline-JSON or gitlink change (`receipts/r4/diff_scope.log`).
- **Verdict POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. Three RESIDUE items (wording only, each with its exact fix) and two SUGGESTIONs are recorded. All five lenses are covered clean at this head.
- Every round-3 finding of both reviews is **resolved**. None is retained or worsened.
- The structural contract holds for the gate's three commands (`check`, `record`, `check-baseline`):
  - one `try` in `main()` after argument parsing;
  - exit 1 only from `judge()`;
  - every other exception exits 2 with `NOT COMPARABLE:`;
  - every printed line is printable ASCII through `emit()`.
  
  I found no input path that escapes it. The two test drivers, `--selftest` and `--fuzz`, run outside the barrier. That is a scoping gap in the module docstring only (RESIDUE R1).
- Real data verdicts are correct:
  - A: the route, 1x1 and 8x8 all exit 0, and the route status is complete;
  - B: the route exits 1 (+625 LUT over 500), and B's 1x1 and 8x8 both exit 0;
  - A's 1x1 at 10 ns exits 2 (standalone clock identity).
- My verdict, findings and ledger came from my own pass over the round-4 diff and my own probes. I then read R446-3 (5969323709) and my own R447-3 to resolve them; that table is below. I did not read the R446-4 report or any other reviewer's round-4 material.

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (as loaded), and the docs map.
2. Issue #234's body and comments:
   - the lane assignment (5966260488) and the takeover;
   - the rulings (5967852698) and the owner decision (5967924270);
   - the round-2 and round-3 assignments, and REVIEW READY rounds 1 to 3;
   - the **round-4 assignment (5969446300)**;
   - round-4 REVIEW READY (5970259375).
3. `git diff b5894838..79e53831` in full. Also `1269cdaf..79e53831` by name, the commit history, and the PR body's Round 4 section, read after my structural pass.
4. Public evidence:
   - `43ad8362:review-evidence/234-r1/author/evidence` (the round-1 records), used by my unchanged round-1 and round-2 probes;
   - the archived round-4 census `6c098ef13:review-evidence/234-r1/author-r4/receipts/armq-census.tsv`, for R447-3 R1 only;
   - the A and B measurement directories, read only.
5. Exact-head hosted check runs, recorded as a snapshot only.
6. After my own pass: R446-3, and my own R447-3 report.

## Findings

```text
[R447] R1 RESIDUE Docs - syn/ooc/pp_resource_gate.py:22-28 (module docstring) - the barrier sentence is scoped to all of main(), but --selftest and --fuzz run outside it
Evidence: main() returns from --selftest at :669-671 and from --fuzz at :672-675, both before the try at :679. receipts/r4/probe_r4_structure.log runs three test-mode cases as real processes. --fuzz with an absent --baseline, an absent directory, or an endpoint the baseline lacks each exit 1 with a traceback (FileNotFoundError, FileNotFoundError, KeyError). The docstring says "main() holds one barrier around everything after argument parsing ... So exit 1 comes only from judge(), no input reaches a traceback, and every line is printed as printable ASCII". The three gate commands do hold this: 48 of the probe's 48 command cases exit as the contract says, none with a traceback, all ASCII. AREA_BUDGET.md:189-194, the recipe at :462-464 and the PR body scope the claim to check or to "every command", so they are accurate.
Why RESIDUE: no verdict, measurement, test or gate command changes. A test driver that cannot start fails closed (non-zero, visible traceback), and hosted CI does not run --fuzz. The defect is the sentence's scope, and the fix below is wording only.
Exact fix: in the docstring, replace "main() holds one barrier around everything after argument parsing:" with "For check, record and check-baseline, main() holds one barrier around everything after argument parsing:". Replace "and every line is printed as printable ASCII" with "and every line those commands print is printable ASCII". Then append: "--selftest and --fuzz are test drivers outside the barrier: a non-zero exit there means the test failed or could not start."
```

```text
[R447] R2 RESIDUE Docs - docs/design/AREA_BUDGET.md:207; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:475 - "holds every case to this contract" claims more than the generative oracle checks
Evidence: violations() (pp_resource_gate.py:577-585) requires each case to exit 0, 1 or 2 with no traceback, to give a reason with 2, and to exit 2 for a broken shape. It does not check "exit 1 comes from one place, the comparison" (AREA_BUDGET.md:191), which is part of "this contract". receipts/r4/probe_r4_fuzzkill.log: the mutant "check-baseline problems exit 1" passes the generative block at seed 234 (500 cases) and at seed 447 (5,000 cases). receipts/r4/probe_r4_oracle.log 2a: it also passes 2,000 cases. The arms kill it (selftest rc 1). The PR body's own description of the oracle ("exit 0, 1 or 2 with no traceback, a reason with 2, and 2 for every broken shape") is accurate.
Why RESIDUE: the claim about exit-1 provenance is tested by the arms, and no verdict or test changes. Only the sentence over-describes the generative oracle.
Exact fix:
- AREA_BUDGET.md:207 becomes: "A seeded generative test changes baselines and reports at random: every case must exit 0, 1 or 2 without a traceback, give its reason with 2, and exit 2 when it breaks a documented shape."
- The recipe at :475 becomes: "Each case changes the baseline or one report at random; it must exit 0, 1 or 2 without a traceback, and 2 when it breaks a documented shape."
```

```text
[R447] R3 RESIDUE Docs - PR #638 body, Description table, row "syn/ooc/pp_resource_gate.py, _selftest.py, _mutants.py" - "two bounded converters"
Evidence: real() (pp_resource_gate.py:374-382) bounds nothing but finiteness. A 17-digit half BRAM tile is accepted as a finite float and judged (receipts/r4/probe_r4_structure.log, "half BRAM tile 17 digits": rc 1, ceiling). That is what AREA_BUDGET.md:196 and the PR body's own Round 4 paragraph state ("whole() (1 to 15 ASCII digits) or real() (finite)").
Exact fix: replace "every number goes through one of two bounded converters" with "every number goes through one of two converters, whole() (1 to 15 ASCII digits) or real() (a finite float)".
```

```text
[R447] S1 SUGGESTION Tests - syn/ooc/pp_resource_gate.py:577-585 (violations) - the generative oracle could check exit-1 provenance as well
Two cheap checks would make the generative test catch the one class it now misses:
- check-baseline never exits 1;
- check exits 1 only with "RESULT: MATERIAL REGRESSION".
receipts/r4/probe_r4_oracle.log:
- 1a/1b: with both checks added in-process, the head keeps 0 failures over 10,000 fixture cases (seeds 234 and 4474), so the stricter oracle is sound;
- 2b: it detects the "check-baseline problems exit 1" mutant (43 failures in 2,000), which the shipped oracle misses (2a).
```

```text
[R447] S2 SUGGESTION Tests - syn/ooc/pp_resource_gate_selftest.py:800-951 (mutate_json, mutate_report) - two inputs are outside the generator's space
The generator never changes the budget page. It also never changes an image-manifest key into one outside the name class, or writes NaN or a repeated key into the manifest. So the mutants "budget cell via float()" and "manifest via json.loads" pass the generative block at both seeds. Arms kill both (receipts/r4/probe_r4_fuzzkill.log; shipped "budget cell converter" and "image manifest strict" are killed in receipts/gates/gate_mutants.log). Adding a budget-page target and manifest key and number operators would let the --fuzz runs exercise them too. No refusal is untested today.
```

## Round-4 structural review (my own pass)

### The barrier, emit() and exit 1

- **Code.** `main()` (`pp_resource_gate.py:655-708`):
  - Argument parsing and the two test drivers come first (`:657-677`).
  - Everything for `check`, `record` and `check-baseline` follows inside one `try` (`:679-705`), and `except Exception` (`:706-708`) prints through `emit()` and returns 2.
  - The only returns of 1 are `judge()`'s status (`:703-705`). `check-baseline` returns 2 or 0 (`:684`), and `record` returns 0.
  - `judge()` returns 2 for a kind, identity or identical-input refusal, 1 for a regression or an incomplete route, and 0 otherwise.
- **Probe.** `probe_r4_structure.py` runs every case as a separate process with standard output forced to strict ASCII (`PYTHONIOENCODING=ascii:strict`): **51 cases, 0 off expectation** (`receipts/r4/probe_r4_structure.log`). The only tracebacks are the three `--fuzz` cases in R1. It covers:
  - the unknown endpoint that round 4 moved inside the barrier (rc 2);
  - an endpoint name with an undecodable byte (rc 2, printed `\udcff`);
  - a measurement directory named with undecodable bytes (rc 0, printed escaped);
  - a directory that is a file, a 300-character name, a baseline or budget that is a directory (all rc 2);
  - a candidate sub-block named `u_nvm` + `é‮` (rc 0, printed escaped). `record --write` of that candidate gives rc 2 with the write target unchanged.
- **Inside emit() itself.** `emit()` (`:646-652`) joins strings that are all f-strings and escapes every character outside `" "`..`"~"`, so it cannot raise on content. Only a failure of standard output itself could make it raise; the executor states that as a limit, and the assignment puts it out of scope. `str(error)` in the barrier is built-in exception text and cannot raise for any input.
- **Fault probes.** `probe_r4_fuzzkill.py` gives two more confirmations:
  - "barrier returns 1" is detected by both generative blocks and the self-test;
  - "emit prints raw" is detected by all three.

### Converters at every site

- Every `int(` and `float(` in the gate and the hierarchy parser is inside `whole()` (`pp_baseline_rank.py:29-36`) or `real()` (`pp_resource_gate.py:374-382`). The one other conversion is `json.loads` in `fuzz()` (`:604`), a test driver. `\d` appears only in the tool-build text match (`:206`), which is compared as text and never converted.
- `probe_r4_structure.py` plants each site, through `check` and, for JSON, through `check-baseline` too. Each exits 2 and names its converter:
  - JSON: a 16-digit figure, scope count, tolerance, ceiling and `schema` note; a `1e400` figure; a 401-digit decimal tolerance; a `-1e400` floor; and `1E999` in the `measured` note;
  - reports: a 16-digit utilization count; a 401-digit half tile; a 401-digit WNS; 16-digit THS endpoints; a 16-digit route status count; a 16-digit hierarchy count;
  - a 401-digit budget cell.
- Two controls reach `judge()` as designed:
  - a 15-digit LUT count gives rc 1, a regression;
  - a 17-digit half tile gives rc 1 at the ceiling.
- `whole()`'s 15 digits stay below 2^53, so every accepted whole number is exact as a float.

### Names

- `named()` (`:400-409`) applies `SCOPE_NAME` to every key and refuses a repeat. `load()` holds endpoint names to `NAME` (`:480-481`), and `shape_problems()` holds policy figure names to it (`:464-465`). Record, identity, figure and scope-count keys are exact sets.
- Probe results:
  - a bracketed endpoint name, a bracketed tolerance figure and a bracketed identity key each give rc 2;
  - a bracketed scope `u_pp/g_x[7].y` is accepted (rc 0), as the manager accepted;
  - a scope name holding a space, a repeated key and a 129-character key each give rc 2.

### The generative test

- **Self-test.** The 500 cases at seed 234 pass, with case digest `86e4babaf25c21c8`, inside the 247-arm self-test (`receipts/gates/gate_selftest.log`).
- **My `--fuzz` runs** (`run_fuzz.sh`, `receipts/fuzz/`) total 90,000 cases with 0 failures and no traceback. That is at the executor's seed and at an independent seed:

  | Target | Cases | Seed | Failures | Case digest |
  |---|---:|---:|---:|---|
  | fixtures | 20,000 | 234 | 0 | `36552f395d6ef669` |
  | fixtures | 20,000 | 4474 | 0 | `c1ae5b943640e555` |
  | A real route | 20,000 | 234 | 0 | `1c07ac027c0c26b3` |
  | A real route | 20,000 | 4474 | 0 | `c8cd802dc3a55463` |
  | A real 1x1 | 5,000 | 234 | 0 | `9f1495ce5396f57b` |
  | A real 8x8 | 5,000 | 4474 | 0 | `771275195cc373b5` |

  The operator tallies show where a changed report still exits 0. In every such case the edit touches only reported, ungated data, or lines outside what the gate reads:
  - census and hierarchy truncation: CARRY4 and sub-blocks are reported, never gated;
  - image-manifest edits: the input digest only;
  - timing truncation after the summary.
  
  No shape-breaking case exits 0 or 1.
- **Would it catch a removed barrier or converter?** `probe_r4_fuzzkill.py`, 23 single-span mutants (`receipts/r4/probe_r4_fuzzkill.log`): the self-test kills **23 of 23**.
  - The generative block alone (500 at seed 234, or 5,000 at seed 447) detects 17:
    - `whole()` unbounded, and `whole()` bypassed;
    - `real()` keeping non-finite values;
    - JSON integers or decimals bypassing their converter;
    - route status, timed endpoint, utilization, hierarchy and slack converters bypassed;
    - duplicate keys kept;
    - the key name class removed, and brackets allowed in endpoint names (5,000 only);
    - policy figure names unchecked;
    - the half tile via `float()` (5,000 only);
    - "barrier returns 1";
    - raw printing.
  - It does not detect the barrier narrowed to `Refusal`. With every inner handler intact, no input reaches the barrier. When an inner handler is also removed, the shipped oracle detects the double mutant at once: `probe_r4_oracle.log` case 3, 120 failures in 500. The planted-exception arms kill the single mutant.
  - It also misses three mutants that the barrier makes equivalent under the contract: the unknown-endpoint refusal removed, the record handler narrowed, and "check-baseline problems exit 1". The last is S1 and R2.
  - It misses two inputs outside its space: the budget cell and the manifest (S2).

### Real data

`receipts/real/` uses my unchanged round-2 `real_data.sh`:
- A route 0 ("route status: complete"), A 1x1 0, A 8x8 0;
- A 1x1 at 10 ns 2 (`standalone_clock_ns`);
- B route 1 (LUT 50,128 to 50,753, +625 over 500; route status complete), B 1x1 0, B 8x8 0.

## Prior findings at this head

This section was written after my verdict, findings and ledger. I re-planted R446-3's cases with my own `probe_r4_resolution.py`.

| Prior finding | State at `79e53831` | Evidence (this round) |
|---|---|---|
| R447-3 F1: a JSON-escaped lone surrogate turns a refusal into exit 1 by traceback | **RESOLVED** | Barrier + `emit()` + name class. `receipts/reruns/r3_probe_text.log`, unchanged: cases A to F rc 2 in both columns, no traceback; control rc 0 / 0. Arms print into a strict ASCII stream (`_selftest.py:569-585`); mutants `barrier`, `ASCII output` and `printable ASCII output` are killed. |
| R447-3 F2: a long integer literal passes load() and crashes judge() | **RESOLVED** | `whole()` via `parse_int`. `r3_probe_bigint_B.log` and `r3_probe_bigint_A.log`: both 10**400 cases rc 2 in both columns; controls B 1 / 0, A 0 / 0. Shipped `baseline integers converted` and `whole number bound` are killed. |
| R447-3 F3: six claimed refusals with no arm | **RESOLVED** | `r3_extra_mutants_r3.log`, unchanged: 13 of 13 KILLED, 0 survived, control passes. Arms at `_selftest.py:205`, `:231`, `:243`, `:403`, `:446`, `:451`. |
| R447-3 R1: the packet file was absent | **RESOLVED** | The PR body's Round 3 row carries the exact fix's re-derivation text. The archived `6c098ef13:.../author-r4/receipts/armq-census.tsv` (sha256 `c9a81132...`) lists A 1,153, B 1,260 and A-8x8 1,318, with the same census digests as `receipts/reruns/r3_armq_count.log`. |
| R447-3 S1: duplicate keys | **Taken** | `named()`; `r3_probe_text.log` case F rc 2 / 2. |
| R447-3 S2: bool scope count, late hierarchy cell | **Taken** | Arm `_selftest.py:479`; both reviewer mutants KILLED (`r3_extra_mutants_r3.log`). |
| R446-3 F1: a slack too long to be finite passes | **RESOLVED** | `real()` at `:157` and `:134`. `receipts/r4/probe_r4_resolution.log`: a WNS, a WHS and a negative WNS of 401 integer digits, and a 401-digit half tile, all rc 2, named "is not finite"; control 0. |
| R446-3 F2: an oversized integer still reaches a traceback | **RESOLVED** | `probe_r4_resolution.log`: a 4401-digit route status count gives rc 2 (inside `routing()`'s `try`). A baseline WNS_ns or WHS_ns written as a 401-digit integer gives rc 2 in `check` on B (judge would run) and in `check-baseline`; control B 1. |
| R446-3 F3: seven claimed refusals with no arm | **RESOLVED** | Shipped mutants killed (`receipts/gates/gate_mutants.log`): `baseline identity exact keys`, `baseline figures exact`, `baseline scope counts exact`, `baseline input digest type`, `baseline every endpoint validated`, `routing-error row single`, `hierarchy counts end early`. Also killed: the two uncounted ones, `baseline input digest lower case` and `slack fraction`. |
| Round-1 and round-2 findings of both reviews | Resolved earlier; no regression | My round-1 to round-3 probes, rerun unchanged (table below). |

## My round-1 to round-3 probes, rerun unchanged at this head

The copies are under `prior/`, and `prior/ORIGINALS.sha256` binds each to its original.

| Probe | rc | Result | Reading |
|---|---:|---|---|
| r1 `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| r1 `partition_check.py` | 0 | complete partition +79 / 391 / +93; `u_pp` -23 / +107 | Equals `AREA_BUDGET.md:167-170` and the findings page `:137-141`. The trailing "documented:" line is fixed round-1 text. |
| r1 `probe_cli.py` | 0 | 54 of 54 as documented | |
| r1 `probe_route_status.py` | 0 | clean exit 2; 37 unrouted exit 2 | Its invented report has no net-count rows, which the gate refuses by design (since round 3). |
| r1 `replay_records.py` | 0 | A 0/0/0; B 1/0/0; 10 ns 2 | |
| r1 `extra_mutants.py` | 0 | 16 killed, 0 survived, 2 not unique | `CLI refusal exits 0` was rewritten by the barrier, and `baseline floor value` by round 3. Shipped `refusal exit status` and `baseline floor value` are killed. |
| r2 `classify_mutants.py` | 0 | 145 ARM, 4 ESCAPED, 0 survived, control passes | Each ESCAPED mutant removes a handler, so an arm sees the escape. |
| r2 `partition_r2.py` | 0 | net +79 / +93, abs 391 / 121; `u_pp` -23 / +107 | |
| r2 `probe_contract.py` | 0 | every edited case rc 2 in both columns; control 1 / 0 | |
| r2 `probe_policy.py` | 0 | 107 of 107 | |
| r2 `probe_route_real.py` A / B | 0 / 0 | 15 of 15 / 14 of 15 | The B miss is B's own +625 LUT at rc 1. |
| r2 `real_data.sh` (as r3) | - | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | `receipts/real/` |
| r3 `extra_mutants_r3.py` | 0 | 13 of 13 KILLED | |
| r3 `probe_text.py`, `probe_bigint.py` (A, B), `probe_gaps.py` | 0 | every edited case rc 2, no traceback; gaps 6 of 6 rc 2 | |
| r3 `hier_compare.py` | 0 | 7 reports, 0 differing (`b5894838` against head `hierarchy()`) | |
| r3 `armq_count.py` | 0 | A 1,153, B 1,260, A-8x8 1,318; digests unchanged | |
| r3 `run_gates.sh` | - | 31 of 31 jobs rc 0 | `receipts/gates/`. GNU Make 4.3 first on PATH, built from the release tarball (sha256 `e05fdde4...`). `ooc_tcl_selftest` was rerun in the foreground after the detached driver stopped before writing its rc (`NOTE.txt`): 58 arms passed, rc 0. |

The gates include:
- the gate self-test (247 arms and 500 generated cases);
- the shipped mutant campaign (158 of 158 fail; control passes);
- `check-baseline` (3 endpoints);
- the `pp_baseline` self-tests and mutants;
- `ci_scope` and `ci_events`;
- the docs set, with `make -C gptp-processor docs` under Make 4.3;
- the Python ratchets;
- `git diff --check 1269cdaf HEAD`.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-4 assignment items 1 to 6 against `pp_resource_gate.py:22-43`, `:374-416`, `:646-708` and `pp_baseline_rank.py:17-36`. The acceptance criteria as ruled (5967852698, 5967924270), unchanged by round 4. Real data `receipts/real/` (A 0/0/0, B 1/0/0, 10 ns 2). `.github/workflows/rtl-fast.yml:212-214` and `scripts/ci_events.py:2328-2330` (hosted half of criterion 4). | R447-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| RTL | CLEAN | `receipts/r4/diff_scope.log`: no HDL, XDC or Tcl file in `1269cdaf..79e53831`, and gitlinks equal at base and head (`631eeb34`, `5dce647a`, `efeb541a`). The lens applies to the tooling as the integer and float width and overflow contract: `whole()` 15 digits < 2^53, `real()` finite, `probe_r4_structure.log` converter sites. Census `r3_armq_count.log`. | R447-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Robustness | CLEAN | `probe_r4_structure.log` (51 cases), `probe_r4_resolution.log` (11 cases), `receipts/fuzz/` (90,000 generated cases, 0 failures), reruns `r2_probe_contract`, `r3_probe_text`, `r3_probe_bigint` A/B, `r3_probe_gaps`, `r2_probe_route_real` A/B. | R447-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Tests | CLEAN (S1, S2 optional) | `pp_resource_gate_selftest.py` (247 arms, 500 cases), `pp_resource_gate_mutants.py` (158 killed, `receipts/gates/gate_mutants.log`), `probe_r4_fuzzkill.log` (23 of 23 killed by the self-test), `probe_r4_oracle.log`, reruns `r1_extra_mutants`, `r2_classify_mutants`, `r3_extra_mutants_r3`. | R447-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Docs | CLEAN (R1, R2, R3 are RESIDUE) | `AREA_BUDGET.md:184-208`, recipe `:242` and `:456-477`, the gate docstring `:3-44`, the PR body Round 4 section and Description row, `r1_check_tables` (49 groups, 0 mismatches), partition reruns equal to the prose, the R447-3 R1 census archive. | R447-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |

## Real limits

- No Vivado run. Every real-data check reads the existing A and B run directories. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No RTL is in the diff, so the scoped Verilator was not used.
- Signals, argparse and a failure of standard output itself are out of scope, as assigned. The barrier does not cover a closed output pipe, which the executor states.
- Receipts replace host paths with `$VALIDATION_STORAGE`, `$CHECKOUT`, `$PACKET` and `$TOOLS`. No other byte was changed.
- Hosted snapshot (`receipts/r4/hosted_check_runs.tsv`, read at the time in `hosted_check_runs.read_at`):
  - completed successfully: `rtl-fast`, `yosys-elaboration`, `verilator-lint`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, and Verilator shards 0 and 3;
  - in progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4;
  - `Physical gPTP` was skipped, which is not evidence.
  
  The manager owns hosted and local-replica acceptance.
- After every probe the clone was verified exact (`receipts/verify_tree.log`):
  - HEAD, tree and index tree equal the head;
  - worktree bytes and modes equal HEAD, and `ls-files -s` equals `ls-tree -r HEAD`;
  - nothing is untracked or ignored;
  - submodule worktrees are clean at their gitlinks.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the contexts still in progress.
- The merge-turn candidate on live dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`, distinct from this source review (source base `1269cdaf`).
- The merge-bank Vivado `check` (manager ruling).
- Carrying R1, R2 and R3 to the residue checklist with their exact fixes.
- Publishing this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R447-4 FINISHED
