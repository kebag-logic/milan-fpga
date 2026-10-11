[R570] NEGATIVE - exact head f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1

# R570-4: internal cleared-context review of PR #707 (issue #621)

- Head: `f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1`, tree `f0f6817a7ded140dd22e14cd997c1c123bb02e1e`.
- Gitlinks at head: `gptp-processor` `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, `protocol-processor` `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `third_party/verilog-axis` `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
- Source base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee` (donor pin `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`).
- Pre-delta head (R570-3/R571-3): `83239549a500604baabc65e443ed90876d65a36e`.
- Delta in this round: `9182cee7`, `0e3eef5b` and `f5d0fb0e`, the `milan_dp` runtime round ([assignment 6101380300](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6101380300)).
- Coverage: all five lenses over the whole lane diff `5603c353..f5d0fb0e`, with depth on the delta.

**Verdict: NEGATIVE on one MINOR (Tests).** Correct at this head:

- the gPTP correction;
- the suite split;
- the split's documentation.

Passing at this head:

- the new `milan_dp_gm_steps` suite;
- the slimmed `milan_dp`;
- the #621 step regression.

The defect: the split left two documented runner tests in `tb/verilator/milan_dp` asserting the `run` recipe step that the split removed.

## Scope reconstructed from public state

- **Issue #621 items 1 and 2** ([assignment 6084306147](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6084306147)):
  - reproduce the 2 s asCapable loss for +10 ms and -10 ms PHC steps in simulation, and name the mechanism;
  - fix it so asCapable and a valid link delay survive a step, with a planted defect that fails;
  - effects: media, `tu`, GPTP_GM_CHANGED and CLOCK_DOMAIN counts.
- **Issue item 3**, the bench repeat, belongs to a later lane. It is not claimed here.
- **Capture-harness rulings** 6087415319, 6087498843, 6087655217, 6088189432 and 6089776382 were resolved in rounds 1 to 3. The delta does not touch them.
- **Runtime round (6101380300)**, the focus of this round:
  1. measure `milan_dp` per leg at base and head, natively;
  2. bring `milan_dp` to at most 60% of its 4800 s limit on hosted, removing no coverage. The chosen option is a separate suite:
     - it runs on every PR;
     - it is outside the scheduled and physical partitions;
     - its owning shard has headroom, per the five-worker landmarks;
  3. no RTL, donor or graded-expectation change, and the gitlink stays `7dda9c3b`;
  4. native per-leg times at the new head.

## Findings

### R570-4-F1 - MINOR - Tests - the runner tests still require a removed `run` step

**Artifacts:**

- `tb/verilator/milan_dp/test_sim_pool.py:889`;
- `tb/verilator/milan_dp/test_sim_pool_backpressure.py:95-96,108-110,128-132`.

**Authority:** AGENTS.md section 6, Tests lens. Existing regressions remain green, and tests do not encode superseded behaviour.

**What changed.** `0e3eef5b` removed three things from `milan_dp`'s `run`:

- `gmstep` from the `run` prerequisites (`tb/verilator/milan_dp/Makefile:541`);
- the `#387 GM step re-base` banner after `python3 render_mutants.py` (`:632`);
- the `python3 gmstep_mutants.py` line there.

**What the tests still expect.**

- `test_sim_pool.py:889` asserts `render_at < lines.index("python3 gmstep_mutants.py")` against `make -n run`.
- `test_sim_pool_backpressure.py`:
  - `:128-132` expect the gmstep banner in the recipe transcript and require `gmstep-controls-ran` in the recipe cases;
  - `:95-96` still plant a fake `gmstep_mutants.py`;
  - `:108-110` still treat `gmstep` as a `run` prerequisite.
- `tb/verilator/milan_dp/README.md:52-53` lists both tests. `:50-55` says they check the "Makefile inventory".

**Executed.**

- Unmodified, `test_sim_pool.py` exits 1 at base, pre-delta and head (`receipts/test_sim_pool_{base,head}.log`).
  - The failing arm is `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs`.
  - The cause is a pre-existing dev gap: `LEGACY_LEGS` (`:72-92`) lacks the #658 `dynmap` leg. That failure masks this defect.
- `scripts/probe_sim_pool_dynmap.py` adds only the missing `dynmap` leg, in disposable clones, and runs that arm alone (`receipts/probe_sim_pool_dynmap_{base,pre,head}.*`):

  | Revision | Result |
  |---|---|
  | base `5603c353` | rc 0 |
  | pre-delta `83239549` | rc 0 |
  | head `f5d0fb0e` | rc 1, `ValueError list.index(x): x not in list` at `:889` |

  The remaining failure belongs to this lane.
- The backpressure recipe controls hang the same way at pre-delta and head (rc 124, `receipts/probe_backpressure_recipe_{pre,head}.*`). Their gmstep expectations are established by reading `:128-132` against the head recipe, not by execution.

**Impact.**

- Both runner tests now encode a recipe that no longer exists.
- Once the pre-existing `dynmap` gap is repaired, `test_sim_pool.py` will still fail, with an unexplained `ValueError` rather than a message about the split.
- The backpressure recipe cases would require a GM-step banner and a controls run that `milan_dp` no longer performs.
- The runtime round's evidence says it reran "the two suites whose inputs changed". These documented tests of the same Makefile were neither updated nor run.

**Required outcome.**

- Both tests' `run` recipe expectations describe the head recipe:
  - no `python3 gmstep_mutants.py` line;
  - no GM-step banner;
  - no `gmstep` prerequisite;
  - `render_mutants.py` is the last recipe step after the pool.
- Nothing else in either test is weakened.
- The pre-existing `LEGACY_LEGS`/`dynmap` gap and the recipe-control hang are dev defects, not this lane's (see Observations). Whether to repair them here is the manager's scope call.

**Verification.**

- At the fixed head, `scripts/probe_sim_pool_dynmap.py` exits 0 (it adds the `dynmap` leg in a disposable copy).
- `grep -n gmstep tb/verilator/milan_dp/test_sim_pool*.py` shows no expectation of a GM-step step in `milan_dp`'s `run`.

### R570-4-R1 - RESIDUE - Docs - PR #707 body, Status section, line 2

- **Wording:** "The runtime-round head is local; hosted confirmation follows the push."
- **Facts:** the head is pushed. `rtl-full` run 38095215734 is executing at `f5d0fb0e`. `docs`, `elaborate` and `rtl-fast` have completed successfully.
- **Why RESIDUE:** wording only. It changes no figure, verdict, test or claim.
- **Exact fix:** "The runtime-round head is pushed; hosted results at `f5d0fb0e` are the manager's to confirm."

### Suggestions (no lens effect)

- **R570-4-S1 (Tests).** `sim_gmstep.cpp:69-72` says `--no-small-steps` "leaves the #621 phase out, and nothing else". No committed check enforces "nothing else".
  - `gmstep_mutants.py` `verdict()` grades only that a control's named check fails and that the positive control passes.
  - A flag that also skipped the slew or coincident phases would pass the sweep's control runs, because no sweep control names a check in those phases.
  - No coverage is lost today: the clean leg runs every phase.
  - `scripts/compare_short_leg.py` shows the property holds at this head (see Executed evidence).
  - Option: have the driver require the positive control's tally to equal the clean leg's minus the phase's 86 checks.
- **Carried, unchanged and not reopened:**
  - R570-1-S1..S5 and R571-1-S1..S3;
  - R570-2-S1 / R571-2-S1, the allowedLostResponses reading;
  - R570-3-S1 and R571-3-S1.

### Observations: pre-existing dev defects, not attributable to this lane

- `tb/verilator/milan_dp/test_sim_pool.py` `LEGACY_LEGS` lacks the #658 `dynmap` leg. Its Makefile-inventory arm already fails at base `5603c353` (`receipts/test_sim_pool_base.log`).
- The backpressure test's recipe controls (`make-*`) did not finish within 9 min at base or head (`receipts/test_sim_pool_backpressure_head.log`, rc 124).
  - The single `make-copy-normal-drain` control also hangs at pre-delta and head.
  - All 14 direct controls pass.
- No gate or workflow invokes either runner test. A new issue is the manager's decision.

## Resolution of prior public findings at this head

| Finding | Status at `f5d0fb0e` | Evidence |
|---|---|---|
| R570-1-F1 = R571-1-F1: test-evidence ratchet | RESOLVED, stands | At head, `measure_test_evidence.py --check` exits 0 with 0 unexplained readers, and `--selftest` exits 0. The delta changes only the gmstep disposition (`measure_test_evidence_readers.py:142-147`), not the `phc_step.py` one |
| R570-1-F2: receipt arm could opt out of the bound | RESOLVED, stands | The delta does not touch the receipt gate. `git diff --stat 83239549..f5d0fb0e` lists 12 files, none of them `scripts/check_nvm_capture.py`, under `tb/verilator/nvm_capture_cpu/` or under `hdl/` |
| R570-1-F3 = R571-1-F3: design page figures | RESOLVED, stands | The delta does not touch `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` or `measurements.json` |
| R570-1-F4 = R571-1-F2: crossing liveness credit | RESOLVED, stands | `gptp_plane` at head: `phc_step` 62/0. The campaign rejects `liveness-not-marked` and `r571-no-liveness` by name (`receipts/suite_gptp_plane_head.log:131-132`) |
| R570-1-F5: closing keyword | RESOLVED, stands | The live body has no closing keyword. It says the later lane's physical repeat completes #621 |
| R570-1-R1 / R571-1-R1: status wording | Superseded | The runtime-round Status wording is stale again; see R570-4-R1 |
| R571-2-F1: an unanswered crossing earns no credit | RESOLVED, stands | `credit-on-step` is rejected by name (`receipts/suite_gptp_plane_head.log:133`), and `nocease-control` passes (campaign 8/8) |
| R571-2-RES-1, RES-2 | RESOLVED, stand | The delta does not touch `GPTP_PLANE.md`, the disposition at `:104-110` or the hold page |

## Executed evidence (this round, exact head unless stated)

- **Simulator:** the pinned `Verilator 5.050 2026-07-01 rev v5.050`, through a wrapper with sha256 `905795b9…e92f`.
- **Isolation:** every run used a disposable local clone. Each clone was checked out at the named revision, with each submodule at its gitlink.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp_gm_steps` with `VERILATOR_JOBS=6` | rc 0 in 602.5 s wall. The clean leg is 190/0. The driver is 6/6: the positive control passes under `--no-small-steps`, and all five acceptance controls are caught by name. `suite_tally --verdict` exits 0 | `receipts/suite_gm_steps_head.{log,rc,verdict.txt}` |
| `make -C tb/verilator/milan_dp` with `VERILATOR_JOBS=6 SIM_JOBS=2`, run concurrently with the row above | rc 0 in 1735.5 s wall: 11955 checks in 15 tallies, 0 failures. The log has no gmstep build or run | `receipts/suite_milan_dp_head.{log,rc,verdict.txt}` |
| Combined tally | 11955 + 196 = 12151 checks in 15 + 2 tallies, 0 failures. This equals the published pre-split count of 12151 in 17 tallies, so no check left the default sweep | `receipts/suite_tally_combined_head.txt` |
| `make -C tb/verilator/gptp_plane` | rc 0: `run` 29/29, `phc_step` 62/0 and the campaign 8/8. All six planted defects are rejected by name, and `nocease-control` passes | `receipts/suite_gptp_plane_head.*` |
| Short leg against the full leg | `Vmilan_dp_gmstep aemi.bin --no-small-steps` exits 0 with 104 checks in 38.9 s. `compare_short_leg.py`: the short transcript is the full 190 with exactly one contiguous block of 86 removed. Every removed check is a `621:` check or a `licence:` check graded inside the #621 phase. Every other name and expected value is identical | `receipts/gmstep_short_head.*`, `receipts/compare_short_leg.log` |
| Argument probes | A duplicate flag, an unknown `--bogus`, the flag without an image and three positionals each exit 2 with the usage line. A feed delay of `-5` exits 2 | `receipts/gmstep_argv_probe.log` |
| Reproduction: original donor generator `5dce647a` under the head harness | 14 of 62 fail. "asCapable never falls after step" and "no invalid link-delay publication" fail for every signed step | `receipts/probe_phc_orig*.log` |
| Own plant `no-pdstep`: the servo step no longer sets `S_PDSTEP` | Rejected: 10 of 62 fail, the same two checks per step plus the liveness arm | `receipts/probe_phc_no-pdstep*.log` |
| Own plant `clear-nrr`: the step also clears `S_NRR` | NOT RUN. The generator refuses it: "leg SERVO (17 words) does not fit". Recorded, not evidence | `receipts/probe_phc_clear-nrr.*` |
| `test_sim_pool.py`, `test_sim_pool_backpressure.py` and the dynmap-repaired probes | See F1 and the Observations | `receipts/test_sim_pool_*`, `receipts/probe_sim_pool_dynmap_*`, `receipts/probe_backpressure_recipe_*` |
| Static gates | Each exits 0. See the static gate list below | `receipts/gates_head.txt`, `receipts/gate_*.log` |
| Renderer-dependent doc gates, using the hash-pinned renderer in a disposable environment | Each exits 0. See the doc gate list below | `receipts/gate_venv_*.log` |
| Shard ownership at 5 workers, computed with `suite_shards.py` | Worker 3 owns `milan_dp_gm_steps` and 12 other suites. Worker 4 owns `milan_dp` alone, as the ownership step in `rtl.yml` requires | Derived in this report from the helper |

**Static gates, each rc 0:**

- `suite_shards.py --selftest`, with the landmark `milan_dp_gm_steps`: 3;
- `measure_test_evidence.py --check`: 32 of 101 suites armed, `milan_dp_gm_steps` armed by its `run` driver;
- `measure_test_evidence.py --selftest`;
- `check_py_idiom`, `check_cpp_idiom`, `check_doc_style`, `check_doc_paths` and `docs_check`;
- `check_hygiene --check`;
- `ci_events.py --check`, with 1741 contract items;
- `check_rtl_source_lists`.

**Renderer-dependent doc gates, each rc 0:**

- `check_em_dash.py --base 5603c353`: 0 findings over 278 added lines;
- `check_em_dash.py --base 83239549`: 0 findings over 167 added lines;
- `gen_toc.py --selftest`: 1501 of 1501 arms;
- `gen_toc.py --check`;
- `gen_toc.py --verify-anchors`: 419 links.

### Hosted evidence (observed; acceptance is the manager's)

- **`rtl-full` run 38095215734 at `f5d0fb0e`:**
  - `Verilator shard 3/5` succeeded. `milan_dp_gm_steps` ran from the preceding suite's PASS at 23:39:49.95 UTC to its own PASS at 23:55:35.97 UTC. That is 946 s, 52.6% of its 1800 s budget.
  - `Verilator shard 4/5` succeeded. `milan_dp` passed 1811 s after the shard's suite banner (`shard: 4/5`, printed after preflight). That is 37.7% of 4800 s.
  - Shard 0/5 and the Yosys shards succeeded.
  - Shards 1/5 and 2/5 were still running at 00:41 UTC, inside their usual 80 to 89 min.
  - Physical gPTP was skipped by design.
  - Receipts: `receipts/hosted_rtl_full_38095215734_jobs.txt` and `receipts/hosted_shard{3,4}_job_*.log`.
- **Other workflows at this head**, each completed successfully:
  - `docs` 38095215670, where docs-check skipped 0 of 55 steps;
  - `elaborate` 38095215668;
  - `rtl-fast` 38095215727.
- **Cited dev windows:** checked against the API. Worker 3 jobs took 459 s in run 37968528697 and 673 s in run 38067159953.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | See Conformance below | R570-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| RTL | CLEAN | See RTL below | R570-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Robustness | CLEAN | See Robustness below | R570-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Tests | UNCLEAN (R570-4-F1) | See Tests below | R570-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Docs | CLEAN (RESIDUE R570-4-R1 only) | See Docs below | R570-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |

**Conformance**, examined artifacts:

- Issue #621 items 1 and 2:
  - the original donor reproduces the loss (14 of 62 fail);
  - the head fix passes 62/0;
  - my own `no-pdstep` plant is rejected.
- Donor `gen_gptp_ucode.py`, read against IEEE 802.1AS-2020 11.2.2, 11.2.19.3.3, 11.2.19.3.4 and 11.2.20:
  - the SERVO step, `:836-838`;
  - the TMR clear, `:1298`;
  - PDEPOCH, `:1727-1739`.
- Runtime round items 1 to 4:
  - per-leg tables at `tb/verilator/milan_dp_gm_steps/README.md:50-111`;
  - its own default-partition suite on worker 3, `suite_shards.py:189`;
  - hosted 946 s and 1811 s;
  - no `hdl/` or gitlink change in `83239549..f5d0fb0e`;
  - graded names and expected values identical, `compare_short_leg.log`.

**RTL**, examined artifacts:

- The delta changes no RTL or donor file: 12 files, and the gitlinks `7dda9c3b`/`2ad2f845` are unchanged.
- The donor microcode legs and the scratch invariants `S_NR3`, `S_NR4`, `S_PDSTEP` and `S_PDGOT` executed through `gptp_plane` at head: 29 + 62 checks, campaign 8/8.
- `milan_dp` (11955/0) and the gmstep leg (190/0) elaborate the head datapath.

**Robustness**, examined artifacts:

- `sim_gmstep.cpp:1299-1332` argument handling: five malformed forms each exit 2.
- After the omitted phase, the later phases start from the CRF selection that phase restores (`:1003-1007`, `:1178`).
- `gmstep_mutants.py:259-288`: the freshness check and the run directory moved to `DP`.
- Two suites share generated images in one checkout. The sweep runs them serially, and hosted workers use separate checkouts.
- The donor's loss, excess-delay, crossing and unanswered-crossing arms.

**Tests**, examined artifacts:

- `milan_dp_gm_steps/Makefile`.
- `gmstep_mutants.py`: `verdict`, `run_leg` and `main`.
- The suite run: 190 + 6 checks, with all five controls caught by name.
- The short/full transcript comparison and the `phc_step` campaign.
- The runner tests `test_sim_pool.py:889` and `test_sim_pool_backpressure.py:95-132`, read against the head recipe (F1).

**Docs**, examined artifacts:

- `milan_dp_gm_steps/README.md`. Its projection arithmetic was rechecked:
  - 627.3 / 2870.1 = 21.9%;
  - 3519.6 x 0.781 = 2750 s, which is 57.3%;
  - 741 x 1.226 = 909 s.
- `milan_dp/README.md:81,897-939,1381-1386`.
- `milan_dp/Makefile:21-27,369-381,419-425`.
- `sim_gmstep.cpp:17-22,61-72`.
- `tb/verilator/README.md:62-64`.
- `TESTING.md:278,385-391,599`.
- `CI_WORKFLOWS.md:281-305`.
- `GM_LOSS_RECOVERY.md:227-239,275`.
- `measure_test_evidence_readers.py:142-147`.
- The doc gates, each rc 0.
- The PR body (R1).

## Real limits

- **No bank.** No full parent, protocol-processor, gPTP, Yosys or builder bank was run. This round ran only `milan_dp`, `milan_dp_gm_steps`, `gptp_plane` and the listed gates.
- **`gmstep-mutants` not run.** I did not run the explicit whole-inventory campaign (20 controls) at this head. The delta leaves its graded content unchanged: `CONTROLS` and every check call are identical. It is not claimed.
- **Wall times.** Local wall times come from a shared host. `milan_dp` and `milan_dp_gm_steps` ran concurrently with 6-job builds. They are not runtime evidence. Hosted figures are quoted only as observations.
- **Backpressure test.** Its recipe controls could not run to completion at any revision, because of the pre-existing hang. F1's backpressure half rests on reading the code.
- **Ratio retention.** The `clear-nrr` plant does not fit the ROM. So this round did not observe ratio retention across a step, consistent with R570-1-S1.
- **Hardware.** Physical calibration was NOT RUN. Skipped field contexts are not hardware proof. Issue item 3, the bench five-step repeat, is outside this lane.
- **Redaction.** In the local suite logs, the host's home-directory prefix was replaced by `<home>` (CONTRIBUTING section 6). Nothing else was edited.
- **Restore.** After the probes, the review clone was verified at the exact head (`receipts/restore_check.txt`):
  - tree `f0f6817a`, and `git write-tree` gives `f0f6817a`;
  - the index equals HEAD, and the work tree equals the index;
  - gitlinks `7dda9c3b`, `2ad2f845` and `48ff7a7e` are at stage 0 with mode 160000;
  - the submodules are clean;
  - the only artifact was a bytecode cache this session created under `scripts/`, and it was removed;
  - every probe ran in a disposable clone.

## Pending manager duties

- Disposition of F1.
- Whether the pre-existing `LEGACY_LEGS` and recipe-control defects go to a new issue.
- Hosted acceptance of `rtl-full` 38095215734, including shards 1/5 and 2/5, which were still running when observed.
- Carrying R570-4-R1 to the residue checklist.
- The current-dev merge candidate at the merge turn, with its builder and native banks. Its source base is `5603c353`, and live dev is `1fb0ed9a`.
- Publishing the donor `7dda9c3b` before the parent.
- The later bench lane for issue item 3.

R570-4 FINISHED
