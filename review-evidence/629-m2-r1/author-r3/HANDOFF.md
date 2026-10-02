# HANDOFF: lane M2 round 3 ([A500]), issue #629, PR #634

Status: REVIEW READY at `0b066b6e66df2a3ba3167805a6a591f8b96fa449` (three commits on `d81198c2`; local, not pushed)

- Start head: `d81198c2001756fd84c353d93c312c133c5af66b` on `629-media-clock-impl`; commits added, none amended; local, not pushed.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5952544402
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5952609830
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5956715967
- Reviews answered: R433-2 (F1, S1), R432-2 (S1, R1).
- GNU make 4.3: built in scratch from the GNU tarball, sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19` (`./configure && sh build.sh`), `GNU Make 4.3`. Host make: `GNU Make 4.4.1`.
- Simulator: the pinned Verilator 5.050 (wrapper first on PATH). Scratch: `$VALIDATION_STORAGE/629-a500/` (not in the tree, not in this directory).

## Items

| # | Item | Commit | State |
|---|---|---|---|
| 1 | R433-2 F1: Entity shape gate under make 4.3 and the host make | `bb65ac498` | done; `make43_checks.sh` gate rc=0 for both makes |
| 2 | Hosted `docs-check` (and every job this PR feeds) replayed step by step under make 4.3 | (no tree change) | done at `0b066b6e`; every job green, every make call 4.3 |
| 3 | R432-2 S1 = R433-2 S1: `max_dev_ns_o` era clear and saturation graded | `7f051b272` | done; both reviewers' probes caught |
| 4 | R432-2-R1: design page meter "Outputs" bullet, the reviewer's exact text | `0b066b6e6` | done |

## Item 1: the change

Cause (reproduced): GNU make 4.4 exports its own flags to `$(shell ...)`. So `make -pqrR`, the inventory's database read (`scripts/shape_consumer_inventory.py:181-209`), ran the root suite's nested `$(shell $(MAKE) ... print-srcs)` in question/print mode. print-srcs failed, and the parse stopped at the `$(error)` on `tb/verilator/milan_dp_mclk/Makefile:59`, before any rule line. 4.4.1 therefore listed no frozen prerequisite for that file, and the gate passed with nothing read. GNU make 4.3 (the hosted runner's) does not export them to `$(shell)`. It read the whole file and listed the `mclk-build` prerequisite in its expanded form, `obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh`. `CLASSIFIED_CONSUMERS` held only the spelled form `$(MCLK_GEN)/gen/adp_shape_defaults.svh`, and a database token is never spelled that way (`:206` drops any token with `$`), so the classification could not match. At `d81198c2` plain mode under make 4.3 also fails, rc 1, 166 checks, 1 failure (`receipts/es_plain_43_head.log`).

Fix (`bb65ac498`):
- `scripts/shape_consumer_inventory.py:274-298`: new `classified_frozen_targets(name)`, called at `:316-329`; the `CLASSIFIED_CONSUMERS` comment at `:68-70` says how a makefile entry is matched. For each classified reference of a makefile that carries a variable, make itself expands it in that makefile's directory (`probe_make`, `$(abspath ...)`), and a frozen prerequisite that resolves to the same repo path is that classified consumer, with its reason. No second literal: the frozen form is derived by make. A reference make cannot settle to one word classifies nothing, so its frozen token stays a finding (fail closed). `_frozen_prereq_findings` asks it only when a token is not classified directly. The classified entry for the root suite, with its reason, is unchanged.
- `tb/verilator/milan_dp_mclk/Makefile:50-54,62,70`: both nested derivations run as `$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C $(DP) ...)`. The nested make takes no flag from the parent (`w`, `q`, `p`, `n` alike), so under 4.4.1 the `-pqrR` parse also completes and the classification is exercised on both makes. `--no-print-directory` stays (R432-1 F2).
- `scripts/entity_shape_selftest.py:340-400` (`_prove_classified_frozen_form`, run at `:724`): three arms on a planted copy of `tb/verilator/csr/Makefile` with a temporary classified fixture reference:
  - 0m (control, `ck`): a classified reference reaching a rule line through a variable resolves clean;
  - 0n (mutation): the derivation removed (classification by the unexpanded text alone, the hosted refusal) is rejected, naming the fixture and "outside the tracked tree";
  - 0o (mutation): a rule line that runs before the variable is defined freezes an empty prefix; that frozen form names another path and is rejected.
- No other consumer changed; no other `CLASSIFIED_CONSUMERS` entry changed.

Evidence (copies in `receipts/`; home prefix written `$HOME`):
- `make43_checks.sh` (R433-2 packet, unmodified) at `bb65ac498`: round-1 Makefile 1 polluted verilator line, head 0; `check_entity_shape.py --self-test` gate rc=0 under make 4.3 (222/0) and under GNU Make 4.4.1 (222/0) (`make43_checks_item1.log`).
- Database probe per makefile (`scripts/db_probe.py`; `receipts/db_probe_final.log` at the final head): after the fix, `milan_dp_mclk/Makefile` reads rc=1 (question mode, not up to date), no stop, token `obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh` under both makes; before, 4.4.1 read rc=2 `Makefile:59: *** ... Stop.` with no token.
- `make -n mclk-build` under `MAKEFLAGS=w MAKELEVEL=1`, both makes: 110 `.sv` sources, 0 polluted tokens.
- Root suite under make 4.3 at `bb65ac498`: `make -C tb/verilator/milan_dp_mclk` rc 0, legs A 55/0, C 32/0, B 50/0, campaign 31/31, 7:02 (`mclk43_item1.log`; the model was up to date from round 2's build, so this run re-derived both nested lists but did not recompile. Shard 2's run below is a clean build).

## Item 2: every hosted job replayed under GNU make 4.3

Method (`scripts/replay_workflow.py`, `scripts/replay_subst.json`, `scripts/run_job.sh`; the sequence scripts beside them):
- The driver reads each job from its workflow file. Every `run:` step runs verbatim with `bash -e` (the runner's default shell), with the workflow, job and step env and the PR event's `${{ }}` expressions resolved (event `pull_request`, base `dev`, recorded base sha `cdf49d1a`, not draft, `GITHUB_SHA` = head, `RUNNER_TEMP` scratch, `CI=true`, `GITHUB_ACTIONS=true`). `GITHUB_OUTPUT`, `GITHUB_ENV` and `GITHUB_PATH` are honoured between steps, and `if:` is evaluated.
- PATH: a `make` shim first, which logs every invocation (step, cwd, argv) and execs GNU make 4.3; then a Python 3.12.13 venv (uv), as the hosted runner's python3; then the host PATH. Nested `$(MAKE)` calls inherit make 4.3's absolute path, so they are make 4.3 too and are not counted. No first-party script names an absolute make path (`git grep` for `/usr/bin/make`: none).
- HOME is a scratch directory per job, so no LiteX, credential or cache from this host leaks in.
- Substitutes (runner provisioning only), each marked SUBSTITUTED in its step log: the diagram dependencies (`rsvg-convert` presence check plus the workflow's pip line), the sv2v install (same pinned zip and digest, into the replay's bin directory), the Yosys install (this host's Yosys 0.66 package with external ABC, version-checked as the step does), and the `docs-check-no-git` step (in a `git archive` export instead of deleting the worktree's `.git`). Path map `/opt/verilator` to a local Verilator 5.050 install. `docs-check` step 43 (`act_ci.py --selftest`) is not run on the host: AGENTS.md section 5. Instead the substitute proves `scripts/act_ci.py` is byte-identical to live dev.
- Actions: checkout means the worktree at the head (live dev is still `cdf49d1a`, so the hosted merge tree is the head's tree). Caches: Verilator and Yosys count as hits; pip, Scala, CPU metadata and the RV32 SDK start cold in the scratch HOME. Upload and download artifact: the aggregates read the replay's own shard outputs through `--seed` links.

Incidents (disclosed in the PR body too):
- The first `docs-check` attempt ran `scripts/act_ci.py --selftest` on the host (rc 0, 3.3 s, offline). The file is byte-identical to live dev `cdf49d1a`. The final replay marks it NOT RUN. That first attempt also failed steps 24 and 26 because I had symlinked the host's RV32 tree into the scratch HOME; the installer refuses a symlinked parent. The final replay installs the pinned Bootlin SDK fresh.
- The first two shard launches were wrong. One was a 2 h background task, stopped seconds in. The other was under `nohup`: SIGHUP ignored, so the sweep's own `hard-HUP` cancellation control could not stop its child. Shards 0 and 1 aborted in preflight and shard 2 refused on the orphans; no suite ran in any of them. Relaunched with `setsid` alone (SIGHUP default); every shard reported here is from that run. The Yosys and `elaborate` sequences ran under `nohup`. No script on their paths names SIGHUP (`git grep` over `syn/`, `sw/litex/`, `sw/builder/test_builder.py`, `scripts/run_litex_sims.sh` and the CI scripts they call), and all their steps passed.

Results at `0b066b6e`, every job green and every make invocation GNU make 4.3 (`receipts/replay/<job>.log`, `<job>.summary.json`, `make_calls_per_step.txt`):

| Job | Steps (run verbatim, of them mapped / substituted; actions; skipped) | make calls | Result |
|---|---|---|---|
| docs.yml `docs-check` | 50 (43, 0 / 3; 4; 0) | 2,947 (19: 1, 25: 1,031, 26: 1,538, 31: 14, 50: 363) | 46/46 rc 0; step 50 `check_entity_shape.py --self-test` 222/0; step 26 builder `ALL GATES PASS EXCEPT 14 NOT RUN` (LiteX gates; hosted docs-check has no LiteX either); step 9 em-dash base derived as `cdf49d1a` (0 findings, 535 lines); step 24 the pinned Bootlin SDK installed fresh and verified (archive sha256 `d42680e9...`); step 43 NOT RUN (AGENTS.md section 5), `act_ci.py` byte-identical to live dev |
| docs.yml `wire-accountability` | 3 (2 / 0; 1; 0) | 0 | rc 0, 77/0 |
| docs.yml `docs-check-no-git` | 2 (0 / 1; 1; 0) | 0 | rc 0: `docs_check` 0 findings (inventory parity skipped, needs git, as hosted), `check_feature_status` 0 findings |
| rtl.yml `full-ci-gate` | 5 (4 / 0; 1; 0) | 0 | rc 0; `rtl=true run_full=true`; default branch read `unreadable` (no credentials in the scratch HOME; informational on a PR) |
| rtl.yml `verilator-shards` 0..4 | 14 each | 41 / 276 / 173 / 55 / 34 | 11/11 (401,934), 23/23 (197,119; tsn-gen built, no declared skip), 12/12 (1,523,725), 12/12 (14,649), 1/1 (11,839); 0 failures |
| rtl.yml `verilator-suites` | 5 (3 / 0; 2; 0) | 0 | 59 suites, 2,149,266 checks, 0 failures; target SHA 5/5 |
| rtl.yml `yosys-shards` 0..3 | 10 each (3 / 2; 4; 1) | 0 | rc 0 each (359 s, 245 s, 129 s, 57 s); result cache cold, every top live |
| rtl.yml `yosys-portability` | 5 (3 / 0; 2; 0) | 0 | 55/55 tops, structural gates, target SHA 4/4 |
| rtl-fast.yml `changes` / `verilator-lint` / `bdd-conformance` / `yosys-elaboration` / `rtl-fast` | 2 / 6 / 4 / 10 / 1 | 0 | rc 0 each: `rtl=true`; lint 90 <= 90 plus `pp_srcs.py --check --selftest`; behave 404 scenarios, 1,968 steps; elaborate tops, OOC self-tests, cache self-test; aggregate all `success` |
| elaborate.yml `elaborate` | 20 (11, 1 / 1; 7; 1) | 1,540 (15: 1,538, 19: 2) | rc 0: LiteX from `sw/litex/litex_pins.txt` into a fresh 3.12 venv, VexiiRiscv at LiteX's pin, the patch series applied; `test_builder.py --require-elaboration --require-rv32` `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's `MAKEFLAGS += -e` arm: make 4.3 does not re-read MAKEFLAGS mid-parse; gate 11: no Arty build report); `run_litex_sims.sh` self-test and 4/4 simulations |

Not replayed: `physical-gptp` (schedule or dispatch only; skipped on a PR, as hosted).

## Item 3: the change (`7f051b272`)

Contract graded: `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:155-158` ("saturating at 65535; a level, cleared by an era start") and `docs/reference/REGISTER_MAP.md` `AAFM_STAT[31:16]` ("clears at every era start: a selection change, a bind edge or the 100 ms timeout. While no AAF source is selected, `[2:0]` and `[31:16]` read zero"). RTL lines graded: era clear `:598`, saturation `:492-493`, the gap/void branch that takes no deviation `:489`. No RTL change.

- `tb/verilator/aaf_clock_meter/sim_main.cpp:340-410`: `max_dev_levels`, run at the end of M1 (`case_rates`, `:459`). It sits in `rates` so both reviewers' probe scripts reach it unmodified: R432-2's `reviewer_meter_probes_r2.py` runs P1 and P2 on `rates`, and R433-2's `meter_probes.py` runs every case.
  - `max_dev_era` (`:357`): a +100 ppm era on listener 0 (largest deviation 187.5 ns, the offset over 15 spacings, checked first so the clear is graded from a non-zero value); then an era start onto a 0 ppm talker, whose ideal timestamps deviate by exactly 0; the new era must read 0. Four era starts: listener change (onto listener 1), entry (with the exit window read in between: "reads 0 while not following"), bind edge, and the 100 ms timeout (read once after the silence, and again after the new era's stream).
  - One lost PDU inside a group at 0 ppm: the PDU after the gap is not compared with PDU 0, so the field reads 0.
  - Steps of +65,535, +65,536, +100,000 and -100,000 ns at group position 5 on a 0 ppm talker: each restarts the history once, and the field reads min(|step|, 65,535) after the restart (the data restart keeps the reading). +65,535 and +65,536 straddle the saturation threshold.
- `tb/verilator/aaf_clock_meter/mutants.py:199-217`: three named mutants with R433-2's own `meter_probes.py` edits, each required to fail its named check.
- `docs/testing/TESTING.md:484`: the meter row names the round-2 probes and what M1 now grades.

## Test rows and failing mutants

| New check (case `rates`, M1) | Fails under |
|---|---|
| `[M1 max_dev, <event>] the old era's largest deviation is the offset over 15 spacings` (4 events) | `max_dev_not_tracked` (round 2's mutant; it reads 0) |
| `[M1 max_dev, listener change] the new era's largest deviation reads 0` | **`max_dev_not_cleared_at_era_start`** (named check; reads 187) |
| `[M1 max_dev, exit] reads 0 while not following` | `max_dev_not_cleared_at_era_start` (187) |
| `[M1 max_dev, entry] the new era's largest deviation reads 0` | `max_dev_not_cleared_at_era_start` (187); `max_dev_includes_gap_pdus` (63,224: the entry cycle's dropped PDU 0 leaves its group unopened) |
| `[M1 max_dev, bind edge] the new era's largest deviation reads 0` | `max_dev_not_cleared_at_era_start` (187) |
| `[M1 max_dev, timeout] reads 0 once the timeout starts an era` and `... the new era's largest deviation reads 0` | `max_dev_not_cleared_at_era_start` (187, both) |
| `[M1 max_dev, a lost PDU] the PDU after the gap is no deviation` | **`max_dev_includes_gap_pdus`** (named check; reads 59,464) |
| `[M1 max_dev, step +65536 @5] reads min(\|step\|, 65,535) after it` | **`max_dev_no_saturation`** (named check; reads 0) |
| `[M1 max_dev, step +100000 @5]` and `[... -100000 @5] reads min(...)` | `max_dev_no_saturation` (34,464 both) |
| `[M1 max_dev, step +65535 @5] reads min(...)` | `max_dev_not_tracked` (boundary control below the threshold; the saturation mutant passes it, as it must) |
| `[M1 max_dev, step <s> @5] restarts the history once` (4 steps) | M3's rule; any mutant that leaves a large step unrestarted |

Runs (`receipts/`):
- Meter suite under make 4.3 with the pinned 5.050, `make -C tb/verilator/aaf_clock_meter`: rc 0; cases 465/0 (446 before; +19), servo 6/0, campaign 36/36 (35 mutants and the clean control; 33/33 before), 734 s (`meter_suite_item3.log`).
- R433-2 `meter_probes.py`, unmodified: clean control PASS; `max_dev_not_cleared_at_era_start` CAUGHT, `max_dev_no_saturation` CAUGHT, `max_dev_includes_gap_pdus` CAUGHT (the third probe of that run, which escaped at `d81198c2`), `tu_edge_clears_held_lock` and `tu_edge_pulses_disrupt` CAUGHT (`probes433.log`).
- R432-2 `reviewer_meter_probes_r2.py`, unmodified: P1 CAUGHT on `rates` (6 checks), P2 CAUGHT on `rates` (3 checks); P3, P4 and P6 CAUGHT as before; P5 (rising-only `tu`) still escapes the meter suite and is caught at the root, as R432-2 recorded (`probes432.log`). P1 and P2 still pass the other cases each probe runs on, which carry no new check.

## Item 4: the change (`0b066b6e6`)

`docs/design/MEDIA_CLOCK_FOLLOWING.md:994-1001`, the meter's "Outputs" bullet: R432-2-R1's exact text replaces "and a status word with the lock, the rate validity, the followed listener, a history-restart count and the largest `|ts_i - ts_0 - i * 125,000|` seen this era." Checked by joining the bullet's lines: the reviewer's sentence is present verbatim. The following sentences are unchanged.

## Area against the design estimate

No RTL change this round: `git diff --stat d81198c20 HEAD -- hdl sw/litex syn configs` is empty. The seven changed paths are two scripts, the root suite's Makefile, the meter harness and its mutants, and two docs. Re-measured at the head anyway, `syn/yosys/ooc.sh KL_aaf_clock_meter` (Yosys 0.66, `synth_xilinx -family xc7 -flatten`, scratch `ooc_final.log`):

| Block | LUT (LUTRAM) | FF | RAMB18 | DSP | CARRY4 | Design estimate | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `KL_aaf_clock_meter` | 574 (16) | 636 | 0 | 0 | 102 | 380 to 580 LUT, 270 to 420 FF, 0 RAMB18 | unchanged since round 2; LUT inside, FF over (accepted by the ruling on #629, STOP item 8) |
| `KL_mmcm_drp_servo` | 865 | 792 | 0 | 1 | 150 | 871 LUT, 792 FF at the design base | unchanged (round 2's figure; RTL untouched) |

## Shipping image timing

Not rebuilt: no RTL change, and nothing the build reads changed (`hdl/`, `sw/litex/`, `syn/`, `configs/` identical to `d81198c2`, where round 2 built it). The image of record is round 2's, `TAG=a494m2d81198c2 sw/litex/build.sh ax7101`, Vivado v2026.1:
- WNS +0.065 ns, TNS 0 (0 of 180,759 endpoints failing);
- WHS +0.036 ns (0 of 180,678); WPWS +0.264 ns;
- all four sign-off corners "No timing paths found" for negative slack;
- 106,333 of 106,333 nets routed, 0 errors; 0 critical warnings; #607 refusal clean;
- Slice LUTs 80.52 %, Slices 99.90 %; meter placed 483 LUT / 630 FF.
- Bitstream sha256 `f9aa63859da17751732086cdba3277ff99c45628bc08ab615421919ef6e6a937`.

## Gates

All at the final head `0b066b6e66df2a3ba3167805a6a591f8b96fa449` unless noted, from the physical `/data` worktree path, never piped, outputs to logs (copies in `receipts/`). The worktree was clean (`git status --porcelain` empty, submodules clean at their gitlinks) before and after. Suites on Verilator 5.050 (the replay maps `/opt/verilator` to a local 5.050 install; direct runs use the pinned wrapper).

| Gate | Command | Make | Result |
|---|---|---|---|
| R433-2's checks | `sh make43_checks.sh <worktree> <make-4.3 dir>` (R433-2 packet, unmodified) | 4.3 and 4.4.1 | rc 0: round-1 Makefile 1 polluted line, head 0; `check_entity_shape.py --self-test` gate rc=0, 222/0, under both makes (`make43_checks_final.log`; also at `bb65ac498`) |
| Hosted jobs, replayed | `scripts/run_job.sh <workflow> <job> <name>` for every job above (sequences `shards.sh`, `yosys.sh`, `elaborate.sh`) | 4.3 (shim) | every job rc 0; table in Item 2 |
| Meter suite | `make -C tb/verilator/aaf_clock_meter` | 4.3 | rc 0: 465/0, servo 6/0, campaign 36/36, 734 s (at `bb65ac498` + the item 3 edit, committed unchanged as `7f051b272`; and again inside shard 2: 465/0, 6/0, 36/36) |
| Root suite, inherited flag | `MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk` | 4.4.1 | rc 0: A 55/0, C 32/0, B 50/0, 31/31, 440 s (`mclk_host_final.log`) |
| Root suite | `make -C tb/verilator/milan_dp_mclk` | 4.3 | rc 0 at `bb65ac498` (7:02) and inside shard 2 from a clean build: A 55/0, C 32/0, B 50/0, 31/31 |
| Reviewer probes | R433-2 `meter_probes.py`; R432-2 `reviewer_meter_probes_r2.py`, both unmodified | 4.3 | 5/5 CAUGHT; P1, P2, P3, P4, P6 CAUGHT, P5 escapes the meter suite (caught at the root, R432-2) |
| Markdown gates | pinned md venv: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `--verify-anchors`, `check_em_dash.py --base cdf49d1a`, `check_doc_paths.py` | none invoked | rc 0 each (0 findings; 299 anchors; 535 added lines, 0 em-dash findings; 890 paths) |
| Idiom and hygiene | `check_py_idiom.py`, `check_cpp_idiom.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check` | none invoked | rc 0 each (all ratchets at or under budget) |
| OOC area | `syn/yosys/ooc.sh KL_aaf_clock_meter` | none invoked | rc 0: 574 LUT (16 LUTRAM), 636 FF, unchanged |
| `git diff --check` | worktree; `cdf49d1a HEAD` | none | rc 0 both, and `d81198c2 HEAD` rc 0 |

## Parent-visible changes

- RTL, ports, parameters, registers, CSR, AEM, configs, generated files: none. No processor-boundary or top-level port change; no protocol-processor edit; gitlinks unchanged.
- Scripts: `scripts/shape_consumer_inventory.py` (`classified_frozen_targets`; the frozen-prerequisite arm consults it), `scripts/entity_shape_selftest.py` (three arms; `--self-test` grows from 219 to 222 checks).
- Test build: `tb/verilator/milan_dp_mclk/Makefile` (`MAKEFLAGS=` on both nested derivations).
- Tests: `tb/verilator/aaf_clock_meter/sim_main.cpp` (M1 `max_dev_levels`, +19 checks), `mutants.py` (+3 named mutants: 35).
- Docs: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (the meter's Outputs bullet, R432-2-R1's exact text), `docs/testing/TESTING.md` (the meter row).

## Observations outside #629 (for the manager to file if wanted)

- The entity shape gate's database read (`shape_prereqs_from_database`, `scripts/shape_consumer_inventory.py:181-209`) counts a database as readable when the parse stopped at an `$(error)`. Under GNU make 4.4+, `make -pqrR` does that to `tb/verilator/milan_dp_render/Makefile` and `tb/verilator/capture_coherence/Makefile`, whose nested `$(shell $(MAKE) ...)` inherit the question flag (probe: rc 2, `Makefile:60: *** ... Stop.` and `Makefile:103: ...`). Under the hosted make 4.3 both parse in full. Arm I reads only `milan_dp_render` of the two (`capture_coherence` names no shape header), and that file's only frozen shape token under 4.3 is a `configs/generated` copy (arm D's), so arm I loses nothing today. Failing closed on a stopped parse would need `milan_dp_render` to take `MAKEFLAGS=` first. Not changed here: neither file is this PR's.
- `tb/verilator/tsn_fuzz` rewrites `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` (the timestamp line) whenever its field campaign runs (`TSN_GEN_ROOT` set, as on hosted shard 1). The replay's shard 1 did so; the counts were unchanged (164 and 677 pass) and its freshness check passed. Both files were restored to HEAD with `git checkout --`. A local run with the oracle dirties the tree.
- Round 2's notes stand: `milan_dp_render` and `pp_shadow` nested derivations lack `--no-print-directory`; `fw_service_budget/oracle.json` keeps pre-#629 image sizes; the `docs.yml` comment "156 of 256 ids at 8x8" is now 164.

## Receipts and scripts in this directory

- `receipts/`: R433-2's script runs (`make43_checks_item1.log`, `make43_checks_final.log`), the head failure reproduced (`es_plain_43_head.log`), the database probe (`db_probe_final.log`), the meter suite (`meter_suite_item3.log`), the root suite under make 4.3 (`mclk43_item1.log`) and under 4.4.1 with `MAKEFLAGS=w` (`mclk_host_final.log`), both probe scripts' output (`probes433.log`, `probes432.log`), the out-of-context area (`ooc_final.log`).
- `receipts/replay/`: every replayed job's step-by-step log and `summary.json`; `make_calls_per_step.txt`; the key step logs (docs-check step 50 entity shape gate, step 43 not run, step 26 builder tail; the shard logs; the aggregate tallies and target-SHA checks; elaborate steps 15 and 19; shard 2's root and meter suite logs); the first `docs-check` attempt and its step 43.
- `scripts/`: `replay_workflow.py` (the driver), `replay_subst.json` (substitutes and action meanings), `run_job.sh`, `shards.sh`, `yosys.sh`, `elaborate.sh`, `db_probe.py`. They run from the scratch directory `$VALIDATION_STORAGE/629-a500/` (make 4.3 build, venvs, scratch HOMEs, full step logs, suite logs), which is not in the tree or this directory.
- Every file here is under 200 KB; the home-directory prefix in receipts is written `$HOME`.
