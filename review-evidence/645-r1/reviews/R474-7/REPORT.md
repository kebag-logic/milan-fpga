[R474] POSITIVE - exact head 7426045c94c317363e5589856e6f3f9fde1a2d21

Round R474-7 is the internal independent review of issue #645 / PR #672. It covers the delta `1e79ebdc..7426045c`: round 2h (`8e4b1e53`, assignment 6075072415) and round 2i (`7426045c`, assignment 6076487047, REVIEW READY 6076845205).

- Exact head: `7426045c94c317363e5589856e6f3f9fde1a2d21`, tree `472a2a9a844429005aec3dbd396fa02be29bf39d`.
- Source base and live dev: `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.

I applied all five lenses, and each is CLEAN at this head. There is no open BLOCKER, MAJOR or MINOR. The round leaves one RESIDUE, which is wording only, and three SUGGESTIONs.

All four assigned prior findings are RESOLVED: R474-5-F1, R475-6-F1, R474-5-S1 and R475-7-F1.

I wrote my verdict draft before reading any prior review finding: `receipts/DRAFT-VERDICT-PRE-PRIOR-READ.md`. Before that point, the only prior-reviewer material I used was the probe script and probe inputs the assignment names.

## What was examined

Reconstruction order:

1. AGENTS.md / CONTRIBUTING.md.
2. docs/README.
3. The issue body and the manager rulings for rounds 2g, 2h and 2i (6073617515, 6075072415, 6076487047).
4. The handoffs 6074038320, 6075441876 and 6076845205.
5. The delta diff and history.
6. The public author receipts: `author-r2h` (archive `5c575da7`) and `author-r2i` (evidence tip `49a9c79c`).
7. The raw hosted job logs.
8. The PR body's Round 2h and 2i sections.

The delta touches seven files and no RTL:
- `tb/verilator/follow_ring/{Makefile,sim_main.cpp,trace_table.py,test_trace_table.py}`
- `tb/verilator/milan_dp_render/Makefile` (comments only)
- `docs/testing/TESTING.md`
- `scripts/measure_test_evidence_readers.py`

The only non-comment Makefile change is the `run` target at `tb/verilator/follow_ring/Makefile:83-84`, from round 2h. Round 2i's edits to both Makefiles are comment-only. These are byte-identical to `1e79ebdc`:
- `hdl/`
- `scripts/run_all_suites.sh`
- `scripts/measure_test_evidence.py`
- `docs/testing/CI_WORKFLOWS.md`
- `.github/`

### Executed evidence (all in this packet)

The simulator was Verilator 5.050 through the pinned launcher (identity checked). Commands ran on a heavily loaded shared host: load average 40 to 80 on 16 CPUs.

| # | Probe | Result | Receipt |
|---|---|---|---|
| E1 | Cold `follow_ring` default, run exactly as the sweep runs it. Command: `env -u MAKEFLAGS taskset -c 0-3 timeout 1800 make -C tb/verilator/follow_ring`, from a fresh `git archive` of HEAD. | rc 0 in 838.9 s.<br>b8 48/0, pullin 18/0, small pulls 10/10, controller PASS at 6.25/25/50/100 MHz.<br>One `-Mdir obj_dir` elaboration plus the separate `_fine` build.<br>`suite_tally --verdict` rc 0; tally 66 checks, 0 failures. | `receipts/follow_ring_serial_taskset4.{log,rc}`, `scripts/run_suite.sh` |
| E2 | Cold `follow_ring` default under an outer `make -j16 --trace`, on a second fresh copy (CPUs 4-15). | rc 0 in 673.8 s, with the same four legs and all checks.<br>`make[1]: warning: -j4 forced in submake: resetting jobserver mode` shows the leg pool is bounded at four.<br>The `--trace` lines show `build` (obj_dir) made once before `b8`/`pullin` start, plus the nested `_fine` build.<br>Verdict rc 0; tally 66/0. | `receipts/follow_ring_outer_j16_trace.{log,rc}` |
| E3 | Fail path. A first attempt used an archive missing `tb/verilator/common`, which was my packaging error. | The `-j4` sub-make carried the failed build to the caller: top-level rc 2 at `Makefile:84`. | `receipts/incidental_missing_include_fail_path.{log,rc}` |
| E4 | `python3 -B tb/verilator/follow_ring/test_trace_table.py -v` at head. | 8/8 OK. | `receipts/test_trace_table.{log,rc}` |
| E5 | The same unchanged test file against the `8e4b1e53` reader. | rc 1; 22 subtests fail (decimal edges, 1e-30 neighbours, final-bin/servo). | `receipts/test_trace_table_vs_parent_8e4b1e53.*` |
| E6 | R475-7's unchanged `decimal_boundaries.py <source> <packet>`. | Head 9/9 (rc 0); `8e4b1e53` reader 0/9 (rc 1). | `receipts/decimal_boundaries_head.*`, `receipts/decimal_boundaries_parent_8e4b1e53.*`, `probes/r475-7-head/`, `inputs/r475-7/` |
| E7 | R474-5's trace-table probe inputs, `--from-s 0 --to-s 1 --step-s 0.25`. | `slips` 0 in every bin, including the +1.3 to +5.3 margin step. `event_trace unavailable`, so the missing evidence is marked. | `receipts/r474-5-probe-head.txt`, `inputs/r474-5-probe/` |
| E8 | A boundary fuzzer I wrote with an independent integer oracle in 1e-30 s units. Inputs: 6 planted cases plus 120 random decimal origin/from/to/step cases, with events and PDUs at exact edges, ±1 ns and ±1e-30 s. The planted cases include:<br>- 997 bins of 0.1 s from origin 0.3, with edges at k = 1..996<br>- the default −2..60 s window edges<br>- a short final bin<br>- exponent-form CLI values<br>- simultaneous dup/skip/recentre<br>- a bin starting before t = 0<br>- a log with no completion record | Head 126/126 agree on slips, skips, recentres, PDU attribution, row count, servo snapshot and `event_trace`.<br>`8e4b1e53` reader 3/126. | `scripts/boundary_oracle.py`, `receipts/boundary_oracle_head.*`, `receipts/boundary_oracle_parent_8e4b1e53.*`, `probes/boundary-oracle-head/` |
| E9 | 14 planted `trace_table.py` defects against the standing unit tests:<br>- float times<br>- inclusive end / exclusive start for events<br>- inclusive end for PDUs<br>- recentre counted as a slip<br>- recentre masking a simultaneous slip<br>- skips not a subset of slips<br>- strict servo comparison<br>- no final-bin clip<br>- coverage always complete / never complete<br>- float bin index for events / for PDUs<br>- the old margin-jump heuristic | 14/14 caught. | `scripts/trace_table_mutants.py`, `receipts/trace_table_mutants.*` |
| E10 | Real harness controls with `--trace`, from the E1 binary (sha256 in `probes/real-controls/binary.sha256`):<br>- the author's duplicate repro<br>- my own duplicate variant (dwell 8 s, phase 0.3)<br>- my own skip variant (`--peer-ppm 30`, dwell 14 s): 17 genuine skips<br>- the standing pull-in leg | Every printed harness window `[a, e) s: ring slips D+S` agrees with the table run as that one bin. Whole-run totals equal the event records. The pull-in's ~4-tick recentre margin step reports slips 0, recentres 1. | `scripts/real_controls.sh`, `scripts/real_control_tables.py`, `receipts/real_control_tables.*`, `probes/real-controls/` (full PDU traces by hash only) |
| E11 | The hosted windows recomputed from the raw job logs (successive verdict timestamps). | Run 37892515345 / job 113696564335 at `8e4b1e53`, ubuntu-latest (image ubuntu-24.04):<br>- `follow_ring` 1114.209635 s → 1114.2 PASS (325.8 / 685.8)<br>- `milan_dp_render` 1218.689947 s → 1218.7 PASS (221.3 / 581.3)<br>Run 37882435947 / job 113665137864 at `1e79ebdc`:<br>- `follow_ring` 1422.496 s<br>- `milan_dp_render` 1093.949 s | `inputs/hosted/job-*.log` |
| E12 | Focused gates at head:<br>- `docs_check.py`<br>- `check_doc_style.py`<br>- `measure_test_evidence.py --check`<br>- `measure_test_evidence.py --selftest`<br>- `git diff --check` (base..head and 1e79ebdc..head) | All rc 0. `check_em_dash.py` could not judge because its pinned renderer is not installed here. A direct scan of the added Markdown lines (base..head) found 0 U+2014. | `receipts/gates/` |
| E13 | Clone integrity after probes. | HEAD, index == HEAD tree, 1232 tracked blobs and modes match, gitlinks unchanged. One ignored `scripts/__pycache__` that a docs gate created was removed. | `receipts/clone_integrity.txt` |

## Lens results

```text
[R474] PASS Conformance - tb/verilator/follow_ring/Makefile:83-84, trace_table.py:1-152, TESTING.md:288-360, scripts/measure_test_evidence_readers.py:92-98 - ruling 6075072415 items 1-5 and ruling 6076487047 items 1-2 checked one by one against the head. The four standing legs run in a bounded -j4 sub-make after one shared b8/pullin build, under the sweep's own invocation and under outer -j16 (E1, E2); no leg left the default. Slips come from counter events and recentres sit in a separate column (E7, E10). The docstring states depth 16 / target 11 (line 12). Exact [start, end) bins apply to events and PDUs with decimal origins and steps (E6, E8). The records state the 8e4b1e53 hosted windows with run, job and runner class, and keep the replica figures as projections (E11). The mutants clause is present. No target or suite list changed. The hosted figure 1114.2 s at 8e4b1e53 meets the 1260 s line; acceptance at this head is the manager's.
[R474] PASS RTL - git diff 1e79ebdc..7426045c -- hdl (empty); follow_ring/Makefile:83-84; sim_main.cpp:617-625 - no RTL, configuration or pin change, so the round 2f resource records stay applicable. The harness change only prints existing counter/pulse vectors inside write_trace when --trace is given, so default legs produce no new output and no grading change. Make structure: build is a phony dependency of b8 and pullin inside one sub-make and is made once (E2 --trace). small-pullin and settle-control use disjoint MDIRs (obj_dir_fine, obj_dir_control). mutants.py:148 calls `make build`, not `run`, so it is unaffected.
[R474] PASS Robustness - E3, E8, E10; trace_table.py:43-52,78-85 - a failed leg or build propagates a non-zero rc through the sub-make (E3). Non-finite and non-decimal times are rejected; a non-positive step and an empty range are rejected. 126/126 oracle cases agree, including 1e-30 s neighbours, a 997-bin decimal walk, default window edges, a short final bin and bins before t=0. Real dup, skip and recentre traces match the harness's own counts. A log without the completion record is marked unavailable, not zero-proof. Concurrent leg output: no split line in E1/E2 or in the author logs (see S1).
[R474] PASS Tests - tb/verilator/follow_ring/test_trace_table.py:49-160 at 7426045c - every planted reader defect fails at least one standing test (E9, 14/14). The parent reader fails 22 subtests (E5). R475-7's probe gives 9/9 at head and 0/9 at the parent (E6). The tests drive the real CLI and grade its CSV output, not helpers. The real-trace controls (E10) cover what fixtures cannot. follow_ring's default keeps all four legs and every check (E1/E2: 48 + 18 + 10/10 + 4 rates).
[R474] PASS Docs - docs/testing/TESTING.md:288-360; tb/verilator/follow_ring/Makefile:22-37; tb/verilator/milan_dp_render/Makefile:46-61; PR body Round 2h/2i sections; trace_table.py:1-31 - every figure was recomputed and matches its receipt: hosted 1114.2/1218.7 and 1422.5/1093.9 from the raw job logs (E11); replica 437.204/793.308 from author-r2h jobs/{follow,render}-default.result.json; 800.2/826.7 from R474-5 receipts/runs/T1,T2 .time (800.207507093, 826.708349028); ratios 1.78 and 1.324 (rounded up); projections 778.2/1050.3; every margin (17.5/377.5, 346.1/706.1, 661.8/1021.8, 389.7/749.7, 325.8/685.8, 221.3/581.3, 481.8 to 1260); ~11 % (1218.7/1093.9 = 1.114); 708 = 1260/1.78. The render underestimate is stated. One wording residue (R474-7-R1).
```

## Findings

### R474-7-R1 RESIDUE

- **Lenses:** Docs.
- **Location:** `tb/verilator/follow_ring/trace_table.py:20-21`.
- **Evidence:** the docstring says the servo columns are taken "before the step's end". The code (`trace_table.py:131`, `w[0] <= te`) and the standing test `test_partial_last_bin_and_servo_timestamp` (`test_trace_table.py:142`) take the last window at or before the bin end. A window stamped exactly at the end is included, and the E9 `servo-strict` mutant is caught for excluding it.
- **Impact:** wording only. No figure, test, code or output changes.
- **Exact fix:** "trim (ppm) and the meter's rate validity at or before the step's end".
- **Verification:** read the docstring against `trace_table.py:131`.

### R474-7-S1 SUGGESTION

- **Lenses:** Robustness, Tests.
- **Location:** `tb/verilator/follow_ring/Makefile:84`.
- **Evidence:** the four legs now share the suite log concurrently. Their C stdout is block-buffered when redirected, and b8 prints 4484 bytes (author r2h log), so the one line that straddles its 4096-byte flush can be split by another leg's line.
- **Why it does not affect the sweep today:** at the current output layout that line is b8's `ERROR-DISTRIBUTION: [SW] CRF to AAF` line, which no sweep reader parses. The tally and `RESULT:` lines are always in the final contiguous write. No split was seen in E1, E2 or the author logs, and a split could only produce a loud accounting failure, never a masked pass.
- **Optional outcome:** `$(MAKE) -j4 --output-sync=target ...` (or line-buffered stdout in the harness) would make leg output atomic.
- **Verification:** grep the suite log for mid-line markers, and run `suite_tally --verdict`.

### R474-7-S2 SUGGESTION

- **Lenses:** Robustness.
- **Location:** `sim_main.cpp:271,606,622-631`.
- **Evidence:** `trace_table.py` is now exact over the digits it reads. The harness prints them at different resolutions: events %.9f (1 ns), PDU arrivals %.7f (100 ns), servo and the CLOCK_SOURCE origin %.6f (1 µs). So an event and a PDU at the same simulator instant can, very rarely, fall on opposite sides of a bin edge.
- **Optional outcome:** print every trace time at 1 ns, or state the input resolutions in the docstring.
- **Verification:** a traced run with equal-precision columns.

### R474-7-S3 SUGGESTION

- **Lenses:** Docs.
- **Location:** `docs/testing/TESTING.md:354-356`.
- **Evidence:** the line says the unit tests cover "genuine duplicate and skip frames". They feed counter-event fixture records; genuine harness traces are exercised only by the published controls (author r2i `fresh-tables/`, E10 here).
- **Optional outcome:** "counter-event duplicate and skip records". Optional because the meaning (counter events rather than margin inference) is recoverable from the next sentences.

## Prior findings at this head

| Finding (original severity / lenses) | Status at 7426045c | Evidence |
|---|---|---|
| R474-5-F1 (MINOR / Tests, Docs) | **RESOLVED** | `TESTING.md:288-345` and both Makefile headers state the measured hosted windows at `8e4b1e53`, with run, job and runner class and both margins. The replica figures are kept as projections and render's underestimate is stated. The remainder R475-7 retained (raw receipts for 437.204 / 793.308) is closed: `author-r2h/jobs/follow-default.result.json` and `render-default.result.json` carry exactly those seconds, rc 0, the stated CPU lists and cold builds. The `env -u MAKEFLAGS` command is recorded in its HANDOFF. All hosted figures were recomputed from the raw logs (E11). |
| R475-6-F1 (MINOR / Tests, Docs) | **RESOLVED** | Counter and pulse events come from `sim_main.cpp:622-625`, and `trace_table.py` keeps slips, skips and recentres separate. The R474-5 probe shows slips 0 / unavailable (E7). The real pull-in recentre gives slips 0, recentres 1. Real dups and 17 skips are counted (E10). The margin-jump mutant is caught (E9). |
| R474-5-S1 (SUGGESTION / Docs) | **RESOLVED** | `scripts/measure_test_evidence_readers.py:97-98` now reads "It is the explicit mutants target, outside the default sweep". `measure_test_evidence --check` and `--selftest` pass (E12). |
| R475-7-F1 (MINOR / Robustness, Tests, Docs) | **RESOLVED** | Exact `Fraction` arithmetic covers origins, bounds, steps, events, PDUs, servo and completion (`trace_table.py:43-131`), with no grace interval. Evidence: R475-7's probe 9/9 (parent 0/9), 126/126 oracle cases, 14/14 mutants, and regressions for inclusive start, exclusive end and interior edges for dup, skip and recentre (`test_trace_table.py:90-160`). |
| R474-4-F1 (MAJOR / Tests, Docs) | Defect remains **RESOLVED**. Acceptance at this head is pending with the manager. | Hosted `follow_ring` was 1114.2 s ≤ 1260 s at `8e4b1e53`. The `run` target is byte-identical since then. |
| R474-1-F1..F4, R474-2-F1, R475-1-F1..F3, and the earlier RESIDUE items | Remain **RESOLVED** | The delta touches none of their artifacts: no `hdl/`, chmap harness, design pages or traceability inputs. |
| R474-2-S1, R474-2-S2, R474-2-S3 / R474-1-S2 (SUGGESTION) | **RETAINED** (optional) | `settle_control.py`, `quiet_distributions.py` and `sim_ax1x1gptp.cpp` are unchanged in the delta. |

## Hosted state at this head (inspected, not owned)

`gh pr checks 672`, read 2026-10-09 08:19 UTC (`receipts/gh_pr_checks_head_final.txt`):

- **Passed (executed):** elaborate, yosys-elaboration, Yosys shards 0-3/4, Verilator shard 3/5, verilator-lint, changes, full-ci-gate, bdd-conformance, docs-check-no-git, wire-accountability.
- **Pending:** Verilator shards 0/5 (which carries `follow_ring` and `milan_dp_render`), 1/5, 2/5 and 4/5, plus docs-check and firmware-unit. The rtl-fast, rtl-full and docs runs are in progress.
- **Skipped context, not executed:** Physical gPTP (nightly and manual).

I do not withhold the verdict for these runs. Accepting them is the manager's duty.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings 6075072415 / 6076487047 against `follow_ring/Makefile:83-84`, `trace_table.py`, `TESTING.md:288-360`, `measure_test_evidence_readers.py:92-98`; E1, E2, E6-E8, E10, E11 | R474-7 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| RTL | CLEAN | empty `hdl/` delta; `follow_ring/Makefile` make graph (E2 `--trace`); `sim_main.cpp:617-625`; `mutants.py:148` | R474-7 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Robustness | CLEAN (S1 and S2 optional) | E3 fail path; E8 126 cases; E10 real controls; `trace_table.py:43-52,78-85` input rejection | R474-7 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Tests | CLEAN | `test_trace_table.py` 8/8; E5 parent 22 failing; E6 9/9 vs 0/9; E9 14/14; E1/E2 default legs with all checks | R474-7 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |
| Docs | CLEAN (R474-7-R1 residue; S3 optional) | `TESTING.md:288-360`; both Makefile headers; PR body 2h/2i; `trace_table.py:1-31` docstring; every figure against its receipt (E11, author-r2h, R474-5 runs) | R474-7 | 7426045c94c317363e5589856e6f3f9fde1a2d21 |

## Real limits

- **Contended wall times:** my wall times (E1 838.9 s, E2 673.8 s) were measured on a host oversubscribed roughly 3 to 5x by unrelated jobs. They do not reproduce or contradict the author's 437.204 s replica or the 708 s replica bar. They show only correct function under contention. The hosted 1114.2 s at `8e4b1e53` is the measured basis, and this head's hosted figure is still pending.
- **`milan_dp_render` default not executed:** its Makefile change since `1e79ebdc` is comment-only, and its hosted PASS at `8e4b1e53` is recorded above.
- **`make mutants` and the `tdm8render-pullin` campaign not run:** `mutants.py` and its inputs are untouched by the delta, and it uses `make build`, not `run`. Both campaigns are owned by the manager's merge bank.
- **Not run (not permitted in this round):** builder, the full docs, parent, processor or Yosys banks, act, and Docker.
- **`check_em_dash.py` could not run:** its pinned renderer is not installed. A direct scan of the added lines was substituted.
- No manager source bank ran at this head, and I claim none. Source-head execution evidence here is my own probes plus the author's published receipts.
- Physical calibration was NOT RUN. Simulation results and field skips are not hardware proof. No hardware was used.

## Pending manager duties

- Hosted acceptance at this exact head: a successful `verilator-suites` with `follow_ring` at or under 1260 s (shard 0/5 is pending), plus the act replica.
- Build and validate the current-dev merge candidate in the builder and native banks. Source base and live dev were both `6aa25dec`; re-check at the merge turn.
- Run the explicit campaigns owned by the merge bank: `make -C tb/verilator/follow_ring mutants SWEEP_JOBS=4` and `make -C tb/verilator/milan_dp_render tdm8render-pullin`.
- Carry R474-7-R1 to the residue checklist. Carry S1-S3 and the retained R474-2-S1/S2/S3 as optional.
- After merge: the B-lane bench repeat of the INTERNAL→AAF and AAF→CRF switches, post-merge containment, and issue closure.

R474-7 FINISHED
