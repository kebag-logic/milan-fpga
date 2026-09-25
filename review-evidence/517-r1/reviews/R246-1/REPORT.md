[R246] NEGATIVE - exact head f36b40ddb5bf7fa5b12bba47d136e0b9d429403c

# R246-1: external independent review of issue #517 / PR #524

- Head `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`, tree `270b9c97701047659ff1ec6040126af77b7141e1`. Source base: dev `5c78ce2e9d831e588e759b696ed549804327e4d8`. Live dev: `1299b46169ac56c9b7aaa7e3b26fb1ae116e6938`.
- Scope: the whole PR, `5c78ce2e..f36b40dd` (4 commits, 8 files). This is the first R246 review of the PR.
- Reconstruction order: AGENTS.md, CONTRIBUTING.md sections 2 and 3, docs/README.md, REQUIREMENTS.md REQ-VER-01/02/04, the issue body and public decisions (shared-header 5780545051, host-tool 5781783857, rebase assignment 5835674224), CODE_QUALITY rule 8, then the diff and history, then public author and manager evidence at `2f5dfa97`.
- I wrote and timestamped my own verdict and ledger (`receipts/independent_pass_before_prior_findings.md`, 2026-09-25T20:56:19Z) before reading R245-1's findings.
- Verdict: **NEGATIVE**. There is one MAJOR finding (F1: Conformance, RTL, Docs) and one MINOR finding (F2: Tests). R245-1 F1 is **closed** at this head. The runner's scheduling, bounds, failure handling, cancellation and output behaviour are sound, and the real suite reproduces the author's results exactly.

## Prior public review findings

| Prior finding | State at f36b40dd | Evidence |
|---|---|---|
| R245-1 F1, MAJOR under Conformance, RTL, Robustness, Tests and Docs: blocked stdout replay stops INT/TERM cancellation and reaping (`sim_pool.py` at 5874895e) | **CLOSED** | (a) `sim_pool.py:236-282`: replay is assembled on disk (`obj_legs/replay.log`). Stdout is written non-blocking from a byte cursor, and waits use `sigtimedwait` on the interrupt set. After cleanup, `main` calls `drain(wait=False)` (`:469`). Descriptor flags are restored in `finally` (`:281-282`). (b) The shipped 28 direct and actual-Makefile controls pass at head (`receipts/head_test_sim_pool_backpressure.py.log`). (c) The same head controls, run against the 5874895e runner, fail all 24 INT/TERM cases with "runner did not shut down while stdout stayed blocked" (`receipts/old-runner-vs-head-backpressure/run-00.log`). The original defect is therefore detectable, and it is gone at head. (d) Mutants M15 (blocking stdout), M16 (final drain waits) and M17 (flags not restored) are each killed (`receipts/mutants/summary.tsv`). (e) Real legs, stdout a 4 KiB pipe that is never read, SIGTERM sent to the process group: the runner ends by SIGTERM within 0.05 s in 7 of 7 cases, with no survivors. This includes a signal sent while a grouped leg's `sh` and `endstation_builder.py` subprocesses were alive (`receipts/real-cancel/*.json`). One of the seven receipts, `cancel-jobs1-25.out`, prints FAIL, but only because my probe's own criterion required a killed leg. At that moment the first leg had already finished and the blocked stdout was holding the pool, so there was nothing running to kill. The runner status was SIGTERM in 0.05 s with no survivors, and all ten remaining legs were named unstarted. |

R245-1 also recorded the 21 original policy-checker findings and the A176 items as resolved. They stay resolved: `check_baremetal_only.py --check` reports 0 findings across 869 files. The shared-header item, however, is superseded by F1 below. R245-1 accepted the premise that `endstation_builder.py:5632-5671` "still writes their repository-relative shape headers". Executable evidence at this head contradicts that premise.

## Findings

### F1: MAJOR, lenses Conformance, RTL, Docs: the stated shared tracked-header write does not happen

- **Artifacts:** `tb/verilator/milan_dp/sim_nxn.cpp:399-400`, `tb/verilator/milan_dp/sim_pool.py:9-12`, `tb/verilator/milan_dp/README.md:26`, `docs/testing/TESTING.md:294`, and the `--exclusive` marks at `tb/verilator/milan_dp/Makefile:547-555`. The authority is the issue's shared-header decision (issue comment 5780545051), which rests on the A176 audit (comment 5780232053).
- **Evidence:**
  - The PR replaces the base comment "no --write-rtl and no --write-fragment, so it touches nothing tracked" with "the builder also rewrites the tracked per-config shape header". It repeats the claim in the runner docstring ("The five sim_nxn legs rewrite repository-relative shape headers"), the README ("Their builder also rewrites tracked per-config shape headers") and TESTING.md ("The five `sim_nxn` header writers").
  - At this head, and unchanged since 483a133 (`git log 483a133e..5c78ce2e -- sw/builder/endstation_builder.py` is empty), `sim_nxn.cpp:405-409` runs the builder from `tb/verilator/milan_dp` with `../../../configs/<cfg>.yaml`.
  - `_repo_relative` (`endstation_builder.py:89-92`) joins that path lexically onto the physical cwd, and `ROOT` is resolved (`:66-67`). It returns `tb/verilator/milan_dp/../../../configs/<cfg>.yaml`, whose first part is `tb`. The tracked branch `source_parts[0] == "configs"` (`:5668`) is therefore never taken, and the header goes to `<-o dir>/<cfg>/gen/adp_shape_defaults.svh`.
- **Measured:**
  1. `scripts/builder_premise_probe.py` runs the exact sim_nxn argv for all three configs. For each one it shows `takes_tracked_branch=False`, the tracked header's mtime unchanged, and the header written privately (`receipts/builder_premise_probe.json`).
  2. Positive control: the same builder invoked from the repository root with `configs/endstation_arty_4x4.yaml` does rewrite the tracked header, and its mtime advances. The probe can therefore see a real write (`receipts/builder_premise_positive_control.txt`).
  3. In my real pooled cold run, all five grouped legs logged `[AECP-IMG] the shipped generator emitted an image = 0x1`. The three tracked headers kept identical mtimes and bytes (`receipts/headers_before_real_run.txt`, `receipts/headers_after_pool.txt`).
  4. A whole-tree write-set audit of the three builder and image-generator calls found no file changed outside the private directories (`receipts/builder_write_set.txt` is empty).
  - The author's and manager's "tracked headers unchanged" receipts compare bytes only, so they cannot tell a write of identical bytes from no write. They do not contradict this finding.
- **Impact:**
  - The settled scope ("The shared-header decision supersedes the original read-only generated-input premise") and four documentation sites now state, as fact, a side effect that does not happen. The PR also replaced an accurate comment with an inaccurate one.
  - The exclusive group serializes five of the eleven legs, the longest ones, for a reason that does not exist. This is safe for correctness, but it limits the measured gain: the ordinary phase goes from 550.4 s to 491.6 s here.
  - AGENTS section 2 requires an Issue/implementation/documentation conflict to be published and decided, not resolved privately. CONTRIBUTING section 3 says "Measure, don't assume". The original audit inferred the write from reading the code and never observed it.
- **Required outcome:**
  - Publish this conflict on #517 for a maintainer decision.
  - Make the code comment, runner docstring, README and TESTING.md state the true write set, measured rather than inferred.
  - If the exclusive group is kept, it should be described as a conservative choice, not as protection against a tracked-header write.
  - Whether to keep or drop the group is the maintainer's decision. I do not prescribe it.
- **Verification:**
  - Re-run `scripts/builder_premise_probe.py` (with its positive control) and my real-run mtime comparison, and check the corrected wording against both.
  - If the scheduling changes, the exclusivity, overlap and inventory controls must be updated and must still reject their planted defects.

### F2: MINOR, lens Tests: `test_sim_pool_backpressure.py` does not give a deterministic verdict

- **Artifacts:** `tb/verilator/milan_dp/test_sim_pool_backpressure.py:148,190-193,218`. Authority: `docs/development/CODE_QUALITY.md` rule 8 ("Every behavioral change has a deterministic, self-checking test").
- **Cause (a), a torn-ledger read race.**
  - In the `child-exit` controls, `L2` is released at `:218`, and it immediately appends its `released` and `end` records.
  - `cancel_blocked` then parses the whole ledger at `:148` (`case.events("start")`) while those appends may be in flight. A partially written line raises `JSONDecodeError`.
  - Twenty unmodified runs under a normalized signal state gave 3 failing runs, all `JSONDecodeError` in a `*-child-exit` control (`receipts/flake_backpressure_20.txt`). An earlier single run gave one more (`receipts/sigint_probe/backpressure_sigint_default.log`).
  - The final ledgers are intact, which confirms a read-while-write race rather than a torn write.
- **Cause (b), dependence on the inherited SIGINT disposition.**
  - The runner is started at `:192-193` without normalizing signals. The sibling `test_sim_pool.py:256-260` does normalize them.
  - When the test inherits SIGINT ignored, the runner correctly keeps it ignored (`sim_pool.py:452`). POSIX gives that state to `cmd &` in any non-interactive shell. The result is 12 of 28 controls failing with "runner did not shut down while stdout stayed blocked".
  - With SIGINT at its default, the same bytes pass (`receipts/sigint_probe/backpressure_sigint_{default,ignored}.log`).
  - My first mutation batch ran in the background and hit this cause on every mutant (`receipts/mutants-run1-background/`). That batch was discarded and re-run with a normalized state (`receipts/mutants/`).
- **Impact:** the 28/28 validation result recorded for this head depends on timing and on how it was invoked. It fails closed, never open, but it is not reproducible evidence.
- **Required outcome:** both causes are removed. For example, the test should establish its own signal preconditions, and it should read the ledger only after the writer is known to be quiescent, or parse it tolerantly.
- **Verification:** at least 20 consecutive runs pass, both with SIGINT default and with SIGINT inherited ignored (`scripts/flake_repeat.py`, `scripts/sigint_disposition_probe.py`). Restored-defect runners (the 5874895e runner, and mutants M15, M16 and M17) still fail.

### Suggestions (SUGGESTION: optional, does not affect coverage)

- **S1 (Tests):** `test_sim_pool.py` and `test_sim_pool_backpressure.py` run in no workflow, sweep preflight or Makefile target (repository-wide grep). Their Makefile-inventory arm (`test_sim_pool.py:858-896`) protects the 11-leg handoff only when someone runs it. The suite's existing `test_render_phase_observation.py` sets the same precedent.
- **S2 (Tests):** five mutants survive. Four of them are narrow claims: the late interrupt (M19, `sim_pool.py:477-479`), duplicate-leg refusal (M20, `:177-178`), stale-capture removal (M21, `:456-457`) and stdin `/dev/null` (M26, `:311`, because the fixture already starts the runner on `/dev/null`). The fifth, M10 (killing the group leader only), is subsumed by subreaper adoption. The backpressure summary line hard-codes `28` (`:262`). Its docstring cites an "outer command guard" (`:12`) that does not exist in the repository, so a broken fixture hangs at `next_start()`.
- **S3 (Robustness):** `clean` (`Makefile:596-597`) does not remove `obj_legs/`. Captures from an earlier run therefore survive a clean, and they remain after a later run fails before the pool starts.
- **S4 (Robustness):** while stdout is blocked, the pool starts and reaps no further legs until the consumer drains. I observed this in `receipts/real-cancel/cancel-jobs1-25.json` and `cancel-jobs2-12.json`. The legacy sequential recipe had the same class of stall, and the sweep writes to a file, so this is a documentation gap only.
- **S5 (Robustness):** `reap_adopted` needs `/proc/<pid>/task/<tid>/children` (`sim_pool.py:109`), but only subreaper support is checked before launch (`:86-98`). Probe M33, with that file made unavailable, left owned processes unreaped on cancellation (`receipts/mutants/M33-*`). Mainstream kernels provide the file, but a pre-launch check would make the stated "refuse before launch" contract complete.

## Assignment verification items

1. **R245-1 findings:** F1 is closed; see the table above.
2. **Policy-mask union** (`scripts/check_baremetal_only.py`):
   - The head-vs-dev diff removes exactly one line: the self-test group list, re-added with both dev's `_arms_act_slot_masks` and the PR's `_arms_sim_pool_host_masks`.
   - The PR-side hunks are identical before and after the rebase (`483a133e..ff7dac32` compared with `5c78ce2e..f36b40dd`).
   - AST key comparison: none of dev's `TERM_MASKS` (4) or `HOST_RUNTIME_MASKS` (6) keys is dropped, and there are no duplicate keys that would shadow a dev mask. The PR adds 3 and 2 keys (`receipts/policy_mask_keys.txt`).
   - `--check`: 0 findings across 869 files. `--selftest`: 700 arms, against 441 on dev (`receipts/baremetal--check.log`, `receipts/baremetal--selftest.log`, `receipts/baremetal_dev_selftest_count.txt`).
3. **Leg inventory** (`receipts/inventory_dev_vs_head.txt`, from `make -n run` of each revision's Makefile, `scripts/inventory.py`):
   - Dev and head each run 14 executable legs (gptp, gptplat and gmstep, then the 11 ordinary legs), with identical banners and order.
   - 14 builds in identical order, and identical post-pool drivers (`render_mutants.py`, `gmstep_mutants.py`). With pool markers removed, the whole interleaved sequence is identical. There are no duplicates.
   - The exclusive legs are exactly notify, nxn, nxndv, nxn8 and nxn4c. `SIM_JOBS=1` differs only in `--jobs`.
   - #508's GSI checks stay in `obj_notify` and #443's CSR checks in `obj_aclk`. Their focused targets (`notify`, `gsi-mutants`, `render-csr-controls`) are unchanged and were not in dev's `run` either.
   - TESTING.md:289-300 and README.md:15-58 list the same eleven. The README table has 14 rows, matching "fourteen elaborations".
   - No leg is dropped or double-run. Mutant M28 (a dropped leg) is killed.
4. **Pool behaviour:**
   - 17/17 unit arms and 28/28 backpressure controls pass at head (with F2's caveat).
   - 32 claim-mapped mutants plus probe M33: 27 of the 32 are killed, and M33 is also killed (`receipts/mutants/summary.tsv`). Those include the bound +1, one-worker mode ignored, exclusion removed, group order reversed, fail-fast removed, exit forced to 0, failure unnamed, crash treated as a pass, unstartable leg ignored, no adoption reaping, no subreaper, SIGHUP unwatched, an ignored interrupt re-enabled, blocking stdout, the final drain waiting, flags not restored, completion-order replay, the empty frame variable ignored, the frame variable ignored, an inherited child mask, no new session, no kill on interrupt, and the Makefile mutants: dropped leg, notify not exclusive, errors ignored, default of 1, crflic made exclusive. The five survivors are listed in S2.
   - Real concurrency across 1887 samples: at most 2 legs, and at most 1 grouped leg (`receipts/wallclock_summary.txt`).
   - One-worker mode reproduces sequential output: all 11 captures and `replay.log` are byte-identical between `--jobs=2` and `--jobs=1`, and identical to the author's published pooled-cold blobs (`receipts/captures_vs_author.txt`).
5. **Wall clock:**
   - The cold pooled run was reproduced with pinned Verilator 5.050 (`receipts/verilator_identity.txt`; the manager-named wrapper path did not exist, so I used a byte-identical copy of the same wrapper, whose SHA-256 matches all 52 wrappers on the host, and verified its `--version`) on 8 CPUs with `VERILATOR_JOBS=8`.
   - A single foreground command is capped at 10 minutes, so I ran `make gptp`, `make gptp-lat`, `make gmstep` and then every `make -n` line of `run` in order, as timed segments (`scripts/seg.py`, `receipts/real-cold-pooled/`).
   - All segments exited 0. The runs made 10074 checks with 0 failures and 16 tallies, and `suite_tally.py --verdict` exits 0 (`receipts/real-cold-pooled/tally.txt`).

   | Phase | Seconds |
   |---|---:|
   | gptp | 100.369 |
   | gptp-lat | 98.921 |
   | gmstep | 37.679 |
   | 14 builds + banners | 153.924 |
   | ordinary pool, `--jobs=2` | 491.551 |
   | `render_mutants.py` | 350.412 |
   | `gmstep_mutants.py` | 138.510 |
   | **Cold pooled total** | **1371.366** (author: 1370.953) |

   - The margin against the unchanged 3600 s budget is 2228.6 s.
   - The same ordinary set at `--jobs=1` took 550.358 s (`receipts/real-warm-seq-ordinary/`). Substituting it gives a sequential-equivalent total of 1430.2 s. The saving is 58.8 s: 4.11% of the suite, and 10.7% of the ordinary phase.
   - These figures come from one shared host under varying load (load average about 8 to 19). They are not hosted timing.
6. **Gates:**
   - `ci_events.py --check` passes with 1647 items, and `--selftest` with 2188 arms.
   - `docs_check.py` passes in git mode (0 findings) and in a git-free copy (0 findings, 1 declared skip). Its `--selftest` passes.
   - `check_em_dash.py --base 5c78ce2e` passes (0 of 60 added lines) using the pinned renderer venv. `gen_toc.py --check` and `--verify-anchors` pass. The first attempts with the system interpreter exit 2 because the renderer is absent; those receipts are kept.
   - The py-idiom, hygiene, TODO-ownership, fail-fast and test-evidence gates pass, and `git diff --check` is clean (`receipts/gates_rc.txt`, `receipts/gate_*.log`).
   - The full default sweep (not re-run by me, as required) matches the published author evidence: 55 suites, 2121993 checks, 0 failures, 4 declared `tsn_fuzz` skips. milan_dp shows 10074/0/16 there, the same as my run.
7. **Merge with live dev 1299b461:**
   - `git merge-tree` is clean, giving tree `3052b62a55a1fb1c512b1069dc56cb6f3ec0725a`. The merge base is the source base. The only file changed on both sides is `docs/testing/TESTING.md`, and it auto-merges.
   - On a probe merge commit of that tree: `check_baremetal_only --check` (0 findings across 878 files), `ci_events --check` (1655 items), `docs_check` (0 findings) and `test_sim_pool.py` (17/17) all pass (`receipts/merge_live_dev.txt`, `receipts/merged_tree_static.txt`). This is not the manager's candidate validation.

## Per-lens results for this round (the artifacts named are at f36b40dd)

- `[R246] UNCLEAN Conformance`: issue #517 acceptance 1-4 and the settled scope were checked against the Makefile, runner and real runs, and are met except for F1.
  - The shared-header decision's premise is contradicted by `receipts/builder_premise_probe.json` and the real-run mtimes.
  - Acceptance 1 is met by the inventory. Acceptance 2 is met by the real comparison. Acceptance 3 is met by the arms and mutants. Acceptance 4 is met by the real suite, tally and gates.
  - Acceptance 5 belongs to the manager.
- `[R246] UNCLEAN RTL`: the host scheduling architecture (`sim_pool.py:285-412`, and `Makefile:540-567`) was examined, covering bounds, the state and signal loop, reaping and non-blocking replay. It is correct, but its exclusive-group constraint rests on the incorrect shared-state analysis in F1.
  - No HDL, firmware, processor pin, clock, reset or wire contract changed: the diff touches 8 files and no `hdl/` or gitlink.
- `[R246] PASS Robustness`: examined `sim_pool.py:149-179,298-347,433-480` together with the real-leg cancellation receipts (`receipts/real-cancel/`). They cover a blocked 4 KiB stdout, SIGTERM during builder subprocesses, and cancellation at jobs=1 and at jobs=2. Mutants covered invalid `--jobs` values, a missing or non-executable leg, a crash, an empty or set frame variable, an ignored inherited interrupt, and repeated signals. There is no open BLOCKER, MAJOR or MINOR; only S3-S5 remain.
- `[R246] UNCLEAN Tests`: `test_sim_pool.py` (17 arms) and `test_sim_pool_backpressure.py` (28 controls) were checked against 33 mutants and the pre-fix runner. Their fault sensitivity is strong, but the backpressure test is nondeterministic (F2).
- `[R246] UNCLEAN Docs`: README.md:1-58, TESTING.md:289-300, the runner docstring and the `sim_nxn.cpp` comment were checked against executable behaviour. They are accurate apart from F1's false write claim.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #517 body, decisions and acceptance; `Makefile:480-567`; `sim_pool.py`; `endstation_builder.py:66-92,5631-5673`; real-run receipts | R246-1 | f36b40ddb5bf7fa5b12bba47d136e0b9d429403c |
| RTL | UNCLEAN (F1) | `sim_pool.py:62-485`; `Makefile` pool line and builds; diff scope (no HDL or pins); concurrency samples | R246-1 | f36b40ddb5bf7fa5b12bba47d136e0b9d429403c |
| Robustness | CLEAN | `sim_pool.py` failure, signal and cancellation paths; `receipts/real-cancel/*`; mutants M05-M09, M11-M17, M22-M25, M27 and M33 | R246-1 | f36b40ddb5bf7fa5b12bba47d136e0b9d429403c |
| Tests | UNCLEAN (F2) | `test_sim_pool.py`, `test_sim_pool_backpressure.py`; `receipts/mutants/`, `flake_backpressure_20.txt`, `sigint_probe/`, `old-runner-vs-head-backpressure/` | R246-1 | f36b40ddb5bf7fa5b12bba47d136e0b9d429403c |
| Docs | UNCLEAN (F1) | `README.md:1-58`, `TESTING.md:289-300`, `sim_pool.py:1-60`, `sim_nxn.cpp:396-400`; doc gates | R246-1 | f36b40ddb5bf7fa5b12bba47d136e0b9d429403c |

Ledger note: my timestamped independent ledger attributed F1 to Conformance and Docs only. I added RTL afterwards by applying the lens definition (the architecture's shared-state and latency understanding). No prior report prompted the change, and no prior report raised F1.

## Limits

- I did not run the full parent, PP, gPTP, Yosys or builder banks, Docker/act, or the host `act_ci`, as the assignment requires. The sweep result is the author's published evidence, which I inspected but did not re-execute.
- The cold run was segmented into timed `make -n` lines because of the 10-minute limit on a foreground command. The sequential figure comes from a warm `--jobs=1` ordinary phase substituted into the cold total. Each figure is a single sample on a shared host.
- Hosted checks at the exact head (`receipts/hosted_checks_exact_head.txt`, PR draft):
  - Executed with success: `rtl-fast`, `changes`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `wire-accountability`.
  - Skipped (draft or schedule): `verilator-suites`, `yosys-portability`, the Verilator and Yosys shards, and Physical gPTP.
  - The skipped contexts are not evidence.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Integrity: every probe ran in disposable copies under the packet's `scratch/`. The reviewed clone passes `scripts/integrity.py` (899 tracked entries by bytes, kind and mode; stage-0 index equal to the tree; no hidden flags; `receipts/integrity_after.txt`). The gitlinks match: `gptp-processor` e5dcea6e, `protocol-processor` 990f9652, `third_party/verilog-axis` 48ff7a7e, and `external` is uninitialised as found. The three required submodules are clean. I removed the two ignored `__pycache__` directories my own test runs created. `git merge-tree` added unreferenced loose objects (for the merge tree) to the clone's object store; no ref, index or tracked byte changed.
- My own mutation probes left two spinning runner processes. They came from mutant M18, which introduced an infinite loop and also blocks SIGTERM. I found and killed them, and no probe process remains.
- Receipts are published with host absolute paths normalized to `$PACKET`, `$CLONE`, `$MANAGER_TMP`, `$TOOLS` and `$HOME`. Two mutant logs had environment mappings echoed by a failing assertion, and those mappings are redacted. The fixture ledgers that dump full environments are not published.

## Pending manager duties

- Publish F1's conflict on #517 for a maintainer decision.
- Arrange correction of F1 and F2, then an exact-head re-review of Conformance, RTL, Tests and Docs.
- The trusted act replica; ready-state hosted `verilator-suites`, `yosys-portability` and the dedicated-worker timing comparison; full source banks at any new head; current-dev candidate validation; the second independent positive review; authorized merge and post-merge containment.

R246-1 FINISHED
