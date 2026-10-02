[R433] POSITIVE - exact head 0b066b6e66df2a3ba3167805a6a591f8b96fa449

# [R433] Round R433-3: external delta review of PR #634 (issue #629, lane M2)

- **Head:** `0b066b6e66df2a3ba3167805a6a591f8b96fa449`, tree `3cc8846c933b348b09bec80f4a1a6b3543c7842b`.
- **Delta:** three commits on round 2's `d81198c2`: `bb65ac498`, `7f051b272` and `0b066b6e6`.
- **Source base and live `dev`:** `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- **Assignment:** [#629 comment 5952544402](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5952544402).
- **Author evidence:** `review-evidence/629-m2-r1/author-r3` on `629-m2-review-evidence` (archive `6811c91c`), and the PR body's "Round 3" section.

## Contents

- [Verdict](#verdict)
- [Scope reconstructed](#scope-reconstructed)
- [Findings](#findings)
- [Assignment items judged](#assignment-items-judged)
- [Prior public review findings](#prior-public-review-findings)
- [Per-lens results](#per-lens-results)
- [Ledger](#ledger)
- [Real limits](#real-limits)
- [Pending manager duties](#pending-manager-duties)
- [Clone integrity](#clone-integrity)
- [Receipts](#receipts)

## Verdict

**POSITIVE.** R433-2-F1 is closed. Both makes now pass the Entity shape gate:

- GNU make 4.3, which I built from the GNU tarball after checking its sha256;
- the host's GNU Make 4.4.1.

The evidence for this:

- I ran R433-2's `make43_checks.sh` unchanged. The gate reported rc 0, 222/0, under both makes.
- The hosted `docs-check` succeeds at this head, including step 51 "Entity shape gate". That step failed in round 2.
- The classification set is unchanged since round 2, keys and reasons alike.
- The new frozen-form match exempts only a token that names the classified path. When I planted a stray header in the same Makefile, the gate still refused it under both makes.

R432-2-S1 / R433-2-S1 is taken and graded:

- The meter suite passes 465/0, and the servo 6/0.
- The full campaign is 36/36, and each new mutant fails its named check.
- R433-2's probes, run unchanged, give 5/5 CAUGHT.
- R432-2's P1 and P2, run unchanged, are CAUGHT on `rates`.
- Four extra probes of mine are all caught, each by the check it targets.

R432-2-R1 is taken with the reviewer's exact text. Round 3 changes no RTL.

Open findings: nothing at MINOR or above. There is one RESIDUE (wording) and one SUGGESTION (a pre-existing gate weakness outside #629, for the manager to file).

## Scope reconstructed

- **Order read:** `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, then the #629 issue body and every public comment. Those comments include the M2 lane assignment, the rulings on the [A491] STOP, the round-3 assignment and the [A500] REVIEW READY.
- **Scope decisions:** the PR "Relates to #629" (lane M2 assignment, 5942692103). Bench acceptance belongs to a later bench lane. The PR body carries no closing keyword.
- **Round-3 items (assignment 5952544402):**
  1. R433-2 F1;
  2. every hosted job replayed under make 4.3;
  3. R432-2 S1 = R433-2 S1;
  4. RESIDUE R432-2-R1.

  No RTL change is expected. A processor-boundary or top-level port change is a STOP.
- **Independent pass first.** I reviewed `git diff d81198c2..0b066b6e` (7 files) on my own, and placed it in the PR's history from `cdf49d1a` (28 commits). Only then did I read the R432-2 and R433-2 reports.

## Findings

No BLOCKER, MAJOR or MINOR.

### R433-3-S1 - SUGGESTION - Robustness, Tests - the gate's database read counts a parse stopped by `$(error)` as readable (pre-existing, outside #629)

- **Where:** `scripts/shape_consumer_inventory.py:184-209` (`shape_prereqs_from_database`). Line 199 accepts any output containing `# Files`. The function is unchanged by this PR: `git diff cdf49d1a..HEAD` touches only the entry at `:83-86` and `:274-333`.
- **Evidence:** `receipts/gate_probes.log`, step 5.
  - I restored round 2's nested derivation (no `MAKEFLAGS=`) in a disposable copy.
  - Under GNU Make 4.4.1, `make -pqrR` then stops at `Makefile:64: *** ../milan_dp print-srcs failed`, and no rule is read.
  - The plain gate still returns rc 0.
  - At this head the parse completes under both makes (step 1), so the root suite's frozen prerequisite is read and classified. Nothing is lost today.
  - The author disclosed this in the REVIEW READY's open risks, for `milan_dp_render`.
- **Impact:** a makefile whose parse stops at `$(error)` under the database read is reported as verified, with no frozen prerequisites. Today this affects no consumer; it is a fail-open path in a guard.
- **Required outcome (optional, separate Issue):** a database whose parse stopped early is "unreadable", which fails closed.
- **Verification:** with the round-2 derivation restored, the plain gate fails under 4.4.1.

### RESIDUE (owner rule 2026-10-02: wording only; no effect on verdict or lens)

- **R433-3-R1.** `docs/design/MEDIA_CLOCK_FOLLOWING.md:997-999`.
  - The new sentence "The root composes the two into `AAFM_STAT`." now sits just before "The last two are the bench's measurement of a talker's timestamp regularity."
  - A reader can take "the last two" to mean the status word and `max_dev_ns_o`. It means the history-restart count and the largest deviation.
  - **Exact fix:** replace "The last two are the bench's measurement of a talker's timestamp regularity." with "The history-restart count and the largest deviation are the bench's measurement of a talker's timestamp regularity."

## Assignment items judged

### (1) R433-2 F1: the Entity shape gate under GNU make 4.3 and the host make

- **Cause, independently confirmed** (`receipts/gate_probes.log` step 5; `receipts/nested_derivation_equiv.log`; `receipts/nested_derivation_r2_host_dryrun_diff.txt`).
  - GNU make 4.4.1 exports its flags to `$(shell ...)`. With round 2's line, the nested `print-srcs` therefore ran under `-pqrR` and the parse stopped.
  - Under `-n`, the nested make printed `echo '--cc ...` into the source list. With round 2's Makefile, `make -n mclk-build` under 4.4.1 produced a different command line from 4.3.
  - With `MAKEFLAGS=` (`tb/verilator/milan_dp_mclk/Makefile:62,70`), the head's `--Mdir` line is identical (hash `f167afed98f55ae4`) in four cases: plain, `MAKEFLAGS=w MAKELEVEL=1`, `-j16`, and under both makes. With an `MCLK_MDIR=` command-line override it differs only by that override, the same under both makes. Under 4.3, round 2's line and the head's are byte-identical, so the change alters no derivation the hosted runner produced.
- **Fix judged.** `classified_frozen_targets` (`scripts/shape_consumer_inventory.py:274-298`) expands each classified makefile reference by make itself.
  - It considers only references containing `$`. For one makefile it returns at most one path. It returns nothing when make fails or the output has whitespace, which fails closed.
  - `_frozen_prereq_findings` (`:301-333`) skips a frozen token only when its resolved path equals one of those paths (`:328`).
  - `receipts/gate_probes.log` step 2 shows the result for `milan_dp_mclk/Makefile`: exactly `tb/verilator/milan_dp_mclk/obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh`, under both makes. `milan_dp/Makefile`'s literal entry yields `[]` and keeps its literal match.
- **No consumer weakened** (`receipts/classification_set_diff.txt`).
  - The set is identical, keys and reasons, between `d81198c2` and the head.
  - Since base `cdf49d1a`, the only addition is the root suite's entry, which carries its reason.
- **Fault probes** (`receipts/gate_probes.log` step 4; `receipts/selftest/fault_no_frozen_match_*`):
  - A stray `obj_stray/endstation_stray/gen/adp_shape_defaults.svh` prerequisite planted in the root suite's Makefile is refused under both makes (rc 1, "outside the tracked tree and is not classified").
  - With the match at `:328` disabled, the plain gate fails under 4.3 with exactly the hosted round-2 refusal. The self-test also fails, at the new control arm "I the classified fixture consumer resolves" (222 checks, 2 failures).
- **The three new self-test arms** (`scripts/entity_shape_selftest.py:340-398`, called at `:724`) all appear in `receipts/selftest/selftest_make43.full.log` and in `selftest_host_alone.full.log`:
  - the control "I the classified fixture consumer resolves = []";
  - "MUTATION rejected: a classified reference matched by its text alone";
  - "MUTATION rejected: a classified reference frozen before its definition".
- **R433-2's `make43_checks.sh`, unchanged** (sha256 `30881ceb...`, equal to the R433-2 packet's copy), gave the following (`receipts/make43_checks.log`):
  - round-1 Makefile: 1 polluted line under 4.3;
  - head: 0;
  - gate rc 0, 222/0, under GNU make 4.3;
  - gate rc 0, 222/0, under GNU Make 4.4.1.
- **Plain gate:** rc 0, 166/0, under both makes (`receipts/gate_plain_make43.log`, `receipts/gate_probes.log` step 3).
- **Root suite under make 4.3** with the pinned Verilator 5.050: rc 0, "31 checks: 31 PASS, 0 FAIL" (`receipts/root_suite_make43.log`).
- **Hosted, exact head:** run 37034468196 `docs-check` succeeded, all 55 steps, including step 51 "Entity shape gate" (`receipts/hosted_docs_check_steps_37034468196.tsv`).

**Note (not a finding):** I first ran the two self-tests at the same time in one copy. The self-test plants fixtures into tracked files, so the host-make run raced and failed at setup ("SELF-TEST SETUP: ... not in the source"). It is kept as `receipts/selftest/selftest_host.RACED-same-copy.*`. Run alone in a separate copy, it passes 222/0 (`selftest_host_alone.*`).

### (2) The author's replay of every hosted job under make 4.3

- **Compared against the hosted run** (`receipts/replay_vs_hosted_docs_check.txt`).
  - The author's `docs-check.summary.json` has 50 steps. Their names equal, in order, the 50 hosted steps of run 37034468196 (setup, post and complete excluded). All are rc 0.
  - 43 steps ran verbatim. 3 are substituted and marked: diagram dependencies (apt replaced by a presence check), sv2v install path, and step 43. The other 4 are action steps.
  - Every step that called make called only GNU make 4.3. Those are steps 19, 25, 26, 31 and 50, with 1 + 1,031 + 1,538 + 14 + 363 = 2,947 calls, as the PR body states.
  - Step 50 ran `--self-test`: 222/0, 363 calls.
- **Hosted contexts at this head** (`receipts/hosted_check_runs_0b066b6e*.tsv`, last read 17:36 UTC):
  - 17 succeeded: rtl-fast and its four jobs, docs-check, docs-check-no-git, wire-accountability, full-ci-gate, elaborate, Verilator shards 0, 3 and 4, and Yosys shards 0 to 3.
  - Physical gPTP is skipped, as on any PR.
  - Verilator shards 1/5 and 2/5 were still in progress, so the `verilator-suites` and `yosys-portability` aggregates had not reported yet.
- **Disclosure noted, not a finding against the head:** the author ran `scripts/act_ci.py --selftest` once on the host during a first replay attempt. AGENTS.md section 5 reserves that self-test for the CI job. The final replay marks step 43 NOT RUN and checks that the file is byte-identical to live `dev`.

### (3) `max_dev_ns_o`: era clear and saturation

- **Checks read** (`tb/verilator/aaf_clock_meter/sim_main.cpp:342-422`, run from `case_rates` at `:459`):
  - each of four era starts reads exactly 0 after a +100 ppm era that read 187 to 189 ns: listener change, entry, bind edge and the 100 ms timeout;
  - the exit window reads 0 while not following;
  - one lost PDU is no deviation;
  - steps of +65,535, +65,536 and ±100,000 ns at position 5 restart once and read min(|step|, 65,535).

  These match the port contract at `KL_aaf_clock_meter.sv:155-158` and the RTL at `:492-493` and `:598`. The count is 446 + 19 = 465.
- **Suite and campaign** (`receipts/meter_suite.log`):
  - Meter suite: "checks: 465 failures: 0".
  - Servo: "checks: 6 failures: 0".
  - That run's serial campaign was stopped by my 10-minute command limit after 24 verdicts, all as required.
  - I re-ran the whole campaign in parallel through the suite's own `MUTANTS`, `mutate`, `build` and `run_case`, imported unchanged: "36/36 as required" (`receipts/meter_mutants_parallel.log`).
  - Each new mutant fails its named check: `max_dev_not_cleared_at_era_start`, `max_dev_no_saturation` and `max_dev_includes_gap_pdus`.
- **R433-2's `meter_probes.py`, unchanged:** 5/5 CAUGHT, clean control PASS (`receipts/r433_2_meter_probes.log`).
- **R432-2's `reviewer_meter_probes_r2.py`, unchanged** (`receipts/r432_2_meter_probes.log`):
  - P1 and P2 are CAUGHT on `rates`.
  - P3, P4 and P6 are CAUGHT.
  - P5 (rising-only `tu`) ESCAPES the meter suite. R432-2 recorded it as caught at the root, and the author's round-3 evidence says the same. I did not run that root probe.
- **My own probes** (`scripts/r433_3_meter_probes.py`, `receipts/r433_3_meter_probes.log`): all 4 CAUGHT, clean control PASS.
  - A data restart clearing the maximum is caught by all four step checks. This grades "a data restart keeps it".
  - Clearing only while disabled is caught by the listener-change, bind-edge and timeout checks.
  - Every era start except the timeout clearing it is caught by both timeout checks.
  - The saturation bound moved up by one is caught by "step +65536".

### (4) The design page's Outputs bullet (R432-2-R1)

`docs/design/MEDIA_CLOCK_FOLLOWING.md:994-999` carries R432-2-R1's exact replacement text, with only the line wraps differing. Its new claim is true: `milan_datapath.sv:5705` assigns `aafm_stat_w = {max_dev_ns_w, status_w}`, and `milan_csr.sv:426` documents 0x8E0 as `{max_dev16, restarts8, idx4, 0, en, rate_valid, locked}`. One wording ambiguity remains next to it: R433-3-R1.

### (5) No RTL change

- `git diff d81198c2 HEAD -- hdl sw syn configs protocol-processor gptp-processor external third_party/verilog-axis` is empty.
- No gitlink changes anywhere in the PR (`cdf49d1a..HEAD`).
- The shipping image therefore stands at round 2's figures from the author's receipts: WNS +0.065 ns, WHS +0.036 ns. I did not re-run Vivado.
- There is no processor-boundary or top-level port change.

## Prior public review findings

| Finding | Original severity | At `0b066b6e` | Evidence (this round) |
|---|---|---|---|
| R433-2-F1: Entity shape gate fails under GNU make 4.3 | MINOR | **CLOSED** | Item (1): `make43_checks.sh` unchanged, rc 0 / 222/0 under both makes; hosted `docs-check` step 51 succeeded; classification set unchanged; fault probes refused |
| R432-2-S1 = R433-2-S1: `max_dev_ns_o` era clear and saturation ungraded | SUGGESTION | **TAKEN, closed** | Item (3): both reviewers' probes now fail named checks; three named mutants; four extra probes caught |
| R432-2-R1: design Outputs bullet | RESIDUE | **TAKEN** | Item (4), exact text; follow-on wording R433-3-R1 |
| R432-1 F1-F7, R433-1 F1-F3 (closed at `d81198c2` by R432-2 and R433-2) | MAJOR/MINOR | **remain CLOSED** | Round 3 touches none of their artifacts except the two documentation lines judged here and the meter suite, which still passes. The root suite passes 31/31 under make 4.3 |
| R432-1 S1 = R433-1 S1 (settle band keyed on `follow_sel_r`) | SUGGESTION | RETAINED, reason accepted | Design change to the merged settle table; no defect observed |
| R433-1 S2, render T30 part | SUGGESTION | RETAINED, reason accepted | Unchanged by round 3 |
| R432-2 note: P5 escapes the meter suite, caught at root | (observation) | unchanged | Re-observed ESCAPED in the meter suite; root probe not re-run by me |

## Per-lens results

```text
[R433] PASS Conformance - assignment 5952544402 items 1-4 against KL_aaf_clock_meter.sv:155-158,492-493,598; MEDIA_CLOCK_FOLLOWING.md:994-999; milan_datapath.sv:5705; hosted docs-check run 37034468196 step 51; PR body "Relates to #629" - each item's required outcome met at 0b066b6e; no RTL, port or gitlink change
[R433] PASS RTL - git diff d81198c2..0b066b6e over hdl/ sw/ syn/ configs/ and the submodules (empty); tb/verilator/milan_dp_mclk/Makefile:62,70 build recipe (receipts/nested_derivation_equiv.log: identical --Mdir line under make 4.3 and 4.4.1, plain, MAKEFLAGS=w, -j16) - no RTL change; build derivation unchanged on the hosted make
[R433] PASS Robustness - shape_consumer_inventory.py:274-333 fail-closed paths (make error, multi-word, frozen-before-definition, stray header under both makes); 4.4 flag export (-pqrR, -n, -j16) on the root suite; sim_main.cpp:342-422 boundaries 65,535/65,536/±100,000, gap, restart, four era starts - all hold; pre-existing fail-open noted as R433-3-S1 (SUGGESTION)
[R433] PASS Tests - entity_shape_selftest.py:340-398 (arms present, 222/0 both makes; control fails with the match disabled); mutants.py:199-219 and the full campaign 36/36; meter 465/0, servo 6/0; R433-2 probes 5/5; R432-2 P1/P2 caught; four reviewer probes caught; root suite 31/31 under make 4.3
[R433] PASS Docs - MEDIA_CLOCK_FOLLOWING.md:994-1001 (R432-2-R1 exact text; claim checked at milan_datapath.sv:5705); TESTING.md:484; Makefile:46-54 comment; inventory docstrings :68-70,:274-288; PR body Round 3 (replay table checked against hosted steps); docs_check.py and check_doc_paths.py rc 0; no round-3 added em-dash; git diff --check clean - wording residue R433-3-R1 only
```

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The round-3 assignment items 1-4; meter port contract `KL_aaf_clock_meter.sv:155-158`, `:492-493`, `:598`; design `MEDIA_CLOCK_FOLLOWING.md:994-999`; `milan_datapath.sv:5705`; hosted `docs-check` 37034468196; PR body Round 3 | R433-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| RTL | CLEAN | Empty RTL/config/submodule diff `d81198c2..0b066b6e` and no gitlink change since `cdf49d1a`; `tb/verilator/milan_dp_mclk/Makefile:62,70` derivation equivalence under both makes; meter max-deviation RTL read against the tests | R433-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Robustness | CLEAN (S1 is SUGGESTION) | `scripts/shape_consumer_inventory.py:184-333` fail-closed and fault probes under both makes; make 4.4 flag-export contexts; `sim_main.cpp:342-422` boundary and era cases | R433-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Tests | CLEAN | `scripts/entity_shape_selftest.py:340-398,724`; `tb/verilator/aaf_clock_meter/sim_main.cpp:342-459`, `mutants.py:199-219`; meter suite, servo, 36/36 campaign; two prior reviewers' probe scripts, unchanged; four reviewer probes; root suite 31/31 under make 4.3; self-test fault probe | R433-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |
| Docs | CLEAN (R1 is RESIDUE) | `docs/design/MEDIA_CLOCK_FOLLOWING.md:994-1001`; `docs/testing/TESTING.md:484`; Makefile and inventory comments; PR body Round 3 and replay table; `docs_check.py`, `check_doc_paths.py`, em-dash scan, `git diff --check` | R433-3 | `0b066b6e66df2a3ba3167805a6a591f8b96fa449` |

## Real limits

- **Not run:**
  - physical calibration, the bench and hardware;
  - Vivado (the image figures are the author's round-2 receipts);
  - the full suite sweep, builder bank, native bank and the Yosys bank (the manager's);
  - Docker or act;
  - the candidate's `act_ci.py` and its self-test;
  - the root-level P5 probe.
- **Hosted:** I read hosted contexts but do not own their acceptance. Two Verilator shards and the two aggregates were still pending at my last read.
- **Make versions:** make 4.3 was built locally from the GNU tarball (sha256 `e05fdde4...e19`). The hosted runner's own make version is inferred from R433-2 and the hosted step result, not from the hosted log.
- **Serial campaign:** the serial campaign inside `make -C tb/verilator/aaf_clock_meter` was cut at my time limit. Its 36/36 verdict is from the parallel replay, which uses the same driver functions.
- **Redaction:** one receipt line (`receipts/gate_probes.log`, step 5, host make) was redacted after capture. Round 2's derivation under 4.4.1 put the nested make's whole database, including the host environment, into that line. `scripts/gate_probes.sh` now truncates that line. Host home paths in the build logs are written as `$HOME`.

## Pending manager duties

- Confirm the hosted Verilator shards 1/5 and 2/5 and the `verilator-suites` and `yosys-portability` aggregates at this head, and accept the act replica.
- The merge turn:
  - protocol-processor #141 lands first and the parent bumps its pin (the design's order rule);
  - then the candidate merge build on current `dev`, and post-merge containment.
- Carry R433-3-R1 to the residue checklist.
- File R433-3-S1 if wanted. The R432-2 note on the unguarded nested derivations in `milan_dp_render/Makefile` and `pp_shadow/Makefile` still applies; both files are outside this PR.

## Clone integrity

`receipts/clone_integrity.txt`, after all probes:

- HEAD `0b066b6e`, tree `3cc8846c`.
- `git status --porcelain --untracked-files=all` is empty.
- The index and the worktree equal HEAD.
- Index (mode, blob, path) entries equal the HEAD tree.
- Every worktree blob re-hashes to its index blob.
- The gitlinks are `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `b2db3a97` and `third_party/verilog-axis` `48ff7a7e`, all unchanged from the base.
- Every probe ran in disposable copies under `scratch/`, each restored and checked by `git diff --quiet`.

## Receipts

Every publishable file is listed with its sha256 in `MANIFEST.sha256`.

- **Scripts** (`scripts/`):
  - `campaign.sh`, `gate_probes.sh`, `selftest_probes.sh`, `nested_derivation_equiv.sh`, `meter_mutants_parallel.py` and `r433_3_meter_probes.py` are mine;
  - `make43_checks.sh`, `meter_probes.py` and `reviewer_meter_probes_r2.py` are the prior reviewers', unchanged.
- **Receipts** (`receipts/`): the logs and rc files named above, the hosted check and step tables, `replay_vs_hosted_docs_check.txt`, `classification_set_diff.txt` and `clone_integrity.txt`.

R433-3 FINISHED
