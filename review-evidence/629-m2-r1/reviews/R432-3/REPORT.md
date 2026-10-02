[R432] POSITIVE - exact head 0b066b6e66df2a3ba3167805a6a591f8b96fa449

# R432-3: internal cleared-context delta review of PR #634 (issue #629, lane M2), round 3

- **Head:** `0b066b6e66df2a3ba3167805a6a591f8b96fa449`, tree `3cc8846c933b348b09bec80f4a1a6b3543c7842b`. That is three commits on round 2's `d81198c2` (`bb65ac49`, `7f051b27`, `0b066b6e`), each a one-line message with no trailers. The source base and live `dev` are both `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- **Scope:** the [round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5952544402), items 1 to 4, plus the round-3 review focus.
- **Lenses applied:** Conformance, RTL, Robustness, Tests, Docs.
- **Verdict:** POSITIVE.
  - Nothing at MINOR or above is open.
  - One new RESIDUE (wording) and one new SUGGESTION are recorded.
  - Every prior finding on this PR is closed, taken, or retained with its reason, as shown in the table below.

## Summary

1. **R433-2-F1 is closed.**
   - R433-2's `make43_checks.sh`, run unchanged:
     - Under GNU make 4.3: Entity shape gate rc 0, 222/0.
     - Under the host's GNU Make 4.4.1: rc 0, 222/0.
     - With the round-1 Makefile, 1 polluted verilator line; at the head, 0.
   - The hosted `docs-check` step "Entity shape gate" succeeded at this exact head. This was run 37034468196, job 110929120688, on ubuntu-24.04: 222/0, and the three new arms appear in its log.
   - I reproduced the defect by restoring round 2's three files: under make 4.3 the plain gate gives rc 1 and the self-test 219/1.
   - Each new self-test arm can fail. My three planted defects in `classified_frozen_targets` and its caller are each rejected by a named arm, under both makes:
     - the derivation removed;
     - classification by file rather than by path;
     - another makefile's classification leaking in.
   - `CLASSIFIED_CONSUMERS` is byte-for-byte the same 5 entries as at `d81198c2`. The 4 entries already present at `cdf49d1a` are unchanged. The fix adds a match path only for a makefile's own `$`-classified references. A frozen token is matched only when make's expansion resolves it to the same repo path.
2. **The author's make 4.3 replay is consistent with the hosted contexts I checked.**
   - The hosted Verilator shard 0 (11 suites, 401,934 checks) and shard 3 (12 suites, 14,649 checks) tallies equal the replay's to the check.
   - The hosted `docs-check` Entity shape gate gives 222/0, equal to the replay's step 50.
   - Hosted shards 1, 2 and 4 and the two aggregates were still in progress at 17:20 UTC. Hosted acceptance belongs to the manager.
3. **The `max_dev_ns_o` checks work.**
   - R433-2's `meter_probes.py`, unchanged: 5/5 CAUGHT, clean control passing.
   - R432-2's `reviewer_meter_probes_r2.py`, unchanged: P1 and P2 are now CAUGHT on `rates` by the new named checks. P3, P4 and P6 are CAUGHT. P5 escapes the meter suite, as R432-2 recorded, and is caught at the root.
   - The three new named mutants fail their named checks in the suite's own campaign: 36/36 under make 4.3.
   - Seven further probes of mine, none of them in the campaign, are all CAUGHT. They plant:
     - a data restart that clears the reading;
     - saturation off by one;
     - a clear only on selection changes;
     - the timeout keeping the reading;
     - the bind edge keeping the reading;
     - a non-zero reading while not following;
     - a signed reading instead of an absolute one.
4. **The design page's Outputs bullet** (`MEDIA_CLOCK_FOLLOWING.md:994-998`) carries R432-2-R1's exact text, once, and the old text is gone.
5. **No RTL change.**
   - `git diff d81198c2..HEAD` touches only seven files: two docs, two scripts, the meter suite's `sim_main.cpp` and `mutants.py`, and the root suite's Makefile. Nothing under `hdl/`, `sw/`, `syn/`, `configs/` or `constraints/` changed, and all four gitlinks are unchanged against `cdf49d1a`.
   - So round 2's shipping image stands. Its WNS of +0.065 ns is the author's receipt; I did not rebuild it.

The author disclosed one host run of `scripts/act_ci.py --selftest` (offline, rc 0). AGENTS.md section 5 reserves that self-test for the CI job. I record it here as noted. It is not a finding against the head: the file's blob, `28f365a0`, is identical at the base, the head and live `dev` (`receipts/act_ci_identity.txt`).

## Findings

### R432-3-R1 - RESIDUE - Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md:998` - "The last two" lost its antecedent

- **Evidence:** R432-2-R1's text inserts a sentence, "The root composes the two into `AAFM_STAT`.", just before "The last two are the bench's measurement of a talker's timestamp regularity."
  - "The last two" meant the history-restart count and the largest deviation.
  - It now follows "the two", which means the status word and `max_dev_ns_o`.
  - The text came from my own round-2 RESIDUE.
- **Impact:** wording only. No measurement, figure, test, code, register or clause claim changes. `REGISTER_MAP.md:2083-2088` states the bit meanings correctly.
- **Exact fix:** replace "The last two are the bench's measurement of a talker's timestamp regularity." with "The history-restart count and the largest deviation are the bench's measurement of a talker's timestamp regularity."
- **Verification:** the replacement sentence is present at the merge head.

### R432-3-S1 - SUGGESTION - Tests, Robustness - `scripts/shape_consumer_inventory.py:199` and `tb/verilator/milan_dp_mclk/Makefile:62,70` - a database parse stopped by `$(error)` still counts as read

- **Evidence:** `receipts/inv_no_makeflags.log`.
  - I removed `MAKEFLAGS=` from both nested derivations.
  - Under make 4.4.1 the root suite's database then lists no frozen shape prerequisite (`(True, [])`).
  - The plain gate and `--self-test` still pass, 222/0, under both makes. So nothing guards the `MAKEFLAGS=` half of the fix.
  - The hosted make 4.3 reads the rules either way, so CI is not blinded.
  - The same pre-existing blind spot hides `tb/verilator/milan_dp_render/Makefile`'s rules under make 4.4.1. There the database read returns rc 2 with `*** ... print-srcs failed ... Stop.` and 0 rule lines, yet it is counted readable. That Makefile is untouched by this PR. The author already disclosed this as outside #629.
- **Impact:** on a make of 4.4 or later, the inventory can pass a makefile whose rule lines it never read. This is not a defect in this PR's head.
- **Suggested outcome (a separate Issue):** the database read fails closed when make stops the parse. For example, a non-zero exit with a `***` stop line could count as unreadable. Optionally, add an arm that plants an `$(error)` stop before a rule line.
- **Verification:** `scripts/probe_inventory.sh <copy> no_makeflags <make-4.3 dir>` fails under make 4.4.1.

No BLOCKER, MAJOR or MINOR finding.

## Prior findings on this PR, resolved or retained at this head

I read these after my own pass over the diff.

| Finding | Severity | Status at `0b066b6e` | Evidence |
|---|---|---|---|
| R433-2-F1: the hosted Entity shape gate is red under make 4.3 | MINOR (Tests, Docs) | CLOSED | `receipts/make43_checks.log`: both makes rc 0, 222/0. `receipts/hosted_docs_check_entity_shape_excerpt.txt`: the hosted step succeeds, 222/0. `receipts/inv_round2.log`: the defect reproduces under make 4.3 with round 2's files. `receipts/classified_set_diff.txt`: no entry weakened. The Docs half: the PR body's Round 3 section and the REVIEW READY state which make ran each step, and the replay table names make 4.3 for every call |
| R433-2-S1 = R432-2-S1: the era clear and saturation of `max_dev_ns_o` are ungraded | SUGGESTION | TAKEN | `sim_main.cpp:342-422` (`max_dev_levels`, run by `case_rates` at `:459`); `mutants.py:199-217`; `receipts/meter_suite43.log` (465/0, servo 6/0, campaign 36/36); `receipts/meter_probes433.log`; `receipts/meter_probes432r2.log`; `receipts/meter_probes432r3.log` |
| R432-2-R1: the Outputs bullet | RESIDUE | TAKEN | exact text present once at `MEDIA_CLOCK_FOLLOWING.md:994-998` (see R432-3-R1 for the knock-on wording) |
| R432-1 and R433-1 findings F1 to F7, the RESIDUE items and S2 | various | CLOSED or TAKEN at `d81198c2` (R432-2 and R433-2 tables) | round 3 touches none of their artifacts; `git diff d81198c2..HEAD --name-only` lists only the seven files in the Summary |
| R432-1-S1 = R433-1-S1: settle band on `mga_sel_w` | SUGGESTION | RETAINED, reason accepted | a design-table change needing its own decision; nothing in round 3 touches it |
| R433-1-S2: two-sided INTERNAL rate for render T30 | SUGGESTION | RETAINED for T30, reason accepted | unchanged since round 2 |
| R432-2 probe P5 (rising-only `tu` detector) | none (recorded escape) | unchanged: escapes the meter suite, caught at the root as R432-2 recorded | `receipts/meter_probes432r2.log` |

## Clean-lens results

These lines follow the AGENTS.md section 6 format.

```text
[R432] PASS Conformance — issue #629 comment 5952544402 items 1-4; KL_aaf_clock_meter.sv:155-158,489-493,583-599; REGISTER_MAP.md:2076-2090; MEDIA_CLOCK_FOLLOWING.md:994-1001; git diff d81198c2..0b066b6e --name-only — every item met as assigned: the gate passes under both makes with the classification kept, max_dev_ns_o graded as the port contract and register map state it (cleared by every era start and while not following, kept by a data restart, saturating at 65,535), R1 text exact; no RTL, port, processor-boundary or gitlink change
[R432] PASS RTL — git diff d81198c2..0b066b6e (no file under hdl/, sw/, syn/, configs/, constraints/; gitlinks equal to cdf49d1a); KL_aaf_clock_meter.sv:254,319,489-493,566-599 read against the new M1 checks — no RTL change; round 2's RTL and its image stand; the max_dev update and clear paths behave as the new checks require (receipts/meter_suite43.log, meter_probes432r3.log)
[R432] PASS Robustness — sim_main.cpp:342-422 (steps +65,535, +65,536, +/-100,000; 4 era events; exit window; lost PDU); milan_dp_mclk/Makefile:62,70 under make 4.3 and 4.4.1 with MAKEFLAGS [] and [w] (receipts/nested_derivation_matrix.txt: 110 sources, 0 "Entering"); shape_consumer_inventory.py:164-182,274-298 (fail-closed probe: an unsettled expansion classifies nothing; receipts/inv_*.log) — boundaries, sign, every era event and both makes handled; R432-3-S1 recorded as a SUGGESTION on a pre-existing gate behaviour
[R432] PASS Tests — mutants.py:199-217 and the campaign 36/36 (receipts/meter_suite43.log); R433-2 meter_probes.py 5/5 and R432-2 probes P1/P2 caught by named checks; 7/7 of my own max_dev probes caught (receipts/meter_probes432r3.log); entity_shape_selftest.py:340-398 arms 0m/0n/0o each failing under a planted defect, both makes (receipts/inv_no_derive.log, inv_overbroad.log, inv_cross_file.log); root suite 31/31 under make 4.3 with inherited MAKEFLAGS=w (receipts/root43.log); hosted shard 0 and 3 tallies equal to the replay — every new check can fail for its defect
[R432] PASS Docs — MEDIA_CLOCK_FOLLOWING.md:994-1001; TESTING.md:484; milan_dp_mclk/Makefile:46-54 comment; shape_consumer_inventory.py:68-70,274-287 docstrings; PR #634 body "Round 3" and its replay table against my receipts (465/0, 36/36, 31/31, 222/0, shard 0 401,934 and shard 3 14,649); git diff --check d81198c2..HEAD and cdf49d1a..HEAD rc 0; hosted docs-check success at the head — all accurate; one wording RESIDUE (R432-3-R1)
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-3 assignment items 1-4; meter port contract `:155-158`; `REGISTER_MAP.md:2076-2090`; design `:994-1001`; delta file list; gitlinks | R432-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| RTL | CLEAN | `KL_aaf_clock_meter.sv:254,319,489-493,566-599`; empty RTL, config and gitlink delta since `d81198c2` | R432-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Robustness | CLEAN (S1 is a SUGGESTION only) | M1 level boundaries and era events; nested derivation under two makes and two flag sets; inventory fail-closed paths | R432-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Tests | CLEAN | meter suite and its 36-run campaign; three prior probe scripts unchanged; 7 new probes; 6 inventory variants; root suite under make 4.3; hosted docs-check, shard 0 and shard 3 logs | R432-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Docs | CLEAN (R432-3-R1 is RESIDUE) | design Outputs bullet; TESTING row; Makefile and inventory comments; PR body Round 3; commit messages; `git diff --check` | R432-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |

## What was run

All of this ran in disposable copies of the exact head under `scratch/`. The review clone was never edited.

- **Make 4.3** was built from `make-4.3.tar.gz`, sha256 `e05fdde4...e19`, checked against the GNU tarball. The host make is GNU Make 4.4.1. The simulator is the pinned Verilator 5.050 (`receipts/tools_and_inputs.txt`).
- **`make43_checks.sh`** (R433-2), unchanged → `receipts/make43_checks.log`.
- **The meter suite:** `make -C tb/verilator/aaf_clock_meter` with make 4.3 first on PATH. This runs the cases, the servo and the campaign → `receipts/meter_suite43.log`, rc 0.
- **The root suite:** `MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk` under make 4.3 → `receipts/root43.log`, 31/31.
- **The prior probe scripts**, unchanged, with sha256 values in `receipts/tools_and_inputs.txt`:
  - `meter_probes.py` → `receipts/meter_probes433.log`;
  - `reviewer_meter_probes_r2.py` → `receipts/meter_probes432r2.log`.
- **`scripts/reviewer_meter_probes_r3.py`** (mine) → `receipts/meter_probes432r3.log`.
- **`scripts/probe_inventory.sh`** (mine), with variants head, round2, no_derive, overbroad, cross_file and no_makeflags → `receipts/inv_*.log`. Each copy was restored to 0 changed paths.
- **`scripts/classified_set.py`** (mine), on `cdf49d1a`, `d81198c2` and the head → `receipts/classified_set_diff.txt`.
- **Hosted context excerpts** at the exact head → `receipts/hosted_*`.
- **Exit codes** → `receipts/exit_codes.txt`.
- **Local paths** in the receipts are replaced by `$SCRATCH`, `$VERILATOR_ROOT`, `$SIM_PREFIX` and `$PINNED_SIM`.
- **Clone integrity** after all probes → `receipts/clone_integrity.txt`:
  - HEAD and tree are as above.
  - The index and the HEAD tree hash identically on (mode, blob, path).
  - Rehashing every worktree blob gives 0 mismatches.
  - The four gitlinks are unchanged.
  - `git status --porcelain --ignored` is empty, after I removed a `__pycache__` that one of my reads created.

## Real limits

- **The full replay was spot-checked, not re-run.** I did not re-run the author's full replay of every hosted job. I compared the hosted `docs-check` Entity shape gate and the hosted shard 0 and shard 3 tallies against it. Shards 1, 2 and 4, `verilator-suites` and `yosys-portability` were still in progress when I last checked.
- **No full banks were run.** Neither the parent, PP, gPTP, Yosys and builder banks nor the Markdown gates were run locally. For the Markdown gates I rely on the hosted `docs-check` success at this head.
- **The root suite** ran once, under make 4.3. Under 4.4.1 I checked only its nested derivation, as a dry run.
- **Not rebuilt:** the shipping image. There was no RTL change, so round 2's timing receipt stands as the author's evidence.
- **The make 4.3 binary** is built from the verified GNU tarball, not the runner's distribution package. The hosted run on ubuntu-24.04 confirms the result on the runner's make.
- **No hardware:** physical calibration NOT RUN, and no bench or hardware evidence was produced. Field skips are not hardware proof.

## Pending manager duties

- **Hosted acceptance** at this head: the remaining Verilator shards and both aggregates.
- **Order rule:** protocol-processor #141 lands first, then the parent bumps its pin.
- **Merge-turn candidate:** build and validate the final current-`dev` candidate (base `cdf49d1a`).
- **Residue checklist:** carry R432-3-R1.
- **Optional Issue:** file one for R432-3-S1, the gate's fail-closed database read.
- **Merge** only with explicit maintainer authorization.

R432-3 FINISHED
