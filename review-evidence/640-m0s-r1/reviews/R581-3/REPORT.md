[R581] POSITIVE - exact head 6904af6b79aae0566e6e47979223f54b8ba0eb6f

# R581-3: external cleared-context delta review of PR #702 (Relates to #640, lane M0s step 2, round 3)

- Head `6904af6b79aae0566e6e47979223f54b8ba0eb6f`, tree `c0e859f0fccbb7af27f75d14e321f9a3e27e361f` (`git write-tree` of the clean index equals it).
- Delta: `d10aee62..6904af6b`, one one-line commit with no trailers, parent `d10aee62` (no rebase or amend). It touches two files: `syn/ooc/pp_placement_selftest.py` (+10/-5) and `syn/ooc/pp_resource_gate_mutants.py` (+2/-0). There is no product code, RTL, firmware, workflow, baseline JSON, documentation or gitlink change. All five gitlinks are identical at base `7c1b52be` and head (`logs/delta_scope.txt`, `logs/delta.diff`).
- Assignment: round 3, #640 comment 6089650427. Ruling: P2, #640 comment 6089329720. Review start: PR #702 comment 6090107350.
- Reconstruction order:
  1. AGENTS.md, CONTRIBUTING.md and docs/README.
  2. The #640 body and every manager and owner comment: lane assignment 6086604096, round 2 6087671877, ruling 6089329720, round 3 6089650427, and the author's REVIEW READY 6089897327.
  3. The gate's documented usage (`syn/ooc/pp_resource_gate.py:48-52`) and its parser (`:715-726`, `:742-777`).
  4. The delta, then the selected-placement section of the recipe page.
- My own pass over the delta and my own probes (`scripts/delta_probes.py`) came first. Only then did I read the round-2 findings (R580-2 6089579727, R581-2 6089640325) and fetch their published probes. I have not read the other round-3 review.

## Verdict summary

- **R580-2-F1 = R581-2-F1 is resolved.** Both default-population loops now call the gate in its documented order:
  - `check <directory> --endpoint ... --baseline ...`;
  - `record <directory> --endpoint ... --baseline ... --write` (`syn/ooc/pp_placement_selftest.py:244-249`, `:258-259`).
- **On CPython 3.12.3**, the hosted runner's interpreter:
  - the gate self-test exits 0 with 138 `placement gate` lines;
  - the gate campaign: control passes and 192 of 192 mutants are detected;
  - the recipe campaign: control passes and 45 of 45 are detected;
  - `check-baseline` passes.

  The same holds on the host's newer CPython. The exact-head hosted `yosys-elaboration` job prints the same lines, and the `rtl-fast` workflow concluded `success`.
- **No assertion is weakened.** For every plant, `record --write` still must exit 2 naming each role, and the baseline bytes are still compared after each judged command (`:250-253`). My probes show this matters:
  - dropping `--write` from the judged pair fails the self-test;
  - making `record --write` ignore the population fails the self-test.
- **No other self-test or driver uses the old order** (search below).
- **R580-2-R1 = R581-2-R1 is resolved.** The PR body states the P2 ruling as decided, in Known limitations and in the Round 2 heading.
- **The optional R580-2-S1 was adopted, and it works.** The new printed-record assertion (`:254-255`) is the only control that detects the "printed record judged" mutant:
  - at `d10aee62` the mutant survives on 3.14.7;
  - at head it is detected on both interpreters;
  - R580-2's P8 M1 is now DETECTED.

The delta has no open BLOCKER, MAJOR, MINOR or RESIDUE. One SUGGESTION (S1) concerns unchanged lines.

## Findings

### R581-3-S1 - SUGGESTION - Tests, Docs - the campaign parallelism cap is ignored on the hosted interpreter

- **Where:**
  - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:277`, `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py`, added by this PR in round 1 and unchanged in this delta.
  - `syn/ooc/pp_resource_gate_mutants.py:354`, `ThreadPoolExecutor(os.cpu_count() or 1)`, which predates the PR.
- **Evidence:** `-X cpu_count` exists only from CPython 3.13. On 3.12.3 the option is accepted and ignored: `os.cpu_count()` returns 128 on this host with `_xoptions={'cpu_count': '4'}`, while 3.14.7 returns 4. The host's process affinity allows 16 CPUs, and `os.cpu_count()` ignores affinity.
- **Impact:** none on any verdict, because each mutant runs in its own copy. The documented cap is silently absent on the CI interpreter, though, and a large host runs up to 128 concurrent self-tests. Through this, my own command-for-command replays exceeded my 16-job allowance (see limits).
- **Optional outcome:** a portable cap, for example a `--jobs` option or the process's affinity count, documented in place of `-X cpu_count`.
- **Verification:** under 3.12.3, the campaign's worker count follows the documented cap.

### Prior findings at this head

| Finding | Status at `6904af6b` | Evidence |
|---|---|---|
| R580-2-F1 (BLOCKER) = R581-2-F1 (MAJOR): default-population self-test fails on the hosted interpreter | **RESOLVED** | Gate self-test rc 0 on 3.12.3 and 3.14.7 (`logs/py312_06_*`, `logs/host_06_*`). `d10aee62` reproduces rc 1 with `wrapper replaced record: ... got (2, ['exited through argparse'])` on 3.12.3 (`logs/base_d10_py312_gate_selftest.*`). Hosted `yosys-elaboration` job 114043347540 succeeded. Reverting either call in a copy fails again on 3.12.3 only (`logs/delta_probes.log`). R580-2's P10 shows `record --write <dir>` exiting through argparse on 3.12.3, while the documented order refuses by role name with the baseline unchanged (`logs/probes/P10_*`). |
| R580-2-R1 = R581-2-R1 (RESIDUE): PR body asks for the P2 decision | **RESOLVED** | The PR body reads "The manager ruled this difference expected (#640 comment 6089329720)" in Known limitations. The heading reads "**P2 `fuzz` and self-test line prefix (ruled expected in #640 comment 6089329720).**" No request remains. |
| R580-2-S1 (SUGGESTION): printed record has no control | **Adopted** | `pp_placement_selftest.py:254-255`, plus the campaign mutant at `pp_resource_gate_mutants.py:288-289` (detected). R580-2's P8 rerun unmodified: 7 of 7 detected, M1 included (`logs/probes/P8_*`). |
| R580-1-F1, R580-1-F2 (MINOR) | Remain **RESOLVED** (round 2; this delta strengthens the F1 controls) | R580-2's P4 rerun unmodified: 96 of 96 rows as expected, synthetic and the published accepted route-1x1 report, on both interpreters. Columns 1-9, and whole lines after path scrubbing, are identical to R580-2's published `d10aee62` receipt (`logs/probes/P4_*`). R580-1's P1 rerun unmodified: 29 of 34, B4 and B5 detected. |
| R580-1-S1 / S2, R581-1-R1 | Unchanged from round 2 (S1 partly adopted, S2 optional and not adopted, R1 resolved) | The P1 survivors are unchanged: G1, G3, G8, G13 and B9. G13 and B9 are caught by the campaign drivers' control assertion. The PR Status sentence is still resolved. |

## Lens coverage at `6904af6b`

```text
[R581] PASS Conformance - syn/ooc/pp_placement_selftest.py:242-260 against syn/ooc/pp_resource_gate.py:48-52,715-716 and #640 comment 6089650427 items 1-2; PR #702 body (Known limitations, Round 2 heading, Round 3) - documented order used in both judged loops; role naming and baseline-byte checks still run for record --write; no other driver uses the old order; P2 ruling stated as decided; no product code, policy, schema, threshold or baseline change (logs/delta_scope.txt; check-baseline "baseline PASS: 3 endpoints" on both interpreters)
[R581] PASS RTL - logs/delta_scope.txt (PR-wide and delta name-status, gitlinks at 7c1b52be and head) - no HDL, constraint, firmware or gitlink change in the delta or the PR; dp_srcs --top milan_datapath and --top KL_pp_shadow rc 0 on both interpreters; exact-head hosted verilator-lint and yosys-elaboration success
[R581] PASS Robustness - logs/probes/P10_cli_order_{py312,host}.txt; logs/probes/P11_printed_record_wrapper_absent.txt; logs/probes/P4_default_population_{py312,host}.tsv - interpreter-dependent argument parsing (old order fails only on 3.12.3, documented order refuses by role on both); printed record exits 0 unjudged for a wrapper-retaining F0-F4 population and exits 2 at the missing wrapper root for "wrapper absent" (the self-test's single exemption is accurate); 96/96 default-population cases including the real route-1x1 report
[R581] PASS Tests - syn/ooc/pp_placement_selftest.py:244-260; syn/ooc/pp_resource_gate_mutants.py:288-289; logs/delta_probes.log; logs/py312_*, logs/host_*; logs/legacy/; logs/probes/P1_*, P8_* - each new or changed assertion fails for the defect it targets (printed-record mutant: survives at d10aee62 on 3.14.7, detected at head on both; --write dropped and record --write ignoring population both detected; the old order detected on 3.12.3); full rtl-fast OOC step 10/10 rc 0 on both interpreters; 212 legacy self-test lines byte-identical at 7c1b52be, d10aee62 and head on both interpreters; P1 29/34 unchanged; P8 7/7
[R581] PASS Docs - docs/testing/PP_SHADOW_BASELINE_RECIPE.md:232-239,274-288; syn/ooc/pp_resource_gate.py:21-23,48-52,763; PR #702 body Round 3; code comments pp_placement_selftest.py:242-243,254 - the recipe's "Printing a record without --write judges nothing" is now pinned by a control; the delta's comments are accurate (P10, P11); PR-body Round 3 claims (line ranges, 138 lines, 192/192, 45/45, 212 identical legacy lines, revert behavior) reproduced; em-dash gate 0 findings, 339/339 arms; R581-3-S1 is optional
```

Every lens was applied to the delta at this head. Earlier rounds stand for the files this delta does not touch. I also re-executed their gates and suites at this head, listed below.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6089650427 items 1-2 against `pp_placement_selftest.py:242-260` and gate usage `pp_resource_gate.py:48-52,715-716`; PR body against ruling 6089329720; driver search; `check-baseline` | R581-3 | 6904af6b79aae0566e6e47979223f54b8ba0eb6f |
| RTL | CLEAN | `logs/delta_scope.txt` (no HDL, constraint or gitlink change; gitlinks equal at base and head); `dp_srcs` tops; hosted verilator-lint and yosys-elaboration | R581-3 | 6904af6b79aae0566e6e47979223f54b8ba0eb6f |
| Robustness | CLEAN | P10 on 3.12.3 and 3.14.7; P11 printed record (wrapper absent, wrapper-retaining F0-F4); P4 96/96 (synthetic and real route-1x1) | R581-3 | 6904af6b79aae0566e6e47979223f54b8ba0eb6f |
| Tests | CLEAN (S1 optional) | Delta probes (10 cases × 2 interpreters); rtl-fast OOC step 10/10 × 2 interpreters; gate campaign 192/192; recipe campaign 45/45; P1 29/34; P8 7/7; 212 legacy lines identical in 6 runs; hosted job log | R581-3 | 6904af6b79aae0566e6e47979223f54b8ba0eb6f |
| Docs | CLEAN (S1 optional) | Recipe page `:232-239,274-288`; gate docstring; delta comments; PR body Round 2/3 and Known limitations; em-dash gate (339/339 arms, 0 findings) | R581-3 | 6904af6b79aae0566e6e47979223f54b8ba0eb6f |

## Executed evidence

Interpreters: CPython 3.12.3 (the hosted ubuntu-24.04 interpreter) and the host's CPython 3.14.7. No bytecode was written, and every command ran with its own log and rc file.

| Command or probe | Result |
|---|---|
| `scripts/rtl_fast_ooc_step.sh` replays `.github/workflows/rtl-fast.yml:207-216` command for command, on 3.12.3 (`logs/py312_*`) and 3.14.7 (`logs/host_*`) | 10 of 10 rc 0 on each. `dp_srcs` self-test 35 arms; OOC tcl 58 arms; recipe self-test PASS; recipe campaign control + 45 detected; gate self-test 447 lines, 138 `placement gate`; gate campaign control + 192 detected; `baseline PASS: 3 endpoints`; both tops |
| Gate self-test at `d10aee62` on 3.12.3 | rc 1, the round-2 defect reproduced |
| `scripts/delta_probes.py` (`logs/delta_probes.log`) | Head and `d10aee62` controls. The printed-record mutant: detected at head on both interpreters, survives at `d10aee62` on 3.14.7. Either call reverted to the old order: rc 1 on 3.12.3, rc 0 on 3.14.7. Printed-record assertion removed: rc 0 (it is the only detector). `--write` dropped: rc 1. `record --write` ignoring population: rc 1 |
| R580-1 P1 `probe_mutants.py`, R580-2 P4 `probe_default_population.py`, P8 `probe_population_mutants.py`, P10 `probe_cli_order.py`, unmodified; git blob ids and sha256 equal their published manifests | P1 29/34 (same survivors); P4 0 unexpected of 96, identical to the `d10aee62` receipt; P8 control + 7/7; P10 as above. Same on both interpreters |
| Legacy self-test lines (`logs/legacy/`), base `7c1b52be`, `d10aee62`, head × 2 interpreters | 212 lines, the same sha256 prefix `063d1e8b7d097ce8` in all six runs |
| Quality gates (`logs/gates/`) | Python idiom, hygiene, naming, fail-fast and test-evidence ratchets rc 0; em-dash `--base 7c1b52be` with the pinned renderer rc 0 (0 findings, 339/339 arms); `git diff --check 7c1b52be HEAD` rc 0; `py_compile` of both changed files rc 0 |
| Hosted, exact head (`logs/hosted_runs_status.txt`, `logs/hosted_yosys_elaboration_114043347540.log`) | rtl-fast run 37996307323 `completed success`: changes, bdd-conformance, verilator-lint, firmware-unit, yosys-elaboration and the aggregate job all success. The job log shows `control: rc=0 PASS`, the `wrapper replaced printed record` line, the unchanged-schema line, `all 192 mutants fail` and `baseline PASS: 3 endpoints`. docs and elaborate success. rtl-full was still running at 22:33 UTC (Verilator shards 1/5 and 2/5 in progress; the other 8 executed jobs success; Physical gPTP skipped, not executed) |

Tree integrity after all probes (`logs/tree_integrity.txt`):
- HEAD and `write-tree` equal the published head and tree.
- `git status --ignored` is empty, and diff-index and diff-files are clean.
- All 1,235 tracked blobs are rehashed equal to the index.
- The five gitlinks are as recorded; `external` and `third_party/lwSRP` are not initialized, as at the start.
- Every probe ran on copies under the packet's scratch directory.

## Limits

- **Parallelism cap exceeded.** The two command-for-command step replays ran the repository's campaign drivers. These size their pools from `os.cpu_count()`, which is 128 on this host, so each campaign briefly ran more than the allowed 16 concurrent jobs (R581-3-S1). The two replays ran one after the other, and nothing else heavy ran beside them. All other probes passed an explicit 16.
- **No full banks.** This round ran no full parent, PP, gPTP, Yosys or builder bank and no manager source bank. The source-head execution evidence is the author's receipts plus the focused runs above.
- **Host-only checks were not repeated.** P2, P3 and the documentation TOC and anchor gates were not rerun here; the delta touches no document and no recipe code.
- **Hosted acceptance is the manager's.** Exact-head rtl-full was not complete when this report was written.
- **No physical calibration, hardware or route.** Physical calibration was NOT RUN. A skipped hosted context is not executed evidence.

## Pending manager duties

- Confirm exact-head `rtl-full` (Verilator shards 1/5 and 2/5) and the remaining protected contexts.
- Build and validate the current-dev merge candidate (source base `7c1b52be`, live dev `8b61b709`) with the builder and native banks, and link the receipts.
- Optionally carry R581-3-S1.

R581-3 FINISHED
